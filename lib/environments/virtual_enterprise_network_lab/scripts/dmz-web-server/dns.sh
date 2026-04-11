#!/bin/sh
set -e

mkdir -p /etc/bind /var/cache/bind /var/run/named

cat > /etc/bind/named.conf << 'EOF'
options {
      directory        "/tmp";
      listen-on        { any; };
      allow-query      { any; };
      allow-transfer   { any; };            # open AXFR — intentional misconfiguration
      recursion yes;
      forwarders       { 8.8.8.8; };
      dnssec-validation no;
};

zone "vlab.local" IN {
    type master;
    file "/etc/bind/vlab.local.zone";
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

cat > /etc/bind/vlab.local.zone << 'EOF'
$ORIGIN vlab.local.
$TTL  300
@             IN    SOA   ns1.vlab.local.   hostmaster.vlab.local (
                         2024031501 ; serial
                         3600       ; refresh
                         900        ; retry
                         604800     ; expire
                         300 )      ; minimum TTL

; Nameserver
@             IN    NS    ns1.vlab.local.

; A-Records
web           IN    A     172.16.1.10
ns1           IN    A     172.16.1.10
ctrl          IN    A     192.168.10.5
file          IN    A     192.168.10.5
bob           IN    A     192.168.10.101
alice         IN    A     192.168.10.100
printer       IN    A     192.168.10.50
EOF

cat > /etc/bind/172.16.rev.zone << 'EOF'
$TTL  300
@       IN    SOA   ns1.vlab.local.   hostmaster.vlab.local (
                         2024031501 ; serial
                         3600       ; refresh
                         900        ; retry
                         604800     ; expire
                         300 )      ; minimum TTL
@       IN    NS    ns1.vlab.local.
1.10    IN    PTR   ns1.vlab.local.
EOF

cat > /etc/bind/192.168.rev.zone << 'EOF'
$TTL  300
@       IN    SOA   ns1.vlab.local.   hostmaster.vlab.local (
                         2024031501 ; serial
                         3600       ; refresh
                         900        ; retry
                         604800     ; expire
                         300 )      ; minimum TTL
@       IN    NS    ns1.vlab.local.
10.5    IN    PTR   ctrl.vlab.local.
10.50   IN    PTR   printer.vlab.local.
10.100  IN    PTR   alice.vlab.local.
10.101  IN    PTR   bob.vlab.local.
EOF

chown -R named:named /etc/bind 2>/dev/null || true
chmod 755 /etc/bind/
chmod 644 /etc/bind/*.zone /etc/bind/named.conf 2>/dev/null || true

named-checkconf /etc/bind/named.conf     || { echo "[dns] named.conf invalid, aborting"; exit 1; }
named-checkzone vlab.local /etc/bind/vlab.local.zone || { echo "[dns] zone invalid, aborting"; exit 1; }

named -4 -c /etc/bind/named.conf
echo "[dns] BIND9 started"
