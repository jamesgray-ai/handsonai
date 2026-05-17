import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';
import { blogSchema } from 'starlight-blog/schema';
import { z } from 'astro/zod';

export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema({
      extend: (context) => blogSchema(context).extend({
        schema_type: z.enum(['Course', 'HowTo', 'TechArticle']).optional(),
        question: z.string().optional(),
        short_answer: z.string().optional(),
        author: z.string().optional(),
        categories: z.array(z.string()).optional(),
        course_provider: z.string().optional(),
        course_url: z.string().optional(),
        course_mode: z.string().optional(),
        course_language: z.string().optional(),
        course_duration: z.string().optional(),
        howto_steps: z.array(z.object({
          name: z.string(),
          text: z.string(),
          url: z.string().optional(),
        })).optional(),
        // Use case library fields
        jtbd: z.string().optional(),
        primitives: z.array(z.enum([
          'content-creation',
          'research',
          'coding',
          'data-analysis',
          'ideation-and-strategy',
          'automation',
        ])).optional(),
        building_blocks: z.array(z.string()).optional(),
        status: z.enum(['draft', 'published']).optional(),
        published: z.date().optional(),
        last_updated: z.date().optional(),
        maven_video_url: z.string().optional(),
        maven_course: z.string().optional(),
      }),
    }),
  }),
};
