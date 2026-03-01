# Docker Environment

All self-hosted services in the irosec homelab run as Docker containers inside a dedicated Ubuntu VM on Proxmox. Containers are managed via Portainer and defined using Docker Compose.

---

## Host VM

| Property | Value |
|---|---|
| OS | Ubuntu 22.04.5 LTS |
| Kernel | 5.15.0-171-generic |
| Docker Version | Docker version 29.1.3, build f52814d |
| Compose Version | Docker Compose version v5.0.0 |
| Management | Portainer |

---

## Running Services

| Service | Purpose | Exposed |
|---|---|---|
| Portainer | Docker container management UI | Local only |
| Wiki.js | This documentation site | Public (wiki.irosec.com) |
| Plex | Personal media server | Public |
| Nginx Proxy Manager | Reverse proxy & SSL termination | Public |
| Glance | Local network homepage/dashboard | Local only |
| Tautulli | Plex monitoring & analytics | Local only |
| Fireshare | Self-hosted video sharing | Public |
| ErsatzTV | Personal IPTV channel server | Local only |
| Zipline | Self-hosted image sharing | Public |
| IT-Tools | Browser-based utility toolkit | Local only |
| Unifi Toolkit | Unifi network utilities | Local only |
| Vaultwarden | Self-hosted password manager | Local only |
| Mealie | Self-hosted recipe manager | Local only |

---

## Reverse Proxy & SSL

All external-facing services sit behind Nginx Proxy Manager and Cloudflare DNS which handles:

- SSL termination via Let's Encrypt
- Subdomain routing (e.g. `wiki.irosec.com`, `plex.irosec.com`)
- Access control for sensitive services

---

## Security Considerations

Running Vaultwarden (passwords) and other sensitive services in this environment means security is a real concern, not just a learning exercise. Current and planned hardening steps are documented in the [Security Stack](/security-stack) section.

---

## Backup Strategy

- VM snapshots are taken before any major changes
- Docker container stacks are manually backed up to the UNAS Pro
- Configs and database files are saved as snapshots on the UNAS Pro
