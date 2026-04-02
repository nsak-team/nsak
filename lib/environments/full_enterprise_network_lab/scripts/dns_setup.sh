#!/bin/sh
# dns_setup.sh — BIND9 authoritative DNS for lab.local
# Zone transfers (AXFR) are intentionally open — classic recon misconfiguration.

set -e

mkdir -p /etc/bind /var/cache/bind /var/run/named

# ── named.conf ────────────────────────────────────────────────────────────────
cat > /etc/bind/named.conf << 'EOF'
options {
    directory       "/var/cache/bind";
    listen-on       { any; };
    allow-query     { any; };
    allow-transfer  { any; };   # intentionally open — AXFR allowed from anywhere
    recursion yes;
    forwarders { 8.8.8.8; };
    dnssec-validation no;
};

zone "lab.local" IN {
    type master;
    file "/etc/bind/lab.local.zone";
    allow-transfer { any; };
};

zone "16.172.in-addr.arpa" IN {
    type master;
    file "/etc/bind/172.16.rev.zone";
};

zone "168.192.in-addr.arpa" IN {
    type master;
    file "/etc/bind/192.168.rev.zone";
};
EOF

# ── Forward zone: lab.local ───────────────────────────────────────────────────
cat > /etc/bind/lab.local.zone << 'EOF'
$TTL 300
@   IN  SOA  ns1.lab.local. hostmaster.lab.local. (
            2024031501 ; serial
            3600       ; refresh
            900        ; retry
            604800     ; expire
            300 )      ; minimum TTL

; Name servers
@           IN  NS   ns1.lab.local.
@           IN  NS   dc01.lab.local.

; Mail exchange
@           IN  MX   10  mail.lab.local.

; SPF / DMARC / DKIM TXT records (recon gold)
@           IN  TXT  "v=spf1 mx a:mail.lab.local -all"
acmecorp    IN  TXT  "v=spf1 mx a:mail.lab.local -all"
_dmarc      IN  TXT  "v=DMARC1; p=none; rua=mailto:dmarc@lab.local; ruf=mailto:forensics@lab.local"

; SRV records for AD/Kerberos/LDAP (exposed via DNS for client discovery)
_kerberos._tcp      IN  SRV  0 100 88   dc01.lab.local.
_kerberos._udp      IN  SRV  0 100 88   dc01.lab.local.
_ldap._tcp          IN  SRV  0 100 389  dc01.lab.local.
_gc._tcp            IN  SRV  0 100 3268 dc01.lab.local.
_kpasswd._tcp       IN  SRV  0 100 464  dc01.lab.local.
_kpasswd._udp       IN  SRV  0 100 464  dc01.lab.local.
_ldap._tcp.dc._msdcs IN SRV  0 100 389  dc01.lab.local.

; DMZ hosts
ns1             IN  A    172.16.1.20
web             IN  A    172.16.1.10
www             IN  CNAME web.lab.local.
acmecorp        IN  A     172.16.1.10
dns             IN  A    172.16.1.20
mail            IN  A    172.16.1.30
smtp            IN  CNAME mail
imap            IN  CNAME mail
jump            IN  A    172.16.1.40
vpn             IN  CNAME jump
bastion         IN  CNAME jump

; LAN hosts
dc01            IN  A    192.168.10.5
ldap            IN  CNAME dc01
kdc             IN  CNAME dc01
ad              IN  CNAME dc01
db              IN  A    192.168.10.10
sql             IN  CNAME db
mysql           IN  CNAME db
fileserver      IN  A    192.168.10.20
fs01            IN  CNAME fileserver
shares          IN  CNAME fileserver
wiki            IN  A    192.168.10.30
git             IN  CNAME wiki
devops          IN  CNAME wiki
monitor         IN  A    192.168.10.50
grafana         IN  CNAME monitor
prometheus      IN  CNAME monitor
alice           IN  A    192.168.10.100
bob             IN  A    192.168.10.101
nsak            IN  A    192.168.10.200
EOF

# ── Reverse zone: 172.16.x.x ─────────────────────────────────────────────────
cat > /etc/bind/172.16.rev.zone << 'EOF'
$TTL 300
@   IN  SOA  ns1.lab.local. hostmaster.lab.local. (
            2024031501 3600 900 604800 300 )
@   IN  NS   ns1.lab.local.

; DMZ reverse
10.1    IN  PTR  web.lab.local.
20.1    IN  PTR  dns.lab.local.
30.1    IN  PTR  mail.lab.local.
40.1    IN  PTR  jump.lab.local.
200.1   IN  PTR  nsak-dmz.lab.local.
EOF

# ── Reverse zone: 192.168.x.x ────────────────────────────────────────────────
cat > /etc/bind/192.168.rev.zone << 'EOF'
$TTL 300
@   IN  SOA  ns1.lab.local. hostmaster.lab.local. (
            2024031501 3600 900 604800 300 )
@   IN  NS   ns1.lab.local.

; LAN reverse
5.10    IN  PTR  dc01.lab.local.
10.10   IN  PTR  db.lab.local.
20.10   IN  PTR  fileserver.lab.local.
30.10   IN  PTR  wiki.lab.local.
50.10   IN  PTR  monitor.lab.local.
100.10  IN  PTR  alice.lab.local.
101.10  IN  PTR  bob.lab.local.
200.10  IN  PTR  nsak.lab.local.
EOF

# Fix permissions — /etc/bind must be traversable by the named user after priv drop
chown -R named:named /etc/bind /var/cache/bind /var/run/named 2>/dev/null || true
chmod 755 /etc/bind/
chmod 644 /etc/bind/*.zone /etc/bind/named.conf 2>/dev/null || true

# Validate config before starting
named-checkconf /etc/bind/named.conf || { echo "[dns] named.conf invalid, aborting"; exit 1; }
named-checkzone lab.local /etc/bind/lab.local.zone || { echo "[dns] zone invalid, aborting"; exit 1; }

# Start BIND9 — explicit -u named so privilege drop works, -4 for IPv4-only container
named -4 -c /etc/bind/named.conf -u named
