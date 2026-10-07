"""Write the feature map and one note per feature (ranked competitor reference pages with their section outlines, our
page's score beside them). Usage: write_feature_notes.py <config.json> <raw_dir>"""
import json, sys, csv, os
cfg = json.load(open(sys.argv[1])); raw = sys.argv[2]; V = cfg["vault_dir"]; os.makedirs(f"{V}/Features", exist_ok=True)
pri = json.load(open(f"{raw}/feature-priority.json")); rows = list(csv.DictReader(open(f"{raw}/feature-map.csv")))
an = json.load(open(f"{raw}/anatomy_full.json")); byurl = {p["url"]: p for g in an for n in an[g] for p in an[g][n]}
if os.path.exists(f"{raw}/our_pages.json"): byurl.update({p["url"]: p for p in json.load(open(f"{raw}/our_pages.json"))})
for r in rows:
    for k in ("composite", "feature_conf", "reference", "outcome", "clarity", "specificity", "proof", "structure"): r[k] = float(r.get(k) or 0)
rn = list(cfg["readers"])
L = ["---", "type: feature-map", f"project: {cfg['project']}", "tags: [competitor, features, landing-page]", "---", "", "# Feature map", "",
     f"Part of [[Competitive research]]. Every competitor landing page and every {cfg['project']} page was mapped by Jev to one feature below, then scored as a reference for building a landing page. Click a feature for its ranked reference pages.", "",
     "Priority is out of 10: 60% how much the reader cares (the higher of the two readers, scored by Jev), 40% how many competitors market it. Uncontested features score low on the second half by design, so read the Market column alongside it. \"We have it\" is Jev reading the brief plus the app's routes.", "",
     "| Priority | Feature | " + " | ".join(f"Care: {x}" for x in rn) + " | Competitors | Market | Our status | Our best page |", "|" + "---|" * (6 + len(rn))]
for p in pri:
    ours = [r for r in rows if "(ours)" in r["competitor"] and r["feature"] == p["feature"] and r["feature_conf"] >= 0.6]
    ob = max(ours, key=lambda r: r["composite"]) if ours else None
    L.append(f"| {p['priority']} | [[{p['feature']}]] | " + " | ".join(str(p.get(f'care_{x}')) for x in rn) + f" | {len(p['competitors'])} | {p['contested']} | {p['status']} | " + (f"{ob['url'].split('/',3)[-1] or '/'} ({ob['composite']})" if ob else "-") + " |")
open(f"{V}/Feature map.md", "w").write("\n".join(L) + "\n")
for p in pri:
    f = p["feature"]; cr = sorted([r for r in rows if r["feature"] == f and "(ours)" not in r["competitor"] and r["feature_conf"] >= 0.4], key=lambda r: -r["composite"])
    ours = [r for r in rows if "(ours)" in r["competitor"] and r["feature"] == f]
    N = ["---", "type: feature", f"feature: {f}", f"priority: {p['priority']}", f"status: {p['status']}", "tags: [feature, landing-page]", "---", "", f"# {f}", "", f"{p['definition']}.", "",
         f"Part of [[Feature map]]. Priority {p['priority']}/10. " + ", ".join(f"{x} care {p.get(f'care_{x}')}" for x in rn) + f". {len(p['competitors'])} competitors market it ({', '.join(p['competitors']) or 'none'}). Our status: {p['status']}.", ""]
    if ours:
        N += ["## Our pages", "", "| Page | Score /10 | Outcome | Clarity | Specific | Proof | Structure | H1 |", "|---|---|---|---|---|---|---|---|"]
        for r in ours: N.append(f"| {r['url']} | {r['composite']} | {r['outcome']:.2f} | {r['clarity']:.2f} | {r['specificity']:.2f} | {r['proof']:.2f} | {r['structure']:.2f} | {r['h1'][:80]} |")
        N.append("")
    if cr:
        N += ["## Reference pages, ranked", "", "Score out of 10: 25% Jev's reference value, 20% states an outcome, 15% clarity, 15% specificity, 10% proof, 15% structure (FAQ, schema, CTAs, length, sections; measured in code).", "",
              "| # | Score | Competitor | Page | H1 | Outcome | Proof |", "|---|---|---|---|---|---|---|"]
        for i, r in enumerate(cr[:20], 1): N.append(f"| {i} | {r['composite']} | [[{r['competitor']}]] | {r['url']} | {r['h1'][:90].replace('|','/')} | {r['outcome']:.2f} | {r['proof']:.2f} |")
        N += ["", "## Section outlines of the top three", ""]
        for r in cr[:3]:
            a = byurl.get(r["url"], {})
            N += [f"### {r['competitor']}: {r['h1'][:100]}", "", f"{r['url']} (score {r['composite']}, {a.get('words','?')} words incl. nav)", ""]
            if a.get("meta"): N.append(f"- Meta: {a['meta']}")
            if a.get("ctas"): N.append(f"- CTAs: {' | '.join(a['ctas'][:6])}")
            N += [f"- H2: {h}" for h in (a.get("h2") or [])[:18]] + [""]
    else:
        N += ["## Reference pages", "", "No competitor has a landing page for this feature. Nothing to copy, nothing to beat: build the page from the brief and borrow structure from the nearest feature.", ""]
    open(f"{V}/Features/{f}.md", "w").write("\n".join(N))
print("wrote", len(pri), "feature notes")
