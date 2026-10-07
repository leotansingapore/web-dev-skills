"""Map every competitor landing page (and ours) to one feature from features.json with Jev, and score each page as a
reference for building a landing page. Usage: features_rank.py <config.json> <raw_dir>
Needs <raw_dir>/anatomy_full.json and <raw_dir>/features.json. config["our_pages"] = list of our URLs to fetch and map.
Writes <raw_dir>/feature-map.csv (one row per page, ours included) and prints spend. Model pinned jev-1.13.0."""
import json, os, sys, csv, time, re, urllib.request
from concurrent.futures import ThreadPoolExecutor
KEY = os.environ["TYPESAFE_API_KEY"]; MODEL = "jev-1.13.0"
cfg = json.load(open(sys.argv[1])); raw = sys.argv[2]
FEAT = json.load(open(f"{raw}/features.json"))
Q = {
 "feature": {"type": "choice", "instructions": "Which single product feature is this landing page mainly about? Judge from `page` (its title, meta description and headings).", "criteria": FEAT},
 "outcome": {"type": "noul", "instructions": "Do the H1 and the first subheading of `page` tell the reader a specific result they get, rather than only naming the feature or product category?", "criteria": {"true": "States a result the reader gets", "false": "Names the feature or category, or is vague"}},
 "clarity": {"type": "score", "instructions": "From the headings of `page` alone, how well could a first-time visitor say what this feature does and who it is for?", "criteria": ["They could not tell what it does", "They would get the general idea", "They could say exactly what it does and who it is for"]},
 "specificity": {"type": "score", "instructions": "How concrete are the claims in `page`'s headings?", "criteria": ["Generic claims any product could make", "Some concrete details", "Concrete numbers, named workflows or examples throughout"]},
 "proof": {"type": "noul", "instructions": "Do the headings or calls to action of `page` show proof such as customer names, user counts, ratings, results or testimonials?", "criteria": {"true": "Proof is shown", "false": "No proof shown"}},
 "reference": {"type": "score", "instructions": "As a reference for a marketer building a landing page for the same feature, how useful is `page`'s structure and copy?", "criteria": ["Not useful: thin, off-topic, or a broken page", "Weak: few sections and generic copy", "Average: a standard feature page", "Strong: clear structure and several moves worth borrowing", "Excellent: a model page with many moves worth borrowing"]},
}
def structure(p):
    s = 0; h2 = p.get("h2") or []
    s += any(re.search(r"faq|question", x, re.I) for x in h2) or "FAQPage" in (p.get("schema") or [])
    s += bool(set(p.get("schema") or []) & {"SoftwareApplication", "FAQPage", "Product", "HowTo"})
    s += len(p.get("ctas") or []) >= 2; s += 800 <= (p.get("words") or 0) <= 8000; s += len(h2) >= 4
    return s / 5
def ask(item):
    who, p = item
    state = {"company": who, "page": {"url": p["url"], "title": p.get("title", ""), "meta": p.get("meta", ""), "h1": (p.get("h1") or [])[:2], "h2": (p.get("h2") or [])[:25], "h3": (p.get("h3") or [])[:30], "ctas": (p.get("ctas") or [])[:8]}}
    body = json.dumps({"model": MODEL, "state": state, "questions": Q}).encode()
    for att in range(5):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request("https://api.typesafe.ai/v1/systemone", data=body, headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 competitor-intel"}), timeout=60))
            a = r["answers"]; return a, r["usage"]["input_tokens"]
        except Exception: time.sleep(2 ** att)
    return None, 0
def fetch_ours(urls):
    from scrapling.fetchers import Fetcher
    out = []
    for u in urls:
        try:
            r = Fetcher.get(u, impersonate="chrome", timeout=30); c = lambda t: re.sub(r"\s+", " ", t or "").strip()
            t = lambda s: [c(e.get_all_text()) for e in r.css(s) if c(e.get_all_text())]
            out.append({"url": u, "bucket": "ours", "status": r.status, "title": c((r.css("title::text").getall() or [""])[0]), "meta": c((r.css('meta[name="description"]::attr(content)').getall() or [""])[0]),
                        "h1": t("h1")[:3], "h2": list(dict.fromkeys(t("h2")))[:40], "h3": list(dict.fromkeys(t("h3")))[:60], "ctas": [x for x in dict.fromkeys(c(e.get_all_text()) for e in r.css("a,button")) if 2 <= len(x) <= 40][:15],
                        "words": len(c(" ".join(r.css("body *::text").getall())).split()), "schema": sorted(set(re.findall(r'"@type"\s*:\s*"(\w+)"', r.html_content)))})
        except Exception as e: out.append({"url": u, "status": "err"})
    return out
a = json.load(open(f"{raw}/anatomy_full.json"))
items = [(n, p) for g in a for n in a[g] for p in a[g][n] if p.get("status") == 200 and p["bucket"] in ("feature", "feature-cluster", "use-case", "comparison", "free-tool", "template", "home")]
ours = fetch_ours(cfg.get("our_pages", [])); items += [(cfg["project"] + " (ours)", p) for p in ours if p.get("status") == 200]
print(len(items), "pages;", len([p for p in ours if p.get("status") == 200]), "ours", flush=True)
rows = []; tok = 0
with ThreadPoolExecutor(12) as ex:
    for (who, p), (ans, t) in zip(items, ex.map(ask, items)):
        tok += t
        if not ans: rows.append({"competitor": who, "url": p["url"], "bucket": p["bucket"], "feature": "error"}); continue
        sc = lambda k, n: ans[k]["score"] / (n - 1)
        parts = {"reference": sc("reference", 5), "outcome": ans["outcome"]["noul"], "clarity": sc("clarity", 3), "specificity": sc("specificity", 3), "proof": ans["proof"]["noul"], "structure": structure(p)}
        W = {"reference": .25, "outcome": .2, "clarity": .15, "specificity": .15, "proof": .1, "structure": .15}
        rows.append({"competitor": who, "url": p["url"], "bucket": p["bucket"], "h1": ((p.get("h1") or [p.get("title", "")])[0])[:160], "feature": ans["feature"]["choice"], "feature_conf": round(ans["feature"]["confidence"], 2),
                     **{k: round(v, 3) for k, v in parts.items()}, "composite": round(sum(W[k] * parts[k] for k in W) * 10, 2), "words": p.get("words"), "model": MODEL})
w = csv.DictWriter(open(f"{raw}/feature-map.csv", "w", newline=""), fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(ours, open(f"{raw}/our_pages.json", "w"), indent=1)
print("rows", len(rows), "errors", sum(r["feature"] == "error" for r in rows), "tokens", tok, "$", round(tok / 1e6 * 0.042, 3))
