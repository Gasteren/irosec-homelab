# 🔒 Security Stack

This section documents the security tooling being deployed across the irosec homelab — covering perimeter defense, intrusion detection, log management, and monitoring.

Unlike a purpose-built security lab, this tooling is being applied to a real, active environment running live services. That means real traffic, real logs, and real events to work with.

---

## 📄 Pages

- [Firewall & Rules](/security-stack/firewall) — Firewall configuration, rules, and traffic policies
- [IDS/IPS](/security-stack/ids-ips) — Intrusion detection and prevention setup
- [SIEM](/security-stack/siem) — Log aggregation, alerting, and threat detection

---

## 🗺️ Stack Overview

| Layer | Tool | Status |
|---|---|---|
| Firewall | Unifi Gateway | ✅ Active |
| IDS/IPS | Unifi Threat Management | ✅ Active |
| SIEM | Wazuh | ✅ Active |
| Log Visualization | *(Grafana — planned)* | 🔜 Planned |

---

*This section grows as new tools are deployed and configured...*
