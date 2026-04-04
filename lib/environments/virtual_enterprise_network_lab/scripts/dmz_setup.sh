#!/bin/sh
set -e # script terminates if error occurs

mkdir -p /etc/bind /var/cache/bind /var/run/named


# named config
cat > /etc/bind/named.conf << 'EOF'
options {
      directory        "/tmp";
      listen-on        { any; };            # listen on all interfaces
      allow-query      { any; };            # answer queries from anyone
      allow-transfer   { any; };            # open AXFR — the misconfiguration
      recursion yes;
      forwarders       { 8.8.8.8; };       # forward unknown queries upstream
      dnssec-validation no;                 # skip DNSSEC (container lab)
};
# Autoritative Zone
zone "vlab.local" IN{
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
# Forward Zone
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

; MX-Records
EOF
# Reverse Zone 172.16.1.10
cat > /etc/bind/172.16.rev.zone << 'EOF'
$TTL  300
@       IN    SOA   ns1.vlab.local.   hostmaster.vlab.local (
                         2024031501 ; serial
                         3600       ; refresh
                         900        ; retry
                         604800     ; expire
                         300 )      ; minimum TTL
; Nameserver
@       IN    NS    ns1.vlab.local.

; Records
1.10    IN    PTR   ns1.vlab.local.
EOF

cat > /etc/bind/192.168.rev.zone <<'EOF'
$TTL  300
@       IN    SOA   ns1.vlab.local.   hostmaster.vlab.local (
                         2024031501 ; serial
                         3600       ; refresh
                         900        ; retry
                         604800     ; expire
                         300 )      ; minimum TTL

@       IN    NS    ns1.vlab.local.
10.5    IN    PTR   ctrl.vlab.local.
10.101  IN    PTR   bob.vlab.local.
10.100  IN    PTR   alice.vlab.local.
10.50   IN    PTR   printer.vlab.local.
EOF

# Fix permissions
chown -R named:named /etc/bind 2>/dev/null || true
chmod 755 /etc/bind/
chmod 644 /etc/bind/*.zone /etc/bind/named.conf 2>/dev/null || true

# Validate config
named-checkconf /etc/bind/named.conf || { echo "[dns] named.conf invalid, aborting"; exit 1; }
named-checkzone vlab.local /etc/bind/vlab.local.zone || { echo "[dns] zone invalid, aborting"; exit 1; }

# Start BIND9
named -4 -c /etc/bind/named.conf