---
title: "UniFi SAB-067 Critical Vulnerabilities"
description: "Date: 28 August 2026"
sidebar:
  order: 3
---

**Date:** 28 August 2026 
**Time to Diagnose:** ~15 minutes (footprint triage) 
**Time to Resolve:** Auto-patched by console; ~30 minutes hands-on verification

> **Snapshot as of 5 September 2026.** Firmware versions and status below reflect that date. Check the console directly before relying on any version claim here.

---

## Impact

| Property | Detail |
|---|---|
| Affected Service | None - no confirmed compromise; console auto-patched |
| Affected Device | UniFi Dream Machine Pro (UDM-Pro) |
| Scope | UniFi OS console only (no Protect, Talk, Access, or self-hosted UniFi OS Server) |
| Severity | Low (for irosec) - management plane not internet-exposed; no public PoC or known exploitation |

---

## Timeline

**26 August 2026** - Ubiquiti publishes Security Advisory Bulletin 067: 22 UniFi vulnerabilities, three rated CVSS 10.0, across Protect, Talk, Access, Network, Connect, and UniFi OS. Triaged the console footprint - four CVEs relevant to a UDM-Pro; CVE-2026-77539 excluded as UniFi OS Server only.

**28 August 2026, ~15:49 CEST** - Console auto-update pulls and applies UniFi OS 5.1.31. No manual patch step. Confirmed from the config-schema migration burst in the logs (firewall, interfaces, DHCP, VPN, system all bumped in one pass).

**Post-update** - Confirmed running version 5.1.31 via `ubnt-device-info summary`, matched against the SAB-067 fixed-version table for the UDM product family.

**Post-update** - Validated WAN, LAN/Wi-Fi, DHCP/DNS, and firewall / port-forward / VLAN config integrity against documented baseline. Migration log confirmed schema upgrade, not reset.

**Post-patch review** - Rechecked management exposure (not internet-reachable), admin accounts (no unexpected accounts or sessions), and config drift versus baseline.

---

## Root Cause

Not an active compromise on this lab. Ubiquiti disclosed and patched 22 UniFi vulnerabilities in a single bulletin. For a UniFi OS console the meaningful risk is chaining: an unauthenticated attacker uses a CRLF authentication-bypass bug (CVE-2026-77549 / 77550) to land a low-privileged session, then uses the access-control bug (CVE-2026-77534) to escalate to full gateway control. That chain only opens if the management interface is reachable from an untrusted network.

The fix reached this console through automatic updates rather than a manual patch. Two lessons stand out. First, auto-update firing is not proof the device is on a fixed build - the running version has to be checked against the advisory table. Second, the fixed firmware landed roughly two days after disclosure because Ubiquiti staggers its rollout across the fleet; that is a normal but real exposure window that manually forcing the update would have closed sooner.

CVE-2026-77539 drew headline coverage but targets self-hosted UniFi OS Server, not console appliances, so it did not apply here.

---

## Relevant CVEs

No IOCs apply - this was a vulnerability disclosure and patch, not an active intrusion. The equivalent reference data is the CVE set for the console.

