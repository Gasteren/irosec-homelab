---
title: "Axios Supply Chain Attack"
description: "Date: April 1, 2026"
sidebar:
  order: 1
---

**Date:** April 1, 2026 
**Time to Diagnose:** ~30 minutes 
**Time to Resolve:** ~2 hours

---

## Impact

| Property | Detail |
|---|---|
| Affected Service | None - proactive response, no confirmed infection |
| Affected Device | Docker server (`10.10.1.20`) - highest risk asset assessed |
| Scope | Homelab-wide assessment across all Docker containers |
| Severity | Low (for irosec) - no containers pulled during attack window |

---

## Timeline

**~20:00** - Watched NetworkChuck's breakdown of the Axios npm supply chain attack. Axios versions 1.14.1 and 0.30.4 were confirmed malicious, published via a compromised maintainer account on March 31 between 00:21–03:29 UTC.

**~20:15** - Assessed all running Docker containers for exposure. Checked pull dates against the attack window. Confirmed no containers were pulled or rebuilt during the 2-hour malicious window.

**~20:20** - Identified the Node.js based containers as the highest-risk group. Confirmed each pins an Axios version well outside the compromised range. Assessed as safe.

**~20:30** - Created outbound firewall rule on UDM Pro blocking all traffic from Internal zone to C2 IP `142.11.206.73`. Syslog logging enabled on the rule.

**~20:40** - Switched IDS/IPS Detection Mode from Notify to Notify and Block across all VLANs (Server, Guest, IoT, Main).

**~21:00** - Added two high-severity custom detection rules on the Wazuh manager targeting the C2 IP and domain, mapped to MITRE ATT&CK T1071 and T1059.

**~21:30** - Validated both rules with `wazuh-logtest` against sample log lines. Wazuh manager restarted and confirmed running.

**~21:45** - Documented incident in irosec wiki under Lessons Learned.

---

## Root Cause

A threat actor compromised the npm account of the primary Axios maintainer and published two malicious versions of the package. Each version injected a hidden dependency (`plain-crypto-js@4.2.1`) containing a postinstall script that drops a cross-platform Remote Access Trojan. The RAT beacons to a C2 server every 60 seconds and self-deletes after execution, leaving no trace in `node_modules`.

With over 100 million weekly downloads, Axios is one of the most widely used JavaScript libraries in existence. Any developer environment or CI/CD pipeline that ran `npm install` during the 2-hour window without a committed lockfile was potentially compromised.

irosec was not directly affected - no containers were built or updated during the attack window, and the Node.js containers most likely to use Axios pin versions far outside the compromised range.

---

## IOCs

| Type | Value |
|---|---|
| IP Address | `142.11.206.73` |
| Domain | `sfrclak.com` |
| Malicious package | `plain-crypto-js@4.2.1` |
| Compromised version | `axios@1.14.1` |
| Compromised version | `axios@0.30.4` |

---

## Fix

### UDM Pro - Firewall Rule
Created outbound block rule on Internal → External zone targeting the C2 IP.

| Property | Value |
|---|---|
| Name | `IOC - Axios RAT C2 - 2026-04-01` |
| Source Zone | Internal (Any) |
| Destination | `142.11.206.73` |
| Action | Block |
| Protocol | All |
| Logging | Enabled |

### UDM Pro - IDS/IPS

| Setting | Before | After |
|---|---|---|
| Detection Mode | Notify | Notify and Block |

### Wazuh - Custom Rules

Two custom IOC rules were added to the local ruleset: one matching the C2 IP address, one matching the C2 domain. Both are set to the highest alert level and mapped to MITRE ATT&CK (T1071 Application Layer Protocol, T1059 Command and Scripting Interpreter). Both were validated with `wazuh-logtest` and confirmed to trigger.

---

## Prevention

**Broader prevention takeaway:** Supply chain attacks are particularly dangerous because they abuse implicit trust in legitimate, widely-used packages. The infection vector is the build step, not the running application - meaning a compromised system leaves no obvious runtime symptoms.

Key defences against this class of attack:

- **Always commit lockfiles** (`package-lock.json` / `yarn.lock`) and use `npm ci` instead of `npm install` in CI/CD pipelines. A committed lockfile would have blocked this attack entirely.
- **Pin dependency versions** explicitly rather than using ranges.
- **Monitor for unexpected outbound beacon traffic** - the 60-second C2 interval is a detectable pattern in network logs and SIEM alerting.
- **Subscribe to npm security advisories** for packages used in your stack.

This incident also demonstrates the value of having a SIEM with custom IOC rules in place before an incident occurs. The Wazuh rules deployed here will now alert on any future traffic matching these IOCs across all monitored agents.

---

## References
- [Socket.dev](https://socket.dev/blog/axios-npm-package-compromised)
- [The Hacker News](https://thehackernews.com/2026/03/axios-supply-chain-attack-pushes-cross.html)
- [Snyk - Technical Writeup](https://snyk.io/blog/axios-npm-package-compromised-supply-chain-attack-delivers-cross-platform/)
- [Malwarebytes - Analysis](https://www.malwarebytes.com/blog/news/2026/03/axios-supply-chain-attack-chops-away-at-npm-trust)
- [NetworkChuck - Video](https://www.youtube.com/watch?v=eGSsoSEppNU)