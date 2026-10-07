# Traps and fixes from the ActivityTracker run

## Decisions and scope

- Most planned pages shouldn't ship. Zero-demand items, pages whose page one serves another reader, and pages a live page already answers fold or park. Report the counts; the owner can reverse a park.
- A bare "ok" is not a go (memory `leo-ok-is-not-go.md`). "Go", "do all", "sure go ahead" are.
- Offer calls as a pick list with your recommendation first; batch them on the decisions page.
- Some calls stay the owner's even when going autonomously: money (the affiliate page promised 40% while payouts computed 30%), facts only they have (meeting length, company number, grant eligibility), legal readings, switching the homepage.
- One audience per page never becomes the whole site: hubs that led with advisor-only pages read as an insurance site; regroup by audience, general first.
- Naming rules bind every page and shared component (ActivityTracker: never "insurance agents", "district", "consultant" for advisors on visible copy; general pages carry no insurance words; guard tests enforce it, and the shared footer is read by page tests, so keep specialised words out of shared components).
- Some things are never public (ActivityTracker: the income projection). Put them in the memory and every brief.

## Truth

- Old pages overclaim. Every revamp found claims the code didn't back (privacy promises, "live" boards that were cached, features that didn't exist). Check against code, cut silently, log real bugs to the kanban.
- A same-day bug fix can make an approved line false (a funnel FAQ said "last 30 days" hours after periods became calendar months). Re-check copy against code right before shipping.
- Copying a competitor into the product is a trap too: 77 of the app's project templates mirrored Todoist's gallery row for row, and Todoist's terms forbid reproducing their service. They were kept off the site until rewritten in the product's own words (similarity-checked against the old copies).
- Platform risk must be disclosed where the product's approach carries it (ActivityTracker links WhatsApp as a device, not via the official Business Platform; WhatsApp's own help page warns unofficial linking may put an account at risk; every WhatsApp page now quotes it, guarded by a test).
- Government and regulator sites often restrict deep links: name and date instead of linking.

## Engineering

- Work in a git worktree per job off origin/main; never the main clone (other sessions use it). Copy node_modules with `cp -Rc`; install a missing dep with `--no-save`.
- Parallel page branches all touch the same list files. On rebase: generated JSON locks, merge both sides' keys (`scripts/merge-json-lock.py`); route and hub arrays, keep both sides (`scripts/merge-keep-both.py`); arrays of route objects, close the first object before the second (`scripts/merge-route-objects.py`); then de-duplicate, type-check and run the page tests.
- The route test on ActivityTracker forbids two routes sharing one OG image and art named `app-*`: generate one card per page.
- A shared SEO hook truncated every title at 60 characters and description at 155 on the client, so Google saw ~150 titles cut mid-word. Check what the rendered head says, not just the prerendered HTML.
- A sticky header that didn't stick: a CSS scoping bug; fixed with a class on html instead of :has().
- The test suite rewrites a fixtures file on some repos (`scripts/qa/fixtures/guides.json`): restore it before committing.
- Suites go red under load on untouched files; rerun alone before blaming your change.
- Subagents die on network drops (ENOTFOUND) and session ends. Resume with SendMessage; check the worktree and origin/main first to see what landed.
- zsh doesn't word-split variables in `for x in $list`; loops that pass sizes to scripts must run under `/bin/bash -c`.
- A live-check loop that matches a generic word ("for") in the title passes on the homepage. Match the exact new title.
- Browser Use test browsers block the clipboard; a locator matching /^Copy/ jumps to another button once the label says "Copied".

## Reporting

- Report what's live with URLs, what was folded/parked, what you decided for the owner, and the one thing they must decide. Don't bury money or legal risks in a list: lead with them.
- Update the kanban and memory after each phase, not at the end.