| CVE | Type | CVSS | Preconditions | Applies here? |
|---|---|---|---|---|
| [CVE-2026-77534](https://nvd.nist.gov/vuln/detail/CVE-2026-77534) | Improper access control, privilege escalation | 9.9 | Low-privileged account, network access | Yes |
| [CVE-2026-77549](https://nvd.nist.gov/vuln/detail/CVE-2026-77549) | CRLF injection, authentication bypass | 9.0 | Unauthenticated, network access, conditional | Yes |
| [CVE-2026-77550](https://nvd.nist.gov/vuln/detail/CVE-2026-77550) | CRLF injection, authentication bypass | 10.0 | Unauthenticated, network access, conditional | Yes |
| [CVE-2026-77539](https://nvd.nist.gov/vuln/detail/CVE-2026-77539) | Improper input validation, command injection | 9.1 | High-privileged account; UniFi OS Server | No (self-hosted server, not console) |

---

## Fix

### UDM Pro - Firmware Update

| Property | Value |
|---|---|
| Update mechanism | Automatic console auto-update (already enabled) |
| Fixed boundary (consoles) | UniFi OS 5.1.31 or later (NAS devices 5.1.32+) |
| Running version | UniFi OS 5.1.31 (build `UDMPRO.al324.v5.1.31.5acc35d.260819.1714`) |
| Applied | 28 August 2026, ~15:49 CEST |

### Verification - Running Version (headline proof)

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

### Verification - Update Timing (config-migration burst)

UniFi OS has no single "firmware installed" log line. The reliable signal is the config-schema migration that runs when new firmware first boots. It ran on 28 August, 15:49 to 15:50 CEST:

```
Aug 28 15:49:52 Dream-Machine-Pro ubios-udapi-server: config-migrate-helper: Starting config .versionFormat 'v2' migration ...
Aug 28 15:49:52 Dream-Machine-Pro ubios-udapi-server: config-migrate-helper: Migrating config .versionDetail.firewall/filter from 5 to 6
Aug 28 15:49:52 Dream-Machine-Pro ubios-udapi-server: config-migrate-helper: Migrating config .versionDetail.firewall/filter from 7 to 8
Aug 28 15:49:55 Dream-Machine-Pro ubios-udapi-server: config-migrate-helper: Migrating config .versionDetail.system from 7 to 8
Aug 28 15:49:57 Dream-Machine-Pro ubios-udapi-server: config-migrate-helper: Finished config .versionFormat 'v2' migration ...
```

Nearly every subsystem schema was bumped in one pass (firewall, interfaces, DHCP, VPN, system). A routine config change does not touch that many schemas at once; a firmware upgrade does. Fingerprint-signature refreshes and the daily `apt` job are decoys, not the SAB-067 fix.

### Validation

| Check | Result |
|---|---|
| Connectivity | WAN up; LAN and Wi-Fi clients reconnect; no DHCP or DNS regressions |
| Throughput | Speed test in line with baseline |
| Config integrity | Firewall rules, port forwards, and VLANs unchanged vs documented baseline; migration log confirms schema upgrade, not reset |
| Exposure | Management interface confirmed not reachable from the public internet |

---

## Prevention

**Broader prevention takeaway:** Auto-update closed the hole, but auto-update is a control, not verification. Because vendors stage rollouts, the fixed build can land days after public disclosure - a window in which the vulnerability is known and the device is still unpatched. For critical, network-reachable bugs, the mature move is to check the advisory when it drops and force the update rather than wait for the fleet rollout to reach you.

Key defences against this class of exposure:

- **Triage by footprint first.** Map each CVE to your actual hardware. Four of 22 applied to this console; CVE-2026-77539 was noise for a UDM-Pro.
- **Verify the running version against the advisory table.** Auto-update firing does not prove a fixed build is installed.
- **Keep the management plane off the public internet.** Unauthenticated, network-reachable bugs only become a clean attack path when the management interface is reachable from untrusted networks.
- **For critical CVEs, force the update manually.** Do not rely on the staggered auto-rollout to close a critical exposure on its own schedule.
- **Document a baseline.** Firewall rules, port forwards, VLANs, and expected version make post-patch diffs fast and drift obvious.

This incident also reinforces the value of knowing each device's evidence trail before you need it. UniFi OS has no clean "updated" log line, so the version string and the config-migration burst are what prove the patch landed.

Related: [/security-stack/](/security-stack/)

---

## References
- [Ubiquiti Security Advisory Bulletin 067](https://community.ui.com/releases/Security-Advisory-Bulletin-067/fc4a3488-7c43-4628-8bab-f715e96dbfc9) - primary advisory (26 August 2026)
- [CVE-2026-77534](https://nvd.nist.gov/vuln/detail/CVE-2026-77534) - UniFi OS, privilege escalation (9.9)
- [CVE-2026-77549](https://nvd.nist.gov/vuln/detail/CVE-2026-77549) - UniFi OS, CRLF authentication bypass (9.0)
- [CVE-2026-77550](https://nvd.nist.gov/vuln/detail/CVE-2026-77550) - UniFi OS, CRLF authentication bypass (10.0)
- [CVE-2026-77539](https://nvd.nist.gov/vuln/detail/CVE-2026-77539) - UniFi OS Server; not applicable to console appliances
