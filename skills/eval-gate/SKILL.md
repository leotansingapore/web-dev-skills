---
name: eval-gate
description: Score an output against Leo's quality rubrics before handing it over. Use BEFORE reporting any work as done, moving a task card to review, delivering generated images or thumbnails, or shipping prose a human will read. Triggers on "is this ready", "eval this", "check before I ship", "score this output", "gate this", or any point where work is about to be handed to Leo, a client, or a task board. Also use proactively at the end of any task that produced an image, copy, or a code change.
---

# Eval gate

Leo is the final gate, not the QA department. He should be choosing between good
options, not catching garbled thumbnail text or unverified "done" claims. This skill
scores an output before it reaches him.

**Canonical rubrics:** `~/Documents/New project/catalyst-opus/docs/EVALS.md`.
Read it when you need the full dimension tables. The condensed gate is below.

## When it fires

| Output type | Run |
|---|---|
| Anything at all | EVAL 1 `did-leo-decide-this` |
| Generated image / thumbnail / diagram / render | + EVAL 2 `visual-asset-usable` |
| Prose a human reads (article, email, report, ad copy, UI string) | + EVAL 3 `copy-ready` |
| Code change | + EVAL 4 `code-shipped` |

Most work triggers two. Score every dimension 0 / 1 / 2 against the artifact itself.

## EVAL 1 — did-leo-decide-this (always)

1. **Don't break production** — exercised live in the real app, or just a grep hit / green build?
2. **Don't waste money** — avoided a paid re-run, a double-build, a second deploy of one commit?
3. **Ship it** — working improvement landed now, not a perfect one pending?
4. **Keep it simple** — smallest change that works, no new abstraction or dependency?
5. **Make it maintainable** — follows existing repo patterns?

**PASS = 7+ of 10 AND no dimension at 0.** A zero anywhere is a hard fail regardless of total.

## EVAL 2 — visual-asset-usable (generated imagery)

1. **Text renders clean** — zero garbled, melted, doubled, or invented glyphs
2. **Exact dimensions** — thumbnails 1280x720, diagrams 1920x1080, platform sizes per spec
3. **Legible at delivery size** — not just at 100% zoom
4. **Faithful to the brief** — nothing invented or dropped
5. **On brand** — design-system tokens, dark mode where applicable

**PASS = 8+ AND dimension 1 at 2.** Any text defect is a re-generate, no exceptions.

You must **Read the image back** before scoring. Scoring a render you have not looked at
is a fabricated eval and worse than no eval. Known repeat failure: Higgsfield MCP `soul`
returns text-free output while CLI `soul_v2` renders text.

## EVAL 3 — copy-ready (prose)

1. **No banned patterns** — zero hits vs `~/.claude/skills/anti-ai-writing/references/banned-patterns.md` (read it, do not score from memory)
2. **ASCII only** in anything a script emits — no em dashes, smart quotes, Unicode specials
3. **Outcome-first** — what now works, not what was touched
4. **Claims are true** — nothing over-claimed; states actual state
5. **Right length** — no preamble, no restating the question

**PASS = 8+ AND dimensions 1, 2, 4 all at 2.** Dimension 4 is absolute for anything
outward-facing.

## EVAL 4 — code-shipped

All five required: build green / driven live at target viewport / console clean / no
regression / one logical change committed with an outcome-focused message.

## Procedure

1. Pick the applicable evals.
2. Score each dimension against the **artifact**, not your intent.
3. FAIL -> fix the specific failing dimension, re-run. **Hard cap: 2 re-runs.**
4. Third consecutive FAIL -> stop. This is a scoping problem, not a quality problem.
   File it for Leo with the scores and the blocking dimension.
5. PASS -> report the scores inline. Never a bare "eval passed":

```
EVAL did-leo-decide-this: 2/2/2/1/2 = 9 PASS
EVAL visual-asset-usable: 2/2/2/2/1 = 9 PASS (1 re-gen: first pass had a malformed "g")
```

## Anti-gaming

A re-run is not a demerit — "PASS after 1 re-gen" is the system working. A clean
first-pass 10/10 on a visual asset reads as an unread eval. If you catch yourself
rounding a 1 up to a 2 to clear the gate, that is the exact failure this skill exists
to prevent: score it honestly and iterate.

In a `/loop` or unattended context, a FAIL never means stop and ask — it means fix and
re-run, then escalate at the cap.
