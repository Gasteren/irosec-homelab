import { getCollection, type CollectionEntry } from 'astro:content';

/** The writeup sections (the addons page has its own live count). */
export const DOC_SECTIONS = ['infrastructure', 'security-stack', 'projects', 'lessons-learned'] as const;

/** URL slug of a docs entry, e.g. "security-stack/siem"; section index pages map to "security-stack". */
export function slugOf(entry: CollectionEntry<'docs'>): string {
  const raw = ('slug' in entry && typeof entry.slug === 'string' ? entry.slug : entry.id) as string;
  return raw.replace(/\.mdx?$/, '').replace(/(^|\/)index$/, '');
}

/** Number of writeups (excluding section index pages) per section. */
export async function writeupCounts(): Promise<Map<string, number>> {
  const counts = new Map<string, number>();
  for (const entry of await getCollection('docs')) {
    const [section, page] = slugOf(entry).split('/');
    if (page && (DOC_SECTIONS as readonly string[]).includes(section)) {
      counts.set(section, (counts.get(section) ?? 0) + 1);
    }
  }
  return counts;
}
