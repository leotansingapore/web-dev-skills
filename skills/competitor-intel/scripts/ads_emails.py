"""Pull a competitor's live ads (Meta Ad Library, Google Ads Transparency, LinkedIn Ad Library) and archived
marketing emails (Milled) with one Browser Use Cloud v4 run per competitor.
Usage: ads_emails.py <config.json> <out_dir> [--only name1,name2] [--max-runs N] [--max-cost-per-run 0.6]
Writes <out_dir>/ads_emails/<competitor>.json. Skips competitors that already have a file (delete to refresh).
Budget from the credit balance before/after (printed), never from totalCostUsd."""
import json, os, sys, time, argparse, urllib.request
from urllib.parse import urlparse
from browser_use_sdk.v4 import BrowserUse

def balance():
    req = urllib.request.Request("https://api.browser-use.com/api/v2/billing/account", headers={"X-Browser-Use-API-Key": os.environ["BROWSER_USE_API_KEY"]})
    return json.load(urllib.request.urlopen(req, timeout=30))["totalCreditsBalanceUsd"]

TASK = """You are collecting public marketing data about the company "{name}" (website {domain}). Visit these public pages, read them, and return JSON only.

1. Meta Ad Library: open https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&media_type=all&search_type=keyword_unordered&q={q}
   Pick the advertiser whose page clearly belongs to {domain}. For up to 12 active ads record: primary_text, headline, cta_button, landing_url, started_running (as printed), platforms, format (image/video/carousel).
2. Google Ads Transparency Center: open https://adstransparency.google.com/?region=anywhere&domain={domain}
   For up to 12 ads record: format, the visible ad text or headline, last_shown (as printed).
3. LinkedIn Ad Library: open https://www.linkedin.com/ad-library/search?accountOwner={q}
   For up to 8 ads record: text, headline, cta, format. Skip if it asks you to log in.
4. Milled email archive: open https://milled.com/search?q={q} and find the store for {domain}. For up to 12 recent emails record: subject, sent_date, preview_text (first line if shown), url.

Rules: never log in, never create accounts, never click Sign up. If a source shows nothing or blocks you, set its "status" to "none" or "blocked" and move on. Copy text exactly as printed; do not summarise or invent. For each source also echo "advertiser_as_printed": the advertiser or store name exactly as the page prints it.
Return only this JSON:
{{"company":"{name}","meta":{{"status":"","advertiser_as_printed":"","total_results_as_printed":"","ads":[]}},"google":{{"status":"","advertiser_as_printed":"","ads":[]}},"linkedin":{{"status":"","advertiser_as_printed":"","ads":[]}},"milled":{{"status":"","advertiser_as_printed":"","emails":[]}}}}"""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("config"); ap.add_argument("out"); ap.add_argument("--only"); ap.add_argument("--max-runs", type=int, default=5); ap.add_argument("--max-cost-per-run", type=float, default=0.6)
    a = ap.parse_args(); cfg = json.load(open(a.config))
    comps = [(n, u) for g in cfg["groups"].values() for n, u in g["competitors"].items()]
    if a.only: comps = [c for c in comps if c[0] in a.only.split(",")]
    os.makedirs(f"{a.out}/ads_emails", exist_ok=True)
    todo = [c for c in comps if not os.path.exists(f"{a.out}/ads_emails/{c[0]}.json")][: a.max_runs]
    before = balance(); print(f"balance before ${before:.3f}; runs {len(todo)}; cap ${a.max_cost_per_run}/run", flush=True)
    client = BrowserUse(); runs = {}
    for n, u in todo:
        dom = urlparse(u).netloc.replace("www.", ""); q = urllib.request.quote(n)
        r = client.runs.create(TASK.format(name=n, domain=dom, q=q), max_cost_usd=a.max_cost_per_run); runs[n] = r.id; time.sleep(1)
    for n, rid in runs.items():
        res = client.runs.wait_for_completion(rid, timeout=900, interval=5)
        raw = res.result or ""
        try: data = json.loads(raw[raw.find("{"): raw.rfind("}") + 1])
        except Exception: data = {"parse_error": True, "raw": raw[:4000]}
        data["_run"] = {"id": str(rid), "status": str(res.status), "model_cost_usd": getattr(res, "total_cost_usd", None), "fetched": time.strftime("%Y-%m-%d")}
        json.dump(data, open(f"{a.out}/ads_emails/{n}.json", "w"), indent=1)
        print(n, res.status, {k: (v.get("status"), len(v.get("ads", v.get("emails", [])))) for k, v in data.items() if isinstance(v, dict) and k != "_run"}, flush=True)
    time.sleep(20); after = balance(); print(f"balance after ${after:.3f}; spent ${before - after:.3f} (${(before - after) / max(1, len(runs)):.3f}/run)")
main()
