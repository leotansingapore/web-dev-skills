# Extract landing-page anatomy (title, meta, H1-H3, CTAs, words, schema) from home, feature, pricing, comparison, use-case,
# free-tool, template and guide pages. Usage: anatomy.py <raw_dir>  -> anatomy_full.json
import json, re, sys, os
os.chdir(sys.argv[1])
from concurrent.futures import ThreadPoolExecutor
from scrapling.fetchers import Fetcher
d = json.load(open("bucketed.json"))
CAP = {"home": 1, "core": 5, "feature": 999, "feature-cluster": 999, "comparison": 999, "free-tool": 999, "use-case": 999, "template": 30, "guide": 15}
def clean(t): return re.sub(r"\s+", " ", t or "").strip()
def grab(url):
    try:
        r = Fetcher.get(url, impersonate="chrome", timeout=30, stealthy_headers=True)
        if r.status != 200: return {"url": url, "status": r.status}
        txt = lambda sel: [clean(e.get_all_text()) for e in r.css(sel)]
        ctas = [clean(e.get_all_text()) for e in r.css("a, button")]
        ctas = [c for c in ctas if 2 <= len(c) <= 40 and re.search(r"(?i)\b(start|try|get|book|demo|sign|free|join|download|talk|see|watch|create|contact|schedule|request)\b", c)]
        body = clean(" ".join(r.css("main *::text").getall() or r.css("body *::text").getall()))
        return {"url": url, "status": 200, "title": clean((r.css("title::text").getall() or [""])[0]),
          "meta": clean((r.css('meta[name="description"]::attr(content)').getall() or [""])[0]),
          "h1": [h for h in txt("h1") if h][:3], "h2": list(dict.fromkeys(h for h in txt("h2") if h))[:40],
          "h3": list(dict.fromkeys(h for h in txt("h3") if h))[:60], "ctas": list(dict.fromkeys(ctas))[:15],
          "words": len(body.split()),
          "schema": sorted(set(re.findall(r'"@type"\s*:\s*"(\w+)"', r.html_content)))[:12]}
    except Exception as e:
        return {"url": url, "status": "err", "error": str(e)[:120]}
jobs = []
for g in d:
    for n, rows in d[g].items():
        for b, cap in CAP.items():
            for r in [x for x in rows if x["bucket"] == b][:cap]:
                jobs.append((g, n, b, r["url"]))
print(len(jobs), "pages", flush=True)
out = {}
with ThreadPoolExecutor(10) as ex:
    for (g, n, b, u), res in zip(jobs, ex.map(lambda j: grab(j[3]), jobs)):
        res["bucket"] = b; out.setdefault(g, {}).setdefault(n, []).append(res)
json.dump(out, open("anatomy_full.json", "w"), indent=1)
ok = sum(1 for g in out for n in out[g] for p in out[g][n] if p["status"] == 200)
print("ok", ok, "of", len(jobs))
for g in out:
    for n in out[g]:
        h = [p for p in out[g][n] if p["bucket"] == "home"]
        if h: print(n, "|", (h[0].get("h1") or ["?"])[0][:80], "| h2s:", len(h[0].get("h2", [])), "| words:", h[0].get("words"))
