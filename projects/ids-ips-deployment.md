# Project: IDS/IPS Deployment

**Status:** ✅ Completed

---

## Objective

The goal was to deploy and configure Intrusion Detection and Prevention across all four VLANs on the Dream Machine Pro — enabling real-time threat detection and automated blocking of malicious traffic on a network running live, externally-exposed services.

Unlike a sandboxed lab environment, the irosec homelab carries real traffic: Plex streams, password manager syncs, smart home automation, and gaming. Deploying IDS/IPS here means working with genuine network noise and making deliberate decisions about what to flag versus what to allow.

---

## Environment

| Component | Detail |
|---|---|
| Device | Unifi Dream Machine Pro |
| Tool | Unifi Threat Management |
| Networks in Scope | All four VLANs (JARVIS, Guest, IoT, FRIDAY) |
| Detection Mode | Notify and Block |
| Signature Updates | Automatic — last updated March 1, 2026 at 17:55 |

---

## Steps

**1. Enabled Threat Management** — Activated Unifi Threat Management on the Dream Machine Pro and set Intrusion Prevention to On.

**2. Set detection mode** — Configured **Notify and Block** rather than Notify only, enabling automated blocking of detected threats rather than passive alerting.

**3. Applied to all networks** — Enabled IDS/IPS across all four VLANs: Server Network (JARVIS), Guest Network, IoT Devices, and Main Network (FRIDAY). Ensuring IoT devices and guest traffic are inspected was a deliberate decision given the number of smart home integrations on the network.

**4. Configured active detection categories** — Reviewed and enabled detection categories appropriate for a mixed home and security lab environment:

| Category | Rules Enabled |
|---|---|
| Botnets and Threat Intelligence | 5 of 5 |
| Viruses, Malware and Spyware | 4 of 4 |
| Hacking and Exploits | 5 of 5 |
| Peer to Peer and Dark Web | 3 of 3 |
| Attacks and Reconnaissance | 7 of 7 |
| Protocol Vulnerabilities | 11 of 12 |

**5. Tuned the Online Games rule** — During testing, the Online Games signature under Protocol Vulnerabilities produced false positives against World of Warcraft in-game voice chat traffic. After confirming this was a false positive via IDS logs, the rule was disabled. All 11 remaining Protocol Vulnerability rules remain active. Full writeup in [Lessons Learned — WoW Voice Chat Blocked](/lessons-learned/wow-voice-ids-block).

**6. Configured identification** — Set identification to **Device and Traffic** mode, enabling the DMP to correlate threat detections with specific device types for richer alert context.

**7. Verified detection** — Monitored the alerts dashboard to confirm traffic was being inspected and that legitimate traffic was not being incorrectly blocked after tuning.

![IDS](http://img.irosec.com/u/ecDCea.jpg)

---

## Results

- Full IDS/IPS coverage across all four VLANs
- Notify and Block mode active — threats are blocked automatically, not just logged
- 35 of 36 total detection rules enabled across all categories
- One rule deliberately disabled with documented justification
- Automatic signature updates keeping detection current

---

## Lessons Learned

Silent blocks — where IDS/IPS drops traffic without any visible error on the client side — are difficult to diagnose without proactively checking the IDS logs. The WoW voice chat incident took an hour to diagnose because the symptoms looked like an audio or application issue, not a network block.

Going forward, the IDS alert dashboard will be an earlier step in any network troubleshooting process. The longer-term fix is deploying Wazuh so IDS alerts are surfaced centrally alongside other logs rather than requiring a manual login to the Unifi controller to discover.
