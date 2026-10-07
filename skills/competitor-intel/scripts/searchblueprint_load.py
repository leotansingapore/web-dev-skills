"""Load site-structure-plan.json into SearchBlueprint so it shows in the product: Keyword Map (Page plan + Diagram),
the Sitemap Planner board and the Blueprint. Creates (or reuses) the project in the OWNER's workspace, then one
analysis carrying metadata.sitemapPlanner (the planner tree, which every sitemap surface prefers) and
metadata.keywordMap (the page-plan rows). Never touches another workspace's rows.
Usage: searchblueprint_load.py <config.json> <raw_dir> --owner-email you@x.com
Needs ~/Documents/seo-audit-tool/.env.local (service role). Writes searchblueprint-ids.json and prints the URLs."""
import json, os, re, sys, uuid, datetime, argparse, urllib.request
ap = argparse.ArgumentParser(); ap.add_argument("config"); ap.add_argument("raw"); ap.add_argument("--owner-email", required=True); a = ap.parse_args()
cfg = json.load(open(a.config)); R = a.raw.rstrip("/") + "/"
env = dict(l.split("=", 1) for l in open(os.path.expanduser("~/Documents/seo-audit-tool/.env.local")).read().splitlines() if re.match(r"^(NEXT_PUBLIC_SUPABASE_URL|SUPABASE_SERVICE_ROLE_KEY)=", l))
U = env["NEXT_PUBLIC_SUPABASE_URL"].strip('"'); K = env["SUPABASE_SERVICE_ROLE_KEY"].strip('"')
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json", "Prefer": "return=representation"}
def req(m, p, b=None): return json.load(urllib.request.urlopen(urllib.request.Request(U + p, data=json.dumps(b).encode() if b is not None else None, method=m, headers=H)))
users = []; page = 1
while True:
    us = req("GET", f"/auth/v1/admin/users?page={page}&per_page=1000").get("users", []); users += us
    if len(us) < 1000: break
    page += 1
owner = next((u for u in users if (u.get("email") or "").lower() == a.owner_email.lower()), None)
if not owner: raise SystemExit(f"no SearchBlueprint user {a.owner_email}")
mem = [m for m in req("GET", f"/rest/v1/workspace_members?select=workspace_id,role&user_id=eq.{owner['id']}") if m["role"] in ("admin", "member")]
if len(mem) != 1: raise SystemExit(f"owner has {len(mem)} admin/member workspaces; pick one by hand")
WS = mem[0]["workspace_id"]; domain = re.sub(r"^https?://(www\.)?", "", cfg["our_site"]).strip("/")
ex = req("GET", f"/rest/v1/projects?select=id&workspace_id=eq.{WS}&archived=eq.false&domain=eq.{domain}")
pid = ex[0]["id"] if ex else req("POST", "/rest/v1/projects", {"workspace_id": WS, "name": domain, "domain": domain, "country": cfg.get("market", "sg"), "color": "#059669", "group_name": None, "branding": {}, "created_by": owner["id"]})[0]["id"]
P = json.load(open(R + "site-structure-plan.json"))
ours = {}
if os.path.exists(R + "our_pages.json"):
    ours = {re.sub(r"^https?://[^/]+", "", o["url"]) or "/": o for o in json.load(open(R + "our_pages.json"))}
nid = lambda: uuid.uuid4().hex[:8]; name = lambda p: p.rstrip("/").split("/")[-1].replace("-", " ").capitalize()
links = P.get("page_links", {})
root = {"id": nid(), "name": cfg["project"], "url": "/", "keywords": [], "children": [], "notes": "Site structure plan from competitor-intel. Internal linking rules:\n" + "\n".join(f"{i}. {r}" for i, r in enumerate(P["linking_rules"], 1))}
hdr = ["URL", "Primary Keyword", "Secondary Keywords", "Local Keywords", "AI Keywords", "Current Meta Title", "Suggested Meta Title", "Title Chars", "Current Meta Description", "Suggested Meta Description", "Desc Chars", "Current H1", "Suggested H1", "H1 Chars", "AI Search Prompts", "Search Volume", "Keyword Difficulty", "Keyword Source"]
cur, sug = [hdr], [hdr]; SRC = f"competitor-intel {datetime.date.today()}: DataForSEO volume summed over {'+'.join(cfg.get('locations', {}))}; Jev-judged fit"
for s in P["sections"]:
    hub = {"id": nid(), "name": s["label"], "url": s["hub"], "keywords": [], "children": [], "notes": f"Status: {s['status']}. Why: {s['why']}."}
    for p in s["pages"]:
        kws = [k for k in [p["keyword"]] + p.get("also", []) if k]
        vols = {k[7:]: v for k, v in p.items() if k.startswith("volume_")}
        note = f"Status: {p['status']}.\n" + (f"Target: {p['keyword']} (" + ", ".join(f"{k.upper()} {v}/mo" for k, v in vols.items()) + (f", difficulty {p['difficulty']}" if p.get("difficulty") is not None else "") + ").\n" if p["keyword"] else "") + "Link to: " + ", ".join([s["hub"]] + links.get(p["path"], []))
        hub["children"].append({"id": nid(), "name": name(p["path"]), "url": p["path"], "keywords": kws, "notes": note, "children": []})
        o = ours.get(p["path"], {}); site = cfg["our_site"].rstrip("/")
        row = [site + p["path"], p["keyword"], ", ".join(p.get("also", [])), "", "", o.get("title", ""), "", 0, o.get("meta", ""), "", 0, (o.get("h1") or [""])[0], "", 0, "", sum(vols.values()), p.get("difficulty") if p.get("difficulty") is not None else "", SRC + (" | NEW PAGE" if p["status"] == "new" else f" | status: {p['status']}")]
        sug.append(row)
        if p["status"].startswith("live"): cur.append(row)
    root["children"].append(hub)
meta = {"sitemapPlanner": {"version": 1, "tree": root, "positions": {}},
        "keywordMap": {"currentTitle": "Current pages", "current": cur, "suggestedTitle": "Suggested Sitemap Keyword Map", "suggested": sug, "suggestedTree": root, "mappedPages": len(cur) - 1, "suggestedPages": len(sug) - 1, "market": cfg.get("market", "sg"), "generatedAt": datetime.datetime.utcnow().isoformat() + "Z"}}
comps = [re.sub(r"^https?://(www\.)?", "", u).strip("/") for g in cfg["groups"].values() for u in list(g["competitors"].values())[:4]]
aid = req("POST", "/rest/v1/analyses", {"domain": domain, "country": cfg.get("market", "sg"), "mode": "keywords", "competitors": comps, "sheet_name": f"{cfg['project']} site structure plan ({datetime.date.today()})", "workspace_id": WS, "project_id": pid, "actor_id": owner["id"], "status": "done", "summary": f"Site structure plan from competitor-intel: {len(root['children'])} hubs, {len(sug) - 1} pages.", "metadata": meta})[0]["id"]
json.dump({"project_id": pid, "analysis_id": aid}, open(R + "searchblueprint-ids.json", "w"))
print(f"https://searchblueprint.io/projects/{pid}/keyword-map\nhttps://searchblueprint.io/projects/{pid}/keyword-map#sitemap\nhttps://searchblueprint.io/planner/{aid}")
