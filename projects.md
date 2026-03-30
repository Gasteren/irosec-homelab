# 🎯 Projects

This section contains hands-on project writeups from the irosec homelab — covering security deployments, hardening exercises, and detection scenarios run against real infrastructure.

The advantage of working on a live homelab rather than a sandboxed lab is that the traffic, logs, and events are real. A port scan shows up alongside actual Plex traffic. An IDS alert fires because something genuinely unexpected happened on a network that's actively used every day.

---

## ✅ Completed Projects

| Project | Description |
|---|---|
| [Hall of Fallen Heroes](/projects/hall-of-fallen-heroes) | Built and secured a self-hosted WoW guild death memorial app, identified a critical auth vulnerability, applied 7 security fixes. |
| [Homelab Documentation](/) | Built and published a full technical wiki documenting the entire homelab stack |
| [VLAN Segmentation](/projects/vlan-segmentation) | Designed and implemented four-VLAN network architecture across all devices |
| [Firewall Policy Design](/projects/firewall-policy) | Configured zone-based firewall with 66 rules across all VLANs on the Dream Machine Pro |
| [IDS/IPS Deployment](/projects/ids-ips-deployment) | Deployed Unifi Threat Management across all four VLANs with full detection category coverage and per-rule tuning |
| [Honeypot Per VLAN](/projects/honeypot) | Configured honeypot addresses on every VLAN for lateral movement and rogue device detection |
| [SIEM Deployment + Unifi Log Forwarding](/projects/siem) | Deployed Wazuh 4.14.3 on a dedicated Proxmox VM and onboarded all homelab hosts including Windows endpoints and Docker host, Forwarded Dream Machine Pro syslog to Wazuh with custom decoders and firewall rules for centralised correlation |
| [NPM Log Parsing](/projects/siem) | Configured Wazuh agent on Docker host to ingest Nginx Proxy Manager access logs across all proxy hosts for centralised web traffic visibility |

---

## ⏳ In Progress

| Project | Description | Status |
|---|---|---|
| Wazuh + Grafana Dashboard | Build a live security dashboard visualising alerts, log volume, and threat trends across all VLANs | ⏳ In Progress |

---

## 🔜 Planned Projects

| Project | Description |
|---|---|
| Port Scan Detection | Run Nmap against a homelab VM and verify detection and alerting end-to-end in the SIEM |
| SIEM Notifications | Configure email or Discord alerts for high severity Wazuh events |

---
