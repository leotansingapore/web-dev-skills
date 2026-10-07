# Page types

What each type is for, what it contains, the kit it's built in, and what the ActivityTracker run learned. Build each type's kit once; later pages of the type are data.

## Contents
1. Feature page
2. Features hub
3. Pricing (value stack)
4. Homepage (variant first)
5. Audience page (/for)
6. Solution page (/solutions)
7. Hubs (free tools, templates, guides, glossary, compare, kpis, integrations, blog, solutions, for)
8. Free tool / calculator
9. Template
10. Template gallery (per-feature library)
11. Guide
12. KPI page
13. Glossary term
14. Compare: roundup, alternative, vs
15. Integration page
16. Blog post
17. Navigation, footer, layout, sitemap
18. Legal pages

## 1. Feature page

One product module, sold as moments in the reader's day. Frame: the CRM page's (kicker cycling the audiences, H1, sub, hero card, 4 stat tiles, a looping GIF, six moments each with a working demo, small stuff, closing, 6-9 FAQs). Demos: one data file, local state only, no real API or AI calls (scripted results), no hint text, `text-base` on inputs. GIF: four corner callouts that are outcome-based and braggy about the module's whole job, picked with hook-check. Full process: the site's page skill (`revamp-page` for ActivityTracker, `sb-revamp-page` for SearchBlueprint) and the repo's playbook. A new feature page ships only if the product really has the feature as a distinct thing (ActivityTracker folded mobile app, Telegram bot, streaks, teams and analytics into existing pages).

## 2. Features hub

