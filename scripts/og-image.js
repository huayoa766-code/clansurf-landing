// Renders scripts/og-image.html to og-image.png at 1200x630.
// Needs Playwright: npx playwright install chromium
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('file://' + path.join(__dirname, 'og-image.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(__dirname, '..', 'og-image.png') });
  await b.close();
})();
