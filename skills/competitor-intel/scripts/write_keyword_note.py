"""Write Keyword research.md: opportunities ranked by search demand from people we can serve, and the keyword list.
Score per keyword = (home-market volume x HOME_WEIGHT + other volume) x fit / (1 + difficulty/50), where fit is 1 for a
product-fit or niche searcher and ADJ for an adjacent one (Jev's judgments), 0 otherwise. Weights live here, in code.
Usage: write_keyword_note.py <config.json> <raw_dir>"""
import json, sys, csv, collections, math, os
cfg = json.load(open(sys.argv[1])); raw = sys.argv[2]; V = cfg["vault_dir"]
LOCS = cfg.get("locations", {"US": 2840}); HOME = list(LOCS)[0]; OTHERS = [m for m in LOCS if m != HOME] or [HOME]
DIFF = next((m for m, c in LOCS.items() if c == cfg.get("difficulty_location")), OTHERS[-1])
HOME_WEIGHT, ADJ = cfg.get("home_weight", 5), 0.4; ADJ_KEYS = cfg.get("adjacent_searchers", ["sales-general", "manager-hr"])
rows = list(csv.DictReader(open(f"{raw}/keywords.csv"))); f = lambda v: float(v) if v not in ("", None, "None") else 0.0
for r in rows:
    for k in ["intent", "satisfied", "audience", "difficulty"] + [f"vol_{m}" for m in LOCS]: r[k] = f(r.get(k))
    r["fit"] = "product" if (r["intent"] >= 0.67 and r["satisfied"] >= 0.5) else ("niche" if r.get("searcher") == "ours" else ("adjacent" if r.get("searcher") in ADJ_KEYS else "off"))
    w = 1 if r["fit"] in ("product", "niche") else (ADJ if r["fit"] == "adjacent" else 0)
    demand = r[f"vol_{HOME}"] * HOME_WEIGHT + sum(r[f"vol_{m}"] for m in OTHERS if m != HOME)
    r["score"] = round(demand * w / (1 + r["difficulty"] / 50), 1)
agg = collections.defaultdict(lambda: {"score": 0, **{m: 0 for m in LOCS}, "kw": [], "types": collections.Counter(), "fits": collections.Counter()})
for r in rows:
    if r["score"] <= 0: continue
    a = agg[r["opportunity"]]; a["score"] += r["score"]
    for m in LOCS: a[m] += r[f"vol_{m}"]
    a["kw"].append(r); a["types"][r["page_type"]] += 1; a["fits"][r["fit"]] += 1
ranked = sorted(agg.items(), key=lambda x: -x[1]["score"])
L = ["---", "type: keyword-research", "tags: [seo, keywords]", "---", "", "# Keyword research", "",
     f"Part of [[Competitive research]]. DataForSEO volumes for {', '.join(LOCS)}, keyword difficulty for {DIFF}, on the seed list in `_raw/seeds.json` plus the keyword ideas DataForSEO returned ({len(rows)} keywords). Jev judged, per keyword, which opportunity it belongs to, whether our product is what the searcher wants (product fit), who most likely searched it (asked with the keyword alone), and what kind of page would satisfy them.", "",
     f"Score = ({HOME} volume x {HOME_WEIGHT} + " + " + ".join(f"{m} volume" for m in OTHERS if m != HOME) + f") x fit / (1 + difficulty / 50). Fit is 1 when the product fits or the searcher is in our niche" + (f", {ADJ} for an adjacent searcher ({cfg.get('adjacent_label', 'a salesperson or people manager outside the niche')})" if any(r['fit'] == 'adjacent' for r in rows) else "") + ", 0 otherwise. DataForSEO reports low volumes in buckets, so 10 means 10 or fewer.", "",
     "## Opportunities ranked", "", "| # | Opportunity | Score | " + " | ".join(f"{m}/mo" for m in LOCS) + f" | Page type | Fit | Top keywords ({'/'.join(LOCS)}/difficulty) |", "|---|---|---|" + "---|" * len(LOCS) + "---|---|---|"]
for i, (o, a) in enumerate(ranked, 1):
    top = sorted(a["kw"], key=lambda r: -r["score"])[:4]
    L.append(f"| {i} | {o} | {a['score']:.0f} | " + " | ".join(str(int(a[m])) for m in LOCS) + f" | {a['types'].most_common(1)[0][0]} | {', '.join(f'{k} {n}' for k, n in a['fits'].most_common())} | " + "; ".join(f"{r['keyword']} (" + "/".join(str(int(r[f'vol_{m}'])) for m in LOCS) + f"/{int(r['difficulty'])})" for r in top) + " |")
L += ["", "## Every keyword that scored", "", "| Keyword | Opportunity | Fit | Searcher | Page type | " + " | ".join(LOCS) + " | Difficulty | Score |", "|---|---|---|---|---|" + "---|" * len(LOCS) + "---|---|"]
for r in sorted([r for r in rows if r["score"] > 0], key=lambda r: -r["score"]):
    L.append(f"| {r['keyword']} | {r['opportunity']} | {r['fit']} | {r.get('searcher','')} | {r['page_type']} | " + " | ".join(str(int(r[f'vol_{m}'])) for m in LOCS) + f" | {int(r['difficulty'])} | {r['score']} |")
L += ["", f"Off-audience keywords ({sum(1 for r in rows if r['fit'] == 'off')}) are in `_raw/keywords.csv` with who Jev thinks searched them. High-volume ones there are traffic, not buyers."]
open(f"{V}/Keyword research.md", "w").write("\n".join(L) + "\n")
print("\n".join(f"{i}. {o} {a['score']:.0f}" for i, (o, a) in enumerate(ranked[:12], 1)))
