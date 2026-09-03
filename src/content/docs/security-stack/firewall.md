---
title: "Firewall & Rules"
description: "The perimeter firewall for the irosec homelab is handled by the Dream Machine Pro. This page documents the zone matri..."
sidebar:
  order: 1
---

The perimeter firewall for the irosec homelab is handled by the Dream Machine Pro. This page documents the zone matrix, firewall policies, and the reasoning behind key decisions.

---

## Firewall Device

| Property | Value |
|---|---|
| Device | Unifi Dream Machine Pro |
| Mode | NAT + Stateful Firewall |
| Rule Count | 66 active policies |
| Protocol Support | IPv4 & IPv6 |

---

## Zone Matrix

The Dream Machine Pro uses a zone-based firewall model. The matrix below shows the default policy between each zone pair:

| Source → Destination | Internal | External | Gateway | VPN | Hotspot | DMZ |
|---|---|---|---|---|---|---|
| **Internal** | Allow All | Allow All | Allow All | Allow All | Allow All | Allow All |
| **External** | Allow Return | Allow Return | Allow Return | Allow Return | Allow Return | Allow Return |
| **Gateway** | Allow All | Allow All | - | Allow All | Allow All | Allow All |
| **VPN** | Allow All | Allow All | Allow All | Allow All | Allow All | Allow All |
| **Hotspot** | Allow Return | Allow All | Allow Return | Allow Return | Block All | Block All |
| **DMZ** | Allow Return | Allow All | Allow Return | Allow Return | Block All | Block All |

Key observations:
- External traffic can only return existing sessions - no unsolicited inbound connections
- Hotspot and DMZ zones are isolated from each other and cannot initiate connections to Internal
- VPN clients have full network access once authenticated

---

## VLAN Layout

| Name | VLAN ID | Subnet | Zone |
|---|---|---|---|
| Server Network - JARVIS | 1 | 10.10.1.0/24 | Internal |
| Guest Network | 2 | 10.10.2.0/24 | Hotspot |
| IoT Devices | 3 | 10.10.3.0/24 | Internal |
| Main Network - FRIDAY | 4 | 10.10.4.0/24 | Internal |

---

## Firewall Rules

The full ruleset is not published. The structure, from top to bottom, is:

| Group | Purpose |
|---|---|
| IPv6 housekeeping | ICMPv6 neighbour discovery between External and Gateway, required for IPv6 to function |
| Inbound port forwards | The three externally reachable services (Plex, reverse proxy, WireGuard) forwarded to their internal hosts |
| Return traffic | Stateful allow for established sessions |
| Local service discovery | mDNS between Internal and Gateway |
| Block invalid traffic | Drops malformed or spoofed packets before any allow rule is evaluated |
| Default deny | Catches anything not explicitly allowed above |

---

## Key Decisions & Reasoning

**WireGuard VPN** is exposed externally to allow secure remote access to the homelab without exposing individual services directly. This is preferable to opening multiple ports per service.

**Plex and Nginx Proxy Manager** are the only application-level services with direct port forwards. All other services are accessed either via the Nginx reverse proxy or over VPN.

**Block Invalid Traffic** sits near the top of the ruleset to drop malformed packets early before they reach any allow rules - a basic but effective hardening measure.

**Guest Network** is mapped to the Hotspot zone which prevents it from initiating connections to Internal zones, keeping guest devices fully isolated from servers and trusted clients.

---

![Firewall Policy UI](https://img.irosec.com/u/hzIxB3.jpg)
