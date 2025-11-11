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

1. Download the officially supported Debian 12 Image from the referenced source

```bash
cd images
```