# Subagent briefs

Copy one, fill the brackets, and hand it to one general-purpose subagent in the background. Two at a time at most. Every brief carries the same spine: the owner's rule on autonomy, the files to read first, the worktree setup, the rules for the page type, the gates, how to ship, and a short final report. The ActivityTracker versions of these briefs are in the session history of 2026-09-25..29 and their outputs are in `~/Documents/*-copy-v1/`.

## Spine (paste into every brief)

```
[Owner]'s standing rule ([memory file], read it): go autonomously, ship when gates pass; hard
stops still apply (money, facts only [owner] has, auth/payment/security, schema, new deps,
breaking shared code, build error not fixed in two attempts); list what you decided for them.

Read first: [repo]/CLAUDE.md and AGENTS.md; .agents/product-marketing.md; ~/.claude/CLAUDE.md
copywriting section; ~/.claude/skills/competitor-site-buildout/references/gates.md and traps.md;
memory [site rules files]. Follow the shipped [type] pages EXACTLY: [paths of the kit, a live
example page, its guard test, its copy .md].

Setup: git -C [repo] fetch -q && git -C [repo] worktree add -b [branch] [worktree] origin/main;
cp -Rc [repo]/node_modules [worktree]/; copy [repo]/.env if the repo uses one; install missing
deps with --no-save. Use the repo's own build, preview, commit and kanban conventions where they
differ from these. Never edit the main clone. [Sibling branches running now, expect conflicts in X.]

QA on a production build served locally (trailing slash), then live: one H1, JSON-LD valid, no
page errors, no overflow at 390/768/1440, internal links 200, [type-specific checks]. Guard test
per page; prove one bites. Full suite to a log (known failures from other sessions: [list]).
Type-check clean on touched files. Ship in chunks: commit ("type: outcome" message ending with
the attribution line), rebase on origin/main (lock files: merge both keys with
scripts/merge-json-lock.py; lists: keep both sides; route objects: keep both whole), push,
confirm live. Mark every build plan item done / folded / merged / parked / held. Update the
kanban card [id] (string-replace, bump DATA_VERSION, verify the headless render). Remove the
worktree.

Final report (your only output): pushed hashes; live URLs; folds and why; what you decided for
[owner]; QA; tests; spend. Under [N] words.
```

## Research only (gap analysis)

```
Goal: find the pages [site] is missing, by [audience | feature | competitor library].
1. Inventory every live public page (routes file), tagged by type and audience.
2. Read the competitors' [resource libraries | template galleries | guides] with Scrapling:
   URL patterns, counts, page anatomy, which pages rank (SERP per head phrase).
3. One DataForSEO volume call per location for up to ~1,000 candidate phrases.
4. Keep only what the product can truly back and no live page answers; dedupe.
5. Write [~/Documents/<site>-gap-<date>/gap.md]: ranked build list (type, URL, head phrase,
   volumes, audience, why it fits, links), batches of ~10; add items to the build plan (phase N).
6. Build and ship the first batch (spine above).
```

## Copy then build (a page type's first page, or a site with review stops)

```
STOP 1: research, brief section, hook pool, code fact-check, 2-3 whole drafts judged by Jev,
aicheck, brief-check; write [~/Documents/<site>-<slug>-copy-v1/<slug>-copy-v1.md] with full copy,
scores, claims cut, and front-end decisions with your default for each. Do not build.
(If the owner goes autonomously: continue straight to the build and ship.)
```

## Site-wide sweep

```
Crawl every public route (routes file + sitemap) locally and live as Googlebot: status, one H1,
unique title and description, canonical, noindex only where intended, JSON-LD parses, og:image,
internal links (404s, chains), orphans, sitemap vs routes, redirects, duplicate intent across
sections (resolve by giving one page the head phrase and retitling the others toward their own
intent, cross-linked; never delete). Fix titles, descriptions, links, sitemap only; don't touch
body copy except to add a link line. Add a guard test for unique titles and one sitemap entry
per indexable page. Report before/after counts.
```
