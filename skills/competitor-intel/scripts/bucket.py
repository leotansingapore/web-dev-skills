# Normalize harvested URLs (English only, deduped across locales) and bucket them by the site's own directory.
# Leftovers stay "other" for jev_classify.py. Usage: bucket.py <raw_dir>  -> bucketed.json
import json, re, collections, sys, os
from urllib.parse import urlparse
os.chdir(sys.argv[1]); d = json.load(open("sitemaps.json"))
LOC = re.compile(r"^(en|en-sg|en-us|en-gb|en-in|en-au|de|de-de|es|fr|it|pt|pt-br|nl|ja|ko|zh|zh-hk|zh-cn|zh-tw|zh-hant|zh-hans|id|id-id|ar|tr|ru|pl|vi|th|ms|tw|hi|br|no|nb|sv|da|fi|cs|he|hu|ro|uk|el)$")
NONEN = LOC.pattern.replace("en|en-sg|en-us|en-gb|en-in|en-au|", "")
DIRS = {
 "blog": "blog a blog-posts post posts articles article news insights stories-blog",
 "guide": "video-tutorials learning-centre guides guide ebook ebooks resources resource-center resource_center learning-article learning-micro-lessons learning-centre learning-topic academy interakt-academy tutorials playbooks webinars events methodologies research",
 "free-tool": "tools tool free-tools bill-estimator",
 "template": "templates template whatsapp-template whatsapp-templates whatsapp-chatbot-templates whatsapp-chatbot-template ai-agent-library whatsapp-ai-agent-library marketplace messenger-marketing-examples mcp",
 "comparison": "compare comparison alternatives alternative alternative-to vs best",
 "integration": "integrations integration integrationen whatsapp-integrations channels-integrations zapier-integrations plugins",
 "feature": "features feature product products functions tour",
 "use-case": "use-cases use-case solutions solution for industries industry role team-size agencies initiatives teams ea",
 "case-study": "customers customer case-study case-studies cases customer-stories success-stories stories client",
 "glossary": "glossary",
 "help-docs": "help docs reference developers",
 "paid-or-geo-lp": "lp geo",
}
D2B = {w: b for b, ws in DIRS.items() for w in ws.split()}
SKIP = re.compile(r"^(legal|privacy|terms|careers|jobs|category|categories|blog-category|blog-categories|tag|tags|author|authors|blog-authors|page|presse|press|partnership|partnerships|partner|partners|affiliate|affiliate-program|cdn-cgi|wp-content|sitemap)")
out = {}
for g in d:
  for n, v in d[g].items():
    urls = {}
    for u in v["urls"]:
      p = urlparse(u); segs = [s for s in p.path.split("/") if s]
      if segs and re.match(NONEN, segs[0].lower()): continue   # non-English copy
      if segs and re.match(r"^[a-z]{2}-[a-z]{2}$", segs[0].lower()) and not segs[0].lower().startswith("en"): continue
      if segs and re.match(r"^geo-.*-(es|pt|ar|id|de|fr|it)$", segs[0].lower()): continue
      if segs and LOC.match(segs[0].lower()): segs = segs[1:]    # en / en-sg prefix
      key = "/" + "/".join(segs)
      if segs and SKIP.match(segs[0].lower()): continue
      if re.search(r"/page/\d+|\?|/feed/?$", key): continue
      if len(segs) >= 2 and segs[-2] in ("category","tag","author","page"): continue
      urls.setdefault(key, u)
    rows = []
    for key, u in sorted(urls.items()):
      segs = [s for s in key.split("/") if s]
      first = segs[0].lower() if segs else ""
      b = D2B.get(first)
      if b is None and first.startswith("whatsapp-") and len(segs) > 1: b = "feature-cluster"
      if not segs: b = "home"
      if first in ("pricing","about","contact","download","downloads","security","signup","login","demo","book-a-demo"): b = "core"
      rows.append({"url": u, "path": key, "bucket": b or "other"})
    out.setdefault(g, {})[n] = rows
json.dump(out, open("bucketed.json", "w"), indent=1)
tot = collections.Counter()
for g in out:
  for n, rows in out[g].items():
    c = collections.Counter(r["bucket"] for r in rows); tot.update(c)
    print(f"{n:12} {len(rows):5} ", dict(c.most_common()))
print("TOTAL", sum(tot.values()), dict(tot))
