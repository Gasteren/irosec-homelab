# Project: Honeypot Per VLAN

**Status:** ✅ Completed

---

## Objective

The goal was to deploy a honeypot address on every VLAN in the homelab to detect lateral movement, rogue devices, and unauthorised scanning activity. Any device that sends traffic to a honeypot address is flagged immediately — because no legitimate device or service should ever have a reason to contact it.

Honeypots are a deception-based detection technique. Rather than relying solely on signature matching, they create a tripwire: anything that touches the honeypot address is suspicious by definition.

---

## Environment

| Component | Detail |
|---|---|
| Device | Unifi Dream Machine Pro |
| Feature | Unifi Honeypot (built into Threat Management) |
| VLANs Covered | All four VLANs |

---

## Steps

**1. Identified suitable honeypot addresses** — Selected an unused IP address on each subnet. The .2 address was chosen for each VLAN as it is outside the DHCP range and would never be legitimately assigned to a device.

**2. Configured honeypot addresses in Unifi** — Created honeypot entries for each network in the Unifi Threat Management settings:

| Network | Subnet | Honeypot Address |
|---|---|---|
| Server Network — JARVIS | 192.168.178.0/24 | 192.168.178.2 |
| Guest Network | 192.168.2.0/24 | 192.168.2.2 |
| IoT Devices | 192.168.69.0/24 | 192.168.69.2 |
| Main Network — FRIDAY | 192.168.5.0/24 | 192.168.5.2 |

**3. Verified no legitimate services use these addresses** — Confirmed across all VMs, containers, and devices that none of the honeypot addresses were in use or assigned via static configuration.

**4. Confirmed alerting** — Verified that the Unifi controller would generate an alert if any device contacted a honeypot address.

![Honeypot settings](http://img.irosec.com/u/jm6lp1.jpg)
![Honeypot alert](http://img.irosec.com/u/Hn9M0S.jpg)

---

## Results

- Honeypot addresses active on all four VLANs
- Any device contacting a honeypot address will generate an immediate alert
- Provides detection coverage for scenarios that signature-based IDS might miss — such as an IoT device being used as a pivot point to scan the server network
- Zero operational overhead once configured

---

## Lessons Learned

Honeypots on every VLAN are particularly valuable in a network with IoT devices. Smart home hardware — vacuums, printers, lights — often runs firmware that cannot be deeply inspected or hardened. If a device on the IoT VLAN is compromised and begins scanning the network, the honeypot provides an early warning that something is probing addresses it has no business contacting.

The current limitation is that honeypot alerts live only in the Unifi controller. Once Wazuh is deployed, forwarding these alerts to the SIEM will allow them to be correlated with other events — for example, matching a honeypot hit with an IDS alert from the same source IP to build a fuller picture of suspicious activity.
