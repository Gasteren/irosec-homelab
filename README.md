# irosec

Content and source for [wiki.irosec.com](https://wiki.irosec.com): a self hosted homelab run as production infrastructure, and 16 published World of Warcraft addons with 880K+ combined downloads.

The written content lives in the folders below, and the site that presents it lives in `site/`. It is built with [Astro Starlight](https://starlight.astro.build) and deployed automatically: pushing to `main` rebuilds and redeploys it through a self hosted GitHub Actions runner, with no manual steps.

## What's here

**Infrastructure and security.** Documentation for a network with real internet exposure and real consequences, not a lab exercise. Each writeup covers the actual configuration, the reasoning behind decisions, known gaps, and what changed after an incident.

**Published software.** 16 World of Warcraft addons on CurseForge, from small utility tools to a guild management addon used by an active raiding guild. Download stats sync automatically from the CurseForge API and stay current on the live site without any manual updates.

## Structure

- `infrastructure/` - Proxmox, Docker, networking, Home Assistant
- `security-stack/` - Firewall, IDS/IPS, SIEM
- `projects/` - Completed project writeups
- `lessons-learned/` - Incidents, gaps, and fixes
- `addons/` - Published World of Warcraft addons and live download stats
- `data/` - Addon download stats and the recent activity feed, kept current by a scheduled workflow
- `site/` - The Astro Starlight site: theme, components, Docker image, and nginx config

## How this deploys

- A push to `main` that changes content or the site triggers a GitHub Actions workflow on a self hosted runner
- The runner mirrors the repo onto the Docker host, rebuilds the image, and redeploys
- Every 10 minutes a cron job on the Docker host dispatches a GitHub hosted workflow (a 30 minute schedule is the backup) that pulls download counts from the CurseForge API and the latest commits across the addon repos, and commits them to `data/`
- The live site reads `data/` from GitHub through its own nginx, so new numbers and activity show up within minutes, with no rebuild and no self hosted runner involved
- No manual build step at any point in either path

## Working on the site

```sh
cd site
npm ci
npm run dev
```

`npm run dev` and `npm run build` first copy the content folders and `data/` into `site/src` (see `site/scripts/sync-content.mjs`). Run `npm run sync` to pick up content edits while the dev server is running. `docker compose up --build` from the repo root builds and serves the production image.
