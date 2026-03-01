---
title: 
description: 
published: true
date: 2026-03-01T21:48:00.768Z
tags: 
editor: markdown
dateCreated: 2026-03-01T21:47:59.154Z
---

# Home Assistant

Home Assistant is the smart home brain of the irosec homelab, running as a dedicated VM on Proxmox. It serves as the central automation and control platform for the entire house — managing over 140 devices across 30 integrations.

This is not a hobby setup with a few smart bulbs. It is a fully integrated smart home environment covering lighting, climate, entertainment, security, appliances, vehicles, and more — all controlled and automated from a single self-hosted platform.

---

## VM Details

| Property | Value |
|---|---|
| OS | Home Assistant OS 17.1 |
| Base | Buildroot Linux |
| Hypervisor | Proxmox VE 8.4.1 |

---

## Scale

| Metric | Value |
|---|---|
| Integrations | 30 |
| Devices | 140+ |

![devices](https://img.irosec.com/u/MLWPkk.jpg)

---

## Known Integrations & Devices

| Category | Device(s) |
|---|---|
| 3D Printers | Bambu Lab A1, Bambu Lab P1S |
| Robot Vacuums | Dreame, iRobot |
| Lighting | Philips Hue (lights & scenes) |
| Entertainment | Smart TVs |
| Vehicle | Tesla |

![integrations](https://img.irosec.com/u/zjR8R6.jpg)

---

## Notable Automations

| Automation | Description |
|---|---|
| Carlo — Arrived Work | Triggers when Carlo arrives at work — likely using GPS/zone detection via the Tesla or phone integration |
| Carlo — Left Work | Triggers when Carlo leaves work — used to prepare the home before arrival (lighting, climate etc.) |
| Dryer — DONE | Sends a notification when the dryer has finished its cycle |
| Washing Machine — DONE | Sends a notification when the washing machine has finished its cycle |
| Happy Anniversary | Sends an anniversary reminder notification on the correct date |
| OctoEverywhere Notification Webhook | Receives webhook notifications from OctoEverywhere — alerts when a 3D print job completes, fails, or needs attention on the Bambu Lab printers |
| Tag Office is scanned | Triggers an automation when an NFC tag in the office is scanned — used to toggle office-related devices or scenes |
| Tag Office off is scanned | Triggers an automation when a the NFC tag is scanned to turn off the office setup |
| Tesla under 20% | Sends a low battery alert when the Tesla drops below 20% charge |

---

## Security Considerations

A Home Assistant instance managing 140+ devices across 30 integrations is a high-value target. The attack surface is significant — a compromised HA instance has reach across lighting, appliances, 3D printers, robot vacuums, and a Tesla vehicle. It represents one of the most sensitive systems in the homelab from a security perspective.

Key security practices applied:

- Home Assistant accessible on local network only — external access via WireGuard VPN
- Multi-factor authentication enabled on the HA account
- HA runs in an isolated VM on Proxmox, separate from the Docker services VM
- IoT devices are on a dedicated VLAN (VLAN 3 — 192.168.69.0/24), separated from the main and server networks

---

## Backups

- Home Assistant built-in backup system is active
- VM snapshots are taken before any major changes
- Docker container stacks are manually backed up to the UNAS Pro
- Configs and database files are saved as snapshots on the UNAS Pro
