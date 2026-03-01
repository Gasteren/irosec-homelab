# irosec Homelab

Personal cybersecurity homelab — a real, active self-hosted environment running 13 services and 140+ smart home devices, with a full security stack layered on top.

This isn't a sandboxed practice lab. Vaultwarden holds real passwords. Home Assistant controls a Tesla. Plex is publicly exposed. Security here has actual consequences.

📖 **Full documentation:** [wiki.irosec.com](https://wiki.irosec.com)

---

## Stack

| Layer | Technology |
|---|---|
| Hypervisor | Proxmox VE 8.4.1 |
| Containers | Docker + Portainer (Ubuntu 22.04) |
| Smart Home | Home Assistant OS 17.1 |
| Networking | Unifi — Dream Machine Pro |
| Reverse Proxy | Nginx Proxy Manager |
| Documentation | Wiki.js |

---

## Security Stack

| Control | Implementation |
|---|---|
| Firewall | Unifi Zone-based — 66 active policies |
| Network Segmentation | 4 VLANs (Servers, Trusted, IoT, Guest) |
| IDS/IPS | Unifi Threat Management — Notify & Block |
| Deception | Honeypot address on every VLAN |
| Remote Access | WireGuard VPN |
| SIEM | Wazuh — planned |

---

## Self-Hosted Services

| Service | Purpose |
|---|---|
| Plex | Personal media server |
| Vaultwarden | Self-hosted password manager |
| Wiki.js | This documentation |
| Nginx Proxy Manager | Reverse proxy & SSL |
| Portainer | Docker management |
| Glance | Local network dashboard |
| Tautulli | Plex analytics |
| Fireshare | Self-hosted video sharing |
| ErsatzTV | Personal IPTV channels |
| Zipline | Self-hosted image sharing |
| IT-Tools | Browser utility toolkit |
| Mealie | Recipe manager |
| Unifi Toolkit | Network utilities |

---

## Repository Structure

```
irosec-homelab/
├── infrastructure/        # Proxmox, Docker, networking, Home Assistant
├── security-stack/        # Firewall, IDS/IPS, SIEM
├── projects/              # Completed project writeups
└── lessons-learned/       # Incidents, gaps, and what was fixed
```

---

## Documentation

All pages are written to a professional standard with full context, reasoning behind decisions, and honest documentation of known gaps and planned improvements.

Full wiki: [wiki.irosec.com](https://wiki.irosec.com)

---

*Actively maintained. Updated as the lab grows.*