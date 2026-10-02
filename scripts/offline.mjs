// Makes a build open from a plain folder: a USB stick, a node's own device, a
// laptop on a local mesh, no web server and no internet. Links that start with
// "/" become relative, and links to a folder point at its index.html.
// Usage: node scripts/offline.mjs <build folder>
import { readdirSync, readFileSync, writeFileSync, statSync, existsSync } from "node:fs";
import { join, relative, dirname, posix } from "node:path";

const root = process.argv[2];
if (!root || !existsSync(root)) throw new Error("usage: node scripts/offline.mjs <build folder>");

const pages = [];
const walk = dir => {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) walk(p);
    else if (name.endsWith(".html")) pages.push(p);
  }
};
walk(root);

for (const page of pages) {
  const up = relative(dirname(page), root).split("\\").join("/") || ".";
  const html = readFileSync(page, "utf8").replace(
    /(\s(?:href|src)=")\/(?!\/)([^"#?]*)([^"]*)"/g,
    (_, attr, path, rest) => {
      let target = path;
      const onDisk = join(root, path);
      if (path === "" || path.endsWith("/") || (existsSync(onDisk) && statSync(onDisk).isDirectory())) {
        target = posix.join(path, "index.html");
      }
      return `${attr}${up}/${target}${rest}"`;
    },
  );
  // relative links to a folder, such as the home page's "docs/"
  const fixed = html.replace(/(\s(?:href|src)=")(?![a-z]+:|\/|#|\.\.?\/index\.html)([^"#?]+\/)([#?][^"]*)?"/g,
    (_, attr, path, rest = "") => `${attr}${path}index.html${rest}"`);
  writeFileSync(page, fixed);
}
console.log(`offline: ${pages.length} pages rewritten in ${root}`);
