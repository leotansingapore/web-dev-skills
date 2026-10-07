# Jev (pinned jev-1.13.0) picks a content type for URLs with no directory to go on. Usage: jev_classify.py <raw_dir>
import json, os, sys, time, urllib.request
os.chdir(sys.argv[1])
from concurrent.futures import ThreadPoolExecutor
KEY = os.environ["TYPESAFE_API_KEY"]
OPTS = {
 "blog": "An article or blog post (listicle, how-to, opinion, news, 'best X' roundup, 'X vs Y' blog article)",
 "guide": "A long-form guide, ebook, course, academy lesson, webinar or video tutorial",
 "free-tool": "An interactive free tool: generator, calculator, checker, estimator, finder",
 "template": "A template, template library entry, or example message/script to copy",
 "comparison": "A page comparing the company's own product with a named competitor or listing alternatives to a competitor",
 "integration": "A page about connecting the product with another named app or channel",
 "feature": "A product page describing one of the company's own features or modules",
 "use-case": "A page for an industry, role, team type, company size, city or region",
 "case-study": "A customer story or testimonial page",
 "help-docs": "Support documentation, FAQ, API reference, changelog or product update notes",
 "skip": "Legal, policy, signup, login, thank-you, careers, brand, test, duplicate or utility pages with no marketing content",
}
def ask(row, site):
    body = json.dumps({"model": "jev-1.13.0", "state": {"company": site, "url_path": row["path"]},
      "questions": {"type": {"type": "choice", "instructions": "Judging only from the URL path of a page on the company's marketing website, what kind of page is `url_path`?", "criteria": OPTS}}}).encode()
    for attempt in range(4):
        try:
            req = urllib.request.Request("https://api.typesafe.ai/v1/systemone", data=body, headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 ci-inventory"})
            r = json.load(urllib.request.urlopen(req, timeout=30))
            a = r["answers"]["type"]; return a["choice"], round(a["confidence"], 2), r["usage"]["input_tokens"]
        except Exception as e:
            time.sleep(2 ** attempt)
    return "unclassified", 0, 0
d = json.load(open("bucketed.json")); jobs = [(r, n) for g in d for n, rows in d[g].items() for r in rows if r["bucket"] == "other"]
print(len(jobs), "to classify", flush=True)
tok = 0
with ThreadPoolExecutor(12) as ex:
    for (r, n), (b, c, t) in zip(jobs, ex.map(lambda j: ask(*j), jobs)):
        r["bucket"], r["jev_conf"], r["by"] = b, c, "jev-1.13.0"; tok += t
json.dump(d, open("bucketed.json", "w"), indent=1)
print("input tokens", tok, "est $", round(tok / 1e6 * 0.042, 4))
