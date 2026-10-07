"""Which competitor blog and guide pages are worth a version for our niche? Jev scores usefulness of a niche rewrite
and flags subjects tied to something irrelevant. Usage: jev_adaptable.py <config.json> <raw_dir>  -> adaptable.csv"""
import json, os, sys, csv, re, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
cfg = json.load(open(sys.argv[1])); os.chdir(sys.argv[2]); KEY = os.environ["TYPESAFE_API_KEY"]
reader = cfg.get("niche_person", cfg.get("niche", ""))
Q = {"useful": {"type": "score", "instructions": "If the article at `url_path` were rewritten for `reader`, how useful would it be to them in their work?", "criteria": ["Useless to them", "Marginal", "Useful", "Directly about a problem they face every week"]},
     "foreign": {"type": "noul", "instructions": "Is the subject of `url_path` tied to something irrelevant to `reader`, such as e-commerce stores, Shopify, developer APIs, a specific software product's settings, or company news?", "criteria": {"true": "Tied to something irrelevant to them", "false": "A general subject they could use"}}}
def ask(r):
    body = json.dumps({"model": "jev-1.13.0", "state": {"reader": reader, "company": r["competitor"], "url_path": re.sub(r"^https?://[^/]+", "", r["url"])}, "questions": Q}).encode()
    for att in range(5):
        try:
            x = json.load(urllib.request.urlopen(urllib.request.Request("https://api.typesafe.ai/v1/systemone", data=body, headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 competitor-intel"}), timeout=60))
            return x["answers"], x["usage"]["input_tokens"]
        except Exception: time.sleep(2 ** att)
    return None, 0
rows = [r for r in csv.DictReader(open("jev-topics.csv")) if r["bucket"] in ("blog", "guide") and r["topic"] != "none" and float(r["topic_conf"]) >= 0.5]
tok = 0
with ThreadPoolExecutor(12) as ex:
    for r, (a, t) in zip(rows, ex.map(ask, rows)):
        tok += t; r["useful"] = round(a["useful"]["score"] / 3, 2) if a else ""; r["foreign"] = round(a["foreign"]["noul"], 2) if a else ""
w = csv.DictWriter(open("adaptable.csv", "w", newline=""), fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows), "rows; tokens", tok, "$", round(tok / 1e6 * 0.042, 3))
