#!/usr/bin/env bash
# Firewall startup — installs iptables and applies zone policy.
# Interfaces assigned by compose.yaml:
#   eth0 = WAN       172.16.1.0/24
#   eth1 = DMZ       192.168.1.0/24
#   eth2 = Intranet  10.10.0.0/24

set -e

apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y iptables iproute2 -qq

# ── IP forwarding ─────────────────────────────────────────────────────────
sysctl -w net.ipv4.ip_forward=1

# ── Flush all existing rules ──────────────────────────────────────────────
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X

# ── Default policies: deny everything not explicitly allowed ──────────────
iptables -P INPUT   DROP
iptables -P FORWARD DROP
iptables -P OUTPUT  ACCEPT

# ── Allow established / related traffic ──────────────────────────────────
iptables -A INPUT   -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

# ── Loopback ──────────────────────────────────────────────────────────────
iptables -A INPUT -i lo -j ACCEPT

# ── Allow ICMP (ping) everywhere — useful for reachability testing ────────
iptables -A FORWARD -p icmp -j ACCEPT

# ── WAN -> DMZ: only public-facing services ───────────────────────────────
# HTTP/HTTPS to web server
iptables -A FORWARD -i eth0 -o eth1 -p tcp -d 192.168.1.10 --dport 80  -j ACCEPT
iptables -A FORWARD -i eth0 -o eth1 -p tcp -d 192.168.1.10 --dport 443 -j ACCEPT
# DNS (UDP + TCP)
iptables -A FORWARD -i eth0 -o eth1 -p udp -d 192.168.1.53 --dport 53  -j ACCEPT
iptables -A FORWARD -i eth0 -o eth1 -p tcp -d 192.168.1.53 --dport 53  -j ACCEPT
# SMTP
iptables -A FORWARD -i eth0 -o eth1 -p tcp -d 192.168.1.25 --dport 25  -j ACCEPT

# ── WAN -> Intranet: BLOCKED by default (lateral movement challenge) ──────
# (No rules — FORWARD default DROP applies)

# ── DMZ -> Intranet: only web -> DB query path ────────────────────────────
iptables -A FORWARD -i eth1 -o eth2 -p tcp \
    -s 192.168.1.10 -d 10.10.0.30 --dport 3306 -j ACCEPT
# web-db to db (MariaDB in DMZ does not need intranet access; rule kept for clarity)

# ── Intranet -> DMZ: workstations may reach web / dns ────────────────────
iptables -A FORWARD -i eth2 -o eth1 -p tcp -d 192.168.1.10 --dport 80  -j ACCEPT
iptables -A FORWARD -i eth2 -o eth1 -p tcp -d 192.168.1.10 --dport 443 -j ACCEPT
iptables -A FORWARD -i eth2 -o eth1 -p udp -d 192.168.1.53 --dport 53  -j ACCEPT
iptables -A FORWARD -i eth2 -o eth1 -p tcp -d 192.168.1.53 --dport 53  -j ACCEPT

# ── Intranet -> WAN: allow outbound with masquerade ──────────────────────
iptables -A FORWARD -i eth2 -o eth0 -j ACCEPT
iptables -t nat -A POSTROUTING -s 10.10.0.0/24 -o eth0 -j MASQUERADE

# ── DMZ -> WAN: allow outbound (mail relay, updates) ─────────────────────
iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth0 -j MASQUERADE

# ── Print active ruleset for Blue team inspection ─────────────────────────
echo "=== iptables -L -v -n ==="
iptables -L -v -n

echo "Firewall ready."
tail -f /dev/null
