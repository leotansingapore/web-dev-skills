// Full-page reference screenshots of babylovegrowth.ai academy pages.
// Usage: node capture.mjs <outDir>
import { chromium } from "playwright-core";
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.argv[2] || "./shots";
mkdirSync(outDir, { recursive: true });

const PAGES = [
  { slug: "academy", url: "https://www.babylovegrowth.ai/en/academy" },
  { slug: "shopify-academy", url: "https://www.babylovegrowth.ai/en/shopify-academy" },
  { slug: "local-seo-academy", url: "https://www.babylovegrowth.ai/en/local-seo-academy" },
];
const VIEWPORTS = [
  { name: "desktop", width: 1440, height: 900 },
  { name: "mobile", width: 390, height: 844, isMobile: true, deviceScaleFactor: 2 },
];

const browser = await chromium.launch({ channel: "chrome", headless: true });
const manifest = [];
for (const page of PAGES) {
  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({
      viewport: { width: vp.width, height: vp.height },
      isMobile: !!vp.isMobile,
      deviceScaleFactor: vp.deviceScaleFactor || 1,
      userAgent: vp.isMobile
        ? "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        : undefined,
    });
    const p = await ctx.newPage();
    const errors = [];
    p.on("pageerror", (e) => errors.push(String(e)));
    await p.goto(page.url, { waitUntil: "networkidle", timeout: 60000 });
    // scroll through to trigger lazy content, then back to top
    const h = await p.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < h; y += 800) {
      await p.evaluate((yy) => window.scrollTo(0, yy), y);
      await p.waitForTimeout(120);
    }
    await p.evaluate(() => window.scrollTo(0, 0));
    await p.waitForTimeout(500);
    const file = `${page.slug}--${vp.name}.png`;
    await p.screenshot({ path: join(outDir, file), fullPage: true });
    const title = await p.title();
    const height = await p.evaluate(() => document.body.scrollHeight);
    // first lesson link per academy, captured once (desktop only)
    let firstLesson = null;
    if (vp.name === "desktop") {
      firstLesson = await p.evaluate(() => {
        const a = [...document.querySelectorAll("a[href*='academy/']")].find((x) => /academy\/[a-z0-9-]+$/.test(x.getAttribute("href") || ""));
        return a ? new URL(a.getAttribute("href"), location.href).href : null;
      });
    }
    manifest.push({ slug: page.slug, viewport: vp.name, url: page.url, file, title, pageHeightPx: height, firstLesson, pageErrors: errors });
    await ctx.close();
  }
}
// one lesson page per academy, desktop, for structure reference
for (const m of manifest.filter((m) => m.viewport === "desktop" && m.firstLesson)) {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const p = await ctx.newPage();
  await p.goto(m.firstLesson, { waitUntil: "networkidle", timeout: 60000 });
  await p.waitForTimeout(500);
  const file = `${m.slug}--lesson-example--desktop.png`;
  await p.screenshot({ path: join(outDir, file), fullPage: true });
  manifest.push({ slug: m.slug, viewport: "desktop", url: m.firstLesson, file, title: await p.title(), kind: "lesson-example" });
  await ctx.close();
}
await browser.close();
writeFileSync(join(outDir, "manifest.json"), JSON.stringify({ capturedAt: new Date().toISOString(), shots: manifest }, null, 2));
console.log(JSON.stringify(manifest.map((m) => ({ file: m.file, title: m.title, h: m.pageHeightPx, err: (m.pageErrors || []).length })), null, 1));
