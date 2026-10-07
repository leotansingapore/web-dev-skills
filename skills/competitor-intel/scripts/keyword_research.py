"""Keyword research for the opportunity list. seeds.json = {opportunity_id: [seed queries]} (Claude writes it from
Skyscraper opportunities). DataForSEO: search volume per location, keyword ideas from the top seed of each opportunity,
keyword difficulty. Every response's cost is summed and printed. Jev then judges each keyword: which opportunity it
belongs to, how well our product matches the searcher's intent, and whether they would be satisfied landing on us.
Usage: keyword_research.py <config.json> <raw_dir> [--max-spend 2.0]   -> keywords.csv
config: dataforseo_env (a .env file with DATAFORSEO_LOGIN/PASSWORD), locations {"SG": 2702, "US": 2840}."""
import json, os, sys, re, csv, time, base64, urllib.request, argparse
from concurrent.futures import ThreadPoolExecutor
ap = argparse.ArgumentParser(); ap.add_argument("config"); ap.add_argument("raw"); ap.add_argument("--max-spend", type=float, default=2.0); ap.add_argument("--jev-only", action="store_true", help="re-judge keywords.csv without calling DataForSEO"); a = ap.parse_args()
cfg = json.load(open(a.config)); os.chdir(a.raw)
envf = os.path.expanduser(cfg.get("dataforseo_env", "~/Documents/seo-audit-tool/.env.local"))
env = dict(l.split("=", 1) for l in open(envf).read().splitlines() if re.match(r"^DATAFORSEO_(LOGIN|PASSWORD)=", l))
AUTH = base64.b64encode(f"{env['DATAFORSEO_LOGIN'].strip().strip(chr(34))}:{env['DATAFORSEO_PASSWORD'].strip().strip(chr(34))}".encode()).decode()
LOCS = cfg.get("locations", {"US": 2840}); spend = 0.0
def dfs(path, body):
    global spend
    if spend > a.max_spend: raise SystemExit(f"stopped: spend ${spend:.3f} passed --max-spend")
    req = urllib.request.Request("https://api.dataforseo.com/v3/" + path, data=json.dumps(body).encode(), headers={"Authorization": "Basic " + AUTH, "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=180)); spend += r.get("cost", 0) or 0
    for t in r.get("tasks", []):
        if t.get("status_code") != 20000: print("  task", path, t.get("status_code"), t.get("status_message"), flush=True)
    return r
seeds = json.load(open("seeds.json"))
if a.jev_only:
    kw = {r["keyword"]: dict(r) for r in csv.DictReader(open("keywords.csv"))}; ks = list(kw)
else:
    kw = {}
    for opp, ks in seeds.items():
        for k in ks: kw.setdefault(k.lower(), {"keyword": k.lower(), "seed_of": opp, "origin": "seed"})
    for name, loc in LOCS.items():
        r = dfs("keywords_data/google_ads/search_volume/live", [{"keywords": [k for k in kw], "location_code": loc, "language_code": "en"}])
        for t in r["tasks"]:
            for it in (t.get("result") or []):
                e = kw.setdefault(it["keyword"].lower(), {"keyword": it["keyword"].lower(), "origin": "seed"})
                e[f"vol_{name}"] = it.get("search_volume") or 0; e[f"cpc_{name}"] = it.get("cpc"); e[f"comp_{name}"] = it.get("competition")
        print(f"volume {name}: spend so far ${spend:.3f}", flush=True)
    heads = [ks[0] for ks in seeds.values()]
    for name, loc in LOCS.items():
        for i in range(0, len(heads), 20):
            r = dfs("keywords_data/google_ads/keywords_for_keywords/live", [{"keywords": heads[i:i + 20], "location_code": loc, "language_code": "en", "sort_by": "search_volume"}])
            for t in r["tasks"]:
                for it in (t.get("result") or [])[:400]:
                    k = it["keyword"].lower(); e = kw.setdefault(k, {"keyword": k, "origin": f"idea"})
                    e[f"vol_{name}"] = max(e.get(f"vol_{name}") or 0, it.get("search_volume") or 0); e.setdefault(f"cpc_{name}", it.get("cpc"))
        print(f"ideas {name}: {len(kw)} keywords, spend ${spend:.3f}", flush=True)
    kw = {k: v for k, v in kw.items() if any((v.get(f"vol_{n}") or 0) >= 10 for n in LOCS) or v["origin"] == "seed"}
    diff_loc = cfg.get("difficulty_location", list(LOCS.values())[-1])
    ks = list(kw)
    for i in range(0, len(ks), 1000):
        r = dfs("dataforseo_labs/google/bulk_keyword_difficulty/live", [{"keywords": ks[i:i + 1000], "location_code": diff_loc, "language_code": "en"}])
        for t in r["tasks"]:
            for res in (t.get("result") or []):
                for it in (res.get("items") or []): kw[it["keyword"].lower()]["difficulty"] = it.get("keyword_difficulty")
    print(f"difficulty: spend ${spend:.3f}; {len(kw)} keywords kept", flush=True)

# Jev: which opportunity, intent match, satisfied
KEY = os.environ["TYPESAFE_API_KEY"]
brief = open(cfg["brief_path"]).read() if os.path.exists(cfg.get("brief_path", "")) else ""
m = re.search(r"## Product overview(.*?)## Target audience", brief, re.S); product = ((m.group(1) if m else brief[:3000]).strip() + "\n" + cfg.get("product_evidence", ""))[:6000]
OPPS = {o: f"Pages about: {', '.join(v[:4])}" for o, v in seeds.items()}; OPPS["none"] = "None of these topics"
Q = {"opportunity": {"type": "choice", "instructions": "Which page topic would best answer the search `keyword`?", "criteria": OPPS},
     "intent": {"type": "score", "instructions": "Someone typed `keyword` into Google. How well does the product in `product` match what they are looking for?", "criteria": ["Not what they want", "Loosely related", "A reasonable match", "Exactly what they are looking for"]},
     "satisfied": {"type": "noul", "instructions": "If that searcher landed on a page by the product in `product`, written for this keyword, would they feel they found what they searched for?", "criteria": {"true": "Yes", "false": "No, they would go back to the results"}},
     "page_type": {"type": "choice", "instructions": "What kind of page would best satisfy someone searching `keyword`?", "criteria": {"landing": "A product or feature page: they want software that does this", "tool": "A free tool, calculator, generator or downloadable template", "guide": "A guide, definition or how-to that explains something", "list": "A comparison or best-of list of products", "none": "None: they want a specific brand, a login, or something unrelated"}}}
# Asked alone with the keyword as the only state: with the product description beside it,
# Jev put 629 of 656 searchers in our niche (tested 2026-09-24). Alternatives in a Choice
# calibrate it; a yes/no audience question leaned yes on everything.
SEARCHER = {"searcher": {"type": "choice", "instructions": "Who most likely typed `keyword` into Google? Judge from the words of `keyword` alone.", "criteria": {
    "ours": cfg.get("niche_person", "Someone in our niche: " + cfg.get("niche", "")), "our-customers": cfg.get("niche_customer", "One of the end customers our niche serves"), "business-owner": "A small business owner or shop running their own marketing or sales",
    "marketer": "A marketer or agency running campaigns", "manager-hr": "A people manager or HR person outside our niche",
    "consumer": "A consumer or individual for personal use", "developer": "A developer or IT person", "other": "Someone else"}}}
def ask(k):
    body = json.dumps({"model": "jev-1.13.0", "state": {"product": product, "keyword": k}, "questions": Q}).encode()
    for att in range(5):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request("https://api.typesafe.ai/v1/systemone", data=body, headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 competitor-intel"}), timeout=60))
            b2 = json.dumps({"model": "jev-1.13.0", "state": {"keyword": k}, "questions": SEARCHER}).encode()
            r2 = json.load(urllib.request.urlopen(urllib.request.Request("https://api.typesafe.ai/v1/systemone", data=b2, headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 competitor-intel"}), timeout=60))
            return {**r["answers"], **r2["answers"]}, r["usage"]["input_tokens"] + r2["usage"]["input_tokens"]
        except Exception: time.sleep(2 ** att)
    return None, 0
tok = 0
with ThreadPoolExecutor(12) as ex:
    for k, (ans, t) in zip(ks, ex.map(ask, ks)):
        tok += t; e = kw[k]
        if ans: e.update({"opportunity": ans["opportunity"]["choice"], "opp_conf": round(ans["opportunity"]["confidence"], 2), "intent": round(ans["intent"]["score"] / 3, 2), "satisfied": round(ans["satisfied"]["noul"], 2), "audience": round(ans["searcher"]["probabilities"].get("ours", 0), 2), "searcher": ans["searcher"]["choice"], "page_type": ans["page_type"]["choice"]})
fields = ["keyword", "origin", "seed_of", "opportunity", "opp_conf", "intent", "satisfied", "audience", "searcher", "page_type", "difficulty"] + [f"{p}_{n}" for n in LOCS for p in ("vol", "cpc", "comp")]
w = csv.DictWriter(open("keywords.csv", "w", newline=""), fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(kw.values())
print(f"DataForSEO spend ${spend:.3f}; Jev tokens {tok} ${tok / 1e6 * 0.042:.3f}; {len(kw)} keywords -> keywords.csv")
