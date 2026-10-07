# Jev (jev-1.13.0) tags each competitor page with one of our topics (topics.json) and whether it targets our niche (config["niche"]).
# Usage: jev_topics.py <config.json> <raw_dir>  -> jev-topics.csv
import json, os, csv, time, urllib.request, re, sys
from concurrent.futures import ThreadPoolExecutor
KEY = os.environ["TYPESAFE_API_KEY"]
os.chdir(sys.argv[2]); cfg = json.load(open(sys.argv[1]))
TOPICS = json.load(open("topics.json"))
def ask(state):
    body = json.dumps({"model": "jev-1.13.0", "state": state, "questions": {
      "topic": {"type": "choice", "instructions": "Judging from `url_path` (a page on `company`'s website; `company_category` says what the company sells), which topic does this page mainly cover?", "criteria": TOPICS},
      "insurance_audience": {"type": "noul", "instructions": "Is this page written specifically for " + cfg.get("niche", "our niche audience") + "?",
         "criteria": {"true": "The page targets that audience", "false": "The page targets other industries or a general audience"}}}}).encode()
    for attempt in range(5):
        try:
            req = urllib.request.Request("https://api.typesafe.ai/v1/systemone", data=body, headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 ci-inventory"})
            r = json.load(urllib.request.urlopen(req, timeout=40)); a = r["answers"]
            return a["topic"]["choice"], round(a["topic"]["confidence"], 2), round(a["insurance_audience"]["noul"], 3), r["usage"]["input_tokens"]
        except Exception as e:
            time.sleep(2 ** attempt)
    return "error", 0, 0, 0
CAT = {g: v.get("category", v.get("label", g)) for g, v in cfg["groups"].items()}
B = json.load(open("bucketed.json"))
rows = [{"group": g, "competitor": n, "bucket": r["bucket"], "url": r["url"]} for g in B for n in B[g] for r in B[g][n] if r["bucket"] not in ("help-docs", "integration", "core", "home", "skip", "unclassified", "other")]
states = [{"company": r["competitor"], "company_category": CAT[r["group"]], "url_path": re.sub(r"^https?://[^/]+", "", r["url"]), "content_type": r["bucket"]} for r in rows]
tok = 0; out = []
with ThreadPoolExecutor(12) as ex:
    for r, (t, c, ins, n) in zip(rows, ex.map(ask, states)):
        r.update({"topic": t, "topic_conf": c, "niche_p": ins}); out.append(r); tok += n
w = csv.DictWriter(open("jev-topics.csv", "w", newline=""), fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print("rows", len(out), "errors", sum(r["topic"] == "error" for r in out), "input tokens", tok, "est $", round(tok / 1e6 * 0.042, 3))
