---
name: revamp-page
description: Revamp one activity-tracker.io /features/* page with the feature page playbook. Use when Leo types /revamp-page <page> or asks to revamp, rebuild or redo a /features page.
---

# Revamp one feature page

Argument: the page slug (tasks, notes, routines, goals, vision, funnel, focus,
ask-ai, pet, reflections, planner). No argument: ask which page, as a pick list.

The process is `docs/FEATURE-PAGE-PLAYBOOK.md` in remix-of-activity-tracker
(`~/remix-of-activity-tracker`). Read it in full before anything else;
it wins over this file. /features/crm and /features/log are the reference builds.

## Setup

Work in a worktree off `origin/main`, never in the main clone (other sessions
use it):

```
git -C ~/remix-of-activity-tracker fetch -q
git -C ~/remix-of-activity-tracker worktree add -b feat/<slug>-page ~/at-<slug> origin/main
cp -Rc ~/remix-of-activity-tracker/node_modules ~/at-<slug>/
cp ~/remix-of-activity-tracker/.env ~/at-<slug>/
cd ~/at-<slug> && npm i --no-save --legacy-peer-deps @tanstack/react-query@5.101.4
```

If the build fails on an unresolved import, main gained a dependency the copied
node_modules lacks: install that package with `--no-save`, then rebuild.

## The two stops (Leo's, never skip)

1. After the brief section, the copy draft and its scores: write the draft to
   `~/Documents/<slug>-copy-v1/<slug>-page-copy-v1.md`, open it, and stop. Port
   nothing until he says go.
2. After rendering the GIF (`node tools/feature-gif/render.mjs <slug>`): open it
   in Safari (Preview does not animate GIFs) and stop until he says go.

A copy reference named in his request (a URL) sets the page's frame; without
one, use the CRM page's frame.

## Rules that caught real bugs on the first two pages

- Copy: marketing about the reader's day, never spec. Reword `judge.py` and
  `cred.py` for the module before scoring (they carry CRM wording). Check every
  claim against the code after drafting; the old pages overclaimed.
- Audience: never one industry. Kicker cycles `AUDIENCES`; say team, deal, what
  it's worth; never insurance agents, premium, district, consultant, case.
- Demos: one data file, local state only, no hint or footer text, `text-base`
  on inputs, announce `deliver` / `drag` / `celebrate` for Biscuit.
- QA: `tools/feature-page-qa/pages/<slug>.json`, then interactions, text-sweep
  and phone-moments against a served `dist/`, then again against live. Two
  Browser Use walkthroughs (desktop, 390x844) with a steps file that asks for
  facts you can verify; about $0.30, measured by balance delta.
- Ship: full suite to a log (name failures that are not yours), rebase, push to
  main (the push is the deploy), verify live, kanban card, memory note.
