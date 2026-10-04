#!/usr/bin/env node
// Hemingway check: flags long sentences, passive voice and jargon in the
// words a visitor reads. It reports; a person decides. Run it on every copy
// change before it ships (see the Hemingway rule in this repo's CLAUDE.md).
//
//   node scripts/hemingway.mjs                 # the built site (dist/ or index.html)
//   node scripts/hemingway.mjs page.html a.md  # just these files
//
// Leave a flag only with a reason: a quote of someone else, another
// project's rule, a dated note in the author's own words, or a passive
// where who did it doesn't matter ("Nothing is deleted").
import fs from "node:fs";
import path from "node:path";

const LONG = 25;
const PASSIVE =
  /\b(is|are|was|were|be|been|being|get|gets|got)\s+(\w+ly\s+)?(\w+ed|\w+en|made|built|left|kept|run|done|set|put|held|shown|known|taken|given|seen|sent|found|told|brought|written|chosen)\b/i;
const JARGON = [
  "leverage", "ecosystem", "stakeholder", "synergy", "scalable", "alignment",
  "robust", "seamless", "empower", "unlock", "framework", "holistic",
  "optimi[sz]e", "solution", "deliverable", "actionable", "journey",
  "landscape", "enable", "facilitat", "utili[sz]", "best practice",
  "bandwidth", "touchpoint", "cutting-edge", "innovative", "revolutioni[sz]",
  "harness", "delve", "elevate", "value creation", "-as-a-",
];
const jargonRe = new RegExp(`(${JARGON.join("|")})`, "i");

const args = process.argv.slice(2);
const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e =>
  e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
let files = args.length ? args
  : fs.existsSync("dist") ? walk("dist").filter(f => f.endsWith(".html"))
  : ["index.html"];

const textOf = (src, file) => {
  if (file.endsWith(".md")) src = src.replace(/^---[\s\S]*?---/, "").replace(/<[^>]+>/g, " ");
  const main = src.match(/<main[\s\S]*?<\/main>/i);
  if (main) src = main[0];
  return src
    .replace(/<(script|style|svg|noscript|template)[\s\S]*?<\/\1>/gi, " ")
    .replace(/<\/(p|li|h\d|dd|dt|td|th|figcaption|summary|blockquote|div|label|legend)>/gi, "\n")
    .replace(/<[^>]+>/g, " ")
    .replace(/&rsquo;|&#8217;/g, "’").replace(/&amp;/g, "&").replace(/&nbsp;|&#160;/g, " ")
    .replace(/&[a-z]+;/g, " ");
};

let total = 0;
for (const file of files) {
  const lines = textOf(fs.readFileSync(file, "utf8"), file).split("\n")
    .map(l => l.replace(/\s+/g, " ").trim()).filter(l => l.split(" ").length >= 5);
  const seen = new Set(), out = [];
  for (const line of lines) for (const s of line.split(/(?<=[.!?])\s+/)) {
    if (seen.has(s)) continue; seen.add(s);
    const flags = [], words = s.split(" ").length;
    if (words > LONG) flags.push(`long ${words}`);
    if (PASSIVE.test(s)) flags.push("passive?");
    const j = s.match(jargonRe); if (j) flags.push(`jargon: ${j[0]}`);
    if (flags.length) out.push(`  [${flags.join(", ")}] ${s.slice(0, 220)}`);
  }
  if (out.length) { console.log(`\n${file}`); console.log(out.join("\n")); total += out.length; }
}
console.log(`\n${total} sentence(s) flagged.`);
