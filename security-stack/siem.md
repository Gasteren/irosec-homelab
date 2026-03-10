# SIEM

This page documents the Security Information and Event Management (SIEM) setup in the irosec lab, used for log aggregation, correlation, alerting, and vulnerability detection.

---

## Stack

| Tool | Role | Status |
|---|---|---|
| Wazuh 4.14.3 | SIEM / EDR / Log analysis / Vulnerability detection | ✅ Active |

---

## Infrastructure

| Host | IP | Role |
|---|---|---|
| Wazuh Server (Proxmox VM) | `192.168.178.200` | SIEM manager + dashboard |
| UniFi Dream Machine Pro | `192.168.178.1` | Gateway / syslog source |
| Docker Host | `192.168.178.233` | Agent + NPM log source |
| Windows-Carlo-PC | Agent ID: 001 | Windows endpoint |
| Windows-Demy-PC | Agent ID: 002 | Windows endpoint |

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
| Windows-Carlo-PC | Windows event logs | Wazuh agent | ✅ Active |
| Windows-Demy-PC | Windows event logs | Wazuh agent | ✅ Active |

---

## Wazuh Server Configuration

### Syslog Receivers (`/var/ossec/etc/ossec.conf`)

```xml
<remote>
  <connection>syslog</connection>
  <port>514</port>
  <protocol>udp</protocol>
  <allowed-ips>0.0.0.0/0</allowed-ips>
  <local_ip>192.168.178.200</local_ip>
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

This creates the `wazuh-archives-*` index in OpenSearch, allowing you to search all ingested logs — not just those that triggered rules.

---

## UniFi Integration

UniFi is configured under **CyberSecure → Traffic Logging → SIEM Server** pointing to `192.168.178.200:514`.

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
  <rule id="100002" level="10" frequency="20" timeframe="60">
    <if_matched_sid>100001</if_matched_sid>
    <same_srcip/>
    <description>UniFi: Possible port scan or brute force from $(srcip)</description>
    <group>firewall,port_scan,</group>
  </rule>
</group>
```

> **Note:** Most hits on rule 100001 are from Cloudflare IPs (`141.101.x.x`, `162.159.x.x`) — legitimate traffic through the Cloudflare proxy.

---

## Docker Host Agent

Agent name: `Docker-Containers` (Agent ID: 003)

Connected to `192.168.178.200:1514/tcp`.

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

### Current Status (as of March 2026)

| Agent | Critical | High | Notes |
|---|---|---|---|
| Docker-Containers | 9 | ~658 | Fully patched; remaining are unpatched Ubuntu 22.04 CVEs |
| Windows-Carlo-PC | 1 | ~105 | Fully patched; remaining are unpatched Windows 11 CVEs |
| Windows-Demy-PC | 2 | 9 | Run Windows Update to resolve 2025 CVEs |

### Packages Cleaned Up

- Removed Node.js 12 + ffmpeg (Pterodactyl leftovers) from Docker host → reduced critical CVEs from 53 to 9
- Removed Python 3.12.4, openclaw, updated 7-Zip, Git, Docker Desktop, Notepad++, Visual Studio on Carlo-PC
- Updated Steam on both Windows PCs

### Known False Positives

- **CVE-2026-24811** — affects CERN ROOT framework (physics research tool). ROOT is not installed on any machine in this lab. This CVE can be safely ignored.

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

## Pending / Next Steps

- [ ] Write custom NPM log decoder to parse response codes, URLs, and client IPs
- [ ] Create alert rules for 401/403 spikes and 404 scanning on NPM
- [ ] Alert on non-Cloudflare IPs hitting services directly (Cloudflare bypass detection)
- [ ] Set up email or Slack/Discord notifications for high severity alerts
- [ ] Enable File Integrity Monitoring (FIM) on Docker host config directories
- [ ] Run Windows Update on Demy-PC to resolve 2025 CVEs
