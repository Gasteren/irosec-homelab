# 🎯 Projects

This section contains hands-on project writeups from the irosec homelab — covering security deployments, hardening exercises, and detection scenarios run against real infrastructure.

The advantage of working on a live homelab rather than a sandboxed lab is that the traffic, logs, and events are real. A port scan shows up alongside actual Plex traffic. An IDS alert fires because something genuinely unexpected happened on a network that's actively used every day.

---

## ✅ Completed Projects

| Project | Description |
|---|---|
| [Homelab Documentation](/) | Built and published a full technical wiki documenting the entire homelab stack |
| [VLAN Segmentation](/projects/vlan-segmentation) | Designed and implemented four-VLAN network architecture across all devices |
| [Firewall Policy Design](/projects/firewall-policy) | Configured zone-based firewall with 66 rules across all VLANs on the Dream Machine Pro |
| [IDS/IPS Deployment](/projects/ids-ips-deployment) | Deployed Unifi Threat Management across all four VLANs with full detection category coverage and per-rule tuning |
| [Honeypot Per VLAN](/projects/honeypot) | Configured honeypot addresses on every VLAN for lateral movement and rogue device detection |

---

## ⏳ In Progress

| Project | Description | Status |
|---|---|---|
| SIEM Deployment | Deploy Wazuh on a dedicated Proxmox VM and onboard all homelab hosts |⏳ In Progress |
| Unifi Log Forwarding | Forward Dream Machine Pro logs to Wazuh for centralised correlation | ⏳ In Progress |

---

## 🔜 Planned Projects

| Project | Description |
|---|---|
| Wazuh + Grafana Dashboard | Build a live security dashboard visualising alerts, log volume, and threat trends across all VLANs |
| Port Scan Detection | Run Nmap against a homelab VM and verify detection and alerting end-to-end in the SIEM |

---
