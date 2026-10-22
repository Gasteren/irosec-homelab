/**
 * Keeps addon download numbers and the Recent activity feed current without
 * rebuilding the site.
 *
 * data/*.json in the repo is refreshed every 10 minutes by the
 * sync-addon-stats workflow (dispatched by a cron job on the Docker host), and
 * nginx serves the latest copy at /api/*.json (see nginx.conf.template). Live
 * elements are rendered with the values from the last build, so when a fetch
 * fails the page keeps showing those.
 *
 * Markup hooks:
 *   [data-live="total-downloads"], [data-live="addon-count"]  numbers
 *   [data-live-addon="<slug>"]                                downloads per addon
 *   time[data-live="synced"]                                  last sync, shown relative
 *   [data-live="next-sync"]                                   "next sync in mm:ss" / "syncing now"
 *   [data-live="countdown"]                                   "mm:ss" / "now"
 *   [data-live-state]                                         "syncing" or "idle"
 *   [data-live-activity]                                      activity feed (RecentActivity.astro)
 *   time[data-relative]                                       other relative timestamps
 */
import { formatDate, formatNumber, timeAgo } from '../lib/format';

interface AddonStats {
  total_downloads: number;
  addon_count: number;
  updated: string;
  addons: { slug: string; downloads: number }[];
}

interface Commit {
  repo: string;
  message: string;
  date: string;
  url: string;
  sha: string;
}

const STATS_URL = '/api/addon-stats.json';
const ACTIVITY_URL = '/api/recent-activity.json';

const SYNC_EVERY = 10 * 60_000; // the cron job dispatches a sync at every 10th minute
const SYNC_DELAY = 30_000; // the workflow needs a moment to commit new data
const SYNC_GRACE = 8 * 60_000; // GitHub's raw CDN can take a few minutes to catch up
const RETRY_EVERY = 45_000; // poll interval while new data is expected
const IDLE_REFRESH = 5 * 60_000; // occasional check outside sync windows
const ACTIVITY_LIMIT = 20;

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const animations = new WeakMap<HTMLElement, number>();

let lastUpdated = initialUpdated();
let lastFetch = 0;
let inFlight = false;
// The first live values replace the build-time snapshot instantly; only
// changes that arrive while the page is open are animated.
let animateChanges = false;

function initialUpdated(): number {
  const el = document.querySelector<HTMLTimeElement>('time[data-live="synced"]');
  const time = el ? Date.parse(el.dateTime) : NaN;
  return Number.isNaN(time) ? 0 : time;
}

async function getJson(url: string): Promise<unknown> {
  try {
    const res = await fetch(url, { cache: 'no-cache', headers: { Accept: 'application/json' } });
    return res.ok ? await res.json() : undefined;
  } catch {
    return undefined;
  }
}

function isStats(data: any): data is AddonStats {
  return (
    !!data &&
    Number.isFinite(data.total_downloads) &&
    Number.isFinite(data.addon_count) &&
    typeof data.updated === 'string' &&
    Array.isArray(data.addons)
  );
}

function isCommit(c: any): c is Commit {
  return (
    !!c &&
    typeof c.repo === 'string' &&
    typeof c.message === 'string' &&
    typeof c.date === 'string' &&
    typeof c.sha === 'string' &&
    typeof c.url === 'string' &&
    c.url.startsWith('https://github.com/')
  );
}

function all<T extends Element = HTMLElement>(selector: string): T[] {
  return Array.from(document.querySelectorAll<T>(selector));
}

