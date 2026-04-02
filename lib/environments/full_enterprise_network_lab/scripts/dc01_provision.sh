#!/bin/sh
# dc01_provision.sh — Samba4 Active Directory Domain Controller
#
# Provisions LAB / lab.local domain with realistic users, OUs, and SPNs.
# Falls back to OpenLDAP + simulated services if Samba4 provisioning fails.
#
# Domain:  LAB / lab.local
# DC IP:   192.168.10.5
# Admin:   Administrator / Password123!

set -e

REALM="LAB.LOCAL"
DOMAIN="LAB"
ADMINPASS="Password123!"
DC_IP="192.168.10.5"
DC_HOST="dc01"

echo "[dc01] Starting Samba4 AD provisioning..."

# Clean up any leftover state
rm -rf /etc/samba/smb.conf /var/lib/samba /var/cache/samba /run/samba
mkdir -p /var/lib/samba /var/cache/samba /run/samba /etc/samba

# Attempt Samba4 domain provision
if samba-tool domain provision \
    --realm="$REALM" \
    --domain="$DOMAIN" \
    --adminpass="$ADMINPASS" \
    --dns-backend=SAMBA_INTERNAL \
    --use-rfc2307 \
    --server-role=dc \
    --host-name="$DC_HOST" \
    --host-ip="$DC_IP" \
    --option="interfaces = lo eth1" \
    --option="bind interfaces only = yes" \
    2>&1; then

    echo "[dc01] Samba4 provision successful — adding users and OUs..."

    # Start Samba temporarily for samba-tool operations
    samba &
    SAMBA_PID=$!
    sleep 5

    # OUs
    samba-tool ou create "OU=IT,DC=lab,DC=local"              2>/dev/null || true
    samba-tool ou create "OU=Finance,DC=lab,DC=local"          2>/dev/null || true
    samba-tool ou create "OU=HR,DC=lab,DC=local"               2>/dev/null || true
    samba-tool ou create "OU=Workstations,DC=lab,DC=local"     2>/dev/null || true
    samba-tool ou create "OU=ServiceAccounts,DC=lab,DC=local"  2>/dev/null || true
    samba-tool ou create "OU=Servers,DC=lab,DC=local"          2>/dev/null || true

    # Regular users
    samba-tool user add jsmith   "$ADMINPASS" --given-name=John  --surname=Smith   --department=Finance   --mail-address=jsmith@lab.local   2>/dev/null || true
    samba-tool user add bjones   "$ADMINPASS" --given-name=Bob   --surname=Jones   --department=IT        --mail-address=bjones@lab.local   2>/dev/null || true
    samba-tool user add mwilson  "$ADMINPASS" --given-name=Mary  --surname=Wilson  --department=HR        --mail-address=mwilson@lab.local  2>/dev/null || true
    samba-tool user add dtaylor  "$ADMINPASS" --given-name=Dave  --surname=Taylor  --department=IT        --mail-address=dtaylor@lab.local  2>/dev/null || true

    # Service accounts (weaker description reveals purpose — recon target)
    samba-tool user add svc_backup  "S3rvice@Backup!" --description="Backup Service - runs nightly to \\FILESERVER\backup" 2>/dev/null || true
    samba-tool user add svc_web     "S3rvice@Web!"    --description="Web Application Pool Account - IIS/nginx auth"        2>/dev/null || true
    samba-tool user add svc_monitor "S3rvice@Mon!"    --description="Prometheus monitoring agent - read-only domain access" 2>/dev/null || true

    # Group memberships
    samba-tool group addmembers "Domain Admins" bjones       2>/dev/null || true
    samba-tool group addmembers "Domain Admins" dtaylor      2>/dev/null || true

    # SPNs — Kerberoasting targets for authorised lab training
    samba-tool spn add "HTTP/wiki.lab.local"          svc_web     2>/dev/null || true
    samba-tool spn add "HTTP/wiki.lab.local:3000"     svc_web     2>/dev/null || true
    samba-tool spn add "MSSQLSvc/db.lab.local:3306"   svc_backup  2>/dev/null || true
    samba-tool spn add "BACKUP/dc01.lab.local"        svc_backup  2>/dev/null || true
    samba-tool spn add "HTTP/monitor.lab.local:9090"  svc_monitor 2>/dev/null || true

    # Relax password policy (training lab only)
    samba-tool domain passwordsettings set \
        --min-pwd-length=8 \
        --complexity=off \
        --min-pwd-age=0 \
        --max-pwd-age=0 \
        2>/dev/null || true

    # DNS records for lab hosts
    for rec in \
        "web A 172.16.1.10" \
        "mail A 172.16.1.30" \
        "jump A 172.16.1.40" \
        "dns A 172.16.1.20" \
        "db A 192.168.10.10" \
        "fileserver A 192.168.10.20" \
        "wiki A 192.168.10.30" \
        "monitor A 192.168.10.50" \
        "alice A 192.168.10.100" \
        "bob A 192.168.10.101"; do
        name=$(echo "$rec" | cut -d' ' -f1)
        type=$(echo "$rec" | cut -d' ' -f2)
        addr=$(echo "$rec" | cut -d' ' -f3)
        samba-tool dns add "$DC_IP" lab.local "$name" "$type" "$addr" \
            -U Administrator --password="$ADMINPASS" 2>/dev/null || true
    done

    echo "[dc01] Samba4 AD setup complete."
    # Samba already running from background — keep it
    wait $SAMBA_PID

