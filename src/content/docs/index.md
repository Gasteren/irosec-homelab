---
title: irosec
description: Homelab and security portfolio documentation. Proxmox, Docker, UniFi, IDS/IPS, VLAN segmentation, and incident writeups.
template: splash
hero:
  title: irosec
  tagline: Documentation for a self hosted homelab, built and maintained as production infrastructure. Auto-deployed from GitHub.
  image:
    file: ../../assets/hero.svg
  actions:
    - text: Infrastructure
      link: /infrastructure/proxmox/
      icon: right-arrow
      variant: primary
    - text: Security Stack
      link: /security-stack/firewall/
      variant: secondary
    - text: GitHub
      link: https://github.com/Gasteren/irosec-homelab
      variant: minimal
---

## About this lab

This is a live environment, not a sandbox: it runs the services the household depends on, it has real internet exposure, and misconfiguration has real consequences. The documentation covers the actual configuration, the reasoning behind decisions, the known gaps, and the incidents that shaped the current state.

## Sections

- [Infrastructure](/infrastructure/proxmox/) - Proxmox, Docker, networking, Home Assistant
- [Security Stack](/security-stack/firewall/) - Firewall, IDS/IPS, SIEM
- [Projects](/projects/vlan-segmentation/) - Completed project writeups
- [Lessons Learned](/lessons-learned/) - Incidents, gaps, and fixes

## Stack

| Layer | Technology |
|---|---|
| Hypervisor | Proxmox VE |
| Containers | Docker, Portainer |
| Smart home | Home Assistant |
| Networking | UniFi Dream Machine Pro |
| Reverse proxy | Nginx Proxy Manager |
| Documentation | Astro Starlight |
