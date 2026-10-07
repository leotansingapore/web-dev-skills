"""Merge the CLI blog-planning batches (blogplan/<topic>-<n>.out.json against .in.json) into blog-items.json.
Articles whose keywords are the same set of words (order, plurals and small words ignored) are merged (refs combined); an article whose keyword a structured item already
targets is dropped, so the blog never competes with its own landing pages. Usage: merge_blog_plan.py <raw_dir>"""
import json, sys, os, re, glob, collections
raw = sys.argv[1]; os.chdir(raw)
STOP = {"a", "an", "the", "for", "to", "of", "in", "on", "and", "or", "with", "how", "what", "is", "your", "my", "vs"}
wordset = lambda k: " ".join(sorted({w.rstrip("s") for w in re.findall(r"[a-z0-9]+", k.lower())} - STOP))
taken = set()
for it in json.load(open("build-items.json")):
    taken |= {wordset(k) for k in [it.get("keyword", "")] + it.get("also", []) if k}
by = {}; dropped = 0; total = 0
for out in sorted(glob.glob("blogplan/*.out.json")):
    jid = os.path.basename(out)[:-9]; topic = re.sub(r"-\d+$", "", jid)
    src = {x["id"]: x for x in json.load(open(f"blogplan/{jid}.in.json"))}
    for a in json.load(open(out)):
        total += 1
        kw = re.sub(r"\s+", " ", str(a.get("keyword", "")).lower()).strip()
        ws = wordset(kw)
        if not kw or ws in taken: dropped += 1; continue
        refs = [src[i]["url"] for i in a.get("refs", []) if i in src]
        if ws in by: by[ws]["refs"] = list(dict.fromkeys(by[ws]["refs"] + refs)); continue
        title = re.sub(r"\s+", " ", str(a.get("title", ""))).strip().replace("—", ",").replace("–", "-")
        s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:70]
        by[ws] = {"type": "blog", "url": f"/blog/{s}", "title": title, "keyword": kw, "also": [], "feature": "", "status": "new", "angle": a.get("angle", ""), "refs": refs, "topic": topic, "phase": None, "compliance": False, "notes": ""}
json.dump(list(by.values()), open("blog-items.json", "w"), indent=1)
print(f"{total} proposed, {dropped} dropped (keyword owned by a structured page), {len(by)} blog items;", collections.Counter(b["topic"] for b in by.values()).most_common())
