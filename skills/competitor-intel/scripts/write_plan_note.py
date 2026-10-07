"""Write Site structure plan.md from site-structure-plan.json (hubs, pages, status, target keyword, volumes, linking rules).
Usage: write_plan_note.py <config.json> <raw_dir>"""
import json, sys
cfg = json.load(open(sys.argv[1])); raw = sys.argv[2]; V = cfg["vault_dir"]
P = json.load(open(f"{raw}/site-structure-plan.json"))
locs = list(cfg.get("locations", {"US": 0}))
tot = sum(len(s["pages"]) for s in P["sections"]); new = sum(1 for s in P["sections"] for p in s["pages"] if p["status"] == "new")
L = ["---", "type: site-structure-plan", f"project: {cfg['project']}", "tags: [seo, site-structure, internal-linking, plan]", "---", "", "# Site structure plan", "",
     f"Part of [[Competitive research]]. The structure {cfg['project']} should grow into: {len(P['sections'])} hubs, {tot} pages, {new} of them new. Hubs follow what competitors run (see [[Site structure]]); each page carries the keyword it targets from [[Keyword research]], with monthly volume for {' and '.join(locs)} summed over its keyword group, and the highest difficulty in the group.", "",
     "```", "/"]
for s in P["sections"]:
    L.append(f"├── {s['hub']}  ({s['status']})")
    for p in s["pages"]: L.append(f"│   ├── {p['path']}  [{p['status']}]")
L += ["```", ""]
for s in P["sections"]:
    L += [f"## {s['label']}: {s['hub']}", "", f"Status: {s['status']}. Why: {s['why']}.", ""]
    if s["pages"]:
        L += ["| Page | Status | Target keyword | " + " | ".join(f"{l}/mo" for l in locs) + " | Difficulty |", "|" + "---|" * (4 + len(locs))]
        for p in s["pages"]:
            L.append(f"| {p['path']} | {p['status']} | {p['keyword'] or '-'} | " + " | ".join(str(p.get(f'volume_{l.lower()}', 0)) for l in locs) + f" | {p['difficulty'] if p['difficulty'] is not None else '-'} |")
        L.append("")
L += ["## Internal linking rules", ""] + [f"{i}. {r}" for i, r in enumerate(P["linking_rules"], 1)] + [""]
open(f"{V}/Site structure plan.md", "w").write("\n".join(L)); print("ok")
