"""Write the build plan into the vault: one note per item under 'Build plan/Items', an Obsidian Base over them, and
'Build plan.md' with the phases and full static tables. Inputs in raw_dir: build-items.json (structured items),
blog-items.json (optional), plan-keywords.csv (volumes and Jev judgments), feature-map.csv (reference pages).
Priority = (home volume x HOME_WEIGHT + other volume, over the keyword and its secondaries) x fit / (1 + difficulty/50);
fit 1 when Jev says the searcher is in our niche or the product fits (intent >= 0.67), 0.4 adjacent (people managers, business owners, or sales outside the niche when the niche is narrower), 0.03 otherwise.
Usage: write_build_plan.py <config.json> <raw_dir>"""
import json, sys, os, re, csv, collections, shutil
cfg = json.load(open(sys.argv[1])); raw = sys.argv[2]; V = cfg["vault_dir"]; D = f"{V}/Build plan"; ITEMS = f"{D}/Items"
LOCS = list(cfg.get("locations", {"US": 0})); HOME, OTHER = LOCS[0], LOCS[-1]; HW = cfg.get("home_weight", 5)
items = json.load(open(f"{raw}/build-items.json")) + (json.load(open(f"{raw}/blog-items.json")) if os.path.exists(f"{raw}/blog-items.json") else [])
K = {r["keyword"]: r for r in csv.DictReader(open(f"{raw}/plan-keywords.csv"))}
f = lambda v: float(v) if v not in ("", None, "None") else 0.0
FM = collections.defaultdict(list); BYCOMP = collections.defaultdict(list)
for d in [raw] + cfg.get("extra_raw_dirs", []):   # other research sets add their references
    if os.path.exists(f"{d}/feature-map.csv"):
        for r in csv.DictReader(open(f"{d}/feature-map.csv")):
            if "(ours)" in r["competitor"]: continue
            BYCOMP[r["competitor"]].append(r)
            if f(r["feature_conf"]) >= 0.4: FM[r["feature"]].append(r)
for k in FM: FM[k].sort(key=lambda r: -f(r["composite"]))
for k in BYCOMP: BYCOMP[k].sort(key=lambda r: -f(r["composite"]))
def fit(k):
    r = K.get(k)
    if not r: return 0.0, "unmeasured"
    # the niche's own customers (job seekers here, policy buyers on AT) never buy the product, however well it "fits"
    if r.get("searcher") == "our-customers": return 0.03, "off-audience"
    if r.get("searcher") == "ours" or f(r.get("intent")) >= 0.67: return 1.0, "niche"
    if r.get("searcher") in ("sales-general", "manager-hr", "business-owner"): return 0.4, "adjacent"
    return 0.03, "off-audience"
TYPE_LABEL = {"fix": "Fix or improve a live page", "hub": "Hub page", "feature": "Feature page", "job-page": "Job page", "audience": "Audience page", "free-tool": "Free tool", "template": "Template",
              "template-set": "Template (programmatic)", "guide": "Guide", "ebook-chapter": "Pillar guide chapter", "glossary": "Glossary term", "comparison": "Comparison or list",
              "integration": "Integration page", "customer-story": "Customer story", "calculator-set": "Calculator (programmatic)", "kpi-set": "KPI page (programmatic)", "blog": "Blog article"}
def single(k):
    r = K.get(k, {}); w, _ = fit(k)
    kd = f(r.get("difficulty")) if r.get("difficulty") not in ("", None, "None") else 0
    return (f(r.get(f"vol_{HOME}")) * HW + f(r.get(f"vol_{OTHER}"))) * w / (1 + kd / 50)
for it in items:
    # Naming variants (item["alt"]): the best-scoring phrasing becomes the primary keyword, the rest stay as secondaries.
    cands = [k for k in [it.get("keyword", "")] + it.get("alt", []) if k]
    if len(cands) > 1:
        best = max(cands, key=single)
        it["keyword"] = best; it["also"] = list(dict.fromkeys(it.get("also", []) + [k for k in cands if k != best]))
for it in items:
    ks = [k for k in [it.get("keyword", "")] + it.get("also", []) if k]
    it["vol_home"] = int(sum(f(K.get(k, {}).get(f"vol_{HOME}")) for k in ks)); it["vol_other"] = int(sum(f(K.get(k, {}).get(f"vol_{OTHER}")) for k in ks))
    kd = [f(K[k]["difficulty"]) for k in ks if k in K and K[k].get("difficulty") not in ("", None, "None")]; it["difficulty"] = int(max(kd)) if kd else None
    w, lab = fit(it.get("keyword", "")) if it.get("keyword") else (0.0, "no keyword")
    it["fit"] = lab; it["score"] = round((it["vol_home"] * HW + it["vol_other"]) * w / (1 + (it["difficulty"] or 0) / 50), 1)
    tgt = cfg.get("comparison_targets", {}).get(it["url"])
    if tgt and tgt in BYCOMP: it["refs"] = [r["url"] for r in BYCOMP[tgt][:5]]
    elif it.get("feature") in FM:
        it["refs"] = list(dict.fromkeys(it.get("refs", []) + [r["url"] for r in FM[it["feature"]][:5]]))[:8]
blogs = sorted([i for i in items if i["type"] == "blog"], key=lambda i: -i["score"])
for n, b in enumerate(blogs): b["phase"] = 3 if n < 60 else 4
for it in items:
    if it.get("phase") is None: it["phase"] = 3
PHASE = {0: "Phase 0: fix what is live", 1: "Phase 1: hubs and the pages with the most demand", 2: "Phase 2: tools, templates, audience pages, first guides",
         3: "Phase 3: comparisons, programmatic sets, glossary, first 60 articles", 4: "Phase 4: publishing cadence"}
