// Renders the two social cards at 1200x630:
//   scripts/og-image.html -> public/og-image.png (the street use case)
//   scripts/og-home.html  -> public/og-home.png  (the home page)
// Needs Playwright: npx playwright install chromium
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  for (const [html, png] of [['og-image.html', 'og-image.png'], ['og-home.html', 'og-home.png']]) {
    await p.goto('file://' + path.join(__dirname, html), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(__dirname, '..', 'public', png) });
  }
  await b.close();
})();
