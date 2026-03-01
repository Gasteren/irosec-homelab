# IDS/IPS

The irosec homelab uses Unifi Threat Management on the Dream Machine Pro as its primary intrusion detection and prevention layer. Because this is a live environment running real services with real external exposure — Plex, Nginx Proxy Manager, and WireGuard are all reachable from the internet — IDS/IPS is monitoring actual traffic, not simulated lab scenarios.

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

A honeypot address is configured on every VLAN. Any device that connects to these addresses is flagged as suspicious, since no legitimate traffic should ever target them.

| Network | Subnet | Honeypot Address |
|---|---|---|
| Server Network — JARVIS | 192.168.178.0/24 | 192.168.178.2 |
| Guest Network | 192.168.2.0/24 | 192.168.2.2 |
| IoT Devices | 192.168.69.0/24 | 192.168.69.2 |
| Main Network — FRIDAY | 192.168.5.0/24 | 192.168.5.2 |

---

## Identification

Set to **Device and Traffic** — the DMP identifies both the device type and inspects traffic content for threat correlation.

---

## Active Detections

All detection categories are fully enabled with the exception of one rule in Protocol Vulnerabilities, detailed below.

| Category | Rules Enabled |
|---|---|
| Botnets and Threat Intelligence | 5 of 5 |
| Viruses, Malware and Spyware | 4 of 4 |
| Hacking and Exploits | 5 of 5 |
| Peer to Peer and Dark Web | 3 of 3 |
| Attacks and Reconnaissance | 7 of 7 |
| Protocol Vulnerabilities | 11 of 12 |

See full configuration here:
[Fullscreen Image](https://img.irosec.com/u/ecDCea.jpg)

### Why Protocol Vulnerabilities is 11 of 12

The one disabled rule is the **Online Games** signature. This network is actively used for hosting and playing games, meaning game traffic would consistently trigger false positives under this rule. Disabling it prevents legitimate game traffic from being flagged or blocked while keeping all other protocol vulnerability detection fully active.

---

## What It Monitors

IDS/IPS runs across all four VLANs — JARVIS, FRIDAY, IoT Devices, and Guest Network. Given the homelab's exposure this includes:

- Inbound traffic to Plex (port 32400)
- Inbound traffic to Nginx Proxy Manager (HTTP/HTTPS)
- WireGuard VPN connection attempts (ports 51820/51822)
- All outbound and inter-VLAN traffic across all four networks

---

## Limitations

Unifi Threat Management is a solid first layer but has real limitations worth acknowledging:

- Log export is limited — alerts are not easily forwarded to an external SIEM without additional tooling
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
