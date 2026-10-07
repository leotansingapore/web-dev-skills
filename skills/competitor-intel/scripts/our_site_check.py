"""Check that each of our public pages serves crawlers its own title, H1 and canonical (no JS). A page whose canonical
points elsewhere, or that shows the default title with no H1, cannot rank no matter how good its copy is.
Usage: our_site_check.py <config.json> <raw_dir>  -> prints a table, writes our-site-check.json"""
import json, sys, re, urllib.request
cfg = json.load(open(sys.argv[1])); raw = sys.argv[2]; out = []
for u in cfg.get("our_pages", []):
    try:
        h = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)"}), timeout=30).read().decode("utf-8", "replace")
    except Exception as e:
        out.append({"url": u, "error": str(e)[:80]}); continue
    title = (re.findall(r"<title[^>]*>(.*?)</title>", h, re.S) or [""])[0].strip()
    canon = (re.findall(r'rel="canonical"[^>]*href="([^"]+)"', h) or re.findall(r'href="([^"]+)"[^>]*rel="canonical"', h) or [""])[0]
    h1 = len(re.findall(r"<h1[\s>]", h))
    ok = bool(title) and h1 >= 1 and (canon.rstrip("/") == u.rstrip("/") or not canon)
    out.append({"url": u, "title": title[:90], "h1": h1, "canonical": canon, "ok": ok})
titles = [o.get("title") for o in out]
for o in out:
    if o.get("title") and titles.count(o["title"]) > 1: o["ok"] = False; o["dup_title"] = True
json.dump(out, open(f"{raw}/our-site-check.json", "w"), indent=1)
bad = [o for o in out if not o.get("ok")]
for o in out: print("OK " if o.get("ok") else "BAD", o["url"], "|", o.get("title", o.get("error")), "| h1", o.get("h1"), "| canonical", o.get("canonical"))
print(f"{len(bad)} of {len(out)} pages cannot rank as served")