else
    echo "[dc01] Samba4 provision failed — falling back to OpenLDAP + service banners..."

    apk add --no-cache openldap openldap-back-mdb openldap-clients python3 2>/dev/null || true

    # ── OpenLDAP fallback ──────────────────────────────────────────────────────
    mkdir -p /etc/openldap/slapd.d /var/lib/openldap/openldap-data

    # Generate LDAP password hash for Password123!
    PASSWD_HASH=$(slappasswd -s "$ADMINPASS" 2>/dev/null || echo "{SSHA}AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    cat > /tmp/slapd.conf << EOLDAP
include    /etc/openldap/schema/core.schema
include    /etc/openldap/schema/cosine.schema
include    /etc/openldap/schema/inetorgperson.schema

pidfile    /run/openldap/slapd.pid
argsfile   /run/openldap/slapd.args

modulepath /usr/lib/openldap
moduleload back_mdb

database   mdb
suffix     "dc=lab,dc=local"
rootdn     "cn=Administrator,dc=lab,dc=local"
rootpw     $PASSWD_HASH
directory  /var/lib/openldap/openldap-data

access to *
    by dn="cn=Administrator,dc=lab,dc=local" write
    by anonymous read
    by * read
EOLDAP

    mkdir -p /run/openldap

    # Bootstrap LDIF
    cat > /tmp/bootstrap.ldif << EOLDIF
dn: dc=lab,dc=local
objectClass: top
objectClass: dcObject
objectClass: organization
o: Acme Corp AG
dc: lab

dn: cn=Administrator,dc=lab,dc=local
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: Administrator
description: Domain Administrator
userPassword: $PASSWD_HASH

dn: ou=IT,dc=lab,dc=local
objectClass: organizationalUnit
ou: IT

dn: ou=Finance,dc=lab,dc=local
objectClass: organizationalUnit
ou: Finance

dn: ou=HR,dc=lab,dc=local
objectClass: organizationalUnit
ou: HR

dn: ou=ServiceAccounts,dc=lab,dc=local
objectClass: organizationalUnit
ou: ServiceAccounts

dn: cn=jsmith,ou=Finance,dc=lab,dc=local
objectClass: inetOrgPerson
cn: jsmith
sn: Smith
givenName: John
uid: jsmith
mail: jsmith@lab.local
userPassword: $PASSWD_HASH
departmentNumber: Finance
description: Finance Manager

dn: cn=bjones,ou=IT,dc=lab,dc=local
objectClass: inetOrgPerson
cn: bjones
sn: Jones
givenName: Bob
uid: bjones
mail: bjones@lab.local
userPassword: $PASSWD_HASH
departmentNumber: IT
description: IT Administrator - Domain Admin

dn: cn=mwilson,ou=HR,dc=lab,dc=local
objectClass: inetOrgPerson
cn: mwilson
sn: Wilson
givenName: Mary
uid: mwilson
mail: mwilson@lab.local
userPassword: $PASSWD_HASH
departmentNumber: HR

dn: cn=dtaylor,ou=IT,dc=lab,dc=local
objectClass: inetOrgPerson
cn: dtaylor
sn: Taylor
givenName: Dave
uid: dtaylor
mail: dtaylor@lab.local
userPassword: $PASSWD_HASH
departmentNumber: IT
description: IT Infrastructure Engineer

dn: cn=svc_backup,ou=ServiceAccounts,dc=lab,dc=local
objectClass: inetOrgPerson
cn: svc_backup
sn: svc_backup
uid: svc_backup
mail: svc_backup@lab.local
description: Backup Service Account - nightly backup to FILESERVER
userPassword: {SSHA}AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

dn: cn=svc_web,ou=ServiceAccounts,dc=lab,dc=local
objectClass: inetOrgPerson
cn: svc_web
sn: svc_web
uid: svc_web
mail: svc_web@lab.local
description: Web Application Pool Account - HTTP/wiki.lab.local
userPassword: {SSHA}AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

dn: cn=svc_monitor,ou=ServiceAccounts,dc=lab,dc=local
objectClass: inetOrgPerson
cn: svc_monitor
sn: svc_monitor
uid: svc_monitor
mail: svc_monitor@lab.local
description: Prometheus monitoring agent - read-only
userPassword: {SSHA}AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
EOLDIF

    slapd -f /tmp/slapd.conf -h "ldap://0.0.0.0:389/" &
    sleep 2
    ldapadd -x -H ldap://127.0.0.1:389 \
        -D "cn=Administrator,dc=lab,dc=local" \
        -w "$ADMINPASS" \
        -f /tmp/bootstrap.ldif 2>/dev/null || true

    # ── Kerberos banner (Python) on port 88 ────────────────────────────────────
    python3 - << 'PYEOF' &
import socket, threading, time
def handle(c, a):
    try:
        c.recv(512)
        # KRB5 KDC_ERR_C_PRINCIPAL_UNKNOWN (6) — realistic minimal response
        c.sendall(b"\x00\x00\x00\x16\x6a\x14\x30\x12\xa0\x03\x02\x01\x05\xa1\x03\x02\x01\x1e\xa4\x06\x30\x04")
    except Exception:
        pass
    finally:
        c.close()

for port in [88, 464]:
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port))
    s.listen(10)
    threading.Thread(target=lambda sv=s: [threading.Thread(target=handle, args=sv.accept(), daemon=True).start() for _ in iter(int, 1)], daemon=True).start()

while True:
    time.sleep(60)
PYEOF

    # ── Samba standalone (SMB shares) ─────────────────────────────────────────
    apk add --no-cache samba 2>/dev/null || true
    mkdir -p /srv/sysvol /srv/netlogon

    cat > /etc/samba/smb.conf << 'EOSMB'
[global]
    workgroup = LAB
    realm = LAB.LOCAL
    server string = Acme Corp AG - Domain Controller
    netbios name = DC01
    security = user
    map to guest = Never
    server role = standalone server

[SYSVOL]
    path = /srv/sysvol
    browseable = yes
    read only = yes
    guest ok = no
    comment = Sysvol

[NETLOGON]
    path = /srv/netlogon
    browseable = yes
    read only = yes
    guest ok = no
    comment = Netlogon
EOSMB

    smbd -D 2>/dev/null || true
    nmbd -D 2>/dev/null || true

    echo "[dc01] OpenLDAP fallback running on :389, Kerberos banner on :88, Samba on :445"
fi
