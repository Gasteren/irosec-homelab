# irosec

Documentation content for [wiki.irosec.com](https://wiki.irosec.com), a self hosted homelab and security portfolio.

This repository holds only the written content. The site itself is built with [Astro Starlight](https://starlight.astro.build) and deployed via a self hosted GitHub Actions runner: pushing to `main` automatically syncs the content below into the site and rebuilds it.

## Structure

- `infrastructure/` - Proxmox, Docker, networking, Home Assistant
- `security-stack/` - Firewall, IDS/IPS, SIEM
- `projects/` - Completed project writeups
- `lessons-learned/` - Incidents, gaps, and fixes

## Editing

Edit the Markdown files in the folders above and push to `main`. The deployment runs automatically; no build step is required here.
