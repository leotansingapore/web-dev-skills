# One note per competitor with the heading/CTA anatomy of every fetched landing page.
# Usage: write_anatomy_notes.py <config.json> <raw_dir>
import json, sys, os
os.chdir(sys.argv[2]); cfg = json.load(open(sys.argv[1]))
a = json.load(open("anatomy_full.json")); sites = {g: v["competitors"] for g, v in cfg["groups"].items()}
V = cfg["vault_dir"] + "/Landing pages"; os.makedirs(V, exist_ok=True)
ORDER = ["home","core","feature","feature-cluster","use-case","comparison","free-tool","template"]
for g in a:
    for n, ps in a[g].items():
        ps = [p for p in ps if p.get("status") == 200]
        if not ps: continue
        L = ["---", f"competitor: {n}", f"group: {g}", f"site: {sites[g][n]}", f"pages: {len(ps)}", "harvested: 2026-09-24", "tags: [competitor, landing-page]", "---", "",
             f"# {n} landing pages", "", f"Part of [[Competitive research]]. Full URL list: [[{n}]]. Patterns across all competitors: [[Landing page inventory - what to use]].", ""]
        for b in ORDER:
            for p in [p for p in ps if p["bucket"] == b]:
                L += [f"## {b}: {(p.get('h1') or [p.get('title','')])[0][:110]}", "", f"- URL: {p['url']}", f"- Title: {p.get('title','')}", f"- Meta: {p.get('meta','')}", f"- Words (incl. nav): {p.get('words')}"]
                if p.get("schema"): L.append(f"- Schema: {', '.join(p['schema'])}")
                if p.get("ctas"): L.append(f"- CTAs: {' | '.join(p['ctas'][:10])}")
                if p.get("h2"): L += ["- H2s:"] + [f"    - {h}" for h in p["h2"][:25]]
                if p.get("h3"): L += ["- H3s:"] + [f"    - {h}" for h in p["h3"][:30]]
                L.append("")
        open(f"{V}/{n} landing pages.md", "w").write("\n".join(L))
print("ok")
