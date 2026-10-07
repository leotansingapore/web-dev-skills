"""Rank features for our landing-page roadmap. Per feature: how many competitors market it (code), how much each reader
cares (Jev score), and whether our product has it (Jev noul against our brief). Usage: features_priority.py <config.json> <raw_dir>
Needs features.json, feature-map.csv. Writes feature-priority.json."""
import json, os, sys, csv, re, time, urllib.request, collections
from concurrent.futures import ThreadPoolExecutor
KEY = os.environ["TYPESAFE_API_KEY"]; MODEL = "jev-1.13.0"
cfg = json.load(open(sys.argv[1])); raw = sys.argv[2]
FEAT = {k: v for k, v in json.load(open(f"{raw}/features.json")).items() if k != "none"}
brief = open(cfg["brief_path"]).read() if cfg.get("brief_path") and os.path.exists(cfg["brief_path"]) else ""
m = re.search(r"## Product overview(.*?)## Target audience", brief, re.S); overview = (m.group(1) if m else brief[:6000]).strip()
def jev(state, qs):
    body = json.dumps({"model": MODEL, "state": state, "questions": qs}).encode()
    for att in range(5):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request("https://api.typesafe.ai/v1/systemone", data=body, headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 competitor-intel"}), timeout=60))
            return r["answers"]
        except Exception: time.sleep(2 ** att)
rows = list(csv.DictReader(open(f"{raw}/feature-map.csv")))
comp = [r for r in rows if "(ours)" not in r["competitor"]]; ours = [r for r in rows if "(ours)" in r["competitor"]]
def one(fid):
    d = FEAT[fid]; out = {"feature": fid, "definition": d}
    fr = [r for r in comp if r["feature"] == fid]
    out["competitor_pages"] = len(fr); out["competitors"] = sorted(set(r["competitor"] for r in fr))
    out["our_pages"] = [r["url"] for r in ours if r["feature"] == fid and float(r["feature_conf"]) >= 0.6]
    a = jev({"product_overview": overview, "product_evidence": cfg.get("product_evidence", ""), "feature": d}, {"has": {"type": "noul", "instructions": "Judging from `product_overview` and `product_evidence`, does the product include the capability described in `feature`?", "criteria": {"true": "The overview or the evidence shows the product does this", "false": "Neither mentions it"}}})
    out["we_have_p"] = round(a["has"]["noul"], 2) if a else None
    for rn, rd in cfg["readers"].items():
        a = jev({"reader": rd["reader"], "pains": rd["pains"], "feature": d}, {"care": {"type": "score", "instructions": "The `reader` has the worries in `pains`. How much would they care about a product that does what `feature` describes?", "criteria": ["Irrelevant to their work", "Nice to have", "Useful: it helps with a problem they have", "It solves one of the problems in `pains`"]}})
        out[f"care_{rn}"] = round(a["care"]["score"] / 3, 2) if a else None
    return out
with ThreadPoolExecutor(8) as ex: res = list(ex.map(one, FEAT))
mx = max(r["competitors"].__len__() for r in res) or 1
for r in res:
    care = max(r.get(f"care_{k}") or 0 for k in cfg["readers"])
    r["care_max"] = care; r["market"] = round(len(r["competitors"]) / mx, 2)
    r["priority"] = round(10 * (0.6 * care + 0.4 * r["market"]), 1)   # weights in code: reader care first, market proof second
    r["contested"] = "uncontested" if not r["competitors"] else ("crowded" if len(r["competitors"]) >= 10 else "contested")
    r["status"] = "page live" if r["our_pages"] else ("we have it, no page" if (r["we_have_p"] or 0) >= 0.6 else ("unclear" if (r["we_have_p"] or 0) >= 0.4 else "not in product"))
res.sort(key=lambda r: -r["priority"]); json.dump(res, open(f"{raw}/feature-priority.json", "w"), indent=1)
for r in res: print(f"{r['priority']:>4} {r['feature']:28} care {' '.join(f"{k}={r.get('care_'+k)}" for k in cfg['readers'])} comps {len(r['competitors']):2} have {r['we_have_p']} -> {r['status']}")
