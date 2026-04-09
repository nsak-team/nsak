#!/bin/sh

set -e

mkdir -p /srv/public /srv/finance /srv/it

cat > /srv/public/README.txt << 'EOF'
NSAK Enterprise — Public File Share
=================================
This share contains company-wide documents.
For restricted documents contact bjones@lab.local

File Server: \\FILESERVER\public (read-only, no auth required)
EOF

# Finance share — requires credentials
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

# Samba conf file
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

# ── Start Samba (must run before smbpasswd) ────────────────────────────────
nmbd -D 2>/dev/null || true
smbd -D 2>/dev/null || true
sleep 1

# ── Set Up Users ─────────────────────────────────────────────────────────────
for user in asmith bjones dtaylor; do
    adduser -D -s /bin/false "$user" 2>/dev/null || true
    printf "Password123!\nPassword123!\n" | smbpasswd -a -s "$user" 2>/dev/null || true
done

# ── Start SSH ─────────────────────────────────────────────────────────────────
ssh-keygen -A
/usr/sbin/sshd
echo "[ctrl-server] Samba and SSH started."

# ── LDAP ─────────────────────────────────────────────────────────────
mkdir -p /run/openldap /var/lib/openldap/openldap-data

cat > /etc/openldap/slapd.conf << 'EOF'
modulepath /usr/lib/openldap
moduleload back_mdb.so

include /etc/openldap/schema/core.schema
include /etc/openldap/schema/cosine.schema
include /etc/openldap/schema/inetorgperson.schema

pidfile /run/openldap/slapd.pid
argsfile /run/openldap/slapd.args

database mdb
suffix "dc=lab,dc=local"
rootdn "cn=Manager,dc=lab,dc=local"
rootpw Password123!
directory /var/lib/openldap/openldap-data

# Anonymous read — intentional misconfiguration for recon training
access to *
    by anonymous read
    by * read
EOF

slapd -f /etc/openldap/slapd.conf -h "ldap:///"
sleep 3

# Base structure + users + groups
ldapadd -x -D "cn=Manager,dc=lab,dc=local" -w Password123! << 'LDIF'
dn: dc=lab,dc=local
objectClass: top
objectClass: domain
dc: lab

dn: ou=Users,dc=lab,dc=local
objectClass: organizationalUnit
ou: Users

dn: ou=Groups,dc=lab,dc=local
objectClass: organizationalUnit
ou: Groups

dn: uid=asmith,ou=Users,dc=lab,dc=local
objectClass: inetOrgPerson
uid: asmith
cn: Alice Smith
sn: Smith
mail: asmith@lab.local
userPassword: Password123!
departmentNumber: Finance

dn: uid=bjones,ou=Users,dc=lab,dc=local
objectClass: inetOrgPerson
uid: bjones
cn: Bob Jones
sn: Jones
mail: bjones@lab.local
userPassword: Password123!
departmentNumber: IT

dn: cn=finance,ou=Groups,dc=lab,dc=local
objectClass: groupOfNames
cn: finance
member: uid=asmith,ou=Users,dc=lab,dc=local

dn: cn=it,ou=Groups,dc=lab,dc=local
objectClass: groupOfNames
cn: it
member: uid=bjones,ou=Users,dc=lab,dc=local
LDIF
echo "[ctrl-server] LDAP started and populated."