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

Download the latest [Raspberry PI Lite OS](https://www.raspberrypi.com/software/operating-systems/) from the official
website and flash it to the SD card:

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
# ip: 10.10.10.10
# username: alice
# password: alice
sudo cp lib/environments/simple_tcp_client_server/config/alice/network-config /mnt/bootfs/network-config
sudo cp lib/environments/simple_tcp_client_server/config/alice/user-data /mnt/bootfs/user-data

# Bob: Copy user and network config to boot partition
# hostname: bob
# ip: 10.10.10.20
# username: bob
# password: bob
sudo cp lib/environments/simple_tcp_client_server/config/bob/network-config /mnt/bootfs/network-config
sudo cp lib/environments/simple_tcp_client_server/config/bob/user-data /mnt/bootfs/user-data

# Unmount SD cards
sudo umount /mnt/bootfs
```

Insert the SD cards into the Raspberry Pi's and power them up, check if you can connect to them via SSH:

```bash
# Add a static ip address to the network interface, which can reach the raspberry pi's (this config is not persistent across reboots):
ip addr
sudo ip addr add 10.10.10.1/24 dev enp45s0
# Enable forwarding of packets between the network interfaces:
sudo sysctl net.ipv4.ip_forward=1
# Verify that the forwarding is set:
sysctl net.ipv4.ip_forward
sudo iptables -t nat -A POSTROUTING -s 10.10.10.0/24 -o wlan0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT

# Alice:
# Verify connectivity
ping 10.10.10.10
# Connect via ssh (user: alice, password: alice)
ssh alice@10.10.10.10

# Bob:
# Verify connectivity
ping 10.10.10.20
# Connect via ssh (user: bob, password: bob)
ssh bob@10.10.10.20

# The following commands must be executed on alice and bob machine:
# System update
sudo apt update && sudo apt upgrade
# Install system dependencies
sudo apt install git python3
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh && source ~/.bashrc
# Download nsak
git clone https://github.com/nsak-team/nsak.git
cd nsak
# Install nsak dependencies
uv sync
```

### Start the client and server scripts on the Raspberry Pi's:

```
# Alice: TCP Client
ssh alice@10.10.10.10
uv run lib/environments/simple_tcp_client_server/alice.py

# Bob: TCP Server
ssh bob@10.10.10.20
uv run lib/environments/simple_tcp_client_server/bob.py
```

As soon as both scripts are running, alice and bob start to communicate, and you should see something like the following
output:

```bash
[Bob] Waiting for connection on 0.0.0.0:5000...
[Bob] Connected by ('10.10.10.10', 52246)
[Bob] Sending: Bob says hello #0
[Bob] Received: Alice says hello #0
[Bob] Sending: Bob says hello #1
[Bob] Received: Alice says hello #1
```

### Run a scenario in the configured environment with real HW

Follow the steps provided in the [README.md](../../scenarios/mitm/environments/simple_tcp_client_server/README.md) of
the MITM scenario.
