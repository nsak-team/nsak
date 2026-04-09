#!/bin/sh
# fileserver_setup.sh — Samba file shares with realistic content for recon training

set -e

# ── Share directories and content ─────────────────────────────────────────────
mkdir -p /srv/public /srv/finance /srv/it /srv/backup /srv/hr

# Public share — readable without credentials (null session)
cat > /srv/public/README.txt << 'EOF'
Acme Corp AG — Public File Share
=================================
This share contains company-wide documents.
For restricted documents contact bjones@lab.local or dtaylor@lab.local.

IT Helpdesk: Ext. 1337 | helpdesk@lab.local
File Server: \\FILESERVER\public (read-only, no auth required)
EOF

cat > /srv/public/Company_Policy_v3.2.txt << 'EOF'
Acme Corp AG — IT Security Policy v3.2
Approved: 2024-01-15 | Owner: Bob Jones (IT)

1. Password Policy
   - Minimum 8 characters
   - Change every 90 days
   - Do not reuse last 5 passwords
   Domain: LAB.LOCAL | DC: dc01.lab.local

2. Network Zones
   - Internet / DMZ: web.lab.local, mail.lab.local, jump.lab.local
   - Internal LAN: 192.168.10.0/24
   - Management access via jump.lab.local (SSH)

3. Data Classification
   - PUBLIC: this share
   - INTERNAL: \\FILESERVER\finance, \\FILESERVER\it
   - RESTRICTED: \\FILESERVER\backup

4. Contacts
   - IT Admin: bjones@lab.local (Domain Admin)
   - IT Engineer: dtaylor@lab.local
   - Security: security@lab.local
EOF

cat > /srv/public/Employee_Handbook_2024.txt << 'EOF'
Acme Corp AG — Employee Handbook 2024
Domain login: LAB\<username>
VPN/Remote: jump.lab.local via SSH
Intranet: http://wiki.lab.local:3000
Monitoring: http://monitor.lab.local:9090
EOF

# Finance share — requires credentials
cat > /srv/finance/Q4_2024_Budget.xlsx.txt << 'EOF'
[CONFIDENTIAL - Finance Department Only]
Q4 2024 Budget Summary
Total Revenue: CHF 4,820,000
IT Infrastructure: CHF 340,000 (DC upgrade, new fileserver)
Personnel: CHF 2,100,000
Contact: jsmith@lab.local (Finance Manager)
EOF

cat > /srv/finance/Payroll_Export_2024-03.csv.txt << 'EOF'
[CONFIDENTIAL - DO NOT DISTRIBUTE]
Username,Department,Salary
jsmith,Finance,95000
bjones,IT,88000
mwilson,HR,72000
dtaylor,IT,85000
EOF

# IT share — requires credentials
cat > /srv/it/dc01_build_sheet.txt << 'EOF'
Host: dc01.lab.local
IP: 192.168.10.5
OS: Alpine Linux 3.19 (Samba4 AD DC)
Role: Domain Controller, DNS, Kerberos, LDAP
Domain: LAB / lab.local
Admin: Administrator
DNS Forwarder: 8.8.8.8
Installed: 2024-01-08
Owner: bjones@lab.local
EOF

cat > /srv/it/network_diagram.txt << 'EOF'
Acme Corp Network Diagram (text version)
=========================================
WAN   10.0.1.0/24   — internet-client, firewall eth1
DMZ   172.16.1.0/24 — web:.10, dns:.20, mail:.30, jump:.40
LAN   192.168.10.0/24
  dc01       .5   (AD DC, DNS, Kerberos, LDAP)
  db         .10  (MariaDB appdb)
  fileserver .20  (Samba shares)
  wiki       .30  (Gitea)
  monitor    .50  (Prometheus)
  ws1        .100 (Finance - jsmith)
  ws2        .101 (IT - bjones)
EOF

cat > /srv/it/infra_credentials.kdbx.txt << 'EOF'
[PLACEHOLDER - In real lab: KeePass database]
This file would contain infrastructure credentials.
For training: see dc01 admin = Administrator / Password123!
EOF

# Backup share — not browseable, restricted
cat > /srv/backup/ad_backup_20240315.tar.gz.txt << 'EOF'
[AD BACKUP - RESTRICTED]
Created: 2024-03-15 02:00 (cron: svc_backup)
Source: dc01.lab.local
Contents: /var/lib/samba, /etc/samba, SYSVOL
Size: 84MB
EOF

cat > /srv/backup/db_backup_20240315.sql.gz.txt << 'EOF'
[DB BACKUP - RESTRICTED]
Created: 2024-03-15 03:00 (cron: svc_backup)
Source: db.lab.local MySQL appdb
Tables: users (247 rows), sessions, config, audit_log
EOF

# ── Samba configuration ────────────────────────────────────────────────────────
cat > /etc/samba/smb.conf << 'EOF'
[global]
    workgroup = VLAB
    realm = VLAB.LOCAL
    server string = NSAK Enterprise File Server
    netbios name = FILESERVER
    security = user
    map to guest = Bad User
    dns proxy = no
    log level = 1
    server role = standalone server
    # NTLM auth (weak, for lab training)
    ntlm auth = yes
    lanman auth = yes

[public]
    path = /srv/public
    browseable = yes
    read only = yes
    guest ok = yes
    comment = Public Documents - No Auth Required

[finance]
    path = /srv/finance
    browseable = yes
    read only = yes
    guest ok = no
    valid users = jsmith mwilson
    comment = Finance Department - Restricted

[it]
    path = /srv/it
    browseable = yes
    read only = no
    guest ok = no
    valid users = bjones dtaylor
    comment = IT Department - Restricted

[backup]
    path = /srv/backup
    browseable = no
    read only = no
    guest ok = no
    valid users = svc_backup
    comment = Backup Storage - Restricted (not visible in share list)
EOF

# ── Create Samba users ─────────────────────────────────────────────────────────
for user in jsmith bjones mwilson dtaylor svc_backup; do
    adduser -D -s /bin/false "$user" 2>/dev/null || true
    printf "Password123!\nPassword123!\n" | smbpasswd -a -s "$user" 2>/dev/null || true
done

# ── SSH (admin access) ─────────────────────────────────────────────────────────
ssh-keygen -A
printf "PasswordAuthentication yes\nPermitRootLogin no\n" >> /etc/ssh/sshd_config
adduser -D -s /bin/sh fsadmin
echo "fsadmin:FileS3rv3r!" | chpasswd

# ── Start services ─────────────────────────────────────────────────────────────
nmbd -D 2>/dev/null || true
smbd -D
/usr/sbin/sshd
echo "[fileserver] Samba and SSH started."

#