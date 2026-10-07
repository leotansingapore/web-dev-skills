---
name: feature-page-builder
description: Use when asked to build or extend product feature landing pages — a /features section, "product pages like <competitor>", marketing pages for capabilities, or a shared marketing nav across public pages. Triggers include "build feature pages", "clone their product pages but better", "one landing page per feature", "add a page for <capability>", or a request to screenshot a competitor's product nav and out-build it.
---

# Feature page builder

> **activity-tracker.io is different.** For its /features/* pages follow
> `docs/FEATURE-PAGE-PLAYBOOK.md` in remix-of-activity-tracker, not this skill: those pages
> are bespoke with working demos, their copy is human-simple marketing copy that Leo reads
> before it is ported (not premium-minimal, not a claim-per-doc registry), and they carry
> a GIF and Biscuit. This skill remains the process for SearchBlueprint-style registry sites.

## Overview

A feature page sells one real capability: hero claim, the reader's problem, documented capabilities, how-it-works, a free way to try the job, lessons that teach the subject, verdict-first FAQs, related features. This skill is the process that shipped SearchBlueprint's /features (13 pages + a shared marketing nav, SB-929, 2026-08-23): content as a **typed registry** rendered by **one template**, held honest by a **gate test**. Sibling process: the academy-builder skill (same capture/gate discipline for curricula).

## The process

1. **Capture the competitor.** Their product-nav URLs come from the RENDERED nav (playwright-core + system Chrome; raw HTML and sitemaps often lack them). Full-page desktop + sampled mobile + defuddle text extracts, archived in the repo (`public/reference/feature-pages/<competitor>/` with manifest.json noting which of their pages you will skip and why).
2. **Inventory YOUR capabilities from the product's own docs**, not from the competitor's list. Map their pages to yours; **skip theirs where your feature is parked/gated** (record the skip in the manifest); **add pages they lack** where you have documented strengths.
3. **Model content as data.** One `FeaturePage` type (hero, problem, capabilities[{title, body, helpHref}], how[], tools[], lessons[], faq[], related[], ctaLabel); one file per page in `src/lib/feature-content/<slug>.ts`; a registry that imports them; ONE route template renders all. Adding a page = one file + one import.
4. **Write the gate before the content.** Every `helpHref` exists on disk; tool/lesson/related links resolve against their registries; meta lengths; banned hype vocabulary; **a banned-claims list for parked/gated capability** ("trusted by", per-assistant tracking, unbuilt white-label). The gate runs in `npm test`.
5. **Gold page first, then fan out.** Write one page yourself grounded in real doc reads; 3-4 subagents write ~3 pages each, every one required to READ the help page before citing it and to report claims they dropped for lack of documentation. That dropped-claims list is the honesty audit.
6. **One shared marketing nav.** Product dropdown fed by the registry, mobile drawer, applied to every public page that hand-rolls a header — except generated pages (a build-artifact homepage changes through its generator only). Removing old headers orphans icon imports: lint the touched files, and verify an "unused" import isn't used further down before deleting it.
7. **e2e at 390px and desktop**, against a production build AND against production: 200s, no console errors, no overflow, JSON-LD parses, internal links resolve, nav renders with working drawer and dropdown. Production-only traps already paid for: `networkidle` never fires under a chat widget's long-polling (use `load` + settle), and an apex link that 301s to a docs subdomain makes Next's prefetch fire a cross-origin RSC fetch the CSP blocks — link the docs origin directly with a plain anchor.
8. **Ship by the host repo's rules** (rebase, build green on the rebased tree, push, verify in production, record on the board). Sitemap (undated evergreen entries), public allowlist, assistant page-guide, footer links from the registry.

## Load-bearing rules

1. **Registry, template, gate — never bespoke pages.** Consistency is what makes 13 pages maintainable and testable.
2. **Every claim cites the doc that documents it**, and the citation is a rendered link. No doc, no claim; parked or gated capability never appears as live.
3. **No proof theater.** No invented counts, testimonials, ratings or "trusted by" — if real proof isn't in the docs, the page has no proof section.
4. **Their page list is a menu, not a spec.** Skip what you can't honestly sell (record why), fold overlapping queries into your strongest page, add the pages your documented strengths deserve.
5. **Free tool in the hero.** "Try free: <tool>" beside the signup CTA converts the skeptic the CTA loses.
6. **Voice compose**: premium-minimal voice + technical-clarity framing + seo-landing-pages structure (the saas-* skills); sentence case, no em dashes, no exclamation marks, verdict-first FAQs.
7. **Writers report dropped claims.** The list of what a page does NOT say is reviewed like the page itself.

## Common mistakes

- Citing a help page from memory: the gate catches the missing file, but only reading catches a doc that says "parked" or "gated".
- FAQPage JSON-LD sold as a rich result — it's valid schema with retrieval value only (FAQ rich results are retired).
- Letting the competitor's stronger claims pull invented capability into your copy — the dropped-claims report is where that pressure goes.
- Verifying only locally: both production-only failures this build found (CSP prefetch, networkidle hang) were invisible on localhost.
