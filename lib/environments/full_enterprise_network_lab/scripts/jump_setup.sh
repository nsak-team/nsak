#!/bin/sh
# jump_setup.sh — SSH bastion host setup

set -e

# SSH config
ssh-keygen -A
cat >> /etc/ssh/sshd_config << 'EOF'
PasswordAuthentication yes
PermitRootLogin no
Banner /etc/ssh/banner.txt
AllowTcpForwarding yes
GatewayPorts no
EOF

# Login banner — reveals company name and contact
cat > /etc/ssh/banner.txt << 'EOF'
########################################################
#         Acme Corp AG — Authorized Access Only        #
#    Unauthorized access is a criminal offense.        #
#    All sessions are logged and monitored.            #
#    Contact: security@lab.local | IT: bjones@lab.local#
########################################################
EOF

# Admin user
adduser -D -s /bin/sh padmin
echo "padmin:JumpH0st!" | chpasswd

# Simulate realistic admin history / known_hosts
mkdir -p /home/padmin/.ssh
cat > /home/padmin/.ssh/known_hosts << 'EOF'
dc01.lab.local,192.168.10.5 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExampleKeyDC01PleaseReplaceWithReal==
fileserver.lab.local,192.168.10.20 ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAQQExampleKeyFS01==
wiki.lab.local,192.168.10.30 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExampleKeyWiki==
monitor.lab.local,192.168.10.50 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExampleKeyMon==
db.lab.local,192.168.10.10 ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBExampleKeyDB==
EOF

# Realistic shell history (recon artifact)
cat > /home/padmin/.ash_history << 'EOF'
ssh bjones@dc01.lab.local
ssh fsadmin@fileserver.lab.local
scp bjones@fileserver.lab.local:/srv/it/network_diagram.txt .
ssh dtaylor@wiki.lab.local
curl -s http://monitor.lab.local:9090/api/v1/targets
dig @dc01.lab.local lab.local
nmap -sn 192.168.10.0/24
EOF

chown -R padmin:padmin /home/padmin

# Start SSH
/usr/sbin/sshd
echo "[jump] SSH bastion started."
