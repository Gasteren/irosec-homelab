# Network Topology

This page documents the network layout of the irosec homelab including all Unifi hardware, IP addressing, and traffic flow.

---

## Network Diagram

[Diagram 1](https://img.irosec.com/u/XeanOW.jpg)
[Diagram 2](https://img.irosec.com/u/xEMUiP.jpg)

>Topology could not be imported due to image size.

---

## Unifi Hardware

| Device | Type | Role |
|---|---|---|
| Dream Machine Pro | Gateway / Router | Core routing, firewall, IDS/IPS, Unifi controller |
| USW Aggregation | Switch | Core aggregation switch (10 GbE SFP+) |
| USW-16-PoE | Switch | PoE distribution switch |
| USW Flex | Switch | Flexible edge switch |
| U6 LR | Access Point | WiFi coverage — 2.4 GHz & 5 GHz |
| U7 Lite | Access Point | WiFi coverage — 2.4 GHz & 5 GHz |
| Unifi Camera - Living Room | Protect Camera | Indoor surveillance |
| Unifi Camera - Kitchen | Protect Camera | Indoor surveillance |
| UNAS Pro | Network Storage | Dedicated storage server connected locally |

---

## VLANs & Segmentation

All network segmentation is handled by the Dream Machine Pro across four VLANs:

| Name | VLAN ID | Subnet | Purpose |
|---|---|---|---|
| Server Network - JARVIS | 1 | 192.168.178.0/24 | Proxmox, VMs, self-hosted services |
| Guest Network | 2 | 192.168.2.0/24 | Isolated guest WiFi access |
| IoT Devices | 3 | 192.168.69.0/24 | Smart home devices, Home Assistant integrations |
| Main Network - FRIDAY | 4 | 192.168.5.0/24 | Trusted client devices |

Inter-VLAN firewall rules are documented in the [Firewall](/security-stack/firewall) page.

---

## ISP & WAN

| Property | Value |
|---|---|
| ISP | Caiway NL |
| WAN Uplink | 10 GbE to Dream Machine Pro |

---

## Traffic Flow

- All traffic is routed through the Dream Machine Pro
- IDS/IPS inspection runs on the DMP for all WAN-bound traffic
- Unifi Protect camera footage is stored locally and cloud for redundancy
- Wireless coverage is split between U6 LR and U7 Lite for full home coverage