slug = lambda u: re.sub(r"[^a-z0-9]+", "-", u.lower()).strip("-") or "home"
if os.path.isdir(ITEMS): shutil.rmtree(ITEMS)
os.makedirs(ITEMS, exist_ok=True)
seen = collections.Counter()
for it in items:
    base = slug(it["url"]) + ("-" + slug(it["title"])[:40] if it["type"] == "fix" else ""); seen[base] += 1
    it["note"] = base + (f"-{seen[base]}" if seen[base] > 1 else "")
    hub = "/" + it["url"].strip("/").split("/")[0] if it["url"].count("/") >= 2 else ""
    fm = ["---", f"type: {it['type']}", f"url: \"{it['url']}\"", f"title: \"{it['title'].replace(chr(34), '')}\"", f"phase: {it['phase']}", f"status: {'fix' if it['type'] == 'fix' else 'todo'}",
          f"keyword: \"{it.get('keyword', '')}\"", f"vol_{HOME.lower()}: {it['vol_home']}", f"vol_{OTHER.lower()}: {it['vol_other']}", f"difficulty: {it['difficulty'] if it['difficulty'] is not None else ''}",
          f"fit: {it['fit']}", f"score: {it['score']}", f"compliance: {str(bool(it.get('compliance'))).lower()}", f"topic: {it.get('topic', '')}", "tags: [build-plan]", "---", ""]
    body = [f"# {it['title']}", "", f"{TYPE_LABEL.get(it['type'], it['type'])}. {PHASE[it['phase']]}. Part of [[Build plan]].", ""]
    if it.get("keyword"):
        body += [f"Target keyword: **{it['keyword']}**" + (f", also {', '.join(it['also'])}" if it.get("also") else "") + f". {HOME} {it['vol_home']}/mo, {OTHER} {it['vol_other']}/mo" + (f", difficulty {it['difficulty']}" if it["difficulty"] is not None else "") + f". Searcher fit: {it['fit']}. Priority score {it['score']}.", ""]
    if it.get("angle"): body += [f"Angle: {it['angle']}", ""]
    if it.get("notes"): body += [it["notes"], ""]
    if it.get("compliance"): body += ["Compliance check before this goes public.", ""]
    if it.get("refs"): body += ["## Pages to beat", ""] + [f"- {u}" for u in it["refs"][:8]] + [""]
    links = [x for x in [hub if hub and hub != it["url"] else "", f"/features/{it['feature']}" if False else ""] if x]
    body += ["## Links", "", f"- Up to its hub: {hub or 'n/a'}", "- Across to 2 to 4 siblings in the same hub", "- To the feature that does this job, and from that feature back", ""]
    body += ["## Checklist", "", "- [ ] Brief section from competitors (CLAUDE.md step 0)", "- [ ] Hooks pooled and scored (hook-check)", "- [ ] Draft as .md, aicheck and brief-check pass", "- [ ] Leo reads the .md",
             "- [ ] Built and added to scripts/marketing-routes.mjs (prerender and sitemap follow)", "- [ ] Internal links in and out", "- [ ] Live and fetched as Googlebot"] if it["type"] not in ("fix",) else ["## Checklist", "", "- [ ] Change made", "- [ ] Verified live as Googlebot"]
    open(f"{ITEMS}/{it['note']}.md", "w").write("\n".join(fm + body) + "\n")
base = """filters:
  and:
    - file.inFolder("Competitive Research/Build plan/Items")
formulas:
  demand: 'vol_%s * %d + vol_%s'
properties:
  formula.demand:
    displayName: "Demand"
views:
  - type: table
    name: "All by priority"
    order: [file.name, type, phase, keyword, vol_%s, vol_%s, difficulty, fit, score, status]
  - type: table
    name: "By phase"
    groupBy:
      property: phase
      direction: ASC
    order: [file.name, type, keyword, vol_%s, vol_%s, score, status]
  - type: table
    name: "By type"
    groupBy:
      property: type
      direction: ASC
    order: [file.name, phase, keyword, vol_%s, vol_%s, score, status]
  - type: table
    name: "Phase 0 and 1"
    filters: 'phase <= 1'
    order: [file.name, type, keyword, vol_%s, vol_%s, score, status]
  - type: table
    name: "Blog backlog"
    filters: 'type == "blog"'
    order: [file.name, topic, keyword, vol_%s, vol_%s, difficulty, fit, score, phase]
  - type: table
    name: "Compliance check"
    filters: 'compliance == true'
    order: [file.name, type, phase]
""" % ((HOME.lower(), HW, OTHER.lower()) + (HOME.lower(), OTHER.lower()) * 5)
open(f"{D}/Build plan.base", "w").write(base)
json.dump(items, open(f"{raw}/build-plan-final.json", "w"), indent=1)
w = csv.writer(open(f"{raw}/build-plan.csv", "w", newline="")); w.writerow(["phase", "type", "url", "title", "keyword", f"vol_{HOME}", f"vol_{OTHER}", "difficulty", "fit", "score", "compliance", "refs"])
for it in sorted(items, key=lambda i: (i["phase"], -i["score"])): w.writerow([it["phase"], it["type"], it["url"], it["title"], it.get("keyword", ""), it["vol_home"], it["vol_other"], it["difficulty"], it["fit"], it["score"], it.get("compliance", False), " ".join(it.get("refs", [])[:5])])
print(len(items), "items;", collections.Counter(i["type"] for i in items), collections.Counter(i["phase"] for i in items))
