# web-dev-skills

Claude Code skills for building and improving Leo's websites: competitor research, gap analysis against other codebases, feature page rebuilds and site-wide page builds. They run in Claude Code as slash commands, for example `/competitor-intel` or `/revamp-page crm`.

## Install

```bash
git clone https://github.com/leotansingapore/web-dev-skills.git
cd web-dev-skills
mkdir -p ~/.claude/skills ~/.local/bin
cp -R skills/* ~/.claude/skills/
cp bin/* ~/.local/bin/
```

Restart Claude Code and the skills appear in the `/` menu. Make sure `~/.local/bin` is on your PATH.

## Skills

| Skill | Use it to |
|---|---|
| `competitor-intel` | Scrape every competitor page for one site: page anatomy, socials, a scored copy bank, keyword research and a build plan, written to an Obsidian folder. |
| `repo-gap-buildout` | Compare one of our products to a GitHub repo, rank the gaps with Jev, then port the top gaps one commit at a time. |
| `revamp-page` | Rebuild one activity-tracker.io `/features` page with the feature page playbook. |
| `sb-revamp-page` | The same for searchblueprint.io `/features` pages. |
| `competitor-site-buildout` | Rebuild a whole marketing site from competitor research: revamp every page, build the missing ones, fix nav, footer and sitemap. It calls the page skills above per page. |
| `feature-page-builder` | Build feature pages as a typed registry with one template and a gate test. |
| `academy-builder` | Build a public learning hub (tracks, chapters, lessons) that a fact gate keeps honest. |
| `seasonal-drop` | Ship a festival drop on activity-tracker.io: themes, pet outfits, an icon pack and the banner. |
| `screenshot-to-code` | Turn a screenshot, mockup, URL or screen recording into code with abi/screenshot-to-code. |
| `eval-gate` | Score your work against the quality rubrics before you hand it over. |
| `anti-ai-writing` | The writing rules all copy follows. `aicheck` reads its banned-patterns list. |
| `humanize` | Fix copy that reads like AI wrote it. Adapted from [MADEVAL/HumanAI](https://github.com/MADEVAL/HumanAI) (MIT, license in the folder). |

## Command-line helpers

| Command | What it does |
|---|---|
| `aicheck <file>` | Scores a draft for AI-writing patterns. Under 15 ships. |
| `brief-check <draft.md>` | Flags words the repo's `.agents/product-marketing.md` says to avoid. |
| `hook-check <spec.json>` | Jev scores each headline out of 10 as the reader would see it. |

## Keys and access

Put keys in your shell profile. Never commit them.

| Key | Used by | Cost |
|---|---|---|
| `TYPESAFE_API_KEY` | Jev (TypeSafe): competitor-intel, repo-gap-buildout, hook-check, aicheck | about $0.04 per million input tokens |
| `BROWSER_USE_API_KEY` | Browser Use Cloud walkthroughs in the page skills | about $0.11 a run |
| `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | competitor-intel keyword volumes, read from the file `dataforseo_env` names in its config.json | about $0.09 per 1,000 phrases |
| Higgsfield CLI login | seasonal-drop artwork | credits |

The skills expect the repos they work on at fixed paths. Ask Leo for access, then clone `remix-of-activity-tracker` to `~/remix-of-activity-tracker` and `seo-audit-tool` to `~/Documents/seo-audit-tool`.

## Not in this repo

- Leo's global `CLAUDE.md`. Several skills point to its copywriting pipeline and to its rule that decisions go to Jev. The copywriting pipeline is in `docs/copy-pipeline.md`; ask Leo for the rest.
- `copy-corpus` and `saas-copy`, which the copy pipeline also reads. They hold copy quoted word for word from other companies' websites, so they stay private.
- Memory notes. When a skill says to read a memory file, ask Leo instead.

Where a skill says "stop for Leo" or "ask Leo", that call is his, not yours.

## License

MIT, see `LICENSE`. `skills/humanize` keeps its own MIT license from MADEVAL/HumanAI.
