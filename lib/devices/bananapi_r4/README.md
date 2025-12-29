# Banana PI BPI R4 Pro (8GB) Setup


## Documentation and resources

- https://docs.banana-pi.org/en/BPI-R4/BananaPi_BPI-R4
- https://docs.banana-pi.org/en/BPI-R4/GettingStarted_BPI-R4

## Kali Linux on ARM HW

After assembling the BananaPI BPI-R 4 board, we wanted to install Kali Linux on it. We realized that this is not trivial
because there are only some very specific prebuilt images available for ARM-based HW. Building Kali Linux Images for another HW
is possible with the following repository:
gitlab.com:kalilinux/build-scripts/kali-arm.git

But after trying out a bit, we realized that this is not really worth the effort, and we want to focus on other things first.

We decided to use a Linux Distro and Image supported by the Banana Pi BPI-R4 board.
A list of supported Distros and their respective Images can be found here:
https://docs.banana-pi.org/en/BPI-R4/BananaPi_BPI-R4

Because we are most familiar with Debian, we decided to use the Debian 12 image.

As we still want to use the Kali Linux tooling, we just add a container with the Kali Linux image.


## Installing Debian 12 via SDCard

1. Download the officially supported Debian 12 Image from the referenced source: https://docs.banana-pi.org/en/BPI-R4/BananaPi_BPI-R4
2. Unzip the image: `unzip 2024-07-18-debian-12-bookworm-bpi-r4-5.4-sd-emmc.img.zip`
3. Insert the SDCard into your PC
4. Find out the device name of the SDCard: `sudo lsblk`
5. Write the image to the SDCard: `sudo dd bs=4M if=debian-12-bookworm-bpi-r4-5.4-sd-emmc.img of=/dev/<device-name>`
6. Eject the SDCard
7. Insert the SDCard into the Banana Pi BPI-R4 board

## USB serial TTY:
Hint: If it's slow, try another USB port

Connect the Banana Pi BPI-R4 board to your PC via USB serial debugger:

```bash
# Find the device name of the USB serial port
ls -l /dev/ttyUSB*
# e.g.: /dev/ttyUSB0

# Start a serial terminal (other tools like minicom are also possible)
sudo screen /dev/ttyUSB0 115200
```

**Login with default credentials:**
Debian 12 BPI-r4 default login
Username: root
PW: bananapi

## Fan control

Set the fan tripping point to 40 degrees Celsius

read current temp: `cat /sys/class/thermal/thermal_zone0/temp`
list current temp tripping points for fan: `grep . /sys/class/thermal/thermal_zone0/trip_point_*_temp`

```bash
/sys/class/thermal/thermal_zone0/trip_point_0_temp:125000
/sys/class/thermal/thermal_zone0/trip_point_1_temp:120000
/sys/class/thermal/thermal_zone0/trip_point_2_temp:115000
/sys/class/thermal/thermal_zone0/trip_point_3_temp:85000
```

Change the tripping point from 85 degree Celsius to 35 degree Celsius

`echo 40000 | tee /sys/class/thermal/thermal_zone0/trip_point_3_temp`

## Target network configuration

Target network: 10.10.10.0/24

Because the provided images for the Banana Pi BPI-R4 board are set up for routing, we want to delete all configurations and start from scratch:

`rm -rf /etc/systemd/network/*`

We start with a simple static IP configuration for our target network:

```
vim /etc/systemd/network/05-eth0.network

[Match]
Name=eth0

[Link]
# Required for DSA CPU port
RequiredForOnline=no

[Network]
ConfigureWithoutCarrier=yes
LinkLocalAddressing=no
DHCP=no
```

@TODO: Currently, this is configured to work with the MITM scenario in the Simple TCP Client Server environment.
We should only bring the interfaces up and then configure the ip address with a discovery drill,
two common scenarios come into mind:
- DHCP: Check if a DHCP server is available and request an IP address from it
- Static IP: Otherwise assign a static IP address after discovering the other hosts

```
vim /etc/systemd/network/20-lan1.network

[Match]
Name=lan1

[Network]
Address=10.10.10.30/24
Address=10.10.20.30/24
Gateway=10.10.20.1
DNS=8.8.8.8
ConfigureWithoutCarrier=yes
```

