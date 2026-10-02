import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import { glob } from "astro/loaders";

const docs = defineCollection({
  loader: glob({ pattern: "**/[^_]*.md", base: "./src/content/docs" }),
  schema: z.object({
    title: z.string(),
    nav: z.string(),
    description: z.string().max(160),
    order: z.number(),
    updated: z.coerce.date(),
  }),
});

export const collections = { docs };
