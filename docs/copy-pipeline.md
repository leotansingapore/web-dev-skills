# Copy pipeline

The rules every skill in this repo follows when it writes words a person will read. Copied from the author's Claude Code CLAUDE.md; drop the section into your own CLAUDE.md to make it binding.

Applies to ALL prose a human will read: landing pages, ads, emails, proposals, posts,
scripts, SOPs, training material, docs. Not optional, not "when it seems worth it".

Run this pipeline in order. Skipping a step is a defect, same as skipping a test.

0. **Read the brief, and the brief is built from competitors first.**
   `.agents/product-marketing.md` in the repo, before anything else. A module's section
   starts from the five or six nearest competitor pages: the category noun and headline
   formula they share, the enemy they name, their section shape, CTA pair, proof and
   recurring words, then the gap none of them claim. The product's own facts fill that
   frame; they never set it (Leo, 2026-09-22: "it should always be based on competitors
   first"). No section for the page you are writing? Read the competitors and write one
   before drafting. No brief at all? Build one the same way with
   `marketing-skills:product-marketing`. Do not draft around the hole. The register (step 3b) and the CTA come from the brief, not from a
   guess. /features/crm shipped three times with "CRM" as the headline noun and "lead" in
   every block while the brief three days old said to avoid both (2026-09-22).
   Where the brief and the page's job conflict (a page about the CRM module cannot avoid
   the word), surface the conflict to Leo before drafting; do not resolve it alone.

1. **Voice source first.** Check `~/.claude/skills/voice-*/` and use it. No voice skill?
   Fall back on the COMPETITORS or the references Leo gave (a URL in the brief is a voice
   source), never on the client's own sibling pages, which are usually unreviewed copy
   with the same problems (Leo, 2026-09-22). Neither? Name a specific person saying this
   to a specific person. NEVER write in neutral "professional marketing voice" - that
   register belongs to nobody, which is why it reads like a machine.
2. **Check the input.** Sales and conversion copy (landing pages, feature pages, ads,
   emails) is features and benefits: what it does, then what that gets the reader in
   their day. That is what a buyer wants to know. Do not reach for internals, caveats
   or what the product will not do; a landing page is not a spec sheet and not a
   changelog (Leo, 2026-09-22). Real numbers and names welcome. For other prose (posts,
   docs, proposals) get 3+ real specifics first: a number, a name, something that went
   wrong, an opinion worth defending. With none of them you are about to write filler,
   so stop and ask.
3. **Read real specimens.** `copy-corpus` skill - open the file for the format you are
   writing and read 20-30 real human specimens in the nearest category. The competitor
   or reference pages from step 1 count as specimens too; put them beside the corpus.
   Calibrate length, altitude and rhythm. Never lift a line.
4. **Apply the rules.** `anti-ai-writing` skill governs every word. Read its
   references/banned-patterns.md before drafting, not after.
5. **Gate it mechanically, then get it read.** Write the draft to a `.md` file and run
   BOTH `aicheck <file>` (under 15 ships) and `brief-check <file>` (zero avoid-words, and
   read its WHO / CTA / VOICE lines against the draft). A PostToolUse hook scores prose
   files automatically, but you run both yourself before presenting work. Then Leo reads
   the `.md` BEFORE the copy goes into code: three deploys to fix a landing page's words
   is the failure this prevents. Port once, after the read.
6. **Repair, do not patch.** Failing score means rewrite the flagged sections from
   scratch via the `humanize` skill. Word-swapping preserves the AI sentence underneath.

Hard rules that override everything above:
- NO em dashes in any prose, ever - not just automation output. Use a period or a comma.
  Em dashes are my single most reliable AI tell and appear in zero words Leo has written.
- No emoji. Sentence case headings, not Title Case. Bold only for a term being defined.
- One register per piece. Do not blend `saas-copy` variants unless explicitly asked.

**Sales and conversion copy has two more steps, between 3 and 4, and they are not
optional** (Leo, 2026-09-22, after /features/crm shipped twice as a spec sheet):
- **3a. The hook gate: competitors' moves, the reader's scores, Jev's pick.** Nothing
  on the page is written from nothing (Leo, 2026-09-22: "don't use ours. everything
  should be based off competitors"). For every H1, sub, H2 and CTA heading:
  1. Pool every hook from 12-16 competitor pages (headline, sub, each section H2, the
     one-line benefits). Tag by source. Put the reader paragraph and the pain lines
     from the brief in the spec.
  2. `hook-check <pool.json>` scores each out of 10 in the reader's shoes (care 30%,
     outcome 25%, clarity, credibility, distinctness, concreteness). 143 hooks cost
     $0.006. The competitor median is the bar.
  3. Take the top 10-15 MOVES and adapt each to this product's nouns, keeping the
     sentence shape. Several adaptations per slot, tagged `adapted:<competitor>` and
     given a `slot`. Never invent an angle the pool did not score.
  4. `hook-check <adapted.json>` picks per slot: highest score with credible >= 0.6.
     `--h2h` on a shortlist of 8 or fewer when two are close.
  5. A slot where nothing clears the bar after two rounds is CUT, not forced. On
     /features/crm the pillar cards (not a competitor move) and the Fields block
     (care never above 0.38) went this way.
  **Then judge the page, not the lines** (Leo, 2026-09-22, after a slot-by-slot page read
  "weird and arbitrary"): write the page as one piece in one voice to the person who USES
  the product, from ONE competitor's frame, then have Jev read 2-3 whole drafts and the
  live page top to bottom in that reader's shoes and pick (remix-of-activity-tracker
  tools/jev-copy/crm-page/judge.py). The hook gate compares lines for one slot; it never
  assembles a page.
  What the first run taught: "CRM for [audience]" headlines, every competitor's and
  ours, scored 2.1 to 3.2; the moves that scored named a moment the reader dreads
  ("Skip the review scramble" 7.5) or a question they ask ("No more guessing who
  needs a call" 7.3). Absolutes ("Nothing falls through the cracks") fail credibility.
  Bodies are the product's facts under the chosen hook, in the competitor body shape
  (what it does, then the so-what), and are checked against the code AFTER the hook
  is chosen. Pool, adapted spec and scores live beside the brief's module section.
- **3b. Register.** `saas-copy`: pick ONE of its twelve registers and read its rules.md
  and formulas.md before drafting. SMB and advisor pages are `human-simple` (you from
  sentence one, contractions on, verb-led feature titles, median sentence under 15 words).
  Say which register and why, in one line. Never blend two.
Persuasion architecture for long-form funnels: `direct-response-copywriter`. Long-form
teaching: `hormozi-content-creator`. Help docs: `notion-style`. Polish pass after the draft:
`marketing-skills:copy-editing`. These set the argument; anti-ai-writing still sets how it
reads, and `aicheck` still gates it.
