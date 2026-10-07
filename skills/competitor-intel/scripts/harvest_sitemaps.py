# Harvest every URL from each competitor sitemap. Usage: harvest_sitemaps.py <config.json> <raw_dir>  -> sitemaps.json
import json, re, sys, gzip
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from scrapling.fetchers import Fetcher

cfg = json.load(open(sys.argv[1])); out = sys.argv[2]
sites = {g: v["competitors"] for g, v in cfg["groups"].items()}

def get(url):
    try:
        r = Fetcher.get(url, impersonate="chrome", timeout=30, stealthy_headers=True)
        if r.status != 200: return None
        body = r.body
        if url.endswith(".gz") or body[:2] == b"\x1f\x8b":
            body = gzip.decompress(body)
        return body.decode("utf-8", "replace")
    except Exception as e:
        return None

def locs(xml): return [l.strip() for l in re.findall(r"<loc>\s*(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?\s*</loc>", xml, re.S)]

def harvest(name, base):
    host = urlparse(base).netloc
    roots = []
    robots = get(base.rstrip("/") + "/robots.txt") or ""
    roots += re.findall(r"(?im)^\s*sitemap:\s*(\S+)", robots)
    for p in ["/sitemap.xml", "/sitemap_index.xml", "/sitemap-index.xml"]:
        roots.append(base.rstrip("/") + p)
    seen, urls, queue = set(), set(), list(dict.fromkeys(roots))
    while queue and len(seen) < 400:
        sm = queue.pop(0)
        if sm in seen: continue
        seen.add(sm)
        xml = get(sm)
        if not xml or "<loc" not in xml: continue
        ls = locs(xml)
        if "<sitemapindex" in xml:
            # skip non-English locale sitemaps
            queue += [l for l in ls if not re.search(r"/(de|fr|es|pt|it|nl|ja|ko|zh|id|ar|tr|ru|pl|vi|th|ms|pt-br|es-mx|zh-hk|zh-cn|zh-tw)[-_/.]", urlparse(l).path + "/")]
        else:
            urls.update(ls)
    return name, host, sorted(seen), sorted(urls)

res = {}
jobs = [(g, n, u) for g, d in sites.items() for n, u in d.items()]
with ThreadPoolExecutor(8) as ex:
    futs = {ex.submit(harvest, n, u): (g, n) for g, n, u in jobs}
    for f, (g, n) in futs.items():
        name, host, sms, urls = f.result()
        res.setdefault(g, {})[name] = {"host": host, "sitemaps": sms, "urls": urls}
        print(f"{g:10} {name:14} sitemaps={len(sms):3} urls={len(urls)}", flush=True)
json.dump(res, open(f"{out}/sitemaps.json", "w"), indent=1)
