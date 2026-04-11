#!/bin/sh
set -e

# ── Shares ────────────────────────────────────────────────────────────────────
mkdir -p /srv/public /srv/finance /srv/it

cat > /srv/public/README.txt << 'EOF'
NSAK Enterprise — Public File Share
=================================
This share contains company-wide documents.
For restricted documents contact bjones@lab.local

File Server: \\FILESERVER\public (read-only, no auth required)
EOF

cat > /srv/finance/Q4_2024_Budget.xlsx.txt << 'EOF'
[CONFIDENTIAL - Finance Department Only]
Q4 2024 Budget Summary
Total Revenue: CHF 4,820,000
IT Infrastructure: CHF 340,000 (DC upgrade, new fileserver)
Personnel: CHF 2,100,000
Contact: asmith@lab.local (Finance Manager)
EOF

cat > /srv/finance/Payroll_Export_2024-03.csv.txt << 'EOF'
[CONFIDENTIAL - DO NOT DISTRIBUTE]
Username,Department,Salary
asmith,Finance,95000
bjones,IT,88000
EOF

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

# ── Samba config ──────────────────────────────────────────────────────────────
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
    # NTLM auth (weak, intentional for lab training)
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
    valid users = asmith
    comment = Finance Department - Restricted

[it]
    path = /srv/it
    browseable = yes
    read only = no
    guest ok = no
    valid users = bjones dtaylor
    comment = IT Department - Restricted
EOF

# ── Users ─────────────────────────────────────────────────────────────────────
for user in asmith bjones dtaylor; do
    adduser -D -s /bin/false "$user" 2>/dev/null || true
done

# ── Start Samba (nmbd/smbd must be up before smbpasswd) ───────────────────────
nmbd -D 2>/dev/null || true
smbd -D 2>/dev/null || true
sleep 1

for user in asmith bjones dtaylor; do
    printf "Password123!\nPassword123!\n" | smbpasswd -a -s "$user" 2>/dev/null || true
done

echo "[smb] Samba started"