function setNumber(el: HTMLElement, value: number) {
  const from = Number(el.dataset.value);
  if (from === value) return;
  el.dataset.value = String(value);
  const token = (animations.get(el) ?? 0) + 1;
  animations.set(el, token);
  if (!animateChanges || reducedMotion.matches || !Number.isFinite(from)) {
    el.textContent = formatNumber(value);
    return;
  }
  const start = performance.now();
  const step = (now: number) => {
    if (animations.get(el) !== token) return;
    const t = Math.min(1, (now - start) / 900);
    const eased = 1 - Math.pow(1 - t, 3);
    el.textContent = formatNumber(Math.round(from + (value - from) * eased));
    if (t < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
  el.classList.remove('live-bump');
  void el.offsetWidth; // restart the highlight animation
  el.classList.add('live-bump');
}

function applyStats(stats: AddonStats) {
  const updated = Date.parse(stats.updated);
  // Never step back to older data, e.g. a CDN copy that predates this build.
  if (Number.isNaN(updated) || updated < lastUpdated) return;
  lastUpdated = updated;

  all('[data-live="total-downloads"]').forEach((el) => setNumber(el, stats.total_downloads));
  all('[data-live="addon-count"]').forEach((el) => setNumber(el, stats.addon_count));
  const bySlug = new Map(stats.addons.map((addon) => [addon.slug, addon.downloads]));
  all('[data-live-addon]').forEach((el) => {
    const downloads = bySlug.get(el.dataset.liveAddon ?? '');
    if (typeof downloads === 'number' && Number.isFinite(downloads)) setNumber(el, downloads);
  });
  const iso = new Date(updated).toISOString();
  all<HTMLTimeElement>('time[data-live="synced"]').forEach((el) => {
    el.dateTime = iso;
    el.title = formatDate(iso, true);
  });
}

function activityItem(commit: Commit): HTMLLIElement {
  const item = document.createElement('li');
  const link = document.createElement('a');
  link.className = 'activity-item';
  link.href = commit.url;
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  const repo = document.createElement('span');
  repo.className = 'activity-repo';
  repo.textContent = commit.repo;
  const message = document.createElement('span');
  message.className = 'activity-msg';
  message.textContent = commit.message;
  const time = document.createElement('time');
  time.className = 'activity-time';
  time.dateTime = commit.date;
  time.dataset.relative = '';
  time.title = formatDate(commit.date, true);
  time.textContent = timeAgo(Date.parse(commit.date));
  link.append(repo, message, time);
  item.append(link);
  return item;
}

function renderActivity(data: any) {
  const root = document.querySelector<HTMLElement>('[data-live-activity]');
  const list = root?.querySelector('ol');
  if (!root || !list || !Array.isArray(data?.commits)) return;
  const commits: Commit[] = data.commits.filter(isCommit).slice(0, ACTIVITY_LIMIT);
  if (commits.length === 0) return;
  const key = commits.map((c) => `${c.repo}@${c.sha}`).join(',');
  if (root.dataset.key === key) return;
  root.dataset.key = key;
  list.replaceChildren(...commits.map(activityItem));
  updateMoreButton(root, commits.length);
}

function updateMoreButton(root: HTMLElement, count: number) {
  const more = root.querySelector<HTMLButtonElement>('[data-activity-more]');
  if (!more) return;
  more.textContent = `Show all (${count})`;
  more.hidden = root.hasAttribute('data-expanded') || count <= Number(root.dataset.visible ?? 6);
}

async function refresh() {
  if (inFlight) return;
  inFlight = true;
  lastFetch = Date.now();
  try {
    const wantsActivity = document.querySelector('[data-live-activity]') !== null;
    const [stats, activity] = await Promise.all([
      getJson(STATS_URL),
      wantsActivity ? getJson(ACTIVITY_URL) : undefined,
    ]);
    if (isStats(stats)) {
      applyStats(stats);
      animateChanges = true;
    }
    if (activity) renderActivity(activity);
  } finally {
    inFlight = false;
  }
  tick();
}

function mmss(ms: number): string {
  const secs = Math.max(0, Math.ceil(ms / 1000));
  return `${String(Math.floor(secs / 60)).padStart(2, '0')}:${String(secs % 60).padStart(2, '0')}`;
}

function tick() {
  const now = Date.now();
  const mark = Math.floor(now / SYNC_EVERY) * SYNC_EVERY;
  // Only wait for new data if the previous sync arrived; if syncs aren't
  // landing right now, the plain countdown is the honest thing to show.
  const expected = lastUpdated >= mark - SYNC_EVERY;
  const syncing = expected && lastUpdated < mark && now - mark < SYNC_GRACE;
  const remaining = mmss(mark + SYNC_EVERY - now);

  const write = (selector: string, text: string) =>
    all(selector).forEach((el) => {
      if (el.textContent !== text) el.textContent = text;
    });
  write('[data-live="next-sync"]', syncing ? 'syncing now' : `next sync in ${remaining}`);
  write('[data-live="countdown"]', syncing ? 'now' : remaining);
  all('[data-live-state]').forEach((el) => el.setAttribute('data-live-state', syncing ? 'syncing' : 'idle'));
  all<HTMLTimeElement>('time[data-live="synced"], time[data-relative]').forEach((el) => {
    const time = Date.parse(el.dateTime);
    if (Number.isNaN(time)) return;
    const text = timeAgo(time, now);
    if (el.textContent !== text) el.textContent = text;
  });

  if (document.hidden || inFlight) return;
  const sinceFetch = now - lastFetch;
  if ((syncing && now - mark >= SYNC_DELAY && sinceFetch >= RETRY_EVERY) || sinceFetch >= IDLE_REFRESH) {
    void refresh();
  }
}

function initActivity() {
  const root = document.querySelector<HTMLElement>('[data-live-activity]');
  const more = root?.querySelector<HTMLButtonElement>('[data-activity-more]');
  if (!root || !more) return;
  more.addEventListener('click', () => {
    root.setAttribute('data-expanded', '');
    more.hidden = true;
  });
}

initActivity();
void refresh();
setInterval(tick, 1000);
document.addEventListener('visibilitychange', () => {
  if (!document.hidden && Date.now() - lastFetch > 60_000) void refresh();
});
