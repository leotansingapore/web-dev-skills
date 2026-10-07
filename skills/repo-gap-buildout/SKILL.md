---
name: repo-gap-buildout
description: Gap analysis of one of Leo's products against a GitHub repo, then build out the gaps worth closing. Inventories the reference repo's features (changelog, migrations, routes, engine vocab), checks each one in the target repo as HAVE / PARTIAL / MISSING with file evidence, spot-checks the surprises, ranks the gaps with Jev, reports, and on request ports the top gaps into the target's own patterns, one gap per commit. Use when Leo shares a GitHub repo and asks for a "gap analysis", "compare this to our X", "what are we missing vs this repo", "feature parity", "steal the good parts", or "build out what they have". For a whole marketing site against competitor websites, use competitor-site-buildout.
---

# Repo gap analysis and build-out

Two phases. The analysis always runs. The build-out runs only when Leo asks for it, or asks
for both in one go ("gap analysis and build it out").

First used 2026-10-06: github.com/ArnasDon/wacrm against ActivityTracker's CRM, inbox and
AI agents. That run is the worked example in `references/verify-brief.md`.

## Inputs

- The reference repo URL.
- The target: a local repo and the area to compare ("crm/inbox/ai agent features").
  Leo's shorthand maps through memory (`remix of activity tracker` is
  `~/remix-of-activity-tracker`; grep the memory folder for the name). If the target is
  ambiguous across his projects, ask which one; otherwise do not ask.

## Phase 1: analysis

1. Read the target's rules and memory. Its CLAUDE.md / AGENTS.md and the memory area
   file for the project (`~/.claude/projects/-Users-leo-Documents/memory/idx-*.md`).
   Memory holds the deliberate decisions (a removed picker, a "leads belong to many
   advisors" rule) that turn an apparent gap into a choice already made.

2. Clone the reference shallow into the scratchpad (`gh repo clone <owner/repo> --
   --depth 1`). Read `LICENSE` first; it sets what the build-out may do:
   - MIT, BSD, ISC, Apache-2.0: logic may be ported with attribution in the commit body.
   - GPL, AGPL, LGPL, or no license file: ideas only. Write the code fresh; never copy
     files or substantial blocks into Leo's products.
   - Never copy branding, marketing copy or docs text, whatever the license.

3. Inventory the reference. Best sources, in order:
   - `CHANGELOG.md`: dated, user-visible, names the migration per feature. Better than
     the README, which sells.
   - Migrations list: the schema history is the feature list in order.
   - Engine vocabulary: the string enums in automation, flow or agent engines give the
     exact trigger and step names (`grep -o "'[a-z_]*'" src/lib/automations/*.ts | sort -u`).
   - `src/components/*`, `src/app/api/*` (or the stack's equivalent), `docs/`.
   Skip what only matters to a self-hoster (deploy guides, Docker, hosting referrals).
   Write a numbered checklist grouped by section, each item phrased as what a user can
   do, with the reference's own detail ("per-conversation cap and an account-wide rate
   limit", not "rate limits").

4. Verify against the target with one Explore agent (very thorough, in the
   background), using `references/verify-brief.md`. While it runs, draft the gaps file
   for step 6. Do not run the same searches yourself.

5. Spot-check the surprises yourself before reporting anything. Take the 3 to 5
   verdicts that would most change the report and confirm each in the code:
   - A MISSING on something you would expect to exist.
   - A PARTIAL where a management screen exists: check the path that sends or runs it.
     (AT could create Meta templates and never send one. That was the top gap.)
   - Anything absent on purpose: a code comment, a transport limit (Green API cannot send
     reactions), or a recent removal (`git log -S'<concept>'`, then memory). A recorded
     decision is reported as "decided against", never as a gap.
   - Items you added from general knowledge that the reference also lacks: label them
     "neither has it".

6. Rank the gaps with Jev (Leo's rule: ranking is a decision).
   Write `gaps.json` with one entry per MISSING or PARTIAL item, phrased as the missing
   capability. The `product` line says what the product is, who uses it daily for what,
   and its transport limits. Then:
   ```
   python3 ~/.claude/skills/repo-gap-buildout/scripts/rank_gaps.py gaps.json
   ```
   About 22 questions cost well under a cent. Scores bunch: treat gaps within 0.05 as
   tied and let facts decide the order inside a band. A gap the target cannot do on its
   transport, or one Leo decided against, stays out of the ranked list whatever it scores.

7. Report in the terminal, in this order:
   - First line: the single biggest real gap and why it matters, with its evidence link.
   - Scope line: how many items were checked, with HAVE / PARTIAL / MISSING counts.
   - Ranked table: Jev score, gap, what the reference has, what the target has today
     (with a file link). Flag any gap that conflicts with a recorded decision as needing
     Leo's call.
   - Low value for this product: one line each, with the reason (score, or the fact).
   - Where the target is ahead: one paragraph.
   - Porting: license, stack difference, rough size of the reference modules
     (`wc -l`), and which gaps need a migration or a new dependency.
   End with the one next action.

## Phase 2: build-out

Go in Jev rank order, skipping gaps flagged for Leo's call. One gap per subagent in its
own git worktree off origin/main, at most two at once (memory `cap-parallel-subagents.md`).

For each gap:

1. Read the reference implementation for that gap end to end: the module, its migration,
   its tests, and where it is called from.
2. Find the target's nearest existing pattern and extend it. Port the logic into the
   target's conventions (AT: Deno `supabase/functions/_shared/`, React in `src/`), not
   the reference's files or folder layout.
3. Stop and ask before building (Leo's standing stops, which hold even under "go
   autonomously"): a database schema change, a new dependency, auth, payment or
   security changes, money, or a change to shared code you cannot prove safe. Show the
   plan, with the migration text if there is one. A migration also goes through an
   independent review before it is applied (memory `migration-review-before-apply.md`).
4. Test first in the target's framework. Run the target's full suite, typecheck and
   build. For UI, also check for no console errors and no overflow at 390px. Then review
   the diff with `/code-review`.
5. Ship per the target's rules: one gap per commit (`feat: send Meta templates from the
   inbox on Cloud lines`). For a permissive-license port, add `Ported from
   <owner/repo>@<short sha> (<license>)` to the commit body. The push is the deploy
   where the repo auto-deploys; never also run `vercel --prod`.
6. After shipping, re-check that item against the live code so it reads HAVE. Update the
   kanban (`~/kanban/index.html`: string-replace, bump DATA_VERSION, check the headless
   render) and the project's memory area file.

## Traps

- The inventory overstates parity when an agent finds a settings screen and calls it
  done. Always check the send or run path (step 5).
- A transport difference can make a reference feature impossible or pointless. Check it
  before ranking, not after building.
- Jev cannot see the codebase, only the gap's wording. Phrase every gap as what a user
  could do, never as an implementation ("pgvector retrieval").
- Large repos: the verify agent needs the stack layout in its brief, or it spends half
  its time finding where things live.
