# Academy builder: the process in detail

## §1 Capture the reference

Use playwright-core with the system Chrome (no browser download, no MCP profile lock):

```bash
cd <repo> && NODE_PATH=$(pwd)/node_modules node <skill>/references/capture.mjs <outDir>
```

Edit the `PAGES` list in capture.mjs first. It captures each hub at 1440px and 390px (2x), follows the first lesson link on each hub for a lesson-page capture, and writes `manifest.json`. Then extract text for reading without images:

```bash
defuddle parse <url> --md > text/<slug>.md
```

Archive in the repo where the project keeps competitor references (SearchBlueprint: `public/reference/<topic>/` with `manifest.json` + a noindex `index.html` gallery + `text/`), JPEG-compressed (`sips -s format jpeg -s formatOptions 82`) so mobile full-page captures stay under ~3 MB.

## §2 Read the structure

From the extracted text, write one paragraph per hub: hero counters (lessons / chapters / free), featured "start here" lesson, number of chapters, lesson counts per chapter, recurring chapter archetypes across hubs, and the lesson anatomy (opener, stat callouts and whether they are sourced, section count, action box, navigation). Record it in the archive manifest under `observed_structure`. This paragraph is what the curriculum is designed against.

## §3 Design the curriculum

See curriculum-design.md. Output is a typed manifest (`src/lib/academy-tracks.ts` shape): tracks → chapters → lesson plans with slug, title, one-sentence summary. Write it yourself; it is the editorial IP and the spec every writer follows.

## §4 Write the brief

Start from lesson-brief-template.md. Fill in: the output path, the gold lesson path, the product's tool/feature list file, the dated-facts source, the signup/product links the writer may use. Generate the tool/feature list from the codebase (a registry file, a docs folder listing), never from memory.

## §5 Write one gold lesson yourself

Pick the track's first lesson. 900–1,000 words. Obey every rule in the brief. This file is the strongest instruction you will give the writers.

## §6 Fan out writers

One general-purpose subagent per chapter. Prompt shape:

```
Write the <Academy> lessons for chapter `<chapter>` of track `<track>`, in <repo path>.
FIRST read, in order: (1) <brief> — the contract; (2) <manifest> — your chapter's slugs, titles, summaries;
(3) <gold lesson> — match it; (4) <tool/feature list> — the only product references allowed;
(5) <dated facts source>; (6) the product doc page for any feature you mention.
<Chapter-specific fact notes: which named sources apply, which statistics are forbidden without a source,
which product docs are directly relevant.>
Write EVERY lesson listed under your chapter (<n>): <slugs> — each to <path>/<slug>.md.
Run the brief's final check on every lesson and fix failures before finishing.
Return only: files written with body word counts, tools linked per lesson, and any fact you were unsure about and therefore left out.
```

Launch in waves sized to the harness's concurrency cap; feed the queue from completion notifications. Writers take 8–10 minutes and ~130k tokens each.

## §7 Gate every lesson

Add the gate test (gate-test-template.md) to the repo's suite before the first wave lands. Run it after each wave; fix or send back offenders (typical: over-length, a stray em dash, a link to an unplanned slug). Keep the gate strict: it is the only thing standing between "AI wrote 100 pages" and "100 pages are publishable".

## §8 Render

Mirror whatever the host site already does for static markdown (SearchBlueprint: the help-centre loader pattern, read at build time, `generateStaticParams`, `dynamicParams = false`). Pieces:

- **Content layer**: join manifest with files on disk; per lesson compute word count and reading minutes; expose `getPublishedTrack`, `listPublishedTracks`, `getLesson` (with prev/next across chapters).
- **Hub**: counters from published lessons, one card per track with audience + promise + counts + "Start here", a three-point "how it works", a product CTA.
- **Track**: breadcrumb, promise, counters (lessons / chapters / minutes / free), featured start lesson, local progress bar, chapters as numbered sections with lesson rows (tick, title, summary, minutes, level).
- **Lesson**: breadcrumb, chapter label ("Chapter n · Lesson i of m"), title, summary, meta row, markdown body with heading ids shared with the TOC, the `> **Do this now**` blockquote rendered as a callout, tool cards from the registry, Mark-complete island, prev/next, chapter rail (lg+) and TOC (xl+), Article + BreadcrumbList JSON-LD with `isPartOf` Course.
- **Progress**: localStorage only, every access wrapped, renders correctly with nothing stored.
- **Wiring**: sitemap entries derived from published lessons (lastmod from front matter), footer link, public-route allowlist, design tokens of the host theme, 44px tap targets, no horizontal scroll at 390px.

## §9 Ship and verify

See checklist.md. Build green on the rebased tree, the e2e script passes at 390px against the production build, push (one commit per logical change, never force), then check production: hub counters, one lesson's JSON-LD, sitemap inclusion. Record what was verified on the work board.
