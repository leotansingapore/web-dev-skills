---
name: competitor-site-buildout
description: Build out or overhaul a whole marketing website from competitor research, for any of Leo's sites. Revamps every existing marketing page (features, pricing, homepage, hubs) and creates every page the site is missing (audience pages, solution pages, free tools and calculators, templates, guides, KPI pages, comparisons and alternatives, glossary, integrations, template galleries, blog), then fixes the navigation, footer, sitemap and SEO across the whole site. Each page starts from competitors, is judged with Jev, checked against the product and verified live. Use this whenever Leo asks to "revamp the site", "build all the pages", "do the rest of the planned pages", "what pages are we missing", "gap analysis against competitors", "pages for SEO", "do the same for another site", "full pass", "template gallery like Todoist", or any site-wide page build. For a single page use revamp-page (ActivityTracker), sb-revamp-page (SearchBlueprint) or feature-page-builder; this skill runs those per page.
---

# Competitor site buildout

This is the site-wide flow that took activity-tracker.io from 2 rebuilt feature pages to about 450 public pages in five days (2026-09-25 to 09-29). The flow is the same for any site. The worked example is the ActivityTracker repo (`~/remix-of-activity-tracker`) and its research vault (`~/Documents/Activity Tracker/Competitive Research/`); open them when you want to see what a finished stage looks like.

The core idea: no page is written from a blank page. Every page starts from what the best competitors publish for that search, is written in the reader's shoes, is judged against the live page and page one of Google, and only claims what the product really does. A page that would be thin, would repeat a live page, or would serve a different reader than the one searching gets folded into a better page or parked.

## Before starting

1. Read the site's repo rules (CLAUDE.md, AGENTS.md) and its brief (`.agents/product-marketing.md`). No brief: build it from competitors first with `marketing-skills:product-marketing` (Leo's copy rule: the brief is competitor-derived). The repo's rules win over this skill's defaults: its own kanban and decision lanes, its commit and push granularity, a generated homepage, its build and preview commands. Adapt the flow to them and say where you did.
2. Read Leo's memory for the site (the area file in `~/.claude/projects/-Users-leo-Documents/memory/`). Rules that bind every page live there: naming rules, CTA, what must never be public, what's settled.
3. Check how he wants to review. His standing rule since 2026-09-27 is "go autonomously always" (memory `leo-go-autonomously-always.md`): ship when the gates pass, report after. The hard stops still apply (see "Stop and ask"). If a site has no such rule yet, use the decisions page (below) for his calls.
4. Confirm the repo's deploy: most of Leo's sites deploy on push to main. Never also run `vercel --prod`.
5. Inventory what's already shipped before planning anything: list the live public pages (the routes file and the live sitemap), read the site's recent git log for page work and its memory notes, and mark each phase below as done, partly done or not started. Skip or finish what exists rather than rebuilding it; a site may already have had its feature pages or pricing redone.
6. List what the product really offers customers today, not just what the code contains: a feature that exists in code but is switched off, gated as "coming soon" or limited to one customer does not exist for marketing, and live pages that sell it are the site's biggest honesty risk. Fix those pages first (cut or reword the claim) and put anything that needs a product decision to Leo.

## The flow

Run it in this order. Each phase ships before the next starts, because later phases link to earlier pages.

