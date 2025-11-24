# Banana PI BPI R4 Pro (8GB) Setup


## Documentation and resources

- https://docs.banana-pi.org/en/BPI-R4/BananaPi_BPI-R4
- https://docs.banana-pi.org/en/BPI-R4/GettingStarted_BPI-R4

## Kali Linux on ARM HW

After assembling the bananapi BPI-R 4 board we wanted to install Kali Linux on it. We realized that this is not trivial,
because there are only some very specific prebuilt images available for ARM based HW. Building Kali Linux Images for other HW,
is possible with the following repository:
gitlab.com:kalilinux/build-scripts/kali-arm.git

But after trying out a bit, we realized that this is not really worth the effort and we want to focus on other things first.

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

## 

USB serial TTY:
If it's slow, try another USB port

Debian 12 BPI-r4 default login
Username: root
PW: bananapi

## Fan control

Set fan tripping point to 40 degrees Celsius

read current temp: `cat /sys/class/thermal/thermal_zone0/temp`
list current temp tripping points for fan: `grep . /sys/class/thermal/thermal_zone0/trip_point_*_temp`

```bash
/sys/class/thermal/thermal_zone0/trip_point_0_temp:125000
/sys/class/thermal/thermal_zone0/trip_point_1_temp:120000
/sys/class/thermal/thermal_zone0/trip_point_2_temp:115000
/sys/class/thermal/thermal_zone0/trip_point_3_temp:85000
```

Change the tripping point from 85 degree celsius to 35 degree celsius

`echo 40000 | tee /sys/class/thermal/thermal_zone0/trip_point_3_temp`

## Network configuration

Because the provided images for the Banana Pi BPI-R4 board are setup for routing, we want to delete all configurations and start from scatch:

`rm -rf /etc/systemd/network/*`

We start with a simple static IP configuration for our management network:

```
cd /etc/systemd/network/
vim 20-lan0.network

```

### Management network configuration



## System Setup

```bash
date -s "<current utc datetime>"

apt update
apt upgrade
apt install openssh-server ntp
```