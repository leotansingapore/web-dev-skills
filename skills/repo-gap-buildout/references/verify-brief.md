# Verify brief (one Explore agent, very thorough, background)

Fill the brackets. One agent checks every item; splitting the list across agents makes
them re-learn the target repo each time. In a large repo expect about 15 minutes and
200k tokens for 36 items.

```
Search breadth: very thorough. Read-only.

Repo: <target path> (<stack: where the UI, server functions and migrations live>).
I am doing a gap analysis of its <area> features against <reference repo>. For EACH
numbered item below, decide: HAVE (fully present), PARTIAL (exists but narrower; say what
is missing), or MISSING. Cite the strongest evidence as file path(s), with a line if
useful. Do not guess: grep for the concept under several names (e.g. quick replies =
canned / saved replies / snippets / shortcuts; assignment = assignee / assigned_to /
owner / claim). A management screen is not the feature: check the path that actually
runs or sends it. If a code comment says a feature is absent on purpose, quote it.

<Section>
1. <capability phrased as what a user can do, with the reference's own detail>
2. ...

Then a short section "Target-only": up to 15 <area> capabilities this repo has that the
reference does not, each with one evidence path.

Output: a compact table per section: # | verdict | evidence | note (note under 20 words).
No preamble.
```

## Worked example: wacrm vs ActivityTracker (2026-10-06)

Reference: github.com/ArnasDon/wacrm (MIT, Next.js 16 + Supabase, Meta Cloud API only).
Target: ~/remix-of-activity-tracker, area CRM / WhatsApp inbox / AI agents.
Result: 36 items, 8 HAVE, 19 PARTIAL, 2 MISSING, transport BOTH (Green API + Cloud).

The checklist sections that worked: Inbox (transport, assignment, status/reopen, notes,
message actions, quick replies, templates, interactive, media, failure reason, presence,
push, AI badge, take over, AI draft), CRM (tags/fields/import/dedup, deals + currency,
contact view), Broadcasts (template, audience, variables, schedule, delivered/read,
resume), Automations (trigger names, step names, chatbot flows), AI (BYO key, knowledge
retrieval, playground, caps, handoff target + summary, usage log), Platform (dashboard,
roles/invites/ownership, REST API keys, outbound webhooks, MCP, i18n, themes, sessions).

What the spot-check found that the inventory alone would have got wrong:
- Templates: AT could create and sync Meta templates but nothing sent one, so Cloud lines
  could not restart a chat after 24 hours. The top real gap, invisible from the UI.
- Reactions: absent on purpose; a comment in wa/green.ts says Green API cannot send them.
- Assignee picker: removed by Leo on 2026-10-01 (59b623a24). A decision, not a gap.
- Snooze: Jev ranked it first, but wacrm lacked it too. Reported as "neither has it".
- Jev scores for the top 12 gaps sat between 0.71 and 0.83, so the order inside that
  band said little; the facts above decided the lead line.
