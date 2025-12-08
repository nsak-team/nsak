The container is running and hostapd is available

### debug:

`sudo podman logs <container-id>`

check if the wifi is constrained
`rfkill lists` # enabling and disabling wireless devices

`sudo nmcli device status`
the Network Manager put my network in P2P mode

`iw list | grep -A20 "Supported interface modes"`

deactivate network manager
`sudo nmcli device set wlp59s0 managed no`

BFH Open shows

-> # activate network manager
