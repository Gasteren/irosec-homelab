---
title: "UniFi SAB-067"
description: "On 26 August 2026 Ubiquiti published SAB-067 covering 22 UniFi vulnerabilities. The Dream Machine Pro auto-updated to a fixed UniFi OS release; this page records triage, verification, validation, and exposure review."
sidebar:
  order: 3
---

On 26 August 2026 Ubiquiti published Security Advisory Bulletin 067, disclosing and patching 22 UniFi vulnerabilities, three rated CVSS 10.0. The Dream Machine Pro auto-updated to a fixed UniFi OS release before manual intervention. This page documents triage by footprint, confirmation that the fix landed, post-update validation, and whether management exposure made the bugs reachable.

> **Snapshot as of 5 September 2026.** Firmware versions and status below reflect that date. Check the console directly for current state before relying on any version claim here.

---

## Incident Summary

| Property | Value |
|---|---|
| Advisory | [Ubiquiti SAB-067](https://community.ui.com/releases/Security-Advisory-Bulletin-067/fc4a3488-7c43-4628-8bab-f715e96dbfc9) (26 August 2026) |
| Device | UniFi Dream Machine Pro (UDM-Pro) |
| Scope | UniFi OS console only (no Protect, Talk, Access, or self-hosted UniFi OS Server) |
| Auto-update fired | 28 August 2026, ~15:49 CEST |
| Fixed boundary (consoles) | UniFi OS 5.1.31 or later (NAS devices 5.1.32+) |
| Running version after update | UniFi OS 5.1.31 (build `UDMPRO.al324.v5.1.31.5acc35d.260819.1714`) |
| Public PoC / CISA KEV (as of ~28 August 2026) | None known |

---

## Impact

Practical risk stayed small: the management interface was not reachable from the public internet. The serious case for a console is chaining unauthenticated CRLF authentication bypass into privilege escalation, which can take an attacker from no credentials to full gateway control when the management plane is reachable.

Headline coverage included CVE-2026-77539 (command injection). That CVE targets self-hosted UniFi OS Server and does not apply to this console.

---

## Timeline

| Step | When | What |
|---|---|---|
| 1 | 26 August 2026 | Ubiquiti publishes SAB-067 across Protect, Talk, Access, Network, Connect, and UniFi OS |
| 2 | 28 August 2026, ~15:49 CEST | Console auto-update pulls and applies UniFi OS 5.1.31; no manual patch step |
| 3 | Same window | Confirm running version against the SAB-067 fixed-version table for the console product family (Settings → System → Updates) |
| 4 | Post-update | Validate WAN, LAN/Wi-Fi, DHCP/DNS, throughput vs baseline, and firewall / port-forward / VLAN config integrity |
| 5 | Post-patch review | Recheck management exposure, admin accounts, and unexpected config drift vs documented baseline |

---

## Relevant CVEs

| CVE | Type | CVSS | Preconditions | Applies here? |
|---|---|---|---|---|
| [CVE-2026-77534](https://nvd.nist.gov/vuln/detail/CVE-2026-77534) | Improper access control, privilege escalation | 9.9 | Low-privileged account, network access | Yes |
| [CVE-2026-77549](https://nvd.nist.gov/vuln/detail/CVE-2026-77549) | CRLF injection, authentication bypass | 9.0 | Unauthenticated, network access, conditional | Yes |
| [CVE-2026-77550](https://nvd.nist.gov/vuln/detail/CVE-2026-77550) | CRLF injection, authentication bypass | 10.0 | Unauthenticated, network access, conditional | Yes |
| [CVE-2026-77539](https://nvd.nist.gov/vuln/detail/CVE-2026-77539) | Improper input validation, command injection | 9.1 | High-privileged account; UniFi OS Server | No (self-hosted server, not console) |

The dangerous path is chaining, not any single score: unauthenticated CRLF bypass (77549 / 77550) to a low-privileged session, then 77534 to full control. Ubiquiti patched the batch together for that reason.

---

## Root Cause

Not an active compromise on this lab. The lesson is exposure and verification posture around a high-severity UniFi OS bulletin:

- Automatic updates applied the fix without a manual click
- Auto-update is not proof of a fixed build; the running version must be checked against the advisory table
- Unauthenticated, network-reachable bugs only become a clean path in if the management interface is reachable from untrusted networks

---

## Fix

| Step | Action |
|---|---|
| 1 | Rely on the console auto-update to the fixed UniFi OS line (already enabled) |
| 2 | Confirm Settings → System → Updates shows UniFi OS 5.1.31, at or above 5.1.31 for consoles |
| 3 | Match the console product family to the SAB-067 fixed-version table; do not assume "latest" equals "fixed" |
| 4 | Keep version screenshots before/after for records |

---

## Evidence

### Running version (headline proof)

```
# ubnt-device-info summary
              Family: UniFi Dream Machine (UDM)
               Model: UniFi Dream Machine Pro (UDM-Pro)
 Default MAC address: 6c:63:f8:XX:XX:XX
            Firmware: 5.1.31 (5.1.31)

# build string
UDMPRO.al324.v5.1.31.5acc35d.260819.1714
```

The device reports exactly 5.1.31, the SAB-067 fixed boundary for consoles. This proves the fixed code is running regardless of how it got there.

### Update timing (config-migration burst)

UniFi OS has no single "firmware installed" log line. The reliable signal is the config-schema migration that runs when new firmware first boots. It ran on 28 August, 15:49 to 15:50 CEST:

```
Aug 28 15:49:52 Dream-Machine-Pro ubios-udapi-server: config-migrate-helper: Starting config .versionFormat 'v2' migration ...
Aug 28 15:49:52 Dream-Machine-Pro ubios-udapi-server: config-migrate-helper: Migrating config .versionDetail.firewall/filter from 5 to 6
Aug 28 15:49:52 Dream-Machine-Pro ubios-udapi-server: config-migrate-helper: Migrating config .versionDetail.firewall/filter from 7 to 8
Aug 28 15:49:55 Dream-Machine-Pro ubios-udapi-server: config-migrate-helper: Migrating config .versionDetail.system from 7 to 8
Aug 28 15:49:57 Dream-Machine-Pro ubios-udapi-server: config-migrate-helper: Finished config .versionFormat 'v2' migration ...
```

Nearly every subsystem schema was bumped in one pass (firewall, interfaces, DHCP, VPN, system). A routine config change does not touch that many schemas at once; a firmware upgrade does.

---

## Validation

| Check | Result |
|---|---|
| Connectivity | WAN up; LAN and Wi-Fi clients reconnect; no DHCP or DNS regressions |
| Throughput | Speed test in line with baseline |
| Config integrity | Firewall rules, port forwards, and VLANs unchanged vs documented baseline; migration log confirms schema upgrade, not reset |

---

## Key Decisions & Reasoning

**Triage by footprint first.** Four console-relevant CVEs out of 22. CVE-2026-77539 was noise for this hardware.

**Auto-update is a control, not a substitute for verification.** The value added here was confirming the fixed version and validating the network after the update, not clicking Apply.

**Know the device's evidence trail.** UniFi OS has no clean "updated" line, so the version string and the config-migration burst are the proof. Fingerprint refreshes and `apt` jobs are decoys.

**Document a baseline.** Firewall, forwards, VLANs, and expected version make post-patch diffs fast. Admin accounts and sessions were reviewed in this pass; no unexpected accounts or unfamiliar sessions.

Related: [/security-stack/](/security-stack/)

---

## References

| Source | Notes |
|---|---|
| [Ubiquiti Security Advisory Bulletin 067](https://community.ui.com/releases/Security-Advisory-Bulletin-067/fc4a3488-7c43-4628-8bab-f715e96dbfc9) | Published 26 August 2026 |
| [CVE-2026-77534](https://nvd.nist.gov/vuln/detail/CVE-2026-77534) | UniFi OS, privilege escalation (9.9) |
| [CVE-2026-77549](https://nvd.nist.gov/vuln/detail/CVE-2026-77549) | UniFi OS, CRLF authentication bypass (9.0) |
| [CVE-2026-77550](https://nvd.nist.gov/vuln/detail/CVE-2026-77550) | UniFi OS, CRLF authentication bypass (10.0) |
| [CVE-2026-77539](https://nvd.nist.gov/vuln/detail/CVE-2026-77539) | UniFi OS Server; not applicable to console appliances |