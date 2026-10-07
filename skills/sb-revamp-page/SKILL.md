---
name: sb-revamp-page
description: Revamp one SearchBlueprint searchblueprint.io /features/* page with the feature page playbook (moments with working demos, Jev-judged copy, two stops for Leo). Use when Leo asks to revamp, rebuild or redo a SearchBlueprint /features page.
---

# Revamp one SearchBlueprint feature page

Argument: the page slug (any key of FEATURE_PAGES, e.g. on-page-seo,
keyword-research, local-seo). No argument: ask which page, as a pick list.

The process is `docs/FEATURE-PAGE-PLAYBOOK.md` in the seo-audit-tool repo.
Read it in full before anything else; it wins over this file. It is the
ActivityTracker `revamp-page` workflow ported to this site.
/features/on-page-seo is the reference build.

## Setup

Work in the worktree `~/Documents/seo-audit-tool-worktrees/blueprint`
(branch off current main), never the main clone (other sessions use it).
`git pull --rebase origin main` first. Dev server:
`CRON_SECRET= npx next dev -p 3941` from the worktree (pick another free port
if a peer holds it). Playwright scripts must run from inside the worktree so
`playwright` resolves.

## The two stops (Leo's, never skip)

1. After the brief, the copy drafts and their scores: write the chosen draft to
   `~/Documents/<slug>-copy-v1/<slug>-page-copy-v1.md` with the scores and the
   claim check beside it, open it, and stop. Port nothing until he says go.
2. After a GIF exists: open it in Safari and stop until he says go.

A copy reference named in his request (a URL) sets the page's frame; without
one, use activity-tracker.io/features/crm's frame.

## Rules carried over from the first pages

- Copy: marketing about the reader's week, never spec. Reword READER and PAINS
  in `tools/jev-copy/feature-page/drafts.py` for the page before scoring.
  Check every claim against the help doc and the code after drafting.
- Honesty: brag only with what the code or help docs support; sample data is
  labelled; CHECK_COUNT is 36; never promise rankings or traffic.
- Words to avoid come from the brief: fix list, rank tracking, dashboard,
  guaranteed rankings, an audit or report as the headline promise.
- Demos use searchblueprint.io as the sample site (live tags for "today"),
  a made-up business only where SB cannot be the example. One data file, local state only, no hint text, `text-base` inputs,
  `min-h-11` targets, active state for every hover.
- QA: `tools/feature-page-qa/sweep.mjs <slug>` locally, then on the preview.
  Two Browser Use walkthroughs (desktop, 390x844), about $0.30 total by
  balance delta, each echoing two checkable facts.
- Ship: guard tests, rebase, push to main (the pages went live on
  2026-09-25; the push is the deploy), verify on searchblueprint.io, kanban
  card, memory note. Leo waived the copy stop: write the .md, then build.
