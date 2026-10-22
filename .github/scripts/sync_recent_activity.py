#!/usr/bin/env python3
"""Write data/recent-activity.json: the latest commits across the public repos
shown in the "Recent activity" feed on wiki.irosec.com.

The site picks the file up live (nginx proxies it from GitHub), so the feed
stays current without rebuilding the site. The file only changes when the feed
does. If any repo can't be fetched, the previous file is kept as is.

Needs GH_TOKEN (the workflow passes its own github.token).
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

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
LIMIT = 20
OUT = "data/recent-activity.json"


def fetch_commits(repo, token):
    # author= skips the bot commits (e.g. the stats sync in irosec-homelab),
    # which would otherwise crowd out every human commit.
    query = urllib.parse.urlencode({"author": OWNER, "per_page": LIMIT})
    req = urllib.request.Request(
        f"https://api.github.com/repos/{OWNER}/{repo}/commits?{query}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "irosec-activity-sync/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as err:
        if err.code == 409:  # empty repository
            return []
        raise


def main():
    token = os.environ["GH_TOKEN"]
    commits = []
    for repo in REPOS:
        try:
            data = fetch_commits(repo, token)
        except Exception as err:
            print(f"::warning::Could not fetch commits for {repo} ({err}); keeping the previous {OUT}")
            return
        for c in data:
            commit = c["commit"]
            commits.append({
                "repo": repo,
                "message": commit["message"].split("\n", 1)[0].strip()[:100],
                "date": commit["author"]["date"] or commit["committer"]["date"],
                "url": c["html_url"],
                "sha": c["sha"][:7],
            })

    commits.sort(key=lambda c: c["date"], reverse=True)
    out = {"commits": commits[:LIMIT]}

    try:
        with open(OUT, encoding="utf-8") as f:
            if json.load(f) == out:
                print(f"{OUT} unchanged")
                return
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")
    newest = out["commits"][0]["date"] if out["commits"] else "n/a"
    print(f"Wrote {OUT}: {len(out['commits'])} commits, newest {newest}")


if __name__ == "__main__":
    main()