```
# Restart systemd-networkd to apply the changes
systemctl restart systemd-networkd

# Verify the configuration
ip addr
# Output: lan0@eth1 ... 10.10.10.30/24 10.10.20.30/24
```

The interface lan1@eth0 is marked as LAN 1 on the physical device, which has the IP address 10.10.20.30/24 and should be connected to the target network.

### Management network configuration

@TODO: Again, we should only bring the interfaces up and then configure the management network with nsak.
For simplicity, we just configure the management network with a static IP address on the same network interface as the target network.
Management network: 10.10.20.0/24

** On your laptop or computer: **
```bash
# Add a static ip address to the network interface, which can reach the raspberry pi's (this config is not persistent across reboots):
ip addr
sudo ip addr add 10.10.20.1/24 dev enp45s0
# Enable forwarding of packets between the network interfaces:
sudo sysctl net.ipv4.ip_forward=1
# Verify that the forwarding is set:
sysctl net.ipv4.ip_forward
sudo iptables -t nat -A POSTROUTING -s 10.10.20.0/24 -o wlan0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT
```

Now connect the Banana Pi BPI-R4 board to your laptop or computer directly or via network switch.

```bash
# On your laptop or computer:
ping 10.10.20.30

# On the Banana Pi BPI-R4 board (via USB Serial TTY):
ping 10.10.20.1
```

## System Setup

```bash
# Set the correct date
date -s "<current utc datetime>"

# Install timesyncd and enable NTP
apt update
apt install systemd-timesyncd
timedatectl set-ntp true

# Verify the configuration
timedatectl

# Install openssh-server
apt install openssh-server
systemctl enable --now ssh

# Verify the configuration (root:bananapi)
ssh root@10.10.20.30

# Disconnect the USB serial TTY Cable (not only from the PC or Laptop, but also from the Banana Pi BPI-R4 board)

# Reboot Bananapi R4 and verify that you still can connect via SSH (rebooting takes a few seconds and the blue led indicates if the device has booted successfully):
reboot
ssh root@10.10.20.30

# Change hostname
vim /etc/hostname
# Replace default hostname:
nsak
```

Now you can connect to the device via SSH instead of the USB Serial TTY.

**Install NSAK**
```bash
# Connect via SSH (root:bananapi)
ssh root@10.10.20.30
# Install system dependencies
sudo apt install git python3 python3-pip curl podman sudo
ln /usr/bin/sudo /usr/sbin/sudo
ln /usr/bin/podman /usr/sbin/podman
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh && source $HOME/.local/bin/env
# Download nsak
git clone https://github.com/nsak-team/nsak.git
cd nsak
# Install nsak dependencies
uv sync

vim ~/.bashrc
# Add the following line to the end of the file:
export PATH="$HOME/.local/bin:$PATH"
export NSAK_LIBRARY_PATH=/root/nsak/lib/

# The uv installation does not work properly yet, so we run nsak in the virtual environment instead:
uv pip install -e
source .venv/bin/activate

# Verify that nsak is installed correctly:
nsak --help

# Check if you can build a scenario:
nsak scenario list
nsak scenario build mitm

# Set iptables to legacy mode (required for nsak, until we switched everything to nftables)
sudo update-alternatives --config iptables
```

**Optional: Flash the contents of the SDCard to the boards internal flash memory (eMMC)**
Documentation: https://docs.banana-pi.org/en/BPI-R4/GettingStarted_BPI-R4#_how_to_burn_image_to_sd_card

@TODO: Test and verify how it actually works.
```bash
ssh root@10.10.20.30
```

**Optional: Permanently mound an additional block storage (HDD/SSD)**
Documentation: https://docs.banana-pi.org/en/BPI-R4/GettingStarted_BPI-R4#_storage

```bash
ssh root@10.10.20.30

# Get the device name of the additional block storage
lsblk
# e.g.: nvme0n1

# Format the block storage with e.g., ext4
mkfs.ext4 /dev/nvme0n1

# Mount the block storage
mount --mkdir /dev/nvme0n1 /root/data

# Persist the mount on reboot
echo "/dev/nvme0n1 /root/data ext4 defaults 0 0" >> /etc/fstab
```
