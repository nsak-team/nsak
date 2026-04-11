#!/bin/sh
set -e

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

echo "[ldap] slapd started and populated"
