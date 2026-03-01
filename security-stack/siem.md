# SIEM

This page documents the Security Information and Event Management (SIEM) setup in the irosec lab, used for log aggregation, correlation, and alerting.

---

## Planned Stack

| Tool | Role | Status |
|---|---|---|
| Wazuh | SIEM / EDR / Log analysis | 🔜 Planned |
| Grafana | Dashboard / Visualization | 🔜 Planned |

---

## Why Wazuh

Wazuh is an open-source SIEM used in real SOC environments. It provides:

- Agent-based log collection from VMs and endpoints
- File integrity monitoring (FIM)
- Vulnerability detection
- Active response / automated blocking
- Pre-built rules mapped to MITRE ATT&CK

---

## Planned Log Sources

| Source | Type | Method |
|---|---|---|
| Proxmox host | Syslog | Wazuh agent |
| Docker host VM | Syslog + container logs | Wazuh agent |
| Unifi gateway | Syslog | Syslog forwarder |

---

## Deployment Plan

1. Spin up Wazuh server VM on Proxmox
2. Deploy Wazuh agents on all existing VMs
3. Configure Unifi syslog forwarding to Wazuh
4. Build Grafana dashboards on top of Wazuh data
5. Document alert rules and tuning process

> 📌 This page will be updated as Wazuh is deployed.