A grid of every feature page, grouped by what the reader is doing (the day's work; clients and messaging; goals and numbers; the team; staying in it). Card text is LIFTED from each page's shipped copy (choose, don't write), so it can never drift from the page. Above it: a hero, a "start with what slips" row pointing to the 3 pages most visitors need. ItemList JSON-LD from one list of feature links.

## 3. Pricing (value stack)

Change words and the value stack only. Before and after, click every toggle and plan and assert the displayed prices, totals and checkout payloads are byte-identical (ActivityTracker: 259 states, 64 payloads). The value stack lists what each plan really unlocks (read the plan gating in code), with sourced "bought separately" prices if you show a total, and leaves the Offer/Product JSON-LD prices as they were.

## 4. Homepage (variant first)

Build the new version at its own URL (`/vN`), noindexed and out of the sitemap, beside the live homepage; switching it in is one line the owner flips. Frame from the best SaaS homepages (ActivityTracker used Sunsama's: the problem, then one week walked through with working demos, then routing to audiences and resources). Answer "what's in the core plan" on the page (walkthroughs asked every time). One dominant CTA. No testimonials, logos or customer counts that don't exist. Run the same walkthrough steps on the old and new homepage so the owner can compare.

## 5. Audience page (/for)

One reader's week, six moments each mapped to the feature page that does it (with links), reused feature demos with that audience's wording passed as props. Ship only for audiences the product really works as it is: no page promising industry features that don't exist (mortgage brokers wanted loan-system integrations; folded). Keep audience pages from competing with each other: one page per reader and head phrase (sales-teams redirected to sales-reps).

## 6. Solution page (/solutions)

One job-to-be-done ("answer leads at night") as an entry point that routes to the features that do it. Only when it isn't a restated guide. Most planned solution pages fold.

## 7. Hubs

Live pages only, never "coming soon" cards. Grouped by AUDIENCE, general first ("For any seller", then each audience, the most specialised last), so the hub doesn't read as for one industry. One data source per hub feeds the cards, the ItemList/CollectionPage JSON-LD and the nav menu. Each child's breadcrumb links up to its hub. A hub with one card is fine if the section is real and growing.

## 8. Free tool / calculator

Pure logic module with every worked example from the spec as a unit test (exact numbers), a URL share link that restores every input, live results, inputs that accept common formats. Tool above the fold, then how to use it, when, worked examples, what the product does, FAQ. No benchmarks without a primary source. Pair each tool with its glossary term and guide, linked both ways, and use fictional ranges for examples, such as the phone numbers reserved for fiction. A tool whose inputs change every few weeks, like a vendor's price list, folds into an FAQ with a dated source instead.

## 9. Template

The template itself in-page (Copy button that fills the clipboard, Print that prints only the template), plus Word and Excel downloads where the SERP shows people want them, generated from the SAME text data so the three never drift (ActivityTracker: macOS textutil for .docx, zipped XML for .xlsx, no new dependency; each build reads its file back to verify). A table-row line kind for grid templates. A filled-in example. No email gate unless the owner asks.

## 10. Template gallery (per-feature library)

The Todoist/Asana/ClickUp/Zapier pattern: a hub plus one page per template, for features where the APP has a real library (project templates, routine packs, workflow templates, note templates). Each page: what's in it, who it's for, how to use it in the product, the CTA, related templates. A guard test checks every page against the app's real template, so the site can never show a template the app doesn't have, and thin templates with only a few items are noindexed. Only features with a real library get a gallery (6 of 20 on ActivityTracker).

## 11. Guide

Long-form: TL;DR, contents with anchors, sections, a sources table (every figure with URL and read date), FAQ + Article JSON-LD, a "last checked" date, links to the matching tools, templates and glossary terms. Regulatory facts only from the official source; where a regulator restricts deep links, name and date the source without a link. A guide owns the long-form intent; the glossary owns the definition. A multi-chapter "ebook" is usually one pillar guide with anchored sections, not 12 thin pages.

## 12. KPI page

Only for KPIs with demand or a distinct intent the glossary and guide don't serve: formula, how to measure it in a team, what good looks like by role, how to move it, a small calculator. Most KPIs fold into a table on the KPIs guide (19 of 30 on ActivityTracker). Build the /kpis hub only when 5+ pages ship.

## 13. Glossary term

250-600 words: a one-sentence definition first (the snippet answer), how it's worked out with a small example, related terms (live only), where it shows up in the reader's week with one link to the product page that helps, 2-4 FAQs, DefinedTerm (in a DefinedTermSet) and FAQPage JSON-LD, all from one term object per page. Consumer-facing terms (insurance products, government schemes) are education only: no advice, no product or provider names, no quoted premiums, and yearly-changing figures dated or left out.

## 14. Compare pages

- Roundup ("best X"): who it's for, how we picked, comparison table, one section per tool including ours (placed first with a disclosure line), FAQ, ItemList JSON-LD.
- Alternative / vs: the one-line verdict, who should pick which, a side-by-side table, the three differences that matter, switching steps, FAQ.
Every statement about a competitor comes from that competitor's own current page, with URL and read date, shown in a sources list; no disparagement; say where the competitor is the better fit; check for acquisitions and renames; pricing as "see pricing" for ours (a local-currency price beside USD tables reads as a mistake), with competitor links marked rel="nofollow noopener". Tables scroll inside their box on phones with a sticky first column. Pages with no measured demand can still ship when they answer a real sales-call objection.

## 15. Integration page

Only for integrations the product really has, described exactly as the code does it (how to connect, what syncs, limits). No claim of an official partner status the product doesn't hold. An integration open to only some customers is not public.

## 16. Blog post

Only posts with measured demand, deduped against every live page (fold into the page that owns the intent, merge near-duplicate posts). 900-2,000 words as page one needs, 3-6 internal links, one soft CTA to the most relevant product page, BlogPosting + FAQ JSON-LD, sources for every statistic, author line per the site's convention. Batches of 20-30; drafting subagents allowed if every post is reviewed before the gates.

## 17. Navigation, footer, layout, sitemap

One shared marketing header and footer on every public page (find and replace duplicates). Top nav: Product, Solutions, Resources, Pricing, then a quiet Sign in and one filled primary CTA. Mega-menus: keyboard accessible, Esc closes, hover intent; phone menu full-screen, opens at the current section, CTA pinned. Footer mirrors the nav groups plus Company. Make sure the header actually stays sticky (a CSS bug had it scrolling away on every page). Sitemap grouped by section, each hub before its pages, every indexable page exactly once, no variants or noindexed pages. Gate: crawl every public route at 390/768/1440 (nav and footer once, no overflow, every nav/footer link 200, menus by mouse, touch and keyboard), then two walkthroughs that must reach 5 named pages through the nav only.

## 18. Legal pages

A missing legal page linked from the site (e.g. an affiliate agreement) is built from what the site promises and what the code does; where they disagree, follow the code and report the mismatch. Defaults for gaps from reputable comparable agreements, each listed for the owner. Always say a lawyer should review it.
