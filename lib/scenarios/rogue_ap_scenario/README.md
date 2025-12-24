Rouge AP Scenario - Setup & Run Guide

## 1. Requirements

Ensure the following are installed on the host system:

- Wireless card that supports AP mode ( check via: iw list)
- hostapd installed on the host

## 2. Settings

update the nsak/core/access_point/config.py

```commandline

interface=wlp59s0 depends on host wifi interface
ssid=BFH-Open
channel=6
country_code=CH

```

This ensures hostapd initializes correctly inside of the container

## 3. Podman Build

Rootless Podman cannot manipulate host networking, so both build and run must be executed using rootful Podman

## 4. Running the Rogue AP Scenario

Build:
`nsak scenario build rouge_ap_scenario `

Run:
`nsak scenario run rouge_ap_scenario`

Check container status:
`sudo podman ps -a `
`sudo podman logs <container-id>`

If successful, logs show:
`[Scenario] Rouge AP active on wlp59s0 with SSID BFH-Open.`

## 5. Verifying AP is Active

On the host
`iw dev <interface> info `
