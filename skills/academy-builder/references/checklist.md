# Academy builder checklist

## Before the fan-out
- [ ] Reference captured (desktop + mobile + one lesson per hub), JPEG-compressed, archived in the repo with manifest.json, index.html and extracted text.
- [ ] Structure paragraph written into the archive manifest (`observed_structure`).
- [ ] Manifest written by hand: every track has audience, promise, description, startHere; chapters in reading order; every lesson has slug, title, one-sentence summary.
- [ ] Tool/feature list generated from the codebase, not memory.
- [ ] Brief filled in from the template; gold lesson written and itself passing the gate.
- [ ] Gate test added and green on the gold lesson.
- [ ] Work-board card filed and in `doing` (if the repo has a board).

## During the fan-out
- [ ] One writer per chapter; waves sized to the concurrency cap; queue fed from completion notifications.
- [ ] Gate run after each wave; offenders fixed or sent back.
- [ ] Writers' "facts left out" lists skimmed for doc/code drift worth filing.

## Rendering
- [ ] Content layer joins manifest ∩ disk; counters, sitemap and nav derive from it.
- [ ] Hub, track and lesson routes statically generated (`generateStaticParams`, `dynamicParams = false`).
- [ ] `> **Do this now**` renders as a callout; tool cards come from the registry; Mark-complete + ticks are a client island with wrapped storage.
- [ ] JSON-LD: Course on track pages; Article + BreadcrumbList on lessons; `<` escaped in the inline script.
- [ ] Public-route allowlist, sitemap, footer link, host design tokens, 44px tap targets.

## Ship
- [ ] `npm run build` green on the rebased tree (every lesson prerenders).
- [ ] Full test suite green (the gate is part of it).
- [ ] e2e at 390px against the production build: 200s, no console errors, no horizontal overflow, JSON-LD present, callout renders, internal links resolve, sitemap lists hub/track/lesson.
- [ ] Commits pushed per the host repo's rules (pull --rebase first, never force).
- [ ] Production checked: hub counters, a lesson's JSON-LD, sitemap.
- [ ] Board card moved to review/shipped with what was verified; system doc (`docs/ACADEMY.md` or equivalent) committed; reference archive path recorded.
