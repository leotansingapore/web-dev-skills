# Lesson brief (template — fill the <angle-bracket> slots, then hand the whole file to every writer)

You are writing lessons for <Academy name>: a free, public curriculum at <site>/academy. Readers are <audience sentence>. The bar: a reader finishes a lesson knowing exactly what to do next, and nothing in it would embarrass an experienced <domain> practitioner.

## Files

- Curriculum (which lessons exist, their titles, summaries, order): `<path to manifest>`. Write ONLY the lessons assigned to you, with EXACTLY the slugs and titles given there.
- Output path: `<content dir>/<track>/<lesson-slug>.md`.
- Gold standard to match: `<path to the gold lesson>`. Read it first. Match its density, structure and tone.
- What exists in the product (the ONLY tools and features you may reference): `<path to generated tool/feature list>`. Before describing any product feature, read its documentation page so you describe what it really does.
- Dated, verified facts: `<path to the product's facts source, if any>`. If a fact there contradicts your memory, the file wins.

## Frontmatter (exact keys)

```
---
title: <exactly as in the manifest>
summary: <exactly as in the manifest, or a sharper one sentence>
level: beginner | intermediate | advanced
tools: [tool-slug, tool-slug]   # 0-3 slugs from the tool list that the Do-this-now uses; [] if none
updated: <YYYY-MM-DD>
---
```

## Structure (in this order)

1. **Opener, 2-4 sentences, no heading.** A concrete scene or the reader's situation, then the one-sentence thesis. No "In this lesson you will learn".
2. **3-5 `##` sections.** Each teaches one idea: the mechanism first (how it works), then what to do about it. `###` sparingly. Short paragraphs (1-4 sentences). Numbered steps for procedures; bullets only for genuinely parallel items.
3. **A "Do this now" block** (required, exactly this markdown):
   ```
   > **Do this now**
   >
   > <One concrete action completable in 10-30 minutes, with the tool or product page it uses as a markdown link. Say what result to look for.>
   ```
   One per lesson, placed where it lands best.
4. **`## What to take away`** — 3-4 bullets, each a complete sentence the reader could repeat to a colleague.
5. **`## Next`** — one sentence pointing to the next lesson in the chapter (link `/academy/<track>/<slug>`), or the next chapter's first lesson if this is the last.

Length: 700-1,100 words of body. Reading level: a smart non-specialist. Jargon only when it is the real name of the thing, explained in the same sentence the first time.

## Fact discipline (hard rules — a violation fails the lesson)

- **Numbers only with a named source.** A statistic, percentage, threshold or date appears ONLY if you name its source inline in the same sentence. No source, no number: state the mechanism qualitatively. Never cite a study you are not certain exists.
- **Never invent product capability.** The product does exactly what the tool/feature list and its docs say. Link tools as `<tool URL pattern>` by their exact names. Product links allowed: <list: signup, connector, docs pattern>.
- **No guarantees, no "ranks in 30 days", no invented case studies or customer stories.**
- **Documented positions win over folklore.** Where the platform (Google, the CMS vendor) has documented something, describe that. Where something is contested or undocumented, say so in one clause.
- **No retired features as live.** <List the known retired items for the domain.>
- **Date-stamped claims stay honest.** It is <month year>. Do not describe "new" features you cannot date; describe behaviour.

## Voice

- Second person, present tense, contractions. Plain verbs.
- Teach like a calm expert explaining to a smart friend. Warm, never cute. Confident, never hyped.
- Mechanism before tactic: readers who understand WHY adapt when the platform changes.
- Examples are fictional and generic; never name real businesses as examples.
- Forbidden: exclamation marks; rhetorical questions left unanswered; "game-changing", "unlock", "leverage", "seamless", "delve", "robust", "supercharge", "in today's digital landscape", "it's not just X, it's Y", "not only X but also Y"; bullets with bolded lead-ins followed by colons (the `- **Label:** text` pattern — a numbered step opening with a bold full sentence, as the gold lesson does, is fine); em dashes (use a comma, a colon, or two sentences); title case headings; any sentence that sells the product rather than teaches. The product appears ONLY inside "Do this now" and occasionally as "the free [tool name]" where it is the natural instrument.
- Every `##` heading is a plain statement or an action, sentence case.

## Links

- Lessons link to each other with relative paths: `/academy/<track>/<slug>`. Only link to lessons that exist in the manifest AND will be published in the same ship — a planned-but-unwritten target is a live 404 until its file lands.
- External links only to primary sources (the platform's own documentation). Full https URLs, no tracking parameters, no made-up URLs: if unsure the URL is real, name the source without linking it.

## Before you finish each lesson

1. Frontmatter keys exact; title and slug match the manifest.
2. One "Do this now" block, exact format, linking a real tool/page.
3. Zero numbers without a named source in the same sentence.
4. Zero forbidden words and patterns; zero em dashes; zero exclamation marks; sentence-case headings.
5. "What to take away" and "Next" present; the Next link targets an existing slug.
6. 700-1,100 body words.
