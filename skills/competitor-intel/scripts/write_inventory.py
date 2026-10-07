# Write one Obsidian note per competitor listing every English page by content type, plus a CSV of everything.
# Usage: write_inventory.py <config.json> <raw_dir>
import json, sys, csv, re, os
os.chdir(sys.argv[2]); cfg = json.load(open(sys.argv[1]))
from urllib.parse import urlparse
d = json.load(open("bucketed.json")); sites = {g: v["competitors"] for g, v in cfg["groups"].items()}
V = cfg["vault_dir"]; os.makedirs(f"{V}/Content inventory", exist_ok=True)
ORDER = [("free-tool","Free tools"),("template","Templates and libraries"),("guide","Guides, ebooks, academy, webinars"),("comparison","Comparison and alternative pages"),("feature","Feature pages"),("feature-cluster","Feature clusters (topic hubs)"),("use-case","Use case, industry, role pages"),("glossary","Glossary"),("paid-or-geo-lp","Paid and geo landing pages"),("case-study","Case studies"),("integration","Integration pages"),("blog","Blog posts"),("help-docs","Help and docs"),("core","Core pages"),("home","Home")]
GROUP = {g: v.get("label", g) for g, v in cfg["groups"].items()}
TOPIC = {}
if os.path.exists("jev-topics.csv"):
    TOPIC = {r["url"]: (r["topic"], float(r["topic_conf"]), float(r.get("niche_p") or r.get("insurance_p") or 0)) for r in csv.DictReader(open("jev-topics.csv"))}
def title(path):
    s = [x for x in path.split("/") if x]
    return re.sub(r"[-_]+", " ", s[-1]).strip().capitalize() if s else "Home"
w = csv.writer(open("content-inventory.csv", "w", newline="")); w.writerow(["group","competitor","bucket","title_from_slug","url","classified_by","jev_confidence"])
for g in d:
    for n, rows in d[g].items():
        rows = [r for r in rows if r["bucket"] not in ("skip","unclassified")]
        if not rows: continue
        for r in rows: w.writerow([g, n, r["bucket"], title(r["path"]), r["url"], r.get("by","directory"), r.get("jev_conf","")])
        cnt = {b: sum(1 for r in rows if r["bucket"] == b) for b, _ in ORDER}
        L = ["---", f"competitor: {n}", f"group: {g}", f"site: {sites[g][n]}", f"pages: {len(rows)}", "harvested: 2026-09-24", "tags: [competitor, content-inventory]", "---", "",
             f"# {n} content inventory", "", f"Part of [[Competitive research]]. Group: {GROUP[g]}. Page anatomy: [[{n} landing pages]].", "",
             "Every English URL from the site's sitemap, deduped across locales. Titles come from the URL slug. (jev NN) means Jev typed the page from its path alone at NN% confidence; under 50 is worth a second look. #topic is the topic Jev tagged it with, and #niche means Jev judged it written for our niche audience.", "",
             "| Type | Pages |", "|---|---|"] + [f"| {lbl} | {cnt[b]} |" for b, lbl in ORDER if cnt[b]] + [""]
        for b, lbl in ORDER:
            rs = [r for r in rows if r["bucket"] == b]
            if not rs: continue
            L += [f"## {lbl} ({len(rs)})", ""]
            for r in sorted(rs, key=lambda r: r["path"]):
                tag = f" (jev {int(r['jev_conf']*100)})" if r.get("by") else ""
                t = TOPIC.get(r["url"])
                if t and t[0] != "none" and t[1] >= 0.4: tag += f" #{t[0]}"
                if t and t[2] >= 0.5: tag += " #niche"
                L.append(f"- [{title(r['path'])}]({r['url']}){tag}")
            L.append("")
        open(f"{V}/Content inventory/{n}.md", "w").write("\n".join(L))
        print(n, len(rows))
