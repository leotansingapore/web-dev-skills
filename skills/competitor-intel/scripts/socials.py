"""Find each competitor's social profiles (homepage links + JSON-LD sameAs) and list recent YouTube videos with views.
Usage: socials.py <config.json> <out_dir>   -> <out_dir>/socials.json"""
import json, re, sys, subprocess, shutil
from concurrent.futures import ThreadPoolExecutor
from scrapling.fetchers import Fetcher
NETS = {"linkedin": r"linkedin\.com/(company|school|showcase)/[^/?#\"']+", "x": r"(twitter|x)\.com/(?!intent|share|home)[A-Za-z0-9_]{2,}", "youtube": r"youtube\.com/(@[^/?#\"']+|c/[^/?#\"']+|channel/[^/?#\"']+|user/[^/?#\"']+)",
        "instagram": r"instagram\.com/(?!p/)[A-Za-z0-9_.]{2,}", "tiktok": r"tiktok\.com/@[A-Za-z0-9_.]+", "facebook": r"facebook\.com/(?!sharer|dialog|tr\b)[A-Za-z0-9_.\-]{2,}", "threads": r"threads\.net/@[A-Za-z0-9_.]+"}
def find(name, url):
    try: html = Fetcher.get(url, impersonate="chrome", timeout=30, stealthy_headers=True).html_content
    except Exception as e: return name, {"error": str(e)[:100]}
    out = {}
    for net, pat in NETS.items():
        hits = sorted({"https://" + re.sub(r"^www\.", "", m.group(0)).rstrip("/\\").lower() for m in re.finditer(r"(?:www\.)?" + pat, html)})
        if hits: out[net] = hits[:3]
    return name, out
def youtube(url, n=40):
    if not shutil.which("yt-dlp"): return []
    try:
        p = subprocess.run(["yt-dlp", "--flat-playlist", "--playlist-end", str(n), "--print", "%(title)s\t%(view_count)s\t%(url)s", url.rstrip("/") + "/videos"], capture_output=True, text=True, timeout=120)
        return [dict(zip(["title", "views", "url"], l.split("\t"))) for l in p.stdout.splitlines() if l.strip()]
    except Exception: return []
cfg = json.load(open(sys.argv[1])); comps = [(n, u) for g in cfg["groups"].values() for n, u in g["competitors"].items()]
with ThreadPoolExecutor(8) as ex: res = dict(ex.map(lambda c: find(*c), comps))
for n, d in res.items():
    if d.get("youtube"): d["youtube_videos"] = youtube(d["youtube"][0])
    print(n, {k: len(v) for k, v in d.items()})
json.dump(res, open(f"{sys.argv[2]}/socials.json", "w"), indent=1)
