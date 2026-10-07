"""Write 'Build plan.md': what to build, in what order, with every item in static tables and the Base views embedded.
Reads build-plan-final.json (from write_build_plan.py). Usage: write_build_master.py <config.json> <raw_dir>"""
import json, sys, collections
cfg = json.load(open(sys.argv[1])); raw = sys.argv[2]; V = cfg["vault_dir"]
I = json.load(open(f"{raw}/build-plan-final.json")); LOCS = list(cfg.get("locations", {"US": 0})); H, O = LOCS[0], LOCS[-1]
ORDER = ["fix", "hub", "feature", "job-page", "audience", "free-tool", "template", "guide", "ebook-chapter", "comparison", "glossary", "template-set", "kpi-set", "integration", "customer-story", "calculator-set", "blog"]
LABEL = {"fix": "Fixes to live pages", "hub": "Hubs", "feature": "Feature pages", "job-page": "Job pages", "audience": "Audience pages", "free-tool": "Free tools", "template": "Templates",
         "guide": "Guides", "ebook-chapter": "Pillar guide chapters", "comparison": "Comparisons and lists", "glossary": "Glossary", "template-set": "Template families (programmatic)",
         "integration": "Integrations", "customer-story": "Customer stories", "calculator-set": "Commission calculator per product (programmatic)", "kpi-set": "Sales KPI library (programmatic)", "blog": "Blog articles"}
PH = {0: "Fix what is live", 1: "Hubs and the pages with the most demand", 2: "Tools, templates, audience pages, first guides", 3: "Comparisons, programmatic sets, glossary, first 60 articles", 4: "Publishing cadence"}
c = collections.Counter(i["type"] for i in I); p = collections.Counter(i["phase"] for i in I)
dem = lambda xs: (sum(i["vol_home"] for i in xs), sum(i["vol_other"] for i in xs))
L = ["---", "type: build-plan", f"project: {cfg['project']}", "tags: [build-plan, seo, content-plan]", "---", "", "# Build plan", "",
     f"Everything {cfg['project']} should build, fix or publish, drawn from [[Competitive research]]: {len(I)} items. Each item is its own note in `Build plan/Items` with the target keyword, search volume, difficulty, who searches it, a priority score, the competitor pages to beat, and a checklist. The Base below sorts and filters them; the tables under it list every item.", "",
     f"Priority score = ({H} volume x {cfg.get('home_weight', 5)} + {O} volume) x fit / (1 + difficulty / 50). Volumes are summed over the target keyword and its secondaries (DataForSEO; 10 means 10 or fewer). Fit is Jev's read of who searches the keyword: 1 for our niche or when the product fits, 0.4 for salespeople and managers outside it, 0.03 for everyone else (so a huge generic volume, such as 'what is a crm', cannot outrank a niche page). Items with no keyword score 0 and are ordered by phase instead.", "",
     "![[Build plan.base]]", "", "## Phases", "", "| Phase | What | Items |", "|---|---|---|"] + [f"| {k} | {PH[k]} | {p[k]} |" for k in sorted(p)] + ["",
     "## What is in it", "", f"| Type | Items | {H} searches/mo | {O} searches/mo |", "|---|---|---|---|"]
for t in ORDER:
    xs = [i for i in I if i["type"] == t]
    if xs: d = dem(xs); L.append(f"| {LABEL[t]} | {len(xs)} | {d[0]:,} | {d[1]:,} |")
z = sum(1 for i in I if i.get("keyword") and i["vol_home"] + i["vol_other"] == 0)
L += ["", "Searches overlap across items that share a keyword, so the columns do not add up to site demand.", "", f"{z} items target a keyword DataForSEO shows no measurable volume for. They score 0 and sit at the end of their phase: they still earn long-tail and AI-search traffic, so publish them after the measured ones rather than dropping them.", "",
      "## Before building", "", "- Every page goes through the copy pipeline in CLAUDE.md: a brief section built from competitors, hook-check, whole-page judging, aicheck, Leo reads the .md, then code.",
      "- Items marked `compliance: true` (commission and income figures per insurer product) wait for a compliance answer: publishing commission rates may breach agency rules.",
      "- Expansion audiences (property agents, mortgage brokers, generic sales teams) are phase 4 on purpose: decide whether AT sells outside insurance first.",
      "- New routes go into `scripts/marketing-routes.mjs`, which prerenders them and adds them to the sitemap on the next deploy."] + [f"- {n}" for n in cfg.get("plan_notes", [])] + [""]
for t in ORDER:
    xs = sorted([i for i in I if i["type"] == t], key=lambda i: (i["phase"], -i["score"]))
    if not xs: continue
    m = sum(1 for i in xs if i["vol_home"] + i["vol_other"] > 0)
    L += [f"## {LABEL[t]} ({len(xs)})", "", f"{m} of these have measured search demand; the rest are ordered by phase.", "", f"| Page | Phase | URL | Target keyword | {H} | {O} | KD | Fit | Score |", "|---|---|---|---|---|---|---|---|---|"]
    L += [f"| [[{i['note']}\\|{i['title'][:70].replace('|', '/')}]] | {i['phase']} | {i['url']} | {i.get('keyword', '') or '-'} | {i['vol_home']} | {i['vol_other']} | {i['difficulty'] if i['difficulty'] is not None else '-'} | {i['fit']} | {i['score']} |" for i in xs] + [""]
open(f"{V}/Build plan/Build plan.md", "w").write("\n".join(L) + "\n"); print("ok", len(I))
