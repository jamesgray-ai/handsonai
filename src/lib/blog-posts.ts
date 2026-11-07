import { getCollection, type CollectionEntry } from 'astro:content';

export type BlogPost = CollectionEntry<'docs'>;

/* The "New" badge marks genuinely recent posts. Two conditions, and both are load
   bearing, because this blog publishes in bursts and then goes quiet:

   - Within NEW_WINDOW_DAYS. Without a window the top entry wears the badge forever;
     gaps here have run to 71 days, so "newest" and "new" are not the same claim, and
     a permanently lit badge stops being read.
   - Among the NEW_MAX_BADGES most recent. Without a cap, a burst floods the page —
     16 Feb 2026 alone had three posts, and a wider window would have badged roughly
     fifteen at once, which is no signal at all.

   Deliberately NOT "index 0 only": same-day posts are equally new, and badging one of
   three identical-dated entries is just wrong. Outside the window nothing renders,
   which is the honest result — the remedy for a missing badge is publishing. */
const NEW_WINDOW_DAYS = 14;
const NEW_MAX_BADGES = 3;

/** Blog posts, newest first, plus the ids that earn the "New" badge. */
export async function getBlogPosts(): Promise<{ posts: BlogPost[]; newIds: Set<string> }> {
  const docs = await getCollection('docs');
  const posts = docs
    .filter((entry) => entry.id.startsWith('blog/') && entry.id !== 'blog/' && entry.data.date)
    .sort((a, b) => new Date(b.data.date!).getTime() - new Date(a.data.date!).getTime());

  const newCutoff = Date.now() - NEW_WINDOW_DAYS * 86_400_000;
  const newIds = new Set(
    posts
      .slice(0, NEW_MAX_BADGES)
      .filter((p) => new Date(p.data.date!).getTime() >= newCutoff)
      .map((p) => p.id)
  );

  return { posts, newIds };
}

/** "Plugin 9.3.1: your graph links to your systems" → "Your graph links to your systems".
    Version numbers matter on the post itself, not to someone scanning the homepage. */
export function plainTitle(title: string): string {
  const stripped = title.replace(/^Plugin\s+[\d.]+:\s*/i, '');
  return stripped.charAt(0).toUpperCase() + stripped.slice(1);
}
