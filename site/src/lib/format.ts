// Formatting shared by build-time rendering and the live-data script, so live
// updates look exactly like the values rendered at build time.

const numberFormat = new Intl.NumberFormat('en-US');

export function formatNumber(value: number): string {
  return numberFormat.format(value);
}

export function timeAgo(then: number, now = Date.now()): string {
  const mins = Math.floor((now - then) / 60_000);
  if (mins < 1) return 'just now';
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days < 60) return `${days}d ago`;
  return `${Math.floor(days / 30)}mo ago`;
}

/** Absolute fallback shown until the live-data script swaps in a relative time. */
export function formatDate(iso: string, withTime = false): string {
  return new Date(iso).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    ...(withTime ? { hour: '2-digit', minute: '2-digit', hour12: false, timeZoneName: 'short' } : {}),
    timeZone: 'UTC',
  });
}
