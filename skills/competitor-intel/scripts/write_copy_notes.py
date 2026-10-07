"""Write the copy bank notes: Copy bank.md (USP themes per competitor, top hooks per reader), Copy bank/<Competitor>.md
(every line by kind), and a best-hooks section appended to each Features/<feature>.md. Usage: write_copy_notes.py <config.json> <raw_dir>"""
import json, sys, csv, os, collections, statistics as st
cfg = json.load(open(sys.argv[1])); raw = sys.argv[2]; V = cfg["vault_dir"]; os.makedirs(f"{V}/Copy bank", exist_ok=True)
rows = list(csv.DictReader(open(f"{raw}/copy-bank.csv"))); rn = list(cfg["readers"])
for r in rows:
    for k in list(r):
        if k.startswith("score_") or k.startswith("credible_"): r[k] = float(r[k]) if r[k] not in ("", "None") else None
KORDER = ["usp", "hook", "pain-enemy", "benefit", "proof", "objection", "cta", "question", "feature-label"]
comps = sorted({r["competitor"] for r in rows})
themes = [t for t, _ in collections.Counter(r["theme"] for r in rows if r["kind"] in ("usp", "hook", "benefit") and r["theme"] not in ("none", "")).most_common()]
L = ["---", "type: copy-bank", "tags: [competitor, copy, hooks, usp]", "---", "", "# Copy bank", "",
     f"Part of [[Competitive research]]. {len(rows):,} lines: " + ", ".join(f"{n:,} from {k}" for k, n in collections.Counter(("pages" if ":" in r["source"] and not r["source"].startswith("ad:") else ("ads" if r["source"].startswith("ad:") else r["source"])) for r in rows).most_common()) + ". Jev labelled each line's kind and the selling theme it leans on. Hooks, USPs, benefits and pains were then scored out of 10 with hook-check's six questions, once in each reader's shoes: " + ", ".join(rn) + ". Scores are for borrowing the MOVE, never the words.", "",
     "## Line kinds", "", "| Kind | Lines |", "|---|---|"] + [f"| {k} | {n} |" for k, n in collections.Counter(r["kind"] for r in rows).most_common()] + [""]
L += ["## USP themes each competitor leans on", "", "Share of each competitor's USP, hook and benefit lines per theme. Blank means under 5%.", "", "| Competitor | " + " | ".join(themes[:10]) + " |", "|" + "---|" * (min(10, len(themes)) + 1)]
for c in comps:
    cr = [r for r in rows if r["competitor"] == c and r["kind"] in ("usp", "hook", "benefit")]
    cnt = collections.Counter(r["theme"] for r in cr); tot = max(1, len(cr))
    L.append(f"| [[Copy bank/{c}\\|{c}]] | " + " | ".join((f"{100 * cnt[t] // tot}%" if cnt[t] / tot >= 0.05 else "") for t in themes[:10]) + " |")
L.append("")
for x in rn:
    sc = [r for r in rows if r.get(f"score_{x}") is not None]
    if not sc: continue
    med = st.median(r[f"score_{x}"] for r in sc)
    top = sorted([r for r in sc if (r.get(f"credible_{x}") or 0) >= 0.6], key=lambda r: -r[f"score_{x}"])[:40]
    L += [f"## Top hooks for the {x}", "", f"{cfg['readers'][x]['reader'][:220]}...", "", f"Competitor median {med:.1f}/10 across {len(sc):,} scored lines. Only lines the reader finds credible (0.6 or higher) are listed.", "",
          "| Score | Care | Outcome | Kind | Competitor | Line | Where |", "|---|---|---|---|---|---|---|"]
    L += [f"| {r[f'score_{x}']} | {float(r.get(f'care_{x}') or 0):.2f} | {float(r.get(f'outcome_{x}') or 0):.2f} | {r['kind']} | {r['competitor']} | {r['text'][:140].replace('|', '/')} | {r['source']} |" for r in top] + [""]
open(f"{V}/Copy bank.md", "w").write("\n".join(L))
for c in comps:
    cr = [r for r in rows if r["competitor"] == c]
    N = ["---", f"competitor: {c}", "type: copy-bank", "tags: [competitor, copy]", "---", "", f"# {c} copy", "", f"Part of [[Copy bank]]. Landing pages: [[{c} landing pages]]. Scores are out of 10 per reader (" + ", ".join(rn) + ").", ""]
    for k in KORDER:
        kr = [r for r in cr if r["kind"] == k]
        if not kr: continue
        kr.sort(key=lambda r: -max([r.get(f"score_{x}") or 0 for x in rn]))
        N += [f"## {k} ({len(kr)})", ""] + [f"- {r['text']}" + "".join(f" `{x} {r[f'score_{x}']}`" for x in rn if r.get(f"score_{x}") is not None) + f" _{r['theme']}, {r['source']}_" for r in kr[:150]] + [""]
    open(f"{V}/Copy bank/{c}.md", "w").write("\n".join(N))
fm = {r["url"]: r["feature"] for r in csv.DictReader(open(f"{raw}/feature-map.csv"))} if os.path.exists(f"{raw}/feature-map.csv") else {}
byf = collections.defaultdict(list)
for r in rows:
    f = fm.get(r.get("url", ""))
    if f and any(r.get(f"score_{x}") is not None for x in rn): byf[f].append(r)
for f, fr in byf.items():
    p = f"{V}/Features/{f}.md"
    if not os.path.exists(p): continue
    s = open(p).read().split("\n## Best hooks on these pages")[0].rstrip()
    fr.sort(key=lambda r: -max(r.get(f"score_{x}") or 0 for x in rn))
    s += "\n\n## Best hooks on these pages\n\nFrom the copy bank, scored in each reader's shoes. Borrow the move, not the words.\n\n| " + " | ".join(rn) + " | Competitor | Line |\n|" + "---|" * (len(rn) + 2) + "\n"
    s += "\n".join("| " + " | ".join(str(r.get(f"score_{x}") or "-") for x in rn) + f" | {r['competitor']} | {r['text'][:140].replace('|', '/')} |" for r in fr[:15]) + "\n"
    open(p, "w").write(s)
print("copy notes written:", len(comps), "competitors,", len(byf), "features with hooks")
