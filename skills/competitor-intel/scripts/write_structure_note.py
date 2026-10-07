"""Write Site structure.md: how competitors organise their sites (sections, depth, programmatic families, footer hubs)
and our current internal link graph if at-link-graph.json exists. Usage: write_structure_note.py <config.json> <raw_dir>"""
import json, sys, os, collections
cfg = json.load(open(sys.argv[1])); raw = sys.argv[2]; V = cfg["vault_dir"]
S = json.load(open(f"{raw}/site-structure.json")); C = S["competitors"]; n = len(C)
LABEL = {"blog": "Blog", "feature": "Feature pages", "integration": "Integrations", "comparison": "Comparisons and alternatives", "guide": "Guides, ebooks, academy", "case-study": "Customer stories", "use-case": "Use case, industry, role pages", "help-docs": "Help and docs", "free-tool": "Free tools", "template": "Templates", "glossary": "Glossary", "paid-or-geo-lp": "Paid and geo landing pages", "feature-cluster": "Feature topic hubs"}
L = ["---", "type: site-structure", "tags: [competitor, seo, site-structure, internal-linking]", "---", "", "# Site structure", "",
     f"Part of [[Competitive research]]. How {n} competitors organise their sites, from their sitemaps (English pages) and the links in each homepage's footer. The plan for our own structure is in [[Site structure plan]].", "",
     "## Which sections competitors run", "", "| Section | Competitors with it | Share |", "|---|---|---|"]
L += [f"| {LABEL.get(k, k)} | {v} | {100 * v // n}% |" for k, v in S["section_types_used_by"].items()]
L += ["", "## Programmatic families", "", "One parent folder with 20 or more templated children. This is how the largest sites reach thousands of pages.", "", "| Competitor | Parent | Pages |", "|---|---|---|"]
for c, d in sorted(C.items(), key=lambda x: -x[1]["pages"]):
    for f in d["programmatic"][:4]: L.append(f"| [[{c}]] | {f['parent']} | {f['children']} |")
L += ["", "## Each competitor's sections", "", "| Competitor | Pages | Median depth | Largest sections |", "|---|---|---|---|"]
for c, d in sorted(C.items(), key=lambda x: -x[1]["pages"]):
    L.append(f"| [[{c}]] | {d['pages']} | {d['depth_median']} | " + ", ".join(f"{s['path']} ({s['pages']})" for s in d["sections"][:7]) + " |")
foot = collections.Counter()
for d in C.values(): foot.update({p.split("/")[1] if p.count("/") >= 1 and p != "/" else "/" for _, p in d["nav"].get("footer", [])})
L += ["", "## What footers link to", "", "First path segment of footer links, counted once per competitor. Footers are where most of these sites expose their hubs to crawlers.", "", ", ".join(f"/{k} ({v})" for k, v in foot.most_common(30) if k not in ("/", "")), ""]
gp = f"{raw}/at-link-graph.json"
if os.path.exists(gp):
    g = json.load(open(gp)); inb = collections.Counter(t for s, ts in g.items() for t in ts if t != s)
    L += ["## Our pages today", "", "Links found in the HTML crawlers receive (no JavaScript), for every URL in our sitemap.", "", "| Page | Links out | Links in |", "|---|---|---|"]
    L += [f"| {p} | {len(ts)} | {inb.get(p, 0)} |" for p, ts in g.items()]
    orph = [p for p in g if inb.get(p, 0) == 0 and p != "/"]
    L += ["", "Orphans (nothing links to them): " + (", ".join(orph) or "none") + ".", ""]
open(f"{V}/Site structure.md", "w").write("\n".join(L)); print("ok")
