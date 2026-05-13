import { getCollection, type CollectionEntry } from 'astro:content';

export async function getSortedNotes(): Promise<CollectionEntry<'notes'>[]> {
  const all = await getCollection('notes', ({ data }) => data.published);
  return all.sort((a, b) => a.data.num.localeCompare(b.data.num));
}

export async function getSortedProgress(): Promise<CollectionEntry<'progress'>[]> {
  const all = await getCollection('progress', ({ data }) => data.published);
  return all.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

export async function getNoteSiblings(currentNum: string) {
  const sorted = await getSortedNotes();
  const idx = sorted.findIndex((n) => n.data.num === currentNum);
  return {
    prev: idx > 0 ? sorted[idx - 1] : null,
    next: idx >= 0 && idx < sorted.length - 1 ? sorted[idx + 1] : null,
  };
}

export async function getProgressSiblings(currentSlug: string) {
  const sorted = await getSortedProgress();
  const idx = sorted.findIndex((p) => p.id === currentSlug);
  return {
    prev: idx >= 0 && idx < sorted.length - 1 ? sorted[idx + 1] : null,
    next: idx > 0 ? sorted[idx - 1] : null,
  };
}
