# Gates

A page ships only when all of its gates pass. Run them yourself; report the numbers.

## Copy pipeline (every page)

From Leo's global CLAUDE.md "Copywriting" section, which wins over this summary:

1. Brief first (`.agents/product-marketing.md`), built from competitors. If the page's module or audience has no section, write one from 5-6 competitor pages before drafting.
2. Voice source: the competitors and page one, never the site's own older pages.
3. Register: one `saas-copy` register (SMB and advisor pages are `human-simple`).
4. Hook gate: pool 60-120 hooks from 8-16 competitor pages, `hook-check <pool.json>` (scores in the reader's shoes; the competitor median is the bar), adapt the top moves to the product, re-score, pick per slot (credible >= 0.6). A slot nothing clears after two rounds is cut. Cost: about 0.006 USD per 150 hooks.
5. Judge the page, not the lines: 2-3 whole drafts plus the live page (and page one for resources) read by Jev top to bottom in the reader's shoes (`judge.py` in the repo's `tools/jev-copy/<page>/`; a site without them copies them from `~/remix-of-activity-tracker/tools/jev-copy/tasks-page/` (judge.py, cred.py, drafts.py) and rewords them per page type: "would they want to try it", "would they use this calculator and trust the result", "would they trust it and act on it"). Then line credibility (`cred.py`): rewrite any line under 0.55.
6. `aicheck <file>` under 15; `brief-check <file>` (zero avoid-words; it needs the file inside the repo tree, e.g. `.agents/_bc.md`, then delete it).
7. ASCII only, no em dashes, sentence case headings, no emoji.
8. Check every claim against the code after the words are chosen.

## Facts

- Every statistic or benchmark: a primary source with URL and read date, or none. Label invented examples as examples.
- Regulatory facts: the official source (regulator, statute). Where a source's terms restrict deep links, name and date it without a link. Interpretations go in hedged ("on our reading") and in the report.
- Competitor statements: their own current pages, with read dates.
- Before republishing any list, table or library from a source, read its terms (memory `check-source-terms-before-republishing.md`).

## QA (production build, then live)

- Build, serve with the repo's own preview command (`npx vite preview --port <free> --strictPort` on Vite sites, where prerendered routes need the trailing slash; `next build && next start` on Next sites; a static server over the output otherwise), then check at 390, 768 and 1440: one H1, JSON-LD parses, no page errors, no horizontal overflow, no clipped elements, internal links 200.
- Per type: calculators (every input changes the output; share link round-trips; worked examples as tests); templates (Copy fills the clipboard: use a fixed element handle, since a locator matching "Copy" stops matching "Copied"; downloads 200 with the right content type and read back; print shows only the template); guides (contents anchors land; tables scroll inside their box at 390); pages with an animated mascot or overlays (resting over text is a failure, crossing while moving is not; run at phone AND desktop widths).
- Guard test per page (banned words for the audience, required sections, JSON-LD, sources on figures, no claims the product can't back); break the guarded thing once to prove the test fails.
- Full test suite to a log file; name failures that aren't yours (other sessions' failures are known; list them, don't fix them silently).
- Live: fetch as Googlebot for the title, status, canonical; confirm the sitemap entry.

## Walkthroughs (Browser Use Cloud)

Two runs per important page (desktop 1440x900, phone 390x844) with a steps file that asks for 5-6 facts the page prints after specific interactions, plus "would you try it / book, why" and "what was unclear". A run whose echoed facts don't match is discarded. About 0.10-0.15 USD a run by balance delta, not `totalCostUsd`. The test browser often blocks the clipboard ("Couldn't copy"): verify Copy yourself in Chromium and WebKit before believing it.

## Budgets seen on ActivityTracker

- DataForSEO: about 0.19 USD per page batch (one volume call per location plus a few SERPs).
- Jev: 0.01-0.08 USD per batch.
- Browser Use: 0.20-0.33 USD per page pair of walkthroughs.
- The whole run (about 450 pages): under 15 USD of paid APIs.
