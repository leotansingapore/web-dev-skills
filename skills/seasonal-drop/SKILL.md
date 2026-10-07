---
name: seasonal-drop
description: Ship a limited-edition festival drop on activity-tracker.io (themes, scene backdrops, free pet outfits, an icon pack, the log-tab banner and the chooser page). Use when Leo types /seasonal-drop <festival> or asks for Halloween / Christmas / CNY / Deepavali / Hari Raya / Valentine's / any season's themes, outfits, costumes or buttons.
---

# Seasonal drop

One festival = one row in a table + artwork. Two repos move together:
`~/remix-of-activity-tracker` (catalog, UI) and `~/corgi-care-tracker` (outfit
render service; push auto-deploys). Precedents: National Day (auto-applied),
Mid-Autumn (2 themes), Halloween 2026-10-02 (4 themes, 4 outfits, icon pack).
`git log --grep=Halloween` in remix shows every file one drop touches.

Defaults (do not ask): themes, outfits and icon pack are FREE (cost 0) and
OFFERED, never auto-applied (only National Day auto-dresses). Season ends on
the Sunday after the festival, SGT. Ship every scene candidate that looks good
as a theme; Leo prunes on the preview page.

## 1. Season row (remix `src/lib/appScenes.ts`)
- Add the id to `LimitedSeason` and a `LIMITED_SEASONS` row `{ label, lastDaySgt, accent }`.
- Fix every `SeasonVisibility` literal the compiler flags (tests, `NdpPreviewPage`).
- Add `<id>SeasonOpen()` only if a caller needs it (NdpPreviewPage does).
- Visibility, retirement walk-back (themes AND icon packs) and catalog
  filtering are generic off `LIMITED_SEASON_IDS` / `seasonThemeIds` / tile
  `season` - nothing else to write.

## 2. Scenes -> themes
- Add 4 subjects to `scripts/scene-art/generate.mjs` `SUBJECTS` with an id
  prefix (`hw-`, `ma-`). House rules are in its STYLE: empty lower third, no
  characters/animals, no text. Night skies want `dark: true` in APP_SCENES.
- `higgsfield workspace set <ActivityTracker workspace id>`, then
  `node scripts/scene-art/generate.mjs --only=a,b,c,d --concurrency=4` (~4.5 credits each).
- Contact-sheet them and LOOK before wiring.
- Per theme: `<ID>_ID` const, `APP_SCENES` entry, `APP_THEMES` tile with
  `season`, a `<SEASON>_SCENE_CANDIDATES` list (`themeId` on the live ones).
- Wash colour in BOTH `WASH` maps (`ThemesTab.tsx`, `NdpPreviewPage.tsx`).
- CSS in `src/index.css`: a light block after the midautumn light block and a
  `html.dark[...]` block after the midautumn dark block. Keep the wash near-white
  (L 95-96%), pick a hue clear of 31/36/45, do not touch `--primary`; dark
  blocks re-set `--primary-text: 16 85% 64%` (F41). `src/test/contrastTokens.test.ts`
  picks new themes up automatically and gates AA.

## 3. Outfits (3 places must agree or it fails differently each time)
- corgi-care `api/_lib/prompt.ts`: `WEARABLE_PROMPT` (head/face/neck) or
  `HELD_PROMPT` (hand, needs `hold` + `rest` for the sleeping pose). Missing =
  `/api/look` 400 "unknown head wearable".
- corgi-care `api/look-image.ts` `BUNDLES`. Missing = naked pet, silently.
- remix: `looks.ts BUNDLE_SPECS` (`body: 'none'`, `drop: '<season>'`),
  `items.ts` (cost 0), `itemArt.ts`, `scripts/item-art/generate.mjs` SUBJECTS.
- Prompt traps: never mention the mouth (the model parks the object there);
  say where it goes ("in one front paw", "draped over the shoulders"). A
  head-covering costume must leave the face visible or every mood renders the
  same. Single held props get duplicated into both paws sometimes; say "the
  other front paw empty". New pieces get NEW ids; reusing an existing id never
  re-renders (cache key = piece list).
- Reuse a seasonal piece only if it is cost 0; the old `q*_` seasonal items cost
  coins and sit behind a quarterly window.
- Commit + push corgi-care FIRST (it is the deploy), confirm with
  `curl "https://corgi-care-tracker.vercel.app/api/look?key=biscuit.none.none.none.<neck>.happy"`
  (pending/ready, not an error).
- Item art: `node scripts/item-art/generate.mjs --only=...`. If key.py dies on
  numpy, key the cached raws:
  `uv run -q --with numpy --with pillow python scripts/item-art/key.py .art-cache/<id>.png public/items/<id>.webp`
- Warm every render (4 pets x 9 moods per bundle) or the grid shows naked pets:
  `WARM_CONCURRENCY=6 npx tsx scripts/warm-looks.mjs a,b,c,d` (tsx, not node).
  Contact-sheet 4 pets x 4 moods from `/api/look-image` and look.

## 4. Icon pack ("buttons")
- `ICON_PACKS` tile `{ id: '<season>', cost: 0, season }`.
- 9 webps in `public/icon-packs/<season>/` named by `ICON_PACK_ACTIVITIES`.
  Same prompt as `scripts/gen_icon_packs.py` with a seasonal STYLE, nano_banana_2,
  magick trim to 220x220. Do NOT run that script: it builds, commits and pushes.

## 5. Banner + chooser
- `src/components/personal-os/SeasonBanner.tsx`: add a `SEASON_BANNERS` entry
  (year-suffixed flag, 3 teasers one per pet, gradient). Point `LogActivityTab`'s
  `<SeasonBanner season=...>` at the new season; one seasonal banner at a time.
- `src/pages/SeasonPreviewPage.tsx`: add a `SEASON_PREVIEWS` entry. Public URL:
  `/season-preview/<season>` - send Leo this link.

## 6. Tests, ship, record
- `src/lib/__tests__/appScenes.test.ts`: add the new bundle ids to the drop
  test's seasonal set, plus a `<Season> wiring` block (themes free + scene file
  on disk, pieces free + art on disk, all 9 icons, closing date). Prove one bites
  (move an icon away, watch it fail).
- Full suite to a log + `npx vite build`. QA `/season-preview/<season>` at 1280
  and 390 with system Chrome: no overflow, no errors beyond `_vercel/insights` 404.
- Roadmap: entry in `src/data/roadmap.ts` (above the previous drop) and
  `docs/ROADMAP.md`.
- One commit per repo, push remix main (the push is the deploy).
- Update the kanban board and the `seasonal-drops-pipeline` memory.
