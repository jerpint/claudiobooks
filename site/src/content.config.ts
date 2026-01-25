import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const audiobooks = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/audiobooks" }),
  schema: z.object({
    title: z.string(),
    author: z.string(),
    publishedYear: z.number().optional(),
    narrator: z.string().default("AI (OpenAI TTS)"),
    duration: z.string(), // e.g., "15 minutes"
    audioFile: z.string(), // path relative to /audio/
    coverImage: z.string().optional(),
    gutenbergId: z.number().optional(),
    description: z.string(),
    dateAdded: z.date(),
    tags: z.array(z.string()).default([]),
  }),
});

export const collections = { audiobooks };
