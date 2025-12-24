# Simple TCP Client Server Environment

## Simulate a scenario with containers

For a simulation of a scenario in this environment without setting up any HW, you can use the following commands:
```bash
nsak scenario bulid mitm
nsak environment simulate simple_tcp_client_server mitm
```

## Example setup with real hardware

This guide explains how to set up this environment with actual hardware.

**Required Hardware:**
- Layer 2 network switch and cables
- 2x Raspberry Pi: Alice (Client) and Bob (Server)
- Banana PI R4 or Nano PI: Malcom (NSAK)
- Three SD Cards for the operating systems

### Provision Raspberry Pi's

Download the latest [Raspberry PI Lite OS](https://www.raspberrypi.com/software/operating-systems/) from the official website and flash it to the SD card:

####
```bash
cd <nsak-project-root>
wget -P images https://downloads.raspberrypi.com/raspios_lite_arm64/images/raspios_lite_arm64-2025-12-04/2025-12-04-raspios-trixie-arm64-lite.img.xz

# Repeat the following steps for both SD cards

# Find the SD card device e.g. /dev/mmcblk0
sudo lsblk
# This will delete all partitions and data on the SD card!
xzcat images/2025-12-04-raspios-trixie-arm64-lite.img.xz | sudo dd of=/dev/mmcblk0 bs=4M

# Mount the SD cards partitions and apply basic user and network config:
sudo mount --mkdir /dev/mmcblk0p1 /mnt/bootfs

# Alice: Copy user and network config to boot partition
# hostname: alice
# ip: 10.10.10.20
# username: root
# password: root
sudo cp lib/environments/simple_tcp_client_server/config/alice/network-config /mnt/bootfs/network-config
sudo cp lib/environments/simple_tcp_client_server/config/alice/user-data /mnt/bootfs/user-config

# Bob: Copy user and network config to boot partition
# hostname: bob
# ip: 10.10.10.30
# username: root
# password: root
sudo cp lib/environments/simple_tcp_client_server/config/bob/network-config /mnt/bootfs/network-config
sudo cp lib/environments/simple_tcp_client_server/config/bob/user-data /mnt/bootfs/user-config

# Unmount SD cards
sudo umount /mnt/bootfs
```

Insert the SD cards into the Raspberry Pi's and power them up, check if you can connect to them via SSH:

```bash
# Add a static ip address to the network interface, which can reach the raspberry pi's:
ip addr
sudo ip addr add
sudo ip addr add 10.10.10.1/24 dev enp45s0
```
