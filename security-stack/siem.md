---
title: "SIEM"
description: "This page documents the Security Information and Event Management (SIEM) setup in the irosec lab, used for log aggreg..."
sidebar:
  order: 3
---

This page documents the Security Information and Event Management (SIEM) setup in the irosec lab, used for log aggregation, correlation, alerting, and vulnerability detection.

---

## Stack

| Tool | Role | Status |
|---|---|---|
| Wazuh 4.x | SIEM / EDR / Log analysis / Vulnerability detection | ✅ Active |

---

## Infrastructure

| Host | IP | Role |
|---|---|---|
| Wazuh Server (Proxmox VM) | `10.10.1.30` | SIEM manager + dashboard |
| UniFi Dream Machine Pro | `10.10.1.1` | Gateway / syslog source |
| Docker Host | `10.10.1.20` | Agent + NPM log source |
| Workstation-01 | Agent | Windows endpoint |
| Workstation-02 | Agent | Windows endpoint |

Addresses are illustrative.

---

## Why Wazuh

Wazuh is an open-source SIEM used in real SOC environments. It provides:

- Agent-based log collection from VMs and endpoints
- File integrity monitoring (FIM)
- Vulnerability detection with CVE correlation
- Active response / automated blocking
- 3,000+ pre-built rules mapped to MITRE ATT&CK
- GeoLocation enrichment on alerts
- Built-in dashboards for endpoint security, threat intelligence, and compliance

---

## Log Sources

| Source | Type | Method | Status |
|---|---|---|---|
| UniFi Dream Machine Pro | Syslog (UDP 514) | Syslog forwarder | ✅ Active |
| Docker Host | Syslog + journald + NPM logs | Wazuh agent | ✅ Active |
| Workstation-01 | Windows event logs | Wazuh agent | ✅ Active |
| Workstation-02 | Windows event logs | Wazuh agent | ✅ Active |

---

## Wazuh Server Configuration

### Syslog Receivers (`/var/ossec/etc/ossec.conf`)

```xml
<remote>
 <connection>syslog</connection>
 <port>514</port>
 <protocol>udp</protocol>
 <allowed-ips>10.10.1.1</allowed-ips>
 <local_ip>10.10.1.30</local_ip>
</remote>
<remote>
 <connection>secure</connection>
 <port>1514</port>
 <protocol>tcp</protocol>
 <queue_size>131072</queue_size>
</remote>
```

### Archives (for all logs, not just alerts)

In `/var/ossec/etc/ossec.conf`:
```xml
<global>
 <logall>yes</logall>
 <logall_json>yes</logall_json>
</global>
```

In `/etc/filebeat/filebeat.yml`:
```yaml
archives:
 enabled: true
```

This creates the `wazuh-archives-*` index in OpenSearch, allowing you to search all ingested logs - not just those that triggered rules.

---

## UniFi Integration

UniFi is configured under **CyberSecure → Traffic Logging → SIEM Server** pointing to `10.10.1.30:514`.

### Firewall Rules (Proxmox)
- UDP 514 inbound (syslog)
- TCP 1514 inbound (agent communication)

### Searching UniFi logs in Discover
Use index pattern `wazuh-archives-*` with filter:
```
predecoder.hostname: "Dream-Machine-Pro"
```

### Custom Decoder (`/var/ossec/etc/decoders/unifi_decoder.xml`)

```xml
<decoder name="unifi-dnat">
 <prematch>PREROUTING-DNAT</prematch>
 <regex>SRC=(\S+) DST=(\S+) \.+ PROTO=(\w+) SPT=(\d+) DPT=(\d+)</regex>
 <order>srcip,dstip,proto,srcport,dstport</order>
</decoder>
```

### Custom Rules (`/var/ossec/etc/rules/unifi_rules.xml`)

```xml
<group name="unifi,firewall,">
 <rule id="100001" level="6">
 <decoded_as>unifi-dnat</decoded_as>
 <description>UniFi: Port forward connection attempt from $(srcip)</description>
 <group>firewall,connection_attempt,</group>
 </rule>
 <rule id="100002" level="10" frequency="N" timeframe="N">
 <if_matched_sid>100001</if_matched_sid>
 <same_srcip/>
 <description>UniFi: Possible port scan or brute force from $(srcip)</description>
 <group>firewall,port_scan,</group>
 </rule>
</group>
```

> **Note:** Most hits on the connection attempt rule are legitimate traffic arriving through the CDN proxy in front of the public services. Thresholds for the correlation rule are tuned against that baseline and are not published.

---

## Docker Host Agent

Agent name: `Docker-Containers`, connected to the manager over TCP 1514.

### NPM Log Collection (`/var/ossec/etc/ossec.conf` on Docker host)

```xml
<localfile>
 <log_format>syslog</log_format>
 <location>/data/compose/11/data/logs/proxy-host-*_access.log</location>
</localfile>
```

NPM logs are stored at `/data/compose/11/data/logs/` and all `proxy-host-*` files are tracked automatically.

---

## Dashboard Index Patterns

| Index Pattern | Contents |
|---|---|
| `wazuh-alerts-*` | Alerts only (rules that fired) |
| `wazuh-archives-*` | All ingested logs |

The `wazuh-archives-*` pattern must be created manually in **Dashboard Management → Index Patterns**.

---

## Vulnerability Detection

Wazuh automatically scans all connected agents for known CVEs and correlates against the NVD database.

### Approach

All agents are fully patched at the OS level. The remaining findings are CVEs in the distribution's own packages that have no upstream fix yet, and they are reviewed rather than treated as actionable. Per-host counts are not published.

### Packages Cleaned Up

- Removed a legacy Node.js runtime and ffmpeg build (leftovers from a decommissioned game server panel) from the Docker host, which eliminated the majority of the critical findings
- Removed unused runtimes and updated developer tooling on the workstations

### Known False Positives

- **CVE-2026-24811** - affects CERN ROOT framework (physics research tool). ROOT is not installed on any machine. This CVE can be safely ignored.

---

## Pterodactyl Removal

Pterodactyl Wings and Queue Worker were found installed on the Docker host and have been fully removed:

```bash
systemctl stop wings pteroq
systemctl disable wings pteroq
rm /etc/systemd/system/wings.service
rm /etc/systemd/system/pteroq.service
rm -rf /etc/pterodactyl /var/www/pterodactyl
rm /usr/local/bin/wings
systemctl daemon-reload
```

---
