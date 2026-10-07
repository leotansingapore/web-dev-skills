---
name: competitor-intel
description: Full competitor scrape for digital marketing, for any of Leo's websites. Finds and inventories every competitor page (blogs, guides, free tools, templates, comparisons, features, use cases, case studies), their landing-page anatomy, socials and YouTube, ads and emails, and a labelled copy bank of hooks, USPs, pains and proof. Jev maps every page to a master feature list and ranks it as a reference, ranks features for our roadmap, and scores hooks in our reader's shoes. Output is an Obsidian folder built for writing skyscraper landing pages, guides and blogs from references. Use when Leo says "competitor research", "inventory competitors", "what are competitors doing", "skyscraper", "full competitor scrape", "find competitors that do X", or starts marketing for a new site.
---

# Competitor intel

One run produces a reference library for a site's marketing: what every competitor publishes, how their pages are built, what they claim, and where the gaps are. It exists so that landing pages, guides and blogs are built from ranked competitor references rather than from a blank page (CLAUDE.md copy rule: competitors first).

First full run: ActivityTracker, 2026-09-24, 30 competitors, 18,392 pages, about $1.60 of Jev. Its output is at `~/Documents/Activity Tracker/Competitive Research/`; open it to see what a finished run looks like.

## Before starting

1. Confirm the project, our site, the Obsidian vault folder and the product brief (`.agents/product-marketing.md` in the repo). No brief: build one with `marketing-skills:product-marketing` first, because the readers and the feature list come from it.
2. Find competitors. Start from the ones Leo names, then WebSearch "<competitor> alternatives" and G2 or Capterra category pages. Group them (one group per product class Leo describes). Decide which to keep with Jev, not by eye: one Noul per candidate, "does this product offer <the capability set>", with the candidate's homepage title and meta as state. Say which were dropped and why (shut down, a sub-product of a giant sitemap, a different category).
3. State the cost before running (table below) and check the Browser Use balance if ads or emails are in scope.

## Setup (once per machine)

```bash
uv venv ~/.local/share/competitor-intel/.venv --python 3.12
uv pip install --python ~/.local/share/competitor-intel/.venv/bin/python "scrapling[fetchers]" browser-use-sdk
```
`PY=~/.local/share/competitor-intel/.venv/bin/python`, `S=~/.claude/skills/competitor-intel/scripts`. Keys come from `~/.zshenv` (`TYPESAFE_API_KEY`, `BROWSER_USE_API_KEY`); run `source ~/.zshenv` in the same command.

## Per-project inputs (in `<vault>/_raw/`)

- `config.json`: see `config.example.json`. Holds the project name, our site, `our_pages` (our URLs to map and check), `vault_dir`, `brief_path`, `niche` (the audience Jev checks each page against), `readers` (two or so, each a paragraph plus a list of pains, taken from the brief, written to the person who USES the product), `category` (what each group's reader compares against), `product_evidence` (our app's real routes and live features, so "we have it" is not judged from the brief alone), and `groups` of competitors.
- `features.json`: the master feature list, 30 to 50 entries of `id: one-line definition`, plus `none`. Claude writes it after step 4 by reading competitors' feature-page slugs and H1s and our product's modules. Words are Claude's job; Jev only maps pages onto it. Include our unique modules even when no competitor has them.
- `topics.json`: 12 to 16 content topics that match our modules, plus `none`. Used to tag every blog, guide and tool.

## Pipeline

Run from `<vault>/_raw`. Each step writes a file the next one reads; re-running a step overwrites its own output only.

