# Company Network — Red/Blue Team Lab

A containerised multi-zone enterprise network for adversarial security exercises.

## Network topology

```
Internet / WAN (172.16.1.0/24)
│
│  [attacker] 172.16.1.100        ← Red team entry point
│
└── [firewall] 172.16.1.1
          │
          ├── DMZ (192.168.1.0/24)          [internal=true]
          │     ├── web      192.168.1.10   DVWA (vuln web app)
          │     ├── web-db   192.168.1.11   MariaDB for DVWA
          │     ├── dns      192.168.1.53   BIND9 (corp.local)
          │     ├── mail     192.168.1.25   Postfix (open relay)
          │     └── siem     192.168.1.200  ← Blue team (DMZ leg)
          │
          └── Intranet (10.10.0.0/24)       [internal=true]
                ├── dc          10.10.0.10  OpenLDAP (corp.local)
                ├── fileserver  10.10.0.20  Samba (public + confidential shares)
                ├── db          10.10.0.30  MySQL (corpdb)
                ├── workstation 10.10.0.100 Ubuntu 22.04
                └── siem        10.10.0.200 ← Blue team (intranet leg)
```

## Firewall policy (summary)

| Source   | Destination | Allowed ports        |
|----------|-------------|----------------------|
| WAN      | DMZ         | 80, 443, 53, 25      |
| WAN      | Intranet    | none (blocked)       |
| DMZ      | Intranet    | 3306 (web → db only) |
| Intranet | DMZ         | 80, 443, 53          |
| Intranet | WAN         | all (NAT)            |
| DMZ      | WAN         | all (NAT)            |

## Quick start

```bash
# Start the lab (requires podman-compose or docker compose)
cd lib/environments/company_network
podman-compose up -d

# Or via NSAK:
nsak environment simulate company_network <scenario>
```

## Red team exercises

| Exercise | Entry point | Target |
|---|---|---|
| External recon | attacker (172.16.1.100) | nmap scan WAN → DMZ |
| Web exploitation | attacker → DVWA (192.168.1.10) | SQLi, XSS, brute-force |
| Open relay abuse | attacker → mail (192.168.1.25:25) | SMTP relay / phishing |
| Firewall bypass | attacker | Pivot WAN → Intranet |
| Lateral movement | web shell on web | web → db (3306) |
| Credential theft | db access | `corpdb.employees` (plaintext passwords) |
| SMB enumeration | workstation / attacker (after pivot) | fileserver shares |
| LDAP dump | workstation / attacker (after pivot) | `dc:389` anonymous bind |

## Blue team exercises

| Exercise | Tool | Location |
|---|---|---|
| Capture DMZ traffic | `tcpdump -i eth0 -w /tmp/dmz.pcap` | siem |
| IDS alerting | `suricata -i eth0 -c /etc/suricata/suricata.yaml` | siem |
| Firewall log review | `iptables -L -v -n` | firewall |
| Detect open relay | `swaks --to test@external.com --server 192.168.1.25` | attacker |
| Harden firewall | add `DROP` rules to `setup.sh` and restart | firewall |
| Detect plaintext passwords | query `corpdb.secrets` / `employees` | db |

## Credentials (intentionally weak — training only)

| Service | User | Password |
|---|---|---|
| LDAP admin | `cn=admin,dc=corp,dc=local` | `Admin1234!` |
| LDAP alice | `uid=alice,ou=users,dc=corp,dc=local` | `alice123` |
| LDAP bob | `uid=bob,ou=users,dc=corp,dc=local` | `Password1` |
| Samba | `smbuser` | `Password123` |
| MySQL root | `root` | `toor` |
| MySQL app | `appuser` | `apppass123` |
| DVWA / MariaDB | `dvwa` | `p@ssw0rd` |

## Stopping the lab

```bash
podman-compose down
# Remove volumes too:
podman-compose down -v
```
