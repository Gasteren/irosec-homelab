# Project: VLAN Segmentation

**Status:** ✅ Completed

---

## Objective

The goal was to segment the flat home network into isolated VLANs to reduce the blast radius of a compromised device, separate untrusted traffic from servers and trusted clients, and apply the principle of least privilege at the network level.

A flat network where a smart vacuum, a Tesla integration, a Plex server, and a password manager all share the same broadcast domain is a significant security risk. If any one device is compromised, an attacker has direct network access to everything else. VLAN segmentation eliminates that.

---

## Environment

| Component | Detail |
|---|---|
| Router / Firewall | Unifi Dream Machine Pro |
| Switches | USW Aggregation, USW-16-PoE, USW Flex |
| Access Points | U6 LR, U7 Lite |
| Controller | Unifi Network (on Dream Machine Pro) |

---

## Steps

**1. Identified traffic categories** — Mapped all devices and services on the network into logical groups: servers and self-hosted services, trusted personal devices, IoT and smart home devices, and guest access.

**2. Designed the VLAN layout** — Defined four VLANs with separate subnets and clear purposes:

| Name | VLAN ID | Subnet | Purpose |
|---|---|---|---|
| Server Network — JARVIS | 1 | 192.168.178.0/24 | Proxmox, Docker VM, self-hosted services |
| Guest Network | 2 | 192.168.2.0/24 | Isolated guest WiFi |
| IoT Devices | 3 | 192.168.69.0/24 | Smart home devices, Home Assistant integrations |
| Main Network — FRIDAY | 4 | 192.168.5.0/24 | Trusted personal devices |

**3. Created VLANs in Unifi controller** — Configured each network in the Unifi Network controller with the correct VLAN ID, subnet, and DHCP range.

**4. Applied VLANs to switch ports** — Tagged and untagged ports on the USW Aggregation, USW-16-PoE, and USW Flex were configured to carry the appropriate VLANs to the right devices.

**5. Configured wireless networks** — Created separate SSIDs mapped to the appropriate VLANs for IoT devices and guest access, keeping them off the main trusted wireless network.

**6. Assigned firewall zones** — Mapped VLANs to firewall zones in the Dream Machine Pro: Guest Network to the Hotspot zone for automatic isolation, server and client networks to the Internal zone.

**7. Verified isolation** — Tested that devices on the Guest and IoT VLANs could not reach devices on JARVIS or FRIDAY.

![VLAN setup](http://img.irosec.com/u/Ybb4mG.jpg)

---

## Results

- Four isolated VLANs running across all switches and access points
- Guest devices fully isolated in the Hotspot zone — cannot initiate connections to Internal zones
- IoT devices on a dedicated subnet, separated from trusted clients and servers
- All routing controlled by the Dream Machine Pro with firewall rules applied at zone boundaries

---
