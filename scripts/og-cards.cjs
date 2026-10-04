// Renders a 1200x630 social card for every page into public/og/, in the
// site's Swiss style (4 Oct 2026): heavy rule under the header, light
// Archivo headline, the pixel art as the image in its own cell.
// The art is read from the pages pixel.py writes, so it never drifts.
//   CHROMIUM=<path to chrome> node scripts/og-cards.cjs
// Needs playwright-core (npm i --no-save playwright-core).
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const read = f => fs.readFileSync(path.join(root, f), 'utf8');
const block = (html, name) => {
  const m = html.match(new RegExp(`<!--px:${name}-->([\\s\\S]*?)<!--/px:${name}-->`));
  if (!m) throw new Error(`px:${name} not found`);
  return m[1];
};

const home = read('public/index.html');
const css = block(home, 'css');
const hero = block(home, 'hero').replace('preserveAspectRatio="xMidYMax meet"', 'preserveAspectRatio="xMidYMax slice"');
const logo = read('public/logo.svg');

// Docs cards come from each page's own frontmatter.
const docs = fs.readdirSync(path.join(root, 'src/content/docs'))
  .filter(f => f.endsWith('.md'))
  .map(f => {
    const fm = read(`src/content/docs/${f}`).match(/^---\n([\s\S]*?)\n---/)[1];
    const get = k => (fm.match(new RegExp(`^${k}:\\s*(.*)$`, 'm')) || [])[1];
    return { slug: `docs-${f.replace(/\.md$/, '')}`, label: 'Docs', title: get('title') };
  });

const cards = [
  { slug: 'home', label: 'Beta: the first 25 nodes', title: 'Where people and local tech meet <em>everyday human needs.</em>' },
  { slug: 'street', label: 'Use case: one street', title: 'Your street already has what you need. <em>A node makes it findable, offline.</em>' },
  { slug: 'join', label: 'Makers, supporters, maintainers', title: 'Help start one of the first <em class="g">25</em> nodes.' },
  ...docs,
];

const page = c => `<!DOCTYPE html><html lang="en" data-theme="light"><head><meta charset="UTF-8">
<link rel="stylesheet" href="../public/fonts.css">
${css}
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1200px;height:630px;overflow:hidden}
body{background:#f5f6f7;color:#1a1c21;font-family:'Noto Sans',sans-serif;display:grid;grid-template-rows:auto 1fr}
.top{display:flex;justify-content:space-between;align-items:center;padding:30px 56px 26px;border-bottom:4px solid #1a1c21}
.brand{display:flex;align-items:center;gap:12px;font-weight:700;font-size:30px;letter-spacing:-0.01em;color:#45507f}
.brand svg{width:46px;height:46px}
.url,.label{font-family:Archivo;font-stretch:125%;font-weight:600;font-size:16px;letter-spacing:0.1em;text-transform:uppercase}
.url{color:#3a3e46}
.main{display:grid;grid-template-columns:640px 1fr}
.text{padding:44px 40px 48px 56px;display:flex;flex-direction:column}
.label{color:#2f7a4d}
h1{margin-top:auto;font-family:Archivo;font-weight:380;font-stretch:100%;font-size:74px;line-height:1;letter-spacing:-0.03em;text-wrap:balance}
h1 em{font-style:normal;color:#45507f}
h1 em.g{color:#2f7a4d}
.art{border-left:1px solid #1a1c21;overflow:hidden;position:relative}
.art svg{position:absolute;inset:0;width:100%;height:100%;display:block}
.px-t{font-family:Archivo;font-weight:750;font-stretch:75%;font-size:3.7px;letter-spacing:0.02em;fill:#4a2f1c}
</style></head><body>
<div class="top"><span class="brand">${logo}<span>Clansurf</span></span><span class="url">clansurf.com</span></div>
<div class="main">
<div class="text"><p class="label">${c.label}</p><h1>${c.title}</h1></div>
<div class="art">${hero}</div>
</div></body></html>`;

(async () => {
  const out = path.join(root, 'public/og');
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM });
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  // Rendered from a file beside this script, so fonts.css resolves its
  // relative font paths.
  const tmp = path.join(__dirname, '.og-card.html');
  for (const c of cards) {
    fs.writeFileSync(tmp, page(c));
    await p.goto('file://' + tmp, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(out, `${c.slug}.png`) });
    console.log(`public/og/${c.slug}.png`);
  }
  fs.unlinkSync(tmp);
  await b.close();
})();
