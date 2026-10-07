# The content gate (vitest, node environment)

Adapt the paths and the allowed-link sets; keep every assertion. The real file that shipped: `src/lib/__tests__/academy.test.ts` in the SearchBlueprint repo.

```ts
import { describe, it, expect } from "vitest";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { ACADEMY_TRACKS, plannedLessons } from "@/lib/academy-tracks"; // the manifest
import { parseFrontMatter } from "@/lib/help-docs";                     // or any front-matter parser
import { parseToolList, wordCount } from "@/lib/academy";
import { FREE_TOOL_GROUPS } from "@/lib/free-tools-registry";            // the product's tool registry

const ACADEMY = path.join(process.cwd(), "docs", "academy");
const TOOL_SLUGS = new Set(FREE_TOOL_GROUPS.flatMap((g) => g.tools.map((t) => t.slug)));
const PLAN = new Map(ACADEMY_TRACKS.flatMap((t) => plannedLessons(t).map(({ lesson }) => [`${t.slug}/${lesson.slug}`, lesson] as const)));

function published() { /* read every docs/academy/<track>/*.md → { track, slug, file, meta, body } */ }

describe("curriculum", () => {
  it("has unique track, chapter and lesson slugs", ...);
  it("points every track's startHere at a planned lesson", ...);
  it("uses safe slugs everywhere", () => /^[a-z0-9-]+$/);
});

describe("published lessons", () => {
  it("every file on disk is a planned lesson", () => PLAN.has(`${track}/${slug}`));
  it("front matter carries the contract's keys and matches the plan", () => {
    // title === plan.title; summary > 20 chars; level ∈ {beginner, intermediate, advanced};
    // updated matches YYYY-MM-DD; every tools[] slug ∈ TOOL_SLUGS
  });
  it("has the lesson shape", () => {
    // exactly one /^> \*\*Do this now\*\*/m; /^## What to take away/m; /^## Next/m;
    // 550 <= wordCount(body) <= 1400  (brief says 700-1,100; the gate allows a margin)
  });
  it("keeps the house style", () => {
    // no "—"; no "!" outside code spans; headings not Title Case
    // (count capitalised non-proper words after the first; > 1/3 of words = fail; keep a PROPER set: Google, Shopify, GA4...)
  });
  it("links only to pages that exist", () => {
    // for each ](/path) in body:
    //   /academy/<track>/<slug> must be in PLAN (or a known track)
    //   /free-tools/<slug> must be in TOOL_SLUGS
    //   /help/<section>/<slug> must exist on disk
    //   anything else must be in an explicit ALLOWED_PATHS set (signup, connector, hub...)
  });
});
```

Why each assertion exists: an unplanned file is a page nobody designed; a missing callout is a lesson with no conversion; an unknown tool slug is a 404 in the one place the reader was asked to act; the em dash and exclamation rules are the house style's mechanical half; the word range catches both thin lessons and the writer that keeps going; the link check is the difference between "published" and "published with dead ends".

Run after every writer wave: `npx vitest run <gate file>`. Typical first-wave failures: one lesson over length, a Next link to a slug the writer misspelled, a `tools:` value with a tool the writer assumed existed.