| Phase | What | Detail |
|---|---|---|
| 0 | Research base | Competitor inventory, keyword volumes, build plan |
| 1 | Revamp the core pages | Feature pages, then the /features hub |
| 2 | Money pages | Pricing value stack, homepage (a variant first), what's-included |
| 3 | Audience and job pages | /for/*, /solutions/* |
| 4 | Resources | Free tools, templates, guides, KPI pages |
| 5 | Comparison and glossary | /compare (roundups, alternatives, vs pages), /glossary |
| 6 | Hubs, navigation, footer, layout, sitemap | One shared nav and footer, audience-grouped hubs |
| 7 | Gap passes | By audience, by feature (galleries), by competitor library |
| 8 | Blog | Only posts with measured demand |
| 9 | Site-wide SEO sweep | Titles, canonicals, orphans, duplicates, sitemap |

Phases 3-5 can overlap. Phase 6 goes wherever the number of sections makes the old nav break (on ActivityTracker it was after ~150 pages).

### Phase 0: research base

- Find the site's research vault: `~/Documents/<Site name>/Competitive Research/` is the pattern (ActivityTracker's is `~/Documents/Activity Tracker/Competitive Research/`); memory notes for the site usually name it. No vault: run `competitor-intel`, which inventories every competitor page and builds a scored copy bank. It does NOT produce keyword volumes or a build plan; those come next.
- Markets: take them from the brief or the site's memory (ActivityTracker sells in the US and Singapore, so DataForSEO locations 2840 and 2702). Unknown: ask Leo which markets before the first volume call.
- Build plan: create `Build plan/Items/` in the vault if it's missing, one markdown item per planned page (frontmatter: type, url, title, phase, status, keyword, vol_us, vol_sg or the site's markets, difficulty, score, compliance). Each item ends as done, folded, merged, parked, dropped, held or waiting, so nothing stays vague.
- Volumes come from DataForSEO search_volume/live, one call per location covering up to 1,000 phrases at about 0.09 USD a call (creds in `~/Documents/seo-audit-tool/.env.local`). The SERP comes from organic/live/regular at one keyword per request, about 0.002 USD each, and it tells you what kind of page ranks, which a volume alone never does.

### Phases 1-8: every page goes through the same loop

For each page (or batch of 6-12 small pages of one type):

1. **Decide: ship, fold or park.** Ship only if the page has measured demand or a distinct job no live page does, AND the product really supports it. Fold into a live page (a section, a row, an FAQ, or a redirect) when a live page already answers the intent, or when page one serves a different reader: "field sales" returned GPS route apps and "insurance agency KPIs" returned loss ratios, so both folded. Items with no demand are parked with the reason. This decision is where most of the value is: on ActivityTracker, 988 of 1,207 planned blog posts had no demand and were parked, and dozens of pages folded into better ones.
2. **Research the page.** Scrapling (`~/.local/share/uv/tools/scrapling/bin/python`, `Fetcher.get(url, impersonate="chrome")`) on the pages that rank: their inputs and outputs (tools), sections, length, FAQ, schema, upsell. Competitor claims need their own pages as the source.
3. **Write the copy** with the full copy pipeline in `references/gates.md`: brief first, hooks pooled from competitors and scored with `hook-check`, 2-3 whole-page drafts judged by Jev against the live page and page one, credibility per line, `aicheck` under 15, `brief-check`. Record the copy and scores in `~/Documents/<site>-<slug>-copy-v1/`.
4. **Check every claim against the product** (read the code). Claim only what exists; cut or soften the rest. This caught false claims on almost every ActivityTracker page, including privacy promises that weren't true.
5. **Build** in the site's page kit for that type (`references/page-types.md`). One kit per page type, data-driven where pages repeat (glossary, compare, galleries, blog), so the next batch adds data, not code.
6. **QA** on a production build served locally (the repo's own preview command: `vite preview`, `next start`, or a static server over the build output), then again live (`references/gates.md`). Guard test per page; prove one assertion fails when you break the thing it guards.
7. **Ship**: rebase, resolve list conflicts with the scripts in `scripts/`, push, confirm the live title and status, mark the build plan item.
8. **Walkthroughs** on the page types that matter (feature, audience, homepage, pricing, big tools): two Browser Use runs (desktop, phone) that must echo facts the page prints; discard a run whose facts don't match.

### Running it with subagents

Each page type runs as one subagent brief (templates in `references/subagent-briefs.md`): research to live in one go, in its own git worktree off origin/main, never in the main clone. Keep at most two subagents running at once (Leo's cap; memory `cap-parallel-subagents.md`). A subagent's final report is only seen by you: relay what matters. Resume a stopped subagent with SendMessage (network drops and session ends happen; check its worktree before assuming anything landed).

## The decisions page

When Leo has calls to make, don't ask them one by one in chat. Put them on the localhost decisions page in `scripts/decisions-page/`: a site map (live / draft / redirect per page), each decision with your recommended option preselected and a one-line reason, and each copy draft with Go / Go with edits / Hold. He saves, and his answers land in `answers.json` next to the page.

```
mkdir -p ~/Documents/<site>-decisions && cp ~/.claude/skills/competitor-site-buildout/scripts/decisions-page/* ~/Documents/<site>-decisions/
# write decisions.json (see decisions.example.json; set "site" to the live origin so site-map links work), then:
cd ~/Documents/<site>-decisions && (nohup python3 serve.py > /tmp/decisions.log 2>&1 &) && open http://127.0.0.1:8765/
```

Only front-end calls go on it (H1, head phrase, draft pick, sections, placement, redirects). Keep copy true silently and log product bugs to the kanban instead of putting them to Leo (2026-09-26, memory `at-pages-focus-frontend.md`). If no answers were saved and Leo says "go", your picks stand.

## Stop and ask (even when going autonomously)

- Money: prices, discounts, commission rates, anything that changes what a customer or partner is charged or paid. Copy may describe money only as the product and Leo already state it. (ActivityTracker: the affiliate page promised 40% while the system paid 30%, and only Leo could settle it.)
- Facts only Leo has: meeting lengths, company registration details, grant eligibility, customer names and quotes, anything a page would state as fact that neither the site nor the code states.
- Auth, payment, security, database schema, new dependencies, and changes to shared code that could break other pages unless you prove they don't.
- Legal readings: a page may cite a rule from its official source; an interpretation of a rule goes on the page hedged ("on our reading") and in the report for Leo.
- Anything that copies someone else's content into the product or the site (see `references/traps.md`, the Todoist templates).

## Reporting

After each shipped batch: what's live (URLs), what was folded or parked and why, what you decided for Leo (so he can reverse it), QA and test results, spend. End with the one thing he needs to decide, if any. Update the kanban (`~/kanban/index.html`: string-replace, bump DATA_VERSION, check the headless render; never re-serialize) and the memory note for the site.

## Reference files

- `references/page-types.md`: what each page type contains, its kit, and what ranks for it. Read before building a type for the first time.
- `references/gates.md`: the copy pipeline, Jev judging, QA gates and tools, with costs. Read before the first page.
- `references/traps.md`: every trap the ActivityTracker run hit, and the fix. Read once per site; it saves days.
- `references/subagent-briefs.md`: copy-and-fill briefs for each phase.
- `scripts/`: the decisions page, and rebase conflict helpers for the files every page touches.
