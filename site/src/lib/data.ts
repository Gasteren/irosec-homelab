// Build-time snapshot of the live data. scripts/sync-content.mjs copies these
// from data/ at the repo root; on the page, scripts/live-data.ts replaces the
// values with the latest copies served at /api/*.json.
import stats from '../data/addon-stats.json';
import activity from '../data/recent-activity.json';

export { stats, activity };

export function downloadsFor(slug: string): number | undefined {
  return stats.addons.find((addon) => addon.slug === slug)?.downloads;
}
