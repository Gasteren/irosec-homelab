---
title: "Home Assistant"
description: "Home Assistant is the smart home brain of the irosec homelab, running as a dedicated VM on Proxmox. It serves as the ..."
sidebar:
  order: 4
---

Home Assistant is the smart home brain of the irosec homelab, running as a dedicated VM on Proxmox. It serves as the central automation and control platform for the entire house - managing over 140 devices across 30 integrations.

This is not a hobby setup with a few smart bulbs. It is a fully integrated smart home environment covering lighting, climate, entertainment, security, appliances, vehicles, and more - all controlled and automated from a single self-hosted platform.

---

## VM Details

| Property | Value |
|---|---|
| OS | Home Assistant OS |
| Base | Buildroot Linux |
| Hypervisor | Proxmox VE |

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
| Vehicle | EV integration |

![integrations](https://img.irosec.com/u/zjR8R6.jpg)

---

## Notable Automations

| Automation | Description |
|---|---|
| Presence based scenes | Zone based automations that adjust lighting and climate around household presence |
| Appliance notifications | Notifies when the washing machine or dryer has finished its cycle |
| Calendar reminders | Date based reminder notifications |
| OctoEverywhere webhook | Receives webhook notifications when a 3D print job completes, fails, or needs attention |
| NFC tag scenes | Physical NFC tags toggle room scenes on and off |
| Vehicle battery alert | Low battery notification for the vehicle integration |

---

## Security Considerations

A Home Assistant instance managing 140+ devices across 30 integrations is a high-value target. The attack surface is significant - a compromised HA instance has reach across lighting, appliances, 3D printers, robot vacuums, and a vehicle. It represents one of the most sensitive systems in the homelab from a security perspective.

Key security practices applied:

- Home Assistant accessible on local network only - external access via WireGuard VPN
- Multi-factor authentication enabled on the HA account
- HA runs in an isolated VM on Proxmox, separate from the Docker services VM
- IoT devices are on a dedicated VLAN (VLAN 3), separated from the main and server networks

---

## Backups

- Home Assistant built-in backup system is active
- VM snapshots are taken before any major changes
- Docker container stacks are manually backed up to the UNAS Pro
- Configs and database files are saved as snapshots on the UNAS Pro
