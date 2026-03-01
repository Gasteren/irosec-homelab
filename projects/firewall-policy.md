# Project: Firewall Policy Design

**Status:** ✅ Completed

---

## Objective

The goal was to design and implement a comprehensive zone-based firewall policy on the Dream Machine Pro covering all four VLANs — controlling what traffic can flow where, minimising external exposure, and ensuring that only explicitly required connections are permitted.

With real services exposed to the internet (Plex, Nginx Proxy Manager, WireGuard) and sensitive services running internally (Vaultwarden, Home Assistant), a well-defined firewall policy is a core security control, not an optional extra.

---

## Environment

| Component | Detail |
|---|---|
| Firewall Device | Unifi Dream Machine Pro |
| Policy Model | Zone-based firewall |
| Total Rules | 66 active policies |
| Protocol Coverage | IPv4 and IPv6 |
| VLANs in Scope | JARVIS (VLAN 1), Guest (VLAN 2), IoT (VLAN 3), FRIDAY (VLAN 4) |

---

## Steps

**1. Defined the zone model** — Mapped each network to a firewall zone based on its trust level. Guest Network was placed in the Hotspot zone for automatic isolation. Server and client VLANs were placed in the Internal zone.

**2. Established the zone matrix** — Defined default inter-zone policies:
- External → Internal: Allow Return only (no unsolicited inbound)
- Hotspot → Internal: Allow Return only (guests cannot reach servers)
- Hotspot ↔ DMZ: Block All (full isolation between untrusted zones)

**3. Created specific inbound rules** — Only three services have direct port forwards from the External zone:
- **Plex** on TCP/UDP port 32400
- **Nginx Proxy Manager** on HTTP/HTTPS (multiple ports)
- **WireGuard VPN** on UDP ports 51820 and 51822

**4. Added supporting rules** — Configured rules for IPv6 neighbour discovery (ICMPv6), mDNS for local service discovery (UDP 5353), and stateful return traffic.

**5. Hardened with blocking rules** — Added Block Invalid Traffic rule near the top of the ruleset to drop malformed and spoofed packets before they reach any allow rules.

**6. Verified rule behaviour** — Tested that external access to non-forwarded services was rejected, that WireGuard VPN granted correct internal access, and that guest devices could not reach the server network.

![firewall](http://img.irosec.com/u/hzIxB3.jpg)

---

## Results

- 66 active firewall policies covering all zones and VLANs
- Only three services exposed directly from External — Plex, Nginx Proxy Manager, and WireGuard
- Guest network fully blocked from reaching Internal zones
- Invalid and malformed traffic dropped at the perimeter before reaching application rules
- WireGuard VPN provides secure remote access without additional port exposure

---

## Lessons Learned

Using WireGuard VPN as the primary remote access method — rather than exposing individual service ports — significantly reduces the external attack surface. Any service that does not strictly need to be publicly accessible should be VPN-only.
