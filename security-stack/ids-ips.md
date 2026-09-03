---
title: "IDS/IPS"
description: "The irosec homelab uses Unifi Threat Management on the Dream Machine Pro as its primary intrusion detection and preve..."
sidebar:
  order: 2
---

The irosec homelab uses Unifi Threat Management on the Dream Machine Pro as its primary intrusion detection and prevention layer. Because this is a live environment running real services with real external exposure - Plex, Nginx Proxy Manager, and WireGuard are all reachable from the internet - IDS/IPS is monitoring actual traffic, not simulated lab scenarios.

---

## Current Setup

| Property | Value |
|---|---|
| Device | Unifi Dream Machine Pro |
| Tool | Unifi Threat Management |
| Intrusion Prevention | Enabled |
| Detection Mode | Notify and Block |
| Signature Update | March 1, 2026 at 17:55 |
| Selected Networks | All four VLANs |

---

## Honeypot

A honeypot address is configured on every VLAN. Any device that connects to one of these addresses is flagged as suspicious, since no legitimate traffic should ever target them. The addresses themselves are not published. See [Project: Honeypot Per VLAN](/projects/honeypot/) for the deployment writeup.

---

## Identification

Set to **Device and Traffic** - the DMP identifies both the device type and inspects traffic content for threat correlation.

---

## Active Detections

Detection categories are enabled in Block mode with an emphasis on the high-signal groups (threat intelligence, malware, exploits). The exact category and signature selection is not published here, since it describes what the IDS will and will not catch. Individual signatures are tuned only where they produce documented false positives against legitimate traffic; one such case is written up in [Lessons Learned](/lessons-learned/wow-voice-chat-blocked-by-ids-ips/).

---

## What It Monitors

IDS/IPS runs across all four VLANs - JARVIS, FRIDAY, IoT Devices, and Guest Network. Given the homelab's exposure this includes:

- Inbound traffic to the publicly reachable services (Plex, reverse proxy, WireGuard)
- All outbound and inter-VLAN traffic across all four networks

---

## Limitations

Unifi Threat Management is a solid first layer but has real limitations worth acknowledging:

- Log export is limited - alerts are not easily forwarded to an external SIEM without additional tooling
- Detection is primarily signature-based with no behavioural analysis
- All VLANs share the same detection policy with no per-VLAN granularity

---

## Future Plans

- Forward Unifi logs to Wazuh once deployed for centralised correlation across all VLANs
- Cross-reference IDS alerts with Nginx Proxy Manager access logs for a fuller picture of inbound threats
- Investigate moving IoT VLAN to a stricter zone to add an additional detection boundary between smart home devices and the server network

---

## References

- [Unifi Threat Management Docs](https://help.ui.com)