| # | Step | Command | Output | Cost, time (30 sites) |
|---|---|---|---|---|
| 1 | Sitemaps | `$PY $S/harvest_sitemaps.py config.json .` | sitemaps.json | free, 2 min |
| 2 | Bucket by folder | `python3 $S/bucket.py .` | bucketed.json | free |
| 3 | Type flat URLs | `python3 $S/jev_classify.py .` | bucketed.json | Jev ~$0.06 |
| 4 | Page anatomy | `$PY $S/anatomy.py .` | anatomy_full.json | free, 10 min |
| 5 | Topic tags | `python3 $S/jev_topics.py config.json .` | jev-topics.csv | Jev ~$0.55, 20 min |
| 6 | Feature map and ranking | `$PY $S/features_rank.py config.json .` | feature-map.csv, our_pages.json | Jev ~$0.21, 10 min |
| 7 | Feature priority | `python3 $S/features_priority.py config.json .` | feature-priority.json | Jev <$0.01 |
| 8 | Socials and YouTube | `$PY $S/socials.py config.json .` | socials.json | free, 3 min |
| 9 | Ads and emails | see "Ads and emails" below | ads_emails/*.json | paid, decide first |
| 10 | Copy bank | `$PY $S/copy_bank.py config.json .` | copy-bank.csv | Jev ~$0.70, 40 min |
| 10b | Keyword research | write `seeds.json` (opportunity id: 3-9 seed queries) from Skyscraper opportunities, then `python3 $S/keyword_research.py config.json . --max-spend 2` | keywords.csv | DataForSEO ~$0.63 + Jev ~$0.08 |
| 10c | Competitor site structure | `$PY $S/site_structure.py config.json .` | site-structure.json | free, 2 min |
| 10d | Our link graph | crawl our sitemap's pages for `<a>` in the no-JS HTML into `at-link-graph.json` (see the AT run) | link graph | free |
| 10e | Structure plan | Claude writes `site-structure-plan.json` (hubs from what most competitors run, pages from keywords.csv, `page_links`, `linking_rules`); volumes are filled from keywords.csv in code | plan | free |
| 10f | Load into SearchBlueprint | `python3 $S/searchblueprint_load.py config.json . --owner-email <Leo's login>` | project + analysis in Leo's workspace | free |
| 10g | Blog pool | `python3 $S/jev_adaptable.py config.json .` (Jev: is a niche version of each competitor article useful, is its subject foreign) | adaptable.csv | Jev ~$0.12 |
| 10h | Blog plan | per topic, 160 URLs a batch through `claude -p --model sonnet` with `blogplan/prompt.txt` (see the AT run's `_raw/blogplan/run.sh`), then `python3 $S/merge_blog_plan.py .` | blog-items.json | free (Max plan), ~40 min |
| 10i | Build list | Claude writes `build_items.py` (fixes, hubs, features, audience pages, tools, templates, guides, glossary, comparisons, programmatic sets; one owner per keyword, enforced in code) | build-items.json | free |
| 10j | Volumes | collect every keyword into plan-keywords.txt, then `python3 $S/plan_volume.py config.json . plan-keywords.txt --rejudge` | plan-keywords.csv | DataForSEO ~$0.25 per 500 new keywords |
| 10k | Build plan | `python3 $S/write_build_plan.py config.json . && python3 $S/write_build_master.py config.json .` | Build plan/ (one note per item + Base + master) | free |
| 11 | Our site check | `python3 $S/our_site_check.py config.json .` | our-site-check.json | free |
| 12 | Vault notes | `python3 $S/write_inventory.py config.json . && $PY $S/write_anatomy_notes.py config.json . && python3 $S/write_feature_notes.py config.json . && python3 $S/write_socials_note.py config.json . && python3 $S/write_copy_notes.py config.json . && python3 $S/write_keyword_note.py config.json . && python3 $S/write_structure_note.py config.json . && python3 $S/write_plan_note.py config.json .` | notes | free |

Steps 5, 6 and 10 take long. Run them with `nohup ... > step.log 2>&1 &` and wait on the PID with `kill -0`, never on `pgrep -f <name>`: pgrep matches the wait loop's own command line and waits forever.

Client-rendered homepages (no H1 in the HTML) need a real browser. Headless browsers launched from these sessions cannot reach the internet. Use the `chrome-devtools` MCP (`new_page`, then `evaluate_script` with the extractor in `references/extract.js`), save the JSON to `_raw/cdp_<name>.json`, and merge it into anatomy_full.json as the `home` entry. Do only homepages this way; inner pages stay title-and-meta.

## Then write the synthesis notes by hand

The scripts write the reference layer. Claude writes three notes from it, each gated by `aicheck` (under 15):

1. `Competitive research.md`: the index. Scope, groups, roster table, the Jev feature matrix, how it was built, what is not done.
2. `Landing page inventory - what to use.md`: homepage, feature, comparison and free-tool moves worth borrowing, each with who does it and the exact line. This is the hook pool for step 3a of the copy pipeline, never a draft.
3. `Skyscraper opportunities.md`: gaps from the topic tags (topics with zero or blog-only coverage where we have a module), commercial pages, free tools, guides, blog clusters and comparison pages, each with the pages to beat and our angle. Include the our-site-check failures first: a page that cannot rank as served comes before any new page.

## Using the output to build a page

1. Open `Feature map.md`, pick the highest-priority feature whose status is "we have it, no page" (or an uncontested one).
2. Open `Features/<feature>.md`: the top three reference pages, their section outlines, meta and CTAs.
3. Open `Copy bank.md` for that feature's theme: the highest-scoring hooks for our readers are the moves to adapt (hook-check step 3a). Never lift a line.
4. Run the normal copy pipeline from CLAUDE.md: brief section, hook-check, whole-page judging, aicheck, Leo reads the .md, then code.

## SearchBlueprint

The plan lands in SearchBlueprint (`~/Documents/seo-audit-tool`) as one analysis on the site's project in Leo's workspace: `metadata.sitemapPlanner` (the planner tree, which the Keyword Map diagram, the planner board and the Blueprint all prefer) plus `metadata.keywordMap` rows (the Keyword Map page only picks an analysis whose `keywordMap.current` has rows). Leo looks at it on `/projects/<id>/keyword-map` (Page plan tab, and `#sitemap` for the Diagram) and `/planner/<analysis id>` (editable board).
- Check who owns a project before writing to it: on 2026-09-24 the only activity-tracker.io project belonged to a QA account, and a write there would have been invisible to Leo and would have changed QA data. Pass Leo's own login email as `--owner-email`; ask him for it.
- Leave `colorTag` unset: the code reserves it for users.
- Suggested titles and H1s stay blank; they come from the copy pipeline, not from this skill.
- The public v1 API and MCP server cannot create projects or sitemap plans; this uses the service role from `.env.local`.
- `searchblueprint_load.py` was written from the AT run's manual steps and has not been run end to end yet; read its output before trusting it on a new site.

## Ads and emails

Tested 2026-09-24, and none of it worked well enough to run unattended:
- Browser Use Cloud, one agent run per competitor covering Meta, Google, LinkedIn and Milled: about $0.95 a run (balance delta), 20 minutes, and thin results. Google text ads render in iframes, so the text came back empty; Meta keyword search was noisy or returned nothing; Milled blocked the agent.
- Meta Ad Library in the chrome-devtools browser renders fine, but keyword search mixes in other advertisers, and the page ID read off a Facebook page did not match the Ad Library ID.
- Milled is behind Cloudflare for plain fetches. Really Good Emails renders its search client-side.

`scripts/ads_emails.py` is the Browser Use collector: it sets `max_cost_usd` per run and prints the balance before and after. Do not run it for a whole list until Leo picks the ads source. The candidates are a paid ad-library API that returns JSON, the Meta Ad Library API with a Meta token, or Foreplay once it is authorised. Once ads are collected, the `ads-competitor` skill does the analysis.

## Traps

- plan_volume.py bills DataForSEO per request, not per keyword: with four markets one run costs about $0.37 even for a single new keyword. Collect every keyword first and run it once.
- A high intent score must never turn the niche's own customers into buyers: 'virtual assistant employment' (201,000 US, job seekers) scored as fit through intent 0.84 until write_build_plan.py checked the searcher first (fixed 2026-10-07). Even at 0.03 weight a six-figure job-seeker phrase outranks real pages, so retarget the item's keyword.
- A slash in a competitor name ("Offshore 24/7") breaks every per-competitor note path and Obsidian link. Name it without one in config.json before step 1; renaming afterwards means rekeying every JSON and CSV in `_raw`.
- Programmatic sets swamp the stock anatomy caps (999 per page type): Stealth Agents alone has 3,200 role slugs and 1,969 alternatives pages. The Catalyst run (2026-10-06) capped feature, use-case and comparison pages at 150 per competitor, shortest paths first; its `_raw/anatomy.py` is the copy to start from. Service businesses also need their own folder words (services, roles, hire-talent, va-for) in a local bucket.py, or most service pages land in "other".
- Estimate the copy bank from its line count, not a guess: labelling ran about 930 input tokens a line and scoring about 1,000 per hook line per reader. 38,194 lines cost $2.90 on the Catalyst run.
- bucket.py's locale list must cover every language a competitor ships: Plecto's /no, /sv, /da copies (3,371 pages) went to Jev before `no|nb|sv|da|fi|cs|he|hu|ro|uk|el` were added.
- A second research set in a subfolder writes notes with the same names (Feature map, Copy bank): link them with the folder path (`[[Sales gamification/Feature map|Feature map]]`), or Obsidian resolves to the other one.
- Rename visible audience words after keyword ownership is settled, then merge pages that now share a URL, except fixes (several fixes can touch one page).

- Phrase glossary keywords the way the niche searches them. The bare "what is X" form belongs to other meanings: "what is ai" (110,000 US searches) is artificial intelligence, "what is cot" a baby cot, "what is fyp" TikTok.
- The searcher Choice needs a "buys what our niche sells" option (config `niche_customer`). Without it Jev put "integrated shield plan", a consumer search, in the niche.
- Keep off-audience weight tiny (0.03): at 0.15, generic volume ("what is a crm", 22,000) outranked every niche page.
- One owner per keyword, including near-duplicates that differ only in word order ("30 60 90 day sales plan" vs "30 60 90 day plan sales"); `merge_blog_plan.py` compares word sets.

- Ask Jev who searched a keyword in its own request, with the keyword as the only state and realistic alternatives in a Choice. With the product description beside it, or as a yes/no, it put 629 of 656 keywords in our niche. `keyword_research.py` does this; `--jev-only` re-judges without paying DataForSEO again.
- Before calling a page broken, read robots.txt and the route tables. On AT the "unprerendered" calculators were signed-in tools blocked on purpose.

- Budget from the Browser Use balance, never from `totalCostUsd` (model cost only, about a third of the bill).
- Jev reads English best. Non-English locales are dropped in step 2; Wati's Hindi template slugs still get through and are noise.
- Word counts include navigation and footer, so mega-menus inflate them.
- Fetch our own pages as Googlebot (`our_site_check.py` does) as well as with a browser user agent. A prerendered site can serve bots and browsers differently.
- The `(ours)` rows in feature-map.csv say how our pages compare on the same scale as competitors'. Our composite beside the top competitor's is the gap to close.
