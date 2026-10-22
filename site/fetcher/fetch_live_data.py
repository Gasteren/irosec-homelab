#!/usr/bin/env python3
"""Keeps the wiki's live data current: CurseForge download counts for the
published addons, and the latest commits across the addon repos.

Runs as the `fetcher` service next to the site (see docker-compose.yml). It
fetches once at start and then just after every 10-minute mark (UTC), which
is what the "next sync" countdown on the site counts down to. Results are
written atomically to DATA_DIR, which nginx serves as /api/*.json. A failed
fetch keeps the last good file, and `--healthcheck` reports unhealthy once
the data goes stale. With HEALTHCHECKS_PING_URL set, each cycle also reports
to Healthchecks.io (see report()), which emails when fetching keeps failing.
Standard library only.

  fetch_live_data.py                run forever (the container's command)
  fetch_live_data.py --once         one fetch cycle, then exit
  fetch_live_data.py --healthcheck  exit 1 if the data is stale

Environment:
  CURSEFORGE_API_KEY     or the secret file /run/secrets/curseforge_api_key
  GITHUB_TOKEN           optional; GitHub is read unauthenticated otherwise
  HEALTHCHECKS_PING_URL  optional; https://hc-ping.com/<uuid>
  DATA_DIR               default /data
  STATS_STALE_AFTER      seconds, default 2100 (35 min)
  ACTIVITY_STALE_AFTER   seconds, default 7200 (2 h)
"""
import json
import os
import random
import signal
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
STATE_FILE = DATA_DIR / ".state.json"
INTERVAL = 600  # the page's countdown assumes a sync at every 10th minute
OFFSET = 2  # seconds after each mark
STATS_STALE_AFTER = int(os.environ.get("STATS_STALE_AFTER", 35 * 60))
ACTIVITY_STALE_AFTER = int(os.environ.get("ACTIVITY_STALE_AFTER", 2 * 60 * 60))
PING_URL = os.environ.get("HEALTHCHECKS_PING_URL", "").strip().rstrip("/")
USER_AGENT = "irosec-live-data/1.0 (+https://wiki.irosec.com)"

CURSEFORGE = "https://api.curseforge.com/v1"
SLUGS = [
    "handynotes-ancientshrines",
    "handynotes-jetpacks",
    "betterbags-fishing",
    "adibags-fishing",
    "interrupted-x",
    "interruptbar-v1",
    "handynotes-naigtalteleports",
    "handynotes-valteleports",
    "twitch-drops-watcher",
    "leveltimetracker",
    "lozn64-levelup",
    "afkdelight",
    "timestamp",
    "repkeeper",
    "hall-of-fallen-heroes-wd",
    "antisocial",
]

GITHUB = "https://api.github.com"
OWNER = "Gasteren"
REPOS = [
    "irosec-homelab",
    "TwitchDropsWatcher",
    "Adibags_Fishing",
    "BetterBags_Fishing",
    "TimeStamp",
    "RepKeeper",
    "LoZN64",
    "LevelTimeTracker",
    "HandyNotes_ValTeleports",
    "HandyNotes_NaigtalTeleports",
    "HandyNotes_Jetpacks",
    "HandyNotes_AncientShrines",
    "Hall-Of-Fallen-Heroes",
    "AntiSocial",
    "Interrupted",
    "InterruptBar",
    "AfkDelight",
    "FishKeeper",
]
ACTIVITY_LIMIT = 20

RETRYABLE = {429, 500, 502, 503, 504}


