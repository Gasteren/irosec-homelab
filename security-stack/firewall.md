# Firewall & Rules

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
| **Gateway** | Allow All | Allow All | — | Allow All | Allow All | Allow All |
| **VPN** | Allow All | Allow All | Allow All | Allow All | Allow All | Allow All |
| **Hotspot** | Allow Return | Allow All | Allow Return | Allow Return | Block All | Block All |
| **DMZ** | Allow Return | Allow All | Allow Return | Allow Return | Block All | Block All |

Key observations:
- External traffic can only return existing sessions — no unsolicited inbound connections
- Hotspot and DMZ zones are isolated from each other and cannot initiate connections to Internal
- VPN clients have full network access once authenticated

---

## VLAN Layout

| Name | VLAN ID | Subnet | Zone |
|---|---|---|---|
| Server Network — JARVIS | 1 | 192.168.178.0/24 | Internal |
| Guest Network | 2 | 192.168.2.0/24 | Hotspot |
| IoT Devices | 3 | 192.168.69.0/24 | Internal |
| Main Network — FRIDAY | 4 | 192.168.5.0/24 | Internal |

---

## Firewall Rules

| Rule Name | Action | Protocol | Src. Zone | Dst. Zone | Dst. Port | Notes |
|---|---|---|---|---|---|---|
| Allow Neighbor Advertisements | Allow | ICMPv6 | External | Gateway | Any | IPv6 NDP — required for IPv6 operation |
| Allow Neighbor Solicitations | Allow | ICMPv6 | External | Gateway | Any | IPv6 NDP — required for IPv6 operation |
| Allow Port Forward Plex | Allow | TCP/UDP | External | Internal | 32400 | Forwards Plex traffic to Docker host |
| Allow Port Forward Proxy Manager | Allow | TCP/UDP | External | Internal | Multiple | Forwards HTTP/HTTPS to Nginx Proxy Manager |
| Allow Port Forward Wireguard | Allow | TCP/UDP | External | Internal | 51820 | WireGuard VPN tunnel entry point |
| Allow Return Traffic | Allow | All | Multiple | Multiple | Any | Stateful — allows return traffic for established sessions |
| Allow WireGuard VPNs | Allow | UDP | External | Gateway | 51822 | WireGuard VPN on gateway |
| Allow mDNS | Allow | UDP | Internal | Gateway | 5353 | Multicast DNS for local service discovery |
| Block Invalid Traffic | Block | All | Multiple | Multiple | Any | Drops malformed or spoofed packets |
| Allow All Traffic | Allow | All | Multiple | Multiple | Any | Base allow rule — overridden by specific blocks |
| Block All Traffic | Block | All | Multiple | Multiple | Any | Default deny — catches anything not explicitly allowed |

---

## Key Decisions & Reasoning

**WireGuard VPN** is exposed externally to allow secure remote access to the homelab without exposing individual services directly. This is preferable to opening multiple ports per service.

**Plex and Nginx Proxy Manager** are the only application-level services with direct port forwards. All other services are accessed either via the Nginx reverse proxy or over VPN.

**Block Invalid Traffic** sits near the top of the ruleset to drop malformed packets early before they reach any allow rules — a basic but effective hardening measure.

**Guest Network** is mapped to the Hotspot zone which prevents it from initiating connections to Internal zones, keeping guest devices fully isolated from servers and trusted clients.

---

![Firewall Policy UI](https://img.irosec.com/u/hzIxB3.jpg)
