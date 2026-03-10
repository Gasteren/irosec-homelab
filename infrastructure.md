---
title: 
description: 
published: true
date: 2026-03-01T21:48:01.477Z
tags: 
editor: markdown
dateCreated: 2026-03-01T17:12:30.880Z
---

# 🛠️ Infrastructure

This section covers the infrastructure powering the irosec homelab — the hypervisor, virtual machines, Docker environment, and network layout.

---

## 📄 Pages

- [Network Topology](/infrastructure/network-topology) — How the network is structured, VLANs, and traffic flow
- [Proxmox Setup](/infrastructure/proxmox) — Hypervisor configuration and VM layout
- [Docker Environment](/infrastructure/docker) — Container setup, Compose files, and running services
- [Home Assistant](/infrastructure/home-assistant) — Smart home VM and device integrations

---

## 🗺️ Overview

The homelab runs on a single Proxmox VE 8.4.1 host with two VMs:

**VM 1 — Docker Host (Ubuntu 22.04 LTS)** — Runs all self-hosted services via Docker Compose, managed through Portainer. This is the primary services VM hosting everything from Plex to Vaultwarden.

**VM 2 — Home Assistant OS 17.1** — Dedicated VM for smart home automation, integrating lighting, appliances, printers, vacuums, and a Tesla vehicle.

All external access is routed through Nginx Proxy Manager with SSL termination via Let's Encrypt. Networking is handled by Unifi hardware.

> 📌 Network diagram coming soon.
