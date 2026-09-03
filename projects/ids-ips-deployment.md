---
title: "Project: IDS/IPS Deployment"
description: "Status: ✅ Completed"
sidebar:
  order: 3
---

**Status:** ✅ Completed

---

## Objective

The goal was to deploy and configure Intrusion Detection and Prevention across all four VLANs on the Dream Machine Pro - enabling real-time threat detection and automated blocking of malicious traffic on a network running live, externally-exposed services.

Unlike a sandboxed lab environment, the irosec homelab carries real traffic: Plex streams, password manager syncs, smart home automation, and gaming. Deploying IDS/IPS here means working with genuine network noise and making deliberate decisions about what to flag versus what to allow.

---

## Environment

| Component | Detail |
|---|---|
| Device | Unifi Dream Machine Pro |
| Tool | Unifi Threat Management |
| Networks in Scope | All four VLANs (JARVIS, Guest, IoT, FRIDAY) |
| Detection Mode | Notify and Block |
| Signature Updates | Automatic - last updated March 1, 2026 at 17:55 |

---

## Steps

**1. Enabled Threat Management** - Activated Unifi Threat Management on the Dream Machine Pro and set Intrusion Prevention to On.

**2. Set detection mode** - Configured **Notify and Block** rather than Notify only, enabling automated blocking of detected threats rather than passive alerting.

**3. Applied to all networks** - Enabled IDS/IPS across all four VLANs: Server Network (JARVIS), Guest Network, IoT Devices, and Main Network (FRIDAY). Ensuring IoT devices and guest traffic are inspected was a deliberate decision given the number of smart home integrations on the network.

**4. Configured active detection categories** - Reviewed each detection category against the traffic profile of a mixed home and lab environment and enabled the high-signal groups in Block mode. The exact selection is not published.

**5. Tuned for false positives** - During testing, one signature produced false positives against legitimate game traffic. After confirming this via the IDS logs, that single signature was disabled with the justification documented. Full writeup in [Lessons Learned - WoW Voice Chat Blocked](/lessons-learned/wow-voice-chat-blocked-by-ids-ips/).

**6. Configured identification** - Set identification to **Device and Traffic** mode, enabling the DMP to correlate threat detections with specific device types for richer alert context.

**7. Verified detection** - Monitored the alerts dashboard to confirm traffic was being inspected and that legitimate traffic was not being incorrectly blocked after tuning.

---

## Results

- Full IDS/IPS coverage across all four VLANs
- Notify and Block mode active - threats are blocked automatically, not just logged
- One signature deliberately disabled with documented justification
- Automatic signature updates keeping detection current

---

## Lessons Learned

Silent blocks - where IDS/IPS drops traffic without any visible error on the client side - are difficult to diagnose without proactively checking the IDS logs. The WoW voice chat incident took an hour to diagnose because the symptoms looked like an audio or application issue, not a network block.

Going forward, the IDS alert dashboard will be an earlier step in any network troubleshooting process. The longer-term fix is deploying Wazuh so IDS alerts are surfaced centrally alongside other logs rather than requiring a manual login to the Unifi controller to discover.
