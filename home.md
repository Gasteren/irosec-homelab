# Welcome to irosec Lab

This wiki documents my personal homelab — a real, active self-hosted environment that I use daily, progressively hardened and expanded with a cybersecurity focus.

This isn't a practice sandbox. It's a production homelab running over a dozen self-hosted services, a full smart home stack, and real sensitive data — including passwords, media, and home automation. That makes security not optional, but necessary.

---

## 🖥️ Lab at a Glance

| Component | Details |
|---|---|
| Hypervisor | Proxmox VE 8.4.1 |
| Containerization | Docker (Ubuntu 22.04 LTS) |
| Smart Home | Home Assistant OS 17.1 |
| Networking | Unifi |
| Reverse Proxy | Nginx Proxy Manager |
| Documentation | Wiki.js |
| Domain | irosec.com |

---

## 🐳 Hosted Services

| Service | Purpose |
|---|---|
| Plex | Personal media server |
| Vaultwarden | Self-hosted password manager |
| Wiki.js | This documentation site |
| Home Assistant | Smart home automation hub |
| Nginx Proxy Manager | Reverse proxy & SSL termination |
| Portainer | Docker container management |
| Glance | Local network homepage/dashboard |
| Tautulli | Plex monitoring & analytics |
| Fireshare | Self-hosted video sharing |
| ErsatzTV | Personal IPTV channel server |
| Zipline | Self-hosted image sharing |
| IT-Tools | Browser-based utility toolkit |
| Unifi Toolkit | Unifi network utilities |
| Mealie | Self-hosted recipe manager |

---

## 🏠 Smart Home

Home Assistant manages a broad set of smart home devices including Philips Hue lighting, smart TVs, Bambu Lab 3D printers (A1 & P1S), Dreame and iRobot robot vacuums, and a Tesla vehicle integration.

---

## 📁 What's Inside

- [Infrastructure](/infrastructure) — Hardware, VMs, networking and hosted services
- [Security Stack](/security-stack) — Firewall, IDS/IPS, SIEM and monitoring layered on top of real infrastructure
- [Projects](/projects) — Hands-on security scenarios run against live and lab environments
- [Lessons Learned](/lessons-learned) — What broke, why, and how it was fixed

---

## 🎯 Goals

- Maintain and improve a real self-hosted production environment
- Apply security best practices to live infrastructure with actual data at stake
- Deploy and operate blue team tooling used in real SOC environments
- Document everything to a professional standard

---

*This lab is actively maintained. Pages are updated as services are added, changed, or secured.*