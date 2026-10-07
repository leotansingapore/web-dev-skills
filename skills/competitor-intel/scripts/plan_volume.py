"""Volume, difficulty and searcher for every target keyword in a build plan. Reuses keywords.csv rows already measured;
only new keywords go to DataForSEO (one volume call per location + one difficulty call, per 1000). Jev then judges who
searches each new keyword (Choice, keyword-only state) and whether the product fits.
Usage: plan_volume.py <config.json> <raw_dir> <keywords.txt> [--max-spend 1.5]  -> plan-keywords.csv"""
import json, os, sys, re, csv, time, base64, urllib.request, argparse
from concurrent.futures import ThreadPoolExecutor
ap = argparse.ArgumentParser(); ap.add_argument("config"); ap.add_argument("raw"); ap.add_argument("kwfile"); ap.add_argument("--max-spend", type=float, default=1.5); ap.add_argument("--rejudge", action="store_true", help="re-ask who searches every keyword, not only new ones"); a = ap.parse_args()
cfg = json.load(open(a.config)); os.chdir(a.raw); LOCS = cfg.get("locations", {"US": 2840})
want = sorted({k.strip().lower() for k in open(a.kwfile).read().splitlines() if k.strip()})
known = {r["keyword"]: r for r in csv.DictReader(open("keywords.csv"))} if os.path.exists("keywords.csv") else {}
prev = {r["keyword"]: r for r in csv.DictReader(open("plan-keywords.csv"))} if os.path.exists("plan-keywords.csv") else {}
new = [k for k in want if k not in known and k not in prev and 1 <= len(k) <= 80 and re.fullmatch(r"[a-z0-9 .'&+-]+", k)]
env = dict(l.split("=", 1) for l in open(os.path.expanduser(cfg.get("dataforseo_env", "~/Documents/seo-audit-tool/.env.local"))).read().splitlines() if re.match(r"^DATAFORSEO_(LOGIN|PASSWORD)=", l))
AUTH = base64.b64encode(f"{env['DATAFORSEO_LOGIN'].strip().strip(chr(34))}:{env['DATAFORSEO_PASSWORD'].strip().strip(chr(34))}".encode()).decode(); spend = 0.0
def dfs(path, body):
    global spend
    if spend > a.max_spend: raise SystemExit(f"stopped at ${spend:.3f}")
    r = json.load(urllib.request.urlopen(urllib.request.Request("https://api.dataforseo.com/v3/" + path, data=json.dumps(body).encode(), headers={"Authorization": "Basic " + AUTH, "Content-Type": "application/json"}), timeout=180))
    spend += r.get("cost", 0) or 0
    for t in r.get("tasks", []):
        if t.get("status_code") != 20000: print("  task", t.get("status_code"), t.get("status_message"), flush=True)
    return r
rows = {k: {"keyword": k} for k in new}
for i in range(0, len(new), 700):
    chunk = new[i:i + 700]
    for name, loc in LOCS.items():
        for t in dfs("keywords_data/google_ads/search_volume/live", [{"keywords": chunk, "location_code": loc, "language_code": "en"}])["tasks"]:
            for it in (t.get("result") or []):
                k = it["keyword"].lower()
                if k in rows: rows[k][f"vol_{name}"] = it.get("search_volume") or 0
    for t in dfs("dataforseo_labs/google/bulk_keyword_difficulty/live", [{"keywords": chunk, "location_code": cfg.get("difficulty_location", 2840), "language_code": "en"}])["tasks"]:
        for res in (t.get("result") or []):
            for it in (res.get("items") or []):
                k = it["keyword"].lower()
                if k in rows: rows[k]["difficulty"] = it.get("keyword_difficulty")
print(f"DataForSEO: {len(new)} new keywords, ${spend:.3f}", flush=True)
KEY = os.environ["TYPESAFE_API_KEY"]
brief = open(cfg["brief_path"]).read() if os.path.exists(cfg.get("brief_path", "")) else ""
m = re.search(r"## Product overview(.*?)## Target audience", brief, re.S); product = ((m.group(1) if m else brief[:3000]).strip() + "\n" + cfg.get("product_evidence", ""))[:6000]
SEARCHER = {"searcher": {"type": "choice", "instructions": "Who most likely typed `keyword` into Google? Judge from the words of `keyword` alone.", "criteria": {
    "ours": cfg.get("niche_person", cfg.get("niche", "")), "our-customers": cfg.get("niche_customer", "One of the end customers our niche serves"), "business-owner": "A small business owner or shop running their own marketing or sales", "marketer": "A marketer or agency running campaigns",
    "manager-hr": "A people manager or HR person outside our niche", "consumer": "A consumer or individual for personal use", "developer": "A developer or IT person", "other": "Someone else"}}}
FIT = {"intent": {"type": "score", "instructions": "Someone typed `keyword` into Google. How well does the product in `product` match what they are looking for?", "criteria": ["Not what they want", "Loosely related", "A reasonable match", "Exactly what they are looking for"]}}
def post(state, q):
    body = json.dumps({"model": "jev-1.13.0", "state": state, "questions": q}).encode()
    for att in range(5):
        try: return json.load(urllib.request.urlopen(urllib.request.Request("https://api.typesafe.ai/v1/systemone", data=body, headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 competitor-intel"}), timeout=60))
        except Exception: time.sleep(2 ** att)
def judge(k):
    s = post({"keyword": k}, SEARCHER); f = post({"product": product, "keyword": k}, FIT)
    return (s["answers"]["searcher"]["choice"] if s else "", round(s["answers"]["searcher"]["probabilities"].get("ours", 0), 2) if s else "", round(f["answers"]["intent"]["score"] / 3, 2) if f else "")
judge_list = list(new)
if a.rejudge:
    for k in want:
        if k not in rows and (k in prev or k in known):
            src = prev.get(k) or {"keyword": k, **{f"vol_{n}": known[k].get(f"vol_{n}", 0) for n in LOCS}, "difficulty": known[k].get("difficulty")}
            rows[k] = {x: src.get(x) for x in ["keyword"] + [f"vol_{n}" for n in LOCS] + ["difficulty"]}; judge_list.append(k)
with ThreadPoolExecutor(12) as ex:
    for k, (who, p, it) in zip(judge_list, ex.map(judge, judge_list)): rows[k].update({"searcher": who, "ours_p": p, "intent": it})
print(f"Jev judged {len(judge_list)} keywords", flush=True)
out = dict(prev)
for k in want:
    if k in rows: out[k] = rows[k]
    elif k in known:
        r = known[k]; out[k] = {"keyword": k, **{f"vol_{n}": r.get(f"vol_{n}", 0) for n in LOCS}, "difficulty": r.get("difficulty"), "searcher": r.get("searcher", ""), "ours_p": r.get("audience", ""), "intent": r.get("intent", "")}
fields = ["keyword"] + [f"vol_{n}" for n in LOCS] + ["difficulty", "searcher", "ours_p", "intent"]
w = csv.DictWriter(open("plan-keywords.csv", "w", newline=""), fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(out.values())
print(f"plan-keywords.csv: {len(out)} keywords; DataForSEO ${spend:.3f}")
