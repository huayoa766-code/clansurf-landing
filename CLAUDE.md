# clansurf-landing

clansurf.com. The home page and use cases are plain HTML in `public/`;
the docs are Markdown in `src/content/docs/`, built by Astro.
Fonts are served from the site (`public/fonts.css`): Archivo for headings
and labels, Noto Sans for body text (since 4 Oct 2026, wide
language coverage for a worldwide audience). Inter is banned.

## Every copy change: the Hemingway check

**Every copy change passes a Hemingway check before it ships (4 Oct 2026).**
Joshua's rule for all three sites: joshuapoddoku.com, clansurf.com and
huyoworld.com.

- **Short sentences, one idea each.** Over about 25 words, split it.
- **Active voice.** Say who does it. Passive only when the doer doesn't
  matter ("Nothing is deleted").
- **Plain words.** No corporate jargon: leverage, ecosystem, stakeholder,
  framework, solution, enable, empower, unlock, seamless, journey,
  "X-as-a-Y" and the like.
- **Concrete over abstract.** Name the thing, the person, the number.
- **Cut filler** and adverbs that add nothing.

Run `node scripts/hemingway.mjs` after building. It flags long sentences,
likely passives and jargon. Fix each flag or leave it for a stated reason:
a quote of someone else, another project's rule, a dated note in Joshua's
own words, or a headline he chose.

Checks:

```
npm run build
node scripts/hemingway.mjs   # fix or justify each flag
```

## Every design change: Impeccable

**Every design change passes Impeccable's checker (4 Oct 2026).** Run it on
the built pages, served locally, at desktop and phone width:

```
IMPECCABLE_BROWSER=<path to Chromium> npx impeccable@4.1.0 detect --viewport 1280x800 <urls>
IMPECCABLE_BROWSER=<path to Chromium> npx impeccable@4.1.0 detect --viewport 390x844 <urls>
```

Our rules win where they clash. `.impeccable/config.json` switches off four
rules for that reason: shape-assembled-illustration (the pixel art and
diagrams are drawn that way on purpose), oversized-h1 (big headlines are the
brief), kicker-above-heading (small labels hang in the margin) and
numbered-section-labels. Fix every other finding or give the reason. Known
false alarms in 4.1.0: line-length (it measures the box, not the rendered
lines; check the rendered lines instead) and tight-leading on display
headings.

## What the copy must keep (decided 3 to 4 Oct 2026)

- Clansurf helps a community run itself as a node. A node is a group of
  people who help each other and make their own rules.
- Clansurf is an enabler. Money is never mentioned, not even to deny it.
  Rewards may come later, so make no "never" promises about them.
- Contributors, not volunteers. Open worldwide; never name target regions.
- Joining: one maker, one supporter and one maintainer say yes, then the
  node's members vote.
- Clansurf helps a node start, then steps back. Nodes write their own rules.
- The site doesn't name Joshua. HuyoWorld is "researching Clansurf".
- No radios, hardware, blockchain, DAO or tokens on /join.
- Commit as 285669027+huayoa766-code@users.noreply.github.com, or Vercel
  blocks the deploy.
