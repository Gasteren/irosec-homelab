# World of Warcraft In-Game Voice Chat Blocked by IDS/IPS

**Date:** December 2025  
**Time to Diagnose:** ~1 hour  
**Time to Resolve:** ~20 minutes  

---

## Impact

| Property | Detail |
|---|---|
| Affected Service | World of Warcraft in-game voice chat |
| Affected Device | Gaming PC on Main Network — FRIDAY (VLAN 4) |
| Scope | Single user, single application feature |
| Severity | Low — no data loss, no service outage, gaming session unaffected beyond voice |

---

## Timeline

**~19:00** — Joined a World of Warcraft group and attempted to connect to in-game voice chat. Unable to join any voice channel and could not hear other players.

**~19:05** — Initial assumption was an audio or driver issue. Used AI assistants (Copilot and Claude) to troubleshoot, which suggested checking Windows audio settings, microphone permissions, and audio drivers.

**~19:15** — Verified all Windows audio settings were correct. Microphone and speakers worked fine in other applications. Ruled out audio and driver issues.

**~19:20** — Tested Discord voice chat, which worked without any issues. This narrowed the problem to something specific to World of Warcraft's voice implementation rather than a system-wide audio or network problem.

**~19:30** — With Discord working and system audio confirmed fine, focus shifted to a network-level block specific to WoW traffic. Logged into the Unifi Dream Machine Pro controller to review logs.

**~19:45** — Found the root cause in the IDS/IPS logs. The Unifi Threat Management engine had flagged World of Warcraft in-game voice traffic as suspicious and blocked it silently. The block was caused by the **Online Games** signature under the Protocol Vulnerabilities detection category.

**~20:05** — Navigated to Threat Management settings in the Unifi controller. Disabled the Online Games rule specifically within the Protocol Vulnerabilities category. Left all 11 remaining rules in that category active.

**~20:10** — Rejoined World of Warcraft voice chat. Voice connected immediately and functioned normally.

---

## Root Cause

The Unifi IDS/IPS **Protocol Vulnerabilities** category includes an **Online Games** signature that is designed to detect certain game traffic patterns associated with protocol abuse. In this case it produced a false positive, flagging legitimate World of Warcraft in-game voice chat traffic as a threat and blocking it silently without any visible error on the client side.

Because the block happened at the network level without a user-facing error message, the initial symptoms — no voice, no error — pointed toward an audio or application issue rather than a firewall block. This made the root cause harder to find without checking the IDS logs directly.

---

## Fix

Disabled the **Online Games** signature specifically within the Protocol Vulnerabilities category in Unifi Threat Management.

| Category | Before | After |
|---|---|---|
| Protocol Vulnerabilities | 12 of 12 enabled | 11 of 12 enabled |

All other detection categories remain fully enabled. Detection coverage for all non-gaming traffic is unaffected.

---

## Prevention

The Online Games rule remains disabled permanently as the network is actively used for both hosting and playing games. Re-enabling it would cause recurring false positives against legitimate traffic.

**Broader prevention takeaway:** Silent network-level blocks with no client-side error message are particularly difficult to diagnose because they mimic application or system issues. Going forward, the IDS/IPS alert dashboard in the Unifi controller will be an earlier step in any troubleshooting process where a service works on one application but not another.

This incident also reinforces the case for deploying a SIEM — with centralised log aggregation, an IDS block would surface immediately alongside other relevant logs rather than requiring a manual login to the Unifi controller to discover.
