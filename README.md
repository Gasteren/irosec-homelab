# irosec

Content for [wiki.irosec.com](https://wiki.irosec.com): a self hosted homelab run as production infrastructure, and 16 published World of Warcraft addons with 880K+ combined downloads.

This repository holds only the written content, not the site itself. The site is built with [Astro Starlight](https://starlight.astro.build) and deployed automatically: pushing to `main` syncs the content below into the site, rebuilds it, and redeploys, through a self hosted GitHub Actions runner with no manual steps.

## What's here

**Infrastructure and security.** Documentation for a network with real internet exposure and real consequences, not a lab exercise. Each writeup covers the actual configuration, the reasoning behind decisions, known gaps, and what changed after an incident.

**Published software.** 16 World of Warcraft addons on CurseForge, from small utility tools to a guild management addon used by an active raiding guild. Download stats sync automatically from the CurseForge API and stay current on the live site without any manual updates.

## Structure

- `infrastructure/` - Proxmox, Docker, networking, Home Assistant
- `security-stack/` - Firewall, IDS/IPS, SIEM
- `projects/` - Completed project writeups
- `lessons-learned/` - Incidents, gaps, and fixes
- `addons/` - Published World of Warcraft addons and live download stats

## How this deploys

- A push to `main` triggers a GitHub Actions workflow on a self hosted runner
- The runner syncs the folders above into the Astro Starlight site, rebuilds the Docker image, and redeploys
- A separate scheduled workflow polls the CurseForge API every 10 minutes, updates addon download stats, and triggers the same deploy pipeline whenever the numbers change
- No manual build step at any point in either path
