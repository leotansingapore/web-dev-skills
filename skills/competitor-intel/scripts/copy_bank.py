"""Build the copy bank: every competitor headline, subhead, meta description, CTA, YouTube title, ad line and email
subject, labelled by Jev (what kind of line it is, which USP theme it claims) and, for hook-like lines, scored out of 10
in each configured reader's shoes with hook-check's own six questions.
Usage: copy_bank.py <config.json> <raw_dir> [--no-score]   -> <raw_dir>/copy-bank.csv"""
import json, os, sys, csv, re, glob, time, urllib.request
from importlib.machinery import SourceFileLoader
from concurrent.futures import ThreadPoolExecutor
KEY = os.environ["TYPESAFE_API_KEY"]; MODEL = "jev-1.13.0"
cfg = json.load(open(sys.argv[1])); raw = sys.argv[2]
HC = SourceFileLoader("hookcheck", os.path.expanduser("~/.local/bin/hook-check")).load_module()
KIND = {
 "hook": "A headline meant to grab attention: promises a result, names a moment or a problem the reader lives through",
 "usp": "A claim about why this product is different or better than alternatives",
 "benefit": "Says what the user gets from a specific feature",
 "feature-label": "Only names a feature, section or product area",
 "pain-enemy": "Names a problem, frustration or enemy (old tools, chaos, manual work)",
 "proof": "Proof: customer counts, logos, ratings, awards, results, testimonials",
 "objection": "Answers a doubt: price, security, setup time, switching, support",
 "cta": "Asks the reader to act: sign up, book, try, download",
 "question": "A question heading such as an FAQ entry",
 "other": "Navigation, legal, filler, or not marketing copy",
}
THEME = {
 "ai": "AI does the work", "all-in-one": "Everything in one place, replaces several tools", "time-saved": "Saves time, faster work",
 "ease": "Easy to use or set up", "price": "Price, value, free plan", "integrations": "Works with your other tools", "security": "Security, privacy, compliance",
 "support": "Human support and service", "revenue-results": "More revenue, conversions, sales results", "scale-teams": "Built for teams or scale",
 "channels": "Reach customers on WhatsApp or other channels", "focus-wellbeing": "Calm, focus, balance, less stress", "niche-audience": "Built for a specific industry or role",
 "none": "No clear theme",
}
def jev(state, qs):
    body = json.dumps({"model": MODEL, "state": state, "questions": qs}).encode()
    for att in range(5):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request("https://api.typesafe.ai/v1/systemone", data=body, headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 competitor-intel"}), timeout=60))
            return r["answers"], r["usage"]["input_tokens"]
        except Exception: time.sleep(2 ** att)
    return None, 0
lines = {}
def add(comp, group, source, text, url=""):
    t = re.sub(r"\s+", " ", text or "").strip()
    if not (12 <= len(t) <= 240) or re.fullmatch(r"(?i)(footer|faq|frequently asked questions|features|pricing|integrations|resources|log in|sign in)", t): return
    k = (comp, t.lower()); lines.setdefault(k, {"competitor": comp, "group": group, "source": source, "text": t, "url": url})
a = json.load(open(f"{raw}/anatomy_full.json"))
for g in a:
    for n, ps in a[g].items():
        for p in ps:
            if p.get("status") != 200: continue
            for h in (p.get("h1") or [])[:2]: add(n, g, f"{p['bucket']}:h1", h, p["url"])
            add(n, g, f"{p['bucket']}:meta", p.get("meta"), p["url"])
            for h in (p.get("h2") or [])[:25]: add(n, g, f"{p['bucket']}:h2", h, p["url"])
            if p["bucket"] == "home":
                for h in (p.get("h3") or [])[:30]: add(n, g, "home:h3", h, p["url"])
                for c in (p.get("ctas") or [])[:10]: add(n, g, "home:cta", c, p["url"])
grp = {n: g for g in cfg["groups"] for n in cfg["groups"][g]["competitors"]}
if os.path.exists(f"{raw}/socials.json"):
    for n, d in json.load(open(f"{raw}/socials.json")).items():
        for v in d.get("youtube_videos", []): add(n, grp.get(n, ""), "youtube", v.get("title"), v.get("url", ""))
for f in glob.glob(f"{raw}/ads_emails/*.json"):
    d = json.load(open(f)); n = os.path.basename(f)[:-5]
    for src in ("meta", "google", "linkedin"):
        for ad in (d.get(src) or {}).get("ads", []):
            for fld in ("headline", "primary_text", "text", "visible_ad_text_or_headline"): add(n, grp.get(n, ""), f"ad:{src}", ad.get(fld), ad.get("landing_url", ""))
    for e in (d.get("milled") or {}).get("emails", []): add(n, grp.get(n, ""), "email", e.get("subject"), e.get("url", ""))
rows = list(lines.values()); print(len(rows), "lines", flush=True)
Q = {"kind": {"type": "choice", "instructions": "What kind of marketing line is `line`? `company` wrote it; `where` says where it appeared.", "criteria": KIND},
     "theme": {"type": "choice", "instructions": "Which selling theme does `line` lean on most?", "criteria": THEME}}
tok = 0
with ThreadPoolExecutor(12) as ex:
    for r, (ans, t) in zip(rows, ex.map(lambda r: jev({"company": r["competitor"], "where": r["source"], "line": r["text"]}, Q), rows)):
        tok += t; r["kind"] = ans["kind"]["choice"] if ans else "error"; r["kind_conf"] = round(ans["kind"]["confidence"], 2) if ans else 0; r["theme"] = ans["theme"]["choice"] if ans else ""
print("labelled; tokens", tok, flush=True)
if "--no-score" not in sys.argv:
    qs = {k: q for k, (_, q) in HC.DIMENSIONS.items()}
    hooks = [r for r in rows if r["kind"] in ("hook", "usp", "benefit", "pain-enemy") and not r["source"].endswith(":meta")]
    for rname, rd in cfg["readers"].items():
        def score(r):
            cat = cfg["category"].get(r["group"], cfg["category"]["default"])
            ans, t = jev({"reader": rd["reader"], "pains": rd["pains"], "role": "a headline on a landing page or ad", "category": cat, "hook": r["text"]}, qs)
            return (HC.composite(ans) if ans else (None, {})), t
        with ThreadPoolExecutor(12) as ex:
            for r, ((s, parts), t) in zip(hooks, ex.map(score, hooks)):
                tok += t; r[f"score_{rname}"] = s
                for k, v in parts.items(): r[f"{k}_{rname}"] = round(v, 2)
        print("scored for", rname, len(hooks), flush=True)
fields = sorted({k for r in rows for k in r}, key=lambda k: ["competitor", "group", "source", "kind", "kind_conf", "theme", "text"].index(k) if k in ["competitor", "group", "source", "kind", "kind_conf", "theme", "text"] else 99)
w = csv.DictWriter(open(f"{raw}/copy-bank.csv", "w", newline=""), fieldnames=fields); w.writeheader(); w.writerows(rows)
print("rows", len(rows), "tokens", tok, "$", round(tok / 1e6 * 0.042, 3))
