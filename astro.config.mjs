// @ts-check
import { defineConfig } from "astro/config";

// The home page is public/index.html, kept as plain HTML so pixel.py can keep
// writing into it. Astro builds the docs around it.
export default defineConfig({
  site: "https://www.clansurf.com",
  trailingSlash: "always",
  build: { format: "directory", inlineStylesheets: "always" },
  devToolbar: { enabled: false },
});
