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
- `data/` - Build-time snapshot of the addon download stats and the recent activity feed (the live copies come from the fetcher)
- `site/` - The Astro Starlight site: theme, components, Docker image, nginx config, and the live data fetcher (`site/fetcher/`)

## How this deploys

- A push to `main` triggers a GitHub Actions workflow on a self hosted runner
- The runner mirrors the repo onto the Docker host, rebuilds the images, and redeploys
- A small fetcher container next to the site pulls download counts from the CurseForge API and the latest commits across the addon repos every 10 minutes, and nginx serves them to the page, so numbers and activity update without a rebuild, a commit, or the runner
- The CurseForge API key lives only in the `.env` next to `docker-compose.yml` on the server, single-quoted because it contains `$`. The activity feed needs no GitHub token
- If fetching keeps failing, the fetcher container turns unhealthy (visible in Portainer) and the site keeps showing the last good data
- No manual build step at any point

## Working on the site

```sh
cd site
npm ci
npm run dev
```

`npm run dev` and `npm run build` first copy the content folders and `data/` into `site/src` (see `site/scripts/sync-content.mjs`). Run `npm run sync` to pick up content edits while the dev server is running. In dev, `/api/*.json` is proxied to the live site. `docker compose up --build` from the repo root builds and serves the production images (the fetcher needs `CURSEFORGE_API_KEY` in `.env`).
