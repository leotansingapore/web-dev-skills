---
name: screenshot-to-code
description: Use when rebuilding a UI from a visual reference - a screenshot, mockup, exported Figma frame, live URL, or screen recording - into HTML/Tailwind, HTML/CSS, React, Vue, Bootstrap or Ionic code. Triggers on "screenshot to code", "image to code", "video to code", "url to code", "make a page like this", "rebuild this design", "turn this recording into a prototype".
---

# screenshot-to-code

## Overview
Open-source app (github.com/abi/screenshot-to-code, MIT) that turns a visual reference into one standalone code file per variant. It reuses the real logos and images cropped out of the screenshot (Gemini), renders its own output in headless Chromium to check it against the input, and returns 4 variants per run (2 for video) to pick from.

## Decision
Leo registered this tool on 2026-09-15 so it gets used. Pick the first row that matches:

| Situation | Do |
|---|---|
| The reference is for a screen inside an existing repo (fix, restyle, match a mockup) | Edit that repo's code natively. This tool only outputs standalone files. |
| Leo said no API spend for this job | Native build: read the image (or `/watch` the recording for frames), build, compare with Playwright. |
| Any other request to build a new page or prototype from a screenshot, mockup, Figma PNG, URL or recording | Use this tool, even for one plain HTML page. |

- Not installed yet: run Setup below. The install lives in its own folder and touches no project, so it is not a stop condition. The only thing to ask Leo for is an API key.
- It cannot run on the Max plan. This is the accepted exception to the prefer-CLI rule, which is why the cost line below is required before every run.
- Figma links: no Figma import. Ask for the frames exported as PNG.

## Inputs
| Input | Mode | Needs |
|---|---|---|
| Screenshot, mockup, Figma PNG | image | any one of ANTHROPIC / OPENAI / GEMINI key |
| Screen recording | video | GEMINI_API_KEY |
| URL | URL tab, screenshotted via ScreenshotOne | ScreenshotOne key in the app Settings dialog. Free alternative: take a full-page Playwright screenshot yourself and use image mode. |
| Text prompt | text | any LLM key |

GEMINI_API_KEY also turns on real asset extraction. REPLICATE_API_KEY (backend .env only) adds image generation and background removal.

## Cost
Each variant has a hard ceiling of GENERATION_MAX_COST_USD = 3.0 (backend/config.py): up to $12 for an image, URL or text run (4 variants), $6 for video (2), $6 for an update round (2). Before each run, tell Leo in one line: input mode, stack, variant count, ceiling. Then run it.

## Setup on this Mac
Not installed as of 2026-09-15. System python3 is 3.9 (backend needs 3.10+), poetry is missing and pnpm is broken, so use Docker:

```bash
git clone https://github.com/abi/screenshot-to-code ~/screenshot-to-code
cd ~/screenshot-to-code
printf 'ANTHROPIC_API_KEY=...\nGEMINI_API_KEY=...\n' > .env   # root .env, read by docker-compose; ask Leo for keys
open -a Docker                                                  # daemon is often down
docker compose up -d --build                                    # frontend :5173, backend :7001
```

Open http://localhost:5173. Chromium for self-checking is baked into the image.

## Driving it headless
WebSocket `ws://127.0.0.1:7001/generate-code`. Send one JSON message (shape of `CodeGenerationParams` in frontend/src/types.ts):

```json
{"generationType":"create","inputMode":"image","generatedCodeConfig":"html_tailwind",
 "prompt":{"text":"","images":["data:image/png;base64,..."]},
 "isAssetExtractionEnabled":true,"isImageGenerationEnabled":true}
```

Stacks: html_tailwind, html_css, react_tailwind, bootstrap, vue_tailwind, ionic_tailwind. Keys omitted from the message come from .env. Replies are `{type, value, variantIndex}`: `setCode` holds a variant's finished code, then `variantComplete` or `variantError`. Close code 1000 means done; any other code is a failure with the reason on the close. Not yet run from this machine, so check against frontend/src/generateCode.ts on first use.

## After generation
The output is a starting point. Port the chosen variant into the target project's stack, replace every line of copy lifted from the reference (the Copywriting pipeline in CLAUDE.md applies), then run the usual UX, dark mode and 390px checks. Never ship a pixel clone of a third-party site.

## Common mistakes
| Mistake | Fix |
|---|---|
| Opening 127.0.0.1:5173 | Vite binds localhost only. Use http://localhost:5173. |
| Editing .env with containers running | `docker compose up -d --force-recreate` |
| Putting the ScreenshotOne key in .env | It is read from the Settings dialog only |
| Putting REPLICATE_API_KEY in Settings | It is read from backend .env only |
| Using it to tweak an existing app screen | Do that natively |
