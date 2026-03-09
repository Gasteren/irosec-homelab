# Proxmox Setup

Proxmox VE is the hypervisor running the irosec homelab. It hosts all virtual machines and provides snapshot, backup, and resource management capabilities.

---

## Host Detailsz

| Component | Details |
|---|---|
| Proxmox Version | 8.4.1 |
| OS | Debian GNU/Linux 12 (bookworm)
| Kernel| Linux 6.8.12-10-pve
| CPU | i7-7800X CPU @ 3.50GHz |
| RAM | 32gb DDR4 |
| Storage | x4 10TB HDD - x1 1TB SSD

---

## Virtual Machines

| VM ID | Name | OS | Role |
|---|---|---|---|
| 100 | Dockers | Ubuntu 22.04.5 LTS (kernel 5.15.0-171-generic) | All Docker hosted services |
| 101 | Hassio | Home Assistant OS 17.1 (Buildroot) | Smart home automation |

---

## Storage Configuration

| ID | Type | Content | Path / Target | Shared |
|---|---|---|---|---|
| PogChampRaid | ZFS | Disk image, Container | — | No |
| local | Directory | Backup, Disk image, ISO image, Container, Snippets, Container template | /var/lib/vz | No |
| unas | NFS | Disk image | /mnt/pve/unas | Yes |

The `unas` pool is an NFS mount from the UNAS Pro, allowing VM disk images to be stored on network-attached storage. The `PogChampRaid` ZFS pool provides local high-performance storage for containers and disk images.

---

## Backup Strategy

- VM snapshots are taken before any major changes
- Docker container stacks are manually backed up to the UNAS Pro
- Configs and database files are saved as snapshots on the UNAS Pro

### UNAS Pro — Unifi Drive Snapshots

Persistent data is backed up across five drives on the UNAS Pro, each with a snapshot limit of 32. Snapshots run daily at 12:00 AM and currently 160 of 4,096 total snapshots are in use.

| Drive | Snapshot Limit | Schedule |
|---|---|---|
| *(personal drive — redacted)* | 32/32 | Daily at 12:00 AM |
| Carlo van Gasteren | 32/32 | Daily at 12:00 AM |
| PlexMedia | 32/32 | Daily at 12:00 AM |
| DriveForUs | 32/32 | Daily at 12:00 AM |
| ServerFiles | 32/32 | Daily at 12:00 AM |

![Storage](https://img.irosec.com/u/Vdc2sa.jpg)



---

## Notes

- Both VMs set to auto-start on host boot
- VMs use VirtIO drivers for best performance