def log(message):
    print(f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {message}", flush=True)


def iso(epoch):
    return datetime.fromtimestamp(epoch, timezone.utc).isoformat(timespec="seconds")


class HttpError(Exception):
    def __init__(self, status, headers, url):
        super().__init__(f"HTTP {status} from {urllib.parse.urlsplit(url).path}")
        self.status = status
        self.headers = headers


def backoff(attempt, headers=None):
    retry_after = headers.get("Retry-After") if headers else None
    if retry_after and retry_after.isdigit():
        return min(int(retry_after), 60)
    return 5 * 3 ** (attempt - 1) + random.uniform(0, 2)


def http(url, headers, method="GET", payload=None, attempts=3):
    """JSON request with retries on connection errors (resets, TLS, timeouts)
    and on 429/5xx. Returns (response headers, parsed body)."""
    data = None if payload is None else json.dumps(payload).encode()
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json", **headers}
    if data is not None:
        headers["Content-Type"] = "application/json"
    path = urllib.parse.urlsplit(url).path
    for attempt in range(1, attempts + 1):
        try:
            request = urllib.request.Request(url, data=data, headers=headers, method=method)
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.headers, json.loads(response.read() or b"null")
        except urllib.error.HTTPError as err:
            if err.code not in RETRYABLE or attempt == attempts:
                raise HttpError(err.code, err.headers, url) from None
            wait = backoff(attempt, err.headers)
            log(f"HTTP {err.code} from {path}, retrying in {wait:.0f}s")
        except OSError as err:  # URLError, connection resets, TLS errors, timeouts
            if attempt == attempts:
                raise
            wait = backoff(attempt)
            log(f"{getattr(err, 'reason', err)} for {path}, retrying in {wait:.0f}s")
        time.sleep(wait)


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as err:
        log(f"ignoring unreadable {path.name}: {err}")
        return None


def write_json(path, data, mode=0o644):
    """Write via a temp file and rename, so readers never see a partial file."""
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.chmod(tmp, mode)
    os.replace(tmp, path)


def curseforge_key():
    secret = Path("/run/secrets/curseforge_api_key")
    key = secret.read_text().strip() if secret.is_file() else os.environ.get("CURSEFORGE_API_KEY", "")
    return key.strip()


def fetch_stats(state):
    """Download counts for SLUGS -> addon-stats.json (same format the site
    has always used)."""
    key = curseforge_key()
    if not key:
        raise RuntimeError("no API key; set CURSEFORGE_API_KEY in the .env next to docker-compose.yml")
    auth = {"x-api-key": key}

    game_id = state.get("cf_game_id")
    if not game_id:
        _, games = http(f"{CURSEFORGE}/games?pageSize=50", auth)
        game_id = next(
            (g["id"] for g in games.get("data", [])
             if "warcraft" in g.get("name", "").lower() or g.get("slug", "").lower() == "wow"),
            None,
        )
        if game_id is None:
            raise RuntimeError("World of Warcraft not found in /v1/games")
        state["cf_game_id"] = game_id

    # Slugs are resolved to project ids once; after that a cycle is a single request.
    mod_ids = state.setdefault("cf_mod_ids", {})
    for slug in SLUGS:
        if slug not in mod_ids:
            query = urllib.parse.urlencode({"gameId": game_id, "slug": slug, "pageSize": 1})
            _, found = http(f"{CURSEFORGE}/mods/search?{query}", auth)
            if found.get("data"):
                mod_ids[slug] = found["data"][0]["id"]
            else:
                log(f"WARNING: no CurseForge project for slug '{slug}'")

    ids = [mod_ids[slug] for slug in SLUGS if slug in mod_ids]
    if not ids:
        raise RuntimeError("no CurseForge projects resolved")
    _, result = http(f"{CURSEFORGE}/mods", auth, method="POST", payload={"modIds": ids})
    mods = {mod["id"]: mod for mod in result.get("data", [])}

    addons = []
    for slug in SLUGS:
        mod = mods.get(mod_ids.get(slug))
        if mod is None:
            continue
        addons.append({
            "name": mod.get("name"),
            "slug": slug,
            "downloads": int(mod.get("downloadCount", 0)),
            "url": (mod.get("links") or {}).get("websiteUrl"),
        })
    if not addons:
        raise RuntimeError("CurseForge returned none of the requested projects")

    addons.sort(key=lambda addon: addon["downloads"], reverse=True)
    stats = {
        "total_downloads": sum(addon["downloads"] for addon in addons),
        "addon_count": len(addons),
        "updated": datetime.now(timezone.utc).isoformat(),
        "addons": addons,
    }
    write_json(DATA_DIR / "addon-stats.json", stats)
    state["stats_summary"] = f"{stats['total_downloads']:,} downloads across {stats['addon_count']} addons"
    log(f"addon stats: {state['stats_summary']}")
    return True


def simplify(repo, commit):
    details = commit["commit"]
    return {
        "repo": repo,
        "message": details["message"].split("\n", 1)[0].strip()[:100],
        "date": details["author"]["date"] or details["committer"]["date"],
        "url": commit["html_url"],
        "sha": commit["sha"][:7],
    }


def fetch_activity(state):
    """Latest commits across REPOS -> recent-activity.json.

    Unauthenticated GitHub allows 60 requests an hour per IP, and conditional
    requests only save quota when authenticated. So each cycle lists the repos
    once (one request) and only fetches commits for repos whose pushed_at
    changed since the last cycle."""
    now = time.time()
    if now < state.get("gh_blocked_until", 0):
        log(f"activity: GitHub rate limit, waiting until {iso(state['gh_blocked_until'])}")
        return False

    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    pushed_seen = state.setdefault("gh_pushed_at", {})
    cached = state.setdefault("gh_commits", {})
    try:
        response, repos = http(f"{GITHUB}/users/{OWNER}/repos?type=owner&sort=pushed&per_page=100", headers)
        remaining = int(response.get("x-ratelimit-remaining", 60))
        pushed = {repo["name"]: repo["pushed_at"] for repo in repos}
        changed = [r for r in REPOS if r in pushed and (r not in cached or pushed_seen.get(r) != pushed[r])]
        for done, repo in enumerate(changed):
            if remaining < 3:  # keep headroom for the next cycle's repo listing
                log(f"activity: rate limit nearly used, {len(changed) - done} repos wait for the next cycle")
                break
            query = urllib.parse.urlencode({"author": OWNER, "per_page": ACTIVITY_LIMIT})
            try:
                response, commits = http(f"{GITHUB}/repos/{OWNER}/{repo}/commits?{query}", headers)
            except HttpError as err:
                if err.status != 409:  # 409: the repository is empty
                    raise
                response, commits = err.headers, []
            remaining = int(response.get("x-ratelimit-remaining", remaining - 1))
            cached[repo] = [simplify(repo, commit) for commit in commits]
            pushed_seen[repo] = pushed[repo]
    except HttpError as err:
        if err.status in (403, 429) and err.headers.get("x-ratelimit-remaining") == "0":
            state["gh_blocked_until"] = int(err.headers.get("x-ratelimit-reset", now + 3600))
            raise RuntimeError(f"GitHub rate limit reached, paused until {iso(state['gh_blocked_until'])}") from None
        raise

    missing = [r for r in REPOS if r not in pushed]
    if missing:
        log(f"WARNING: not among {OWNER}'s public repos: {', '.join(missing)}")
    if any(r in pushed and r not in cached for r in REPOS):
        return False  # first fill still in progress

    commits = sorted((c for r in REPOS for c in cached.get(r, [])), key=lambda c: c["date"], reverse=True)
    activity = {"commits": commits[:ACTIVITY_LIMIT]}
    path = DATA_DIR / "recent-activity.json"
    if read_json(path) != activity:
        write_json(path, activity)
        log(f"activity: updated, newest {activity['commits'][0]['repo'] if activity['commits'] else 'none'}"
            f" ({len(changed)} repos fetched)")
    return True


def run_cycle():
    state = read_json(STATE_FILE) or {}
    state["started_at"] = STARTED_AT
    errors = state.setdefault("errors", {})
    stats_fetched = False
    for name, fetch, ok_key in (("CurseForge", fetch_stats, "stats_ok_at"),
                                ("GitHub", fetch_activity, "activity_ok_at")):
        try:
            if fetch(state):
                state[ok_key] = time.time()
                errors.pop(name, None)
                stats_fetched = stats_fetched or name == "CurseForge"
        except Exception as err:  # keep the last good data and try again next cycle
            errors[name] = str(err)[:300]
            log(f"{name} fetch failed, keeping the last good data: {err}")
    write_json(STATE_FILE, state, mode=0o600)
    report(state, stats_fetched)


def health_problems(state):
    now = time.time()
    problems = []
    if now - state.get("stats_ok_at", 0) > STATS_STALE_AFTER:
        problems.append("addon stats are stale (check the CurseForge API key and the logs)")
    # A fresh container gets until ACTIVITY_STALE_AFTER for its first activity fetch.
    if now - (state.get("activity_ok_at") or state.get("started_at", 0)) > ACTIVITY_STALE_AFTER:
        problems.append("activity feed is stale (see the logs)")
    return problems


last_report = None  # last ping kind sent, so only changes get logged


def report(state, stats_fetched):
    """Report the cycle to Healthchecks.io: a ping after a cycle that fetched
    the stats, and /fail with the reasons once the data is stale (the same
    thresholds as the Docker healthcheck). A failed cycle in between sends
    nothing, so a single miss stays quiet and the check's grace period
    decides when to alert. Reporting never affects fetching."""
    global last_report
    if not PING_URL:
        return
    if not PING_URL.startswith("https://"):
        if last_report != "invalid":
            log("WARNING: HEALTHCHECKS_PING_URL must start with https://; not reporting")
        last_report = "invalid"
        return
    problems = health_problems(state)
    if problems:
        kind, url = "failure", f"{PING_URL}/fail"
        body = "; ".join(problems + [f"{name}: {error}" for name, error in state.get("errors", {}).items()])
    elif stats_fetched:
        kind, url, body = "ok", PING_URL, state.get("stats_summary", "ok")
    else:
        return
    try:
        request = urllib.request.Request(url, data=body.encode()[:10_000], method="POST",
                                         headers={"User-Agent": USER_AGENT, "Content-Type": "text/plain; charset=utf-8"})
        with urllib.request.urlopen(request, timeout=10) as response:
            status, answer = response.status, response.read(200).decode(errors="replace")
    except Exception as err:  # e.g. Healthchecks.io unreachable; the URL itself is never logged
        log(f"Healthchecks.io ping failed: {getattr(err, 'code', None) or getattr(err, 'reason', None) or err}")
        last_report = None
        return
    # An unknown check still answers 200, with "OK (not found)".
    if "not found" in answer.lower():
        kind = "unknown"
        if kind != last_report:
            log("WARNING: Healthchecks.io doesn't know this check; verify HEALTHCHECKS_PING_URL")
    elif kind != last_report:
        log(f"Healthchecks.io: reported {kind} (HTTP {status})")
    last_report = kind


def healthcheck():
    problems = health_problems(read_json(STATE_FILE) or {})
    print("; ".join(problems) or "ok")
    return 1 if problems else 0


def seconds_until_next_run():
    return INTERVAL - ((time.time() - OFFSET) % INTERVAL)


STARTED_AT = time.time()

if __name__ == "__main__":
    if "--healthcheck" in sys.argv:
        sys.exit(healthcheck())
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if "--once" in sys.argv:
        run_cycle()
        sys.exit(0)
    # PID 1 in a container ignores SIGTERM unless a handler is installed.
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    log(f"fetching every {INTERVAL // 60} min into {DATA_DIR}")
    while True:
        run_cycle()
        time.sleep(seconds_until_next_run())
