## Add nat Rules

- eth0 = uplink interface
- wlan0 = ap_interface

client -> ap_interface -> nsak -> ulink_interface -> Internet
```
sudo sysctl -w net.ipv4.ip_forward=1

sudo iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth1 -j ACCEPT
sudo iptables -A FORWARD -i eth1 -o wlan0 -m state --state RELATED,ESTABLISHED -j A
```
