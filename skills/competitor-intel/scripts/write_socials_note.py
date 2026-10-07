"""Write Socials.md: each competitor's profiles and their most-viewed YouTube videos. Usage: write_socials_note.py <config.json> <raw_dir>"""
import json, sys, os, re
cfg = json.load(open(sys.argv[1])); raw = sys.argv[2]; V = cfg["vault_dir"]
s = json.load(open(f"{raw}/socials.json"))
NETS = ["linkedin", "x", "youtube", "instagram", "tiktok", "facebook", "threads"]
L = ["---", "type: socials", "tags: [competitor, social, youtube]", "---", "", "# Socials", "", "Part of [[Competitive research]]. Profiles come from each homepage's links and structured data. Profiles on sites that render their footer in the browser (no links in the HTML) are missing. YouTube lists come from yt-dlp, up to 40 recent videos per channel; the top five by views are below, and every title is also in the copy bank.", "",
     "| Competitor | " + " | ".join(NETS) + " | YouTube videos |", "|" + "---|" * (len(NETS) + 2)]
skip = ("/groups", "/people", "/business", "/sharer", "/company/linkedin")
for n, d in s.items():
    norm = lambda u: "https://" + re.sub(r"^https?://(www\.)?", "", u).rstrip("/\\").lower()
    cell = lambda net: " ".join(f"[{net}]({u})" for u in sorted({norm(x) for x in d.get(net, [])}) if not u.endswith(skip)) or "-"
    L.append(f"| [[{n}]] | " + " | ".join(cell(x) for x in NETS) + f" | {len(d.get('youtube_videos', []))} |")
L += ["", "## Most-viewed YouTube videos", ""]
for n, d in s.items():
    vids = [v for v in d.get("youtube_videos", []) if (v.get("views") or "NA").isdigit()]
    if not vids: continue
    L += [f"### {n}", ""] + [f"- {int(v['views']):,} views: [{v['title']}]({v['url']})" for v in sorted(vids, key=lambda v: -int(v["views"]))[:5]] + [""]
open(f"{V}/Socials.md", "w").write("\n".join(L)); print("ok")
