#!/usr/bin/env python3
"""
verify.py — Smoke-test suite for Enterprise Network Lab 2.

Tests connectivity, firewall rules, DNS, web, mail, SMB, SSH, monitoring,
and workstation service banners by running commands inside the containers
via `docker exec`.

Usage:
    python3 lib/environments/enterprise_network_lab2/verify.py

    # Run only specific suites:
    python3 verify.py --suites connectivity firewall dns

    # Show all output (including passing tests' details):
    python3 verify.py --verbose

Prerequisites:
    sudo containerlab deploy -t lib/environments/enterprise_network_lab2/topology.clab.yaml
    Docker available (or run with sudo)
"""

import argparse
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Callable

LAB = "clab-enterprise-network-lab2"

RESET  = "\033[0m"
GREEN  = "\033[32m"
RED    = "\033[31m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
BOLD   = "\033[1m"
DIM    = "\033[2m"


# ── Execution helper ──────────────────────────────────────────────────────────

def _exec(node: str, command: str, timeout: int = 10) -> tuple[int, str, str]:
    """Run `command` inside `node` via docker exec."""
    result = subprocess.run(
        ["docker", "exec", f"{LAB}-{node}", "sh", "-c", command],
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


# ── Test infrastructure ───────────────────────────────────────────────────────

@dataclass
class TestResult:
    name:   str
    passed: bool
    detail: str
    note:   str = ""   # optional explanatory note shown even on pass


def run_test(name: str, check: Callable[[], tuple[bool, str]]) -> TestResult:
    try:
        passed, detail = check()
    except subprocess.TimeoutExpired:
        passed, detail = False, "timed out"
    except Exception as exc:
        passed, detail = False, str(exc)
    return TestResult(name=name, passed=passed, detail=detail)


def print_result(result: TestResult, verbose: bool = False) -> None:
    icon   = f"{GREEN}✓{RESET}" if result.passed else f"{RED}✗{RESET}"
    detail = f"  {DIM}{result.detail}{RESET}" if (not result.passed or verbose) and result.detail else ""
    note   = f"  {YELLOW}↳ {result.note}{RESET}" if result.note else ""
    print(f"  {icon}  {result.name}{detail}{note}")


# ── Generic check primitives ──────────────────────────────────────────────────

def tcp_open(node: str, host: str, port: int) -> tuple[bool, str]:
    rc, _, _ = _exec(node, f"nc -zw3 {host} {port}")
    if rc != 0:
        return False, f"port {port} unreachable from {node}"
    return True, f"{host}:{port} open"


def tcp_blocked(node: str, host: str, port: int) -> tuple[bool, str]:
    rc, _, _ = _exec(node, f"nc -zw2 {host} {port}")
    if rc == 0:
        return False, f"port {port} should be blocked but is reachable"
    return True, f"{host}:{port} correctly blocked"


def ping_ok(node: str, host: str) -> tuple[bool, str]:
    rc, _, _ = _exec(node, f"ping -c2 -W2 {host}")
    if rc != 0:
        return False, f"{host} unreachable from {node}"
    return True, f"{host} reachable"


def ping_blocked(node: str, host: str) -> tuple[bool, str]:
    rc, _, _ = _exec(node, f"ping -c2 -W2 {host}")
    if rc == 0:
        return False, f"{host} should be unreachable but replied"
    return True, f"{host} correctly unreachable"


def http_status(node: str, url: str, expected: str = "200") -> tuple[bool, str]:
    rc, out, _ = _exec(
        node,
        f"curl -sk -o /dev/null -w '%{{http_code}}' --connect-timeout 5 {url}",
    )
    if rc != 0 or out != expected:
        return False, f"HTTP {out!r} (expected {expected})"
    return True, f"HTTP {out}"


def http_contains(node: str, url: str, needle: str) -> tuple[bool, str]:
    rc, out, _ = _exec(node, f"curl -sk --connect-timeout 5 {url}", timeout=15)
    if rc != 0:
        return False, f"curl failed (rc={rc})"
    if needle not in out:
        return False, f"{needle!r} not found in response"
    return True, f"found {needle!r}"


def http_header(node: str, url: str, header: str, expected: str) -> tuple[bool, str]:
    rc, out, _ = _exec(
        node,
        f"curl -skI --connect-timeout 5 {url}",
    )
    if rc != 0:
        return False, "curl failed"
    for line in out.splitlines():
        if line.lower().startswith(header.lower() + ":"):
            value = line.split(":", 1)[1].strip()
            if expected.lower() in value.lower():
                return True, f"{header}: {value}"
            return False, f"{header}: {value!r} (expected {expected!r})"
    return False, f"header {header!r} not present"


def banner_contains(node: str, host: str, port: int, needle: str, send: str = "") -> tuple[bool, str]:
    cmd = f"printf '{send}' | nc -w3 {host} {port}" if send else f"nc -w3 {host} {port} </dev/null"
    rc, out, err = _exec(node, cmd)
    combined = out + err
    if needle in combined:
        return True, combined.splitlines()[0][:80] if combined else ""
    return False, f"{needle!r} not in banner: {combined[:80]!r}"


def dns_resolves(node: str, server: str, name: str, expected_ip: str) -> tuple[bool, str]:
    rc, out, _ = _exec(node, f"dig @{server} {name} +short")
    if rc != 0 or expected_ip not in out:
        return False, f'got {out!r}, expected {expected_ip}'
    return True, expected_ip


def dns_axfr(node: str, server: str, zone: str, expected_names: list[str]) -> tuple[bool, str]:
    rc, out, _ = _exec(node, f"dig @{server} {zone} AXFR", timeout=15)
    if rc != 0:
        return False, "AXFR failed"
    missing = [n for n in expected_names if n not in out]
    if missing:
        return False, f"missing in zone: {missing}"
    return True, f"zone transfer OK ({len(out.splitlines())} lines)"


# ── Test suites ───────────────────────────────────────────────────────────────

# 1. Connectivity — basic reachability within and across zones
CONNECTIVITY_TESTS = [
    # LAN internal
    ("Ping: alice → bob  (LAN intra)",
     lambda: ping_ok("alice", "192.168.10.101")),
    ("Ping: bob → alice  (LAN intra)",
     lambda: ping_ok("bob", "192.168.10.100")),
    ("Ping: alice → dc01 (LAN intra)",
     lambda: ping_ok("alice", "192.168.10.5")),
    ("Ping: alice → fileserver (LAN intra)",
     lambda: ping_ok("alice", "192.168.10.20")),
    ("Ping: alice → monitor (LAN intra)",
     lambda: ping_ok("alice", "192.168.10.50")),
    # LAN → DMZ (should work — employees use DMZ services)
    ("Ping: alice → web DMZ (LAN→DMZ)",
     lambda: ping_ok("alice", "172.16.1.10")),
    ("TCP:  alice → web:80 (LAN→DMZ)",
     lambda: tcp_open("alice", "172.16.1.10", 80)),
    # WAN → DMZ (only explicitly allowed ports)
    ("TCP:  internet-client → web:80  (WAN→DMZ allowed)",
     lambda: tcp_open("internet-client", "172.16.1.10", 80)),
    ("TCP:  internet-client → dns:53  (WAN→DMZ allowed)",
     lambda: tcp_open("internet-client", "172.16.1.20", 53)),
    ("TCP:  internet-client → mail:25 (WAN→DMZ allowed)",
     lambda: tcp_open("internet-client", "172.16.1.30", 25)),
    ("TCP:  internet-client → jump:22 (WAN→DMZ allowed)",
     lambda: tcp_open("internet-client", "172.16.1.40", 22)),
]

# 2. Firewall — zone isolation
FIREWALL_TESTS = [
    # WAN → LAN must be fully blocked
    ("FW: internet-client → alice:22  blocked (WAN→LAN)",
     lambda: tcp_blocked("internet-client", "192.168.10.100", 22)),
    ("FW: internet-client → bob:22    blocked (WAN→LAN)",
     lambda: tcp_blocked("internet-client", "192.168.10.101", 22)),
    ("FW: internet-client → dc01:389  blocked (WAN→LAN)",
     lambda: tcp_blocked("internet-client", "192.168.10.5", 389)),
    ("FW: internet-client → db:3306   blocked (WAN→LAN)",
     lambda: tcp_blocked("internet-client", "192.168.10.10", 3306)),
    # WAN → DMZ non-allowed ports blocked
    ("FW: internet-client → web:22    blocked (WAN→DMZ SSH)",
     lambda: tcp_blocked("internet-client", "172.16.1.10", 22)),
    ("FW: internet-client → mail:143  blocked (WAN→DMZ IMAP)",
     lambda: tcp_blocked("internet-client", "172.16.1.30", 143)),
    # DMZ → LAN restricted (only web→db and mail→dc01 and jump→ssh)
    ("FW: web → db:3306   open   (DMZ→LAN web→db)",
     lambda: tcp_open("web", "192.168.10.10", 3306)),
    ("FW: web → alice:22  blocked (DMZ→LAN no direct SSH)",
     lambda: tcp_blocked("web", "192.168.10.100", 22)),
    ("FW: dns → alice:445 blocked (DMZ→LAN no SMB)",
     lambda: tcp_blocked("dns", "192.168.10.100", 445)),
]

# 3. DNS — authoritative zone, AXFR, records
DNS_TESTS = [
    # Forward lookups from internet-client (external)
    ("DNS: web.lab.local → 172.16.1.10  (from WAN)",
     lambda: dns_resolves("internet-client", "172.16.1.20", "web.lab.local", "172.16.1.10")),
    ("DNS: mail.lab.local → 172.16.1.30 (from WAN)",
     lambda: dns_resolves("internet-client", "172.16.1.20", "mail.lab.local", "172.16.1.30")),
    ("DNS: dc01.lab.local → 192.168.10.5 (from LAN)",
     lambda: dns_resolves("alice", "172.16.1.20", "dc01.lab.local", "192.168.10.5")),
    ("DNS: alice.lab.local → 192.168.10.100",
     lambda: dns_resolves("alice", "172.16.1.20", "alice.lab.local", "192.168.10.100")),
    ("DNS: bob.lab.local → 192.168.10.101",
     lambda: dns_resolves("alice", "172.16.1.20", "bob.lab.local", "192.168.10.101")),
    # CNAME aliases
    ("DNS: www CNAME → web.lab.local",
     lambda: dns_resolves("internet-client", "172.16.1.20", "www.lab.local", "172.16.1.10")),
    # MX record
    ("DNS: MX lab.local → mail.lab.local",
     lambda: (lambda rc, out, _: ("mail.lab.local" in out, out[:60]))
             (*_exec("alice", "dig @172.16.1.20 lab.local MX +short"))),
    # SRV records for AD discovery
    ("DNS: SRV _ldap._tcp.lab.local → dc01",
     lambda: (lambda rc, out, _: ("dc01.lab.local" in out, out[:60]))
             (*_exec("alice", "dig @172.16.1.20 _ldap._tcp.lab.local SRV +short"))),
    ("DNS: SRV _kerberos._tcp.lab.local → dc01",
     lambda: (lambda rc, out, _: ("dc01.lab.local" in out, out[:60]))
             (*_exec("alice", "dig @172.16.1.20 _kerberos._tcp.lab.local SRV +short"))),
    # PTR reverse lookups
    ("DNS: PTR 172.16.1.10 → web.lab.local",
     lambda: (lambda rc, out, _: ("web.lab.local" in out, out[:60]))
             (*_exec("alice", "dig @172.16.1.20 -x 172.16.1.10 +short"))),
    # Zone transfer — intentionally open misconfiguration
    ("DNS: AXFR lab.local (zone transfer open — recon!)",
     lambda: dns_axfr("internet-client", "172.16.1.20", "lab.local",
                      ["alice", "bob", "dc01", "fileserver", "mail", "web", "monitor"])),
]

# 4. Web — nginx, TLS cert, headers, content
WEB_TESTS = [
    ("Web: HTTP 200 on web:80",
     lambda: http_status("internet-client", "http://172.16.1.10")),
    ("Web: HTTPS 200 on web:443",
     lambda: http_status("internet-client", "https://172.16.1.10")),
    ("Web: Server header contains nginx",
     lambda: http_header("internet-client", "http://172.16.1.10", "Server", "nginx")),
    ("Web: X-Powered-By header present (PHP/8.2.7)",
     lambda: http_header("internet-client", "http://172.16.1.10", "X-Powered-By", "PHP")),
    ("Web: robots.txt disallows /admin",
     lambda: http_contains("internet-client", "http://172.16.1.10/robots.txt", "/admin")),
    ("Web: robots.txt disallows /backup",
     lambda: http_contains("internet-client", "http://172.16.1.10/robots.txt", "/backup")),
    ("Web: /api/v1/status returns JSON",
     lambda: http_contains("internet-client", "http://172.16.1.10/api/v1/status", "production")),
    ("Web: /api/v1/status reveals db_host",
     lambda: http_contains("internet-client", "http://172.16.1.10/api/v1/status", "db.lab.local")),
    ("Web: /admin returns 401",
     lambda: http_status("internet-client", "http://172.16.1.10/admin", "401")),
    ("Web: TLS cert contains org name",
     lambda: (lambda rc, out, _:
              ("Acme Corp" in out, out[out.find("O ="):out.find("O =")+40] if "O =" in out else out[:60]))
             (*_exec("internet-client",
                     "openssl s_client -connect 172.16.1.10:443 </dev/null 2>/dev/null "
                     "| openssl x509 -noout -subject 2>/dev/null", timeout=15))),
    ("Web: TLS cert SAN contains web.lab.local",
     lambda: (lambda rc, out, _: ("web.lab.local" in out, out[:80]))
             (*_exec("internet-client",
                     "openssl s_client -connect 172.16.1.10:443 </dev/null 2>/dev/null "
                     "| openssl x509 -noout -ext subjectAltName 2>/dev/null", timeout=15))),
    ("Web: index.html mentions Acme Corp",
     lambda: http_contains("internet-client", "http://172.16.1.10", "Acme Corp")),
    ("Web: about.html reveals employee names",
     lambda: http_contains("internet-client", "http://172.16.1.10/about.html", "bjones@lab.local")),
]

# 5. Mail — SMTP banner, EHLO, VRFY user enumeration, IMAP banner
MAIL_TESTS = [
    ("Mail: SMTP banner contains Postfix",
     lambda: banner_contains("internet-client", "172.16.1.30", 25, "Postfix")),
    ("Mail: SMTP banner contains mail.lab.local",
     lambda: banner_contains("internet-client", "172.16.1.30", 25, "mail.lab.local")),
    ("Mail: EHLO reveals STARTTLS capability",
     lambda: banner_contains("internet-client", "172.16.1.30", 25, "STARTTLS",
                             send="EHLO test\\r\\n")),
    ("Mail: EHLO reveals VRFY capability",
     lambda: banner_contains("internet-client", "172.16.1.30", 25, "VRFY",
                             send="EHLO test\\r\\n")),
    ("Mail: VRFY jsmith → 250 (user enumeration)",
     lambda: banner_contains("internet-client", "172.16.1.30", 25, "250",
                             send="EHLO test\\r\\nVRFY jsmith\\r\\n")),
    ("Mail: VRFY nobody → 550 (unknown user)",
     lambda: banner_contains("internet-client", "172.16.1.30", 25, "550",
                             send="EHLO test\\r\\nVRFY nobody_xyz\\r\\n")),
    ("Mail: IMAP banner contains Dovecot",
     lambda: banner_contains("internet-client", "172.16.1.30", 143, "Dovecot")),
    ("Mail: IMAP ID command reveals version",
     lambda: banner_contains("alice", "172.16.1.30", 143, "2.3",
                             send="a1 ID NIL\\r\\n")),
    ("Mail: SMTP port 587 (submission) open",
     lambda: tcp_open("internet-client", "172.16.1.30", 587)),
]

# 6. SSH — banners and access
SSH_TESTS = [
    ("SSH: jump host port 22 open (WAN)",
     lambda: tcp_open("internet-client", "172.16.1.40", 22)),
    ("SSH: jump banner contains OpenSSH",
     lambda: banner_contains("internet-client", "172.16.1.40", 22, "OpenSSH")),
    ("SSH: alice port 22 open (LAN)",
     lambda: tcp_open("bob", "192.168.10.100", 22)),
    ("SSH: alice banner contains OpenSSH",
     lambda: banner_contains("bob", "192.168.10.100", 22, "OpenSSH")),
    ("SSH: bob port 22 open (LAN)",
     lambda: tcp_open("alice", "192.168.10.101", 22)),
    ("SSH: fileserver port 22 open (LAN)",
     lambda: tcp_open("alice", "192.168.10.20", 22)),
    ("SSH: jump known_hosts reveals internal IPs",
     lambda: (lambda rc, out, _: ("192.168.10" in out, out[:80]))
             (*_exec("jump", "cat /home/padmin/.ssh/known_hosts 2>/dev/null"))),
    ("SSH: jump .ash_history reveals admin activity",
     lambda: (lambda rc, out, _: (len(out) > 0, out[:80]))
             (*_exec("jump", "cat /home/padmin/.ash_history 2>/dev/null"))),
]

# 7. SMB — share enumeration on fileserver
SMB_TESTS = [
    ("SMB: fileserver port 445 open",
     lambda: tcp_open("alice", "192.168.10.20", 445)),
    ("SMB: fileserver port 139 open",
     lambda: tcp_open("alice", "192.168.10.20", 139)),
    ("SMB: null session lists shares (public visible)",
     lambda: (lambda rc, out, _: ("public" in out.lower(), out[:120]))
             (*_exec("alice", "smbclient -L //192.168.10.20 -N 2>&1", timeout=15))),
    ("SMB: finance share visible in listing",
     lambda: (lambda rc, out, _: ("finance" in out.lower(), out[:120]))
             (*_exec("alice", "smbclient -L //192.168.10.20 -N 2>&1", timeout=15))),
    ("SMB: backup share NOT in listing (hidden)",
     lambda: (lambda rc, out, _: ("backup" not in out.lower(), out[:120]))
             (*_exec("alice", "smbclient -L //192.168.10.20 -N 2>&1", timeout=15))),
    ("SMB: public share readable without auth",
     lambda: (lambda rc, out, _: (rc == 0 or "README" in out, out[:80]))
             (*_exec("alice", "smbclient //192.168.10.20/public -N -c 'ls' 2>&1", timeout=15))),
    ("SMB: dc01 port 445 open (AD SMB)",
     lambda: tcp_open("alice", "192.168.10.5", 445)),
]

# 8. Workstation services — RDP and WinRM banners
WORKSTATION_TESTS = [
    ("WS: alice RDP port 3389 open",
     lambda: tcp_open("bob", "192.168.10.100", 3389)),
    ("WS: bob RDP port 3389 open",
     lambda: tcp_open("alice", "192.168.10.101", 3389)),
    ("WS: alice WinRM port 5985 open",
     lambda: tcp_open("bob", "192.168.10.100", 5985)),
    ("WS: bob WinRM port 5985 open",
     lambda: tcp_open("alice", "192.168.10.101", 5985)),
    ("WS: alice WinRM returns HTTP 401 Negotiate",
     lambda: http_contains("bob", "http://192.168.10.100:5985/wsman", "401") or
             (lambda rc, out, _: ("Negotiate" in out or "401" in out, out[:80]))
             (*_exec("bob", "curl -s -o /dev/null -w '%{http_code}' http://192.168.10.100:5985/wsman"))),
    ("WS: alice SSH login banner present",
     lambda: banner_contains("bob", "192.168.10.100", 22, "Acme Corp")),
    ("WS: bob SSH login banner present",
     lambda: banner_contains("alice", "192.168.10.101", 22, "Acme Corp")),
]

# 9. Active Directory / LDAP / Kerberos
AD_TESTS = [
    ("AD: dc01 LDAP port 389 open",
     lambda: tcp_open("alice", "192.168.10.5", 389)),
    ("AD: dc01 Kerberos port 88 open",
     lambda: tcp_open("alice", "192.168.10.5", 88)),
    ("AD: dc01 RPC port 135 open",
     lambda: tcp_open("alice", "192.168.10.5", 135)),
    ("AD: dc01 Global Catalog port 3268 open",
     lambda: tcp_open("alice", "192.168.10.5", 3268)),
    ("AD: LDAP base DN readable (anonymous)",
     lambda: (lambda rc, out, _:
              ("lab" in out.lower() or "dc=" in out.lower(), out[:100]))
             (*_exec("alice",
                     "ldapsearch -x -H ldap://192.168.10.5 -b '' -s base namingContexts 2>&1",
                     timeout=15))),
    ("AD: LDAP DIT contains users",
     lambda: (lambda rc, out, _:
              ("jsmith" in out or "bjones" in out or "uid" in out.lower(), out[:120]))
             (*_exec("alice",
                     "ldapsearch -x -H ldap://192.168.10.5 -b 'dc=lab,dc=local' "
                     "'(objectClass=person)' cn uid 2>&1 | head -30",
                     timeout=20))),
]

# 10. Database
DATABASE_TESTS = [
    ("DB: MariaDB port 3306 open (from LAN)",
     lambda: tcp_open("alice", "192.168.10.10", 3306)),
    ("DB: MariaDB port 3306 blocked (from WAN)",
     lambda: tcp_blocked("internet-client", "192.168.10.10", 3306)),
    ("DB: appuser can connect and query",
     lambda: (lambda rc, out, _: (rc == 0 and "ok" in out, out[:80]))
             (*_exec("alice",
                     "mysql -h 192.168.10.10 -u appuser -papppass appdb "
                     "-e 'SELECT 1 AS ok;' 2>&1",
                     timeout=20))),
    ("DB: appdb.users table exists",
     lambda: (lambda rc, out, _: (rc == 0 and "jsmith" in out, out[:120]))
             (*_exec("alice",
                     "mysql -h 192.168.10.10 -u appuser -papppass appdb "
                     "-e 'SELECT username FROM users LIMIT 5;' 2>&1",
                     timeout=20))),
    ("DB: app_config reveals infrastructure hostnames",
     lambda: (lambda rc, out, _: (rc == 0 and "lab.local" in out, out[:120]))
             (*_exec("alice",
                     "mysql -h 192.168.10.10 -u appuser -papppass appdb "
                     "-e 'SELECT key_name, value FROM app_config;' 2>&1",
                     timeout=20))),
    ("DB: web server (172.16.1.10) can connect to db",
     lambda: (lambda rc, out, _: (rc == 0, out[:60]))
             (*_exec("web",
                     "mysql -h 192.168.10.10 -u appuser -papppass appdb "
                     "-e 'SELECT 1;' 2>&1",
                     timeout=20))),
]

# 11. Monitoring — Prometheus topology disclosure
MONITORING_TESTS = [
    ("Monitor: port 9090 open",
     lambda: tcp_open("alice", "192.168.10.50", 9090)),
    ("Monitor: port 9100 open (node exporter)",
     lambda: tcp_open("alice", "192.168.10.50", 9100)),
    ("Monitor: /api/v1/targets returns JSON",
     lambda: http_contains("alice", "http://192.168.10.50:9090/api/v1/targets", "activeTargets")),
    ("Monitor: targets reveal dc01",
     lambda: http_contains("alice", "http://192.168.10.50:9090/api/v1/targets", "dc01")),
    ("Monitor: targets reveal alice workstation",
     lambda: http_contains("alice", "http://192.168.10.50:9090/api/v1/targets", "alice")),
    ("Monitor: targets reveal department labels",
     lambda: http_contains("alice", "http://192.168.10.50:9090/api/v1/targets", "finance")),
    ("Monitor: targets reveal SNMP community string",
     lambda: http_contains("alice", "http://192.168.10.50:9090/api/v1/targets", "public")),
    ("Monitor: /config reveals all scrape targets",
     lambda: http_contains("alice", "http://192.168.10.50:9090/config", "alice.lab.local")),
    ("Monitor: node exporter reveals filesystem mounts",
     lambda: http_contains("alice", "http://192.168.10.50:9100/metrics", "node_filesystem")),
    ("Monitor: unreachable from WAN (blocked by firewall)",
     lambda: tcp_blocked("internet-client", "192.168.10.50", 9090)),
]

# 12. Wiki (Gitea)
WIKI_TESTS = [
    ("Wiki: port 3000 open",
     lambda: tcp_open("alice", "192.168.10.30", 3000)),
    ("Wiki: HTTP 200 on /",
     lambda: http_status("alice", "http://192.168.10.30:3000")),
    ("Wiki: response contains Gitea",
     lambda: http_contains("alice", "http://192.168.10.30:3000", "Gitea")),
    ("Wiki: /explore/repos accessible (unauthenticated)",
     lambda: http_status("alice", "http://192.168.10.30:3000/explore/repos")),
    ("Wiki: SSH port 2222 open",
     lambda: tcp_open("alice", "192.168.10.30", 2222)),
    ("Wiki: unreachable from WAN",
     lambda: tcp_blocked("internet-client", "192.168.10.30", 3000)),
]


# ── Suite registry ────────────────────────────────────────────────────────────

SUITES: dict[str, tuple[str, list]] = {
    "connectivity": ("Connectivity",  CONNECTIVITY_TESTS),
    "firewall":     ("Firewall",      FIREWALL_TESTS),
    "dns":          ("DNS",           DNS_TESTS),
    "web":          ("Web",           WEB_TESTS),
    "mail":         ("Mail",          MAIL_TESTS),
    "ssh":          ("SSH",           SSH_TESTS),
    "smb":          ("SMB",           SMB_TESTS),
    "workstation":  ("Workstations",  WORKSTATION_TESTS),
    "ad":           ("Active Directory / LDAP", AD_TESTS),
    "database":     ("Database",      DATABASE_TESTS),
    "monitoring":   ("Monitoring",    MONITORING_TESTS),
    "wiki":         ("Wiki (Gitea)",  WIKI_TESTS),
}


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Enterprise Network Lab 2 — Smoke Tests")
    parser.add_argument(
        "--suites", nargs="+", choices=list(SUITES), metavar="SUITE",
        help=f"Run only these suites. Choices: {', '.join(SUITES)}",
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detail for passing tests too")
    parser.add_argument("--wait", type=int, default=0,
                        help="Wait N seconds before starting (let containers settle)")
    args = parser.parse_args()

    if args.wait:
        print(f"{DIM}Waiting {args.wait}s for containers to settle…{RESET}")
        time.sleep(args.wait)

    selected = {k: v for k, v in SUITES.items()
                if not args.suites or k in args.suites}

    print(f"\n{BOLD}Enterprise Network Lab 2 — Smoke Tests{RESET}")
    print(f"{DIM}Lab prefix: {LAB}{RESET}\n")

    total = passed = 0

    for key, (suite_name, tests) in selected.items():
        print(f"{BOLD}{CYAN}{suite_name}{RESET}")
        for name, check in tests:
            result = run_test(name, check)
            print_result(result, verbose=args.verbose)
            total += 1
            if result.passed:
                passed += 1
        print()

    failed = total - passed
    color  = GREEN if failed == 0 else RED
    print(f"{BOLD}Results: {color}{passed}/{total} passed{RESET}",
          f"  {DIM}({failed} failed){RESET}" if failed else "")

    if failed > 0:
        print(f"\n{YELLOW}Tip: run with --verbose to see details for all tests.{RESET}")
        print(f"{YELLOW}     run with --suites <name> to focus on a single suite.{RESET}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
