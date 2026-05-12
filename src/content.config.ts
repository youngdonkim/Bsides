import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const notes = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/notes' }),
  schema: z.object({
    num: z.string().regex(/^\d{2}$/),
    en: z.string(),
    ko: z.string(),
    group: z.enum(['discover-plan', 'design-architect', 'build-ship']),
    read_time: z.string(),
    h1_lead: z.string(),
    lead: z.string().max(180),
    italic: z.string(),
    workshop_text: z.string(),
    published: z.boolean().default(true),
  }),
});

const progress = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/progress' }),
  schema: z.object({
    round: z.number().int().positive(),
    date: z.coerce.date(),
    member: z.string(),
    title: z.string().max(80),
    lead: z.string().max(150),
    mentor: z.string().optional(),
    cover: z
      .object({
        image: z.string().optional(),
        gradient: z.enum(['olive', 'sand', 'pink']).optional(),
      })
      .nullable()
      .optional(),
    published: z.boolean().default(true),
  }),
});

export const collections = { notes, progress };
