"""Competitor site structure: section tree from the sitemap (bucketed.json) and the navigation each homepage shows
(header and footer links). Usage: site_structure.py <config.json> <raw_dir>  -> site-structure.json
Per competitor: sections (first path segment) with page counts and content type, depth, programmatic families
(one parent with 20+ children), header nav labels and paths, footer paths. Across competitors: how many use each
kind of section and which nav labels recur."""
import json, sys, os, re, collections, statistics as st
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
from scrapling.fetchers import Fetcher
cfg = json.load(open(sys.argv[1])); os.chdir(sys.argv[2])
B = json.load(open("bucketed.json"))
def nav(name, url):
    try:
        r = Fetcher.get(url, impersonate="chrome", timeout=30, stealthy_headers=True)
    except Exception as e:
        return name, {"error": str(e)[:80]}
    host = urlparse(url).netloc.replace("www.", "")
    def links(sel):
        out = []
        for a in r.css(f"{sel} a"):
            href = a.attrib.get("href") or ""; txt = re.sub(r"\s+", " ", a.get_all_text() or "").strip()
            u = urlparse(urljoin(url, href))
            if u.netloc.replace("www.", "") != host or not txt or len(txt) > 50: continue
            p = re.sub(r"/+$", "", u.path) or "/"
            out.append((txt, p))
        return list(dict.fromkeys(out))
    head = links("header") or links("nav")
    foot = links("footer")
    return name, {"header": head[:80], "footer": foot[:150]}
comps = [(n, u) for g in cfg["groups"].values() for n, u in g["competitors"].items()]
with ThreadPoolExecutor(8) as ex: navs = dict(ex.map(lambda c: nav(*c), comps))
out = {}
for g in B:
    for n, rows in B[g].items():
        rows = [r for r in rows if r["bucket"] not in ("skip", "unclassified")]
        if not rows: continue
        sec = collections.defaultdict(lambda: {"pages": 0, "types": collections.Counter()})
        fam = collections.Counter(); depths = []
        for r in rows:
            segs = [s for s in r["path"].split("/") if s]
            depths.append(len(segs))
            key = "/" + segs[0] if segs else "/"
            sec[key]["pages"] += 1; sec[key]["types"][r["bucket"]] += 1
            if len(segs) >= 2: fam["/" + "/".join(segs[:-1])] += 1
        out[n] = {"group": g, "pages": len(rows), "depth_median": st.median(depths), "depth_max": max(depths),
                  "sections": sorted(({"path": k, "pages": v["pages"], "type": v["types"].most_common(1)[0][0]} for k, v in sec.items()), key=lambda x: -x["pages"])[:40],
                  "programmatic": [{"parent": p, "children": c} for p, c in fam.most_common(15) if c >= 20],
                  "nav": navs.get(n, {})}
kind = collections.Counter(); labels = collections.Counter()
for n, d in out.items():
    kind.update({t for t in (s["type"] for s in d["sections"]) if t not in ("other", "home", "core")})
    labels.update({t.lower() for t, _ in d["nav"].get("header", [])})
json.dump({"competitors": out, "section_types_used_by": dict(kind.most_common()), "header_labels": dict(labels.most_common(60))}, open("site-structure.json", "w"), indent=1)
print("competitors", len(out)); print("section types:", dict(kind.most_common())); print("top header labels:", labels.most_common(35))
