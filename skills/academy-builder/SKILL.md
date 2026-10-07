---
name: academy-builder
description: Use when asked to build, extend or clone a learning hub on a product site — an "academy", curriculum, course section, learning centre, lesson library or programmatic education hub — for SEO, for a vertical (local, e-commerce, agency), or for any product that wants free educational pages that rank and feed its free tools. Triggers include "build an academy", "create lessons/courses for our site", "make a learning centre like <competitor>", "add a new track to the academy", or a request to screenshot and out-build a competitor's academy.
---

# Academy builder

## Overview

An academy is a public, indexable curriculum: tracks → chapters → short lessons, every lesson ending with one action the reader can take right now, usually on a free tool. This skill is the process that built the SearchBlueprint Academy (4 tracks, 36 chapters, ~110 lessons, shipped 2026-08-22) from a competitor reference in one session, with a fact gate that keeps AI-written lessons honest. Follow it in order; the gate at step 7 is what makes the volume safe.

## When to use

- A product site wants a learning hub that earns search traffic and hands readers a tool or a signup at the moment of intent.
- There is a competitor hub to learn from (structure, counts, recurring chapters), and you are asked to match or beat it.
- Extending an existing academy with a new track, vertical or language.

Not for: product documentation or help centres (use the product-education register, e.g. saas-product-education / notion-style); single blog posts; gated course platforms with video and quizzes.

## The process (one pass, nine steps)

| Step | Output | Reference |
|---|---|---|
| 1. Capture the reference | Full-page screenshots (desktop + mobile) of each competitor hub and one lesson, plus extracted text, archived in the repo with a manifest | [process.md](references/process.md) §1, [capture.mjs](references/capture.mjs) |
| 2. Read the structure | One paragraph per hub: counters, featured lesson, chapter count, recurring chapter archetypes, lesson anatomy | process.md §2 |
| 3. Design the curriculum | A manifest file: tracks (audience, promise, startHere) → chapters (title, blurb) → lessons (slug, title, one-sentence summary) | [curriculum-design.md](references/curriculum-design.md) |
| 4. Write the brief | The lesson contract: front matter, shape, fact discipline, voice, links, self-check | [lesson-brief-template.md](references/lesson-brief-template.md) |
| 5. Write one gold lesson yourself | The example every writer must match | process.md §5 |
| 6. Fan out writers | One subagent per chapter, each reading brief + manifest + gold lesson + the product's real tool/feature list | process.md §6 |
| 7. Gate every lesson | A test that fails on unplanned slugs, missing callouts, dead links, unknown tools, em dashes, Title Case, length | [gate-test-template.md](references/gate-test-template.md) |
| 8. Render | Hub, track and lesson routes from manifest ∩ files on disk; sitemap, footer link, public allowlist, JSON-LD, local progress | process.md §8 |
| 9. Ship and verify | Build, e2e at 390px, push, check production, record on the board | [checklist.md](references/checklist.md) |

## Load-bearing rules

1. **Manifest first, files second.** The curriculum file is the plan; a lesson publishes only when its file exists AND its slug is planned. Counters, sitemap and nav derive from the intersection, so nothing half-written ever renders.
2. **Numbers only with a named source in the same sentence.** This is the rule that makes 100 AI-written lessons publishable. Writers list the facts they left out; that list is a feature, not a failure.
3. **Product capability is quoted from the product's own docs, never remembered.** Hand writers the exact list of tools and documented features and forbid everything else.
4. **Every lesson ends in an action wired to a real tool or page.** That is the conversion mechanism and the thing the competitor usually lacks.
5. **One gold lesson before any fan-out.** Writers match an example far better than they follow prose rules.
6. **One writer per chapter, not per lesson or per track.** Three to five lessons is the context size that keeps cross-links coherent and quality even.
7. **The gate runs in the repo's test suite.** A new lesson that breaks the contract fails `npm test`, not a reader.
8. **Mechanism before tactic, sentence-case headings, no em dashes, no exclamation marks, no hype vocabulary.** The house style of the brief; the gate enforces the mechanical parts.
9. **Keep the reference archive in the repo.** Screenshots, extracted text, manifest and the capture script, so the next session can re-compare without re-crawling.
10. **Respect the host repo's rules.** Public-route allowlists, sitemap conventions, design tokens, commit-and-push discipline, work boards: read the project's CLAUDE.md before step 8.

## Quick reference

- Sizing that worked: 8–10 chapters per track, 2–4 lessons per chapter, 700–1,100 words per lesson, 4 tracks for "all audiences" (general, local, e-commerce, agency). The brief's 700–1,100 is the writers' target; the gate deliberately enforces a wider 550–1,400 so one stubborn lesson can't block a ship.
- Extending an existing academy: skip steps 1–2 when the reference archive and system doc exist, reuse the repo's brief and gate unchanged, write the NEW track's manifest entry and its own gold lesson (step 5 applies per track), then fan out. Publish a track only when every lesson a shipped lesson links to ships with it — the e2e link-resolve check is the final guard, because the gate validates links against the PLAN, not against what is published.
- Recurring chapter archetypes worth including: how it works · find the targets · structure · content · AI search · authority · measure · run it with an AI assistant · the 90-day plan.
- Concurrency: writers run ~8–10 minutes each; the harness caps concurrent subagents (20 here), so launch in waves and feed the queue from completion notifications.
- Cost of one academy (~110 lessons): ~36 writer agents at ~130k tokens each.

## Where this skill earns its keep

Validated 2026-08-22 with an A/B test (plan a fifth track + first lesson, with and without the skill). In a repo that already carries the system doc and a live academy, a capable agent reconstructs most of the contract from the repo alone — which is the intended effect of step 9. The skill's differential value: the typed manifest discipline (the baseline produced prose tables, not the appendable structure), the curriculum archetypes, the capture and gate templates, and the step accounting — and on a FRESH product with no academy, all nine steps. Highest value: first build on a new site; lowest: one more lesson on a mature academy.

## Common mistakes

- Letting writers cite statistics from memory. Fix: the source-in-sentence rule plus a report of omitted facts.
- A help page and the code disagreeing about a feature (a "tool" the docs list but the route lacks). Writers will find these; file them rather than paper over them.
- Title Case headings and em dashes creeping in. The gate catches both; keep it strict.
- Counting planned lessons instead of published ones on the hub. Derive every number from the intersection.
- Building a docs-style shell for a marketing surface. The academy is public and indexable; use the site's marketing chrome and keep the docs host noindex.
