#!/usr/bin/env python3
"""
monitor_ui.py — Unauthenticated Prometheus-like monitoring UI.

Ports:
  9090/tcp  Prometheus web UI + API
  9100/tcp  Node Exporter (host metrics, reveals hostname/users/mounts)

Key recon endpoints:
  GET /api/v1/targets       → all monitored hosts with IPs, roles, departments
  GET /api/v1/label/__name__/values  → all metric names
  GET /metrics              → Prometheus own metrics
  GET /graph                → web UI (reveals Prometheus version)

The targets list deliberately reveals the full internal topology:
  dc01, db, fileserver, wiki, ws1, ws2, firewall, web, mail
  with labels: hostname, zone, role, department, snmp_community
"""
import json
import socket
import threading
import time

# ── Scrape target inventory — the recon goldmine ──────────────────────────────
ACTIVE_TARGETS = [
    {
        "discoveredLabels": {"__address__": "dc01.lab.local:9100", "__scheme__": "http"},
        "labels": {
            "hostname": "dc01", "instance": "dc01.lab.local:9100",
            "job": "node", "zone": "lan", "role": "domain-controller",
            "os": "linux", "ip": "192.168.10.5",
        },
        "scrapeUrl": "http://dc01.lab.local:9100/metrics",
        "health": "up", "lastScrape": "2024-03-15T08:00:01Z", "lastScrapeDuration": 0.012,
    },
    {
        "discoveredLabels": {"__address__": "db.lab.local:9100"},
        "labels": {
            "hostname": "db", "instance": "db.lab.local:9100",
            "job": "node", "zone": "lan", "role": "database",
            "os": "linux", "ip": "192.168.10.10",
        },
        "scrapeUrl": "http://db.lab.local:9100/metrics",
        "health": "up", "lastScrape": "2024-03-15T08:00:02Z", "lastScrapeDuration": 0.009,
    },
    {
        "discoveredLabels": {"__address__": "fileserver.lab.local:9100"},
        "labels": {
            "hostname": "fileserver", "instance": "fileserver.lab.local:9100",
            "job": "node", "zone": "lan", "role": "file-server",
            "os": "linux", "ip": "192.168.10.20",
        },
        "scrapeUrl": "http://fileserver.lab.local:9100/metrics",
        "health": "up", "lastScrape": "2024-03-15T08:00:03Z", "lastScrapeDuration": 0.011,
    },
    {
        "discoveredLabels": {"__address__": "wiki.lab.local:3000"},
        "labels": {
            "hostname": "wiki", "instance": "wiki.lab.local:3000",
            "job": "gitea", "zone": "lan", "role": "devops",
            "os": "linux", "ip": "192.168.10.30",
        },
        "scrapeUrl": "http://wiki.lab.local:3000/metrics",
        "health": "up", "lastScrape": "2024-03-15T08:00:04Z", "lastScrapeDuration": 0.018,
    },
    {
        "discoveredLabels": {"__address__": "alice.lab.local:9100"},
        "labels": {
            "hostname": "alice", "instance": "alice.lab.local:9100",
            "job": "node", "zone": "lan", "role": "workstation",
            "department": "finance", "user": "jsmith", "ip": "192.168.10.100",
        },
        "scrapeUrl": "http://alice.lab.local:9100/metrics",
        "health": "up", "lastScrape": "2024-03-15T08:00:05Z", "lastScrapeDuration": 0.008,
    },
    {
        "discoveredLabels": {"__address__": "bob.lab.local:9100"},
        "labels": {
            "hostname": "bob", "instance": "bob.lab.local:9100",
            "job": "node", "zone": "lan", "role": "workstation",
            "department": "it", "user": "bjones", "ip": "192.168.10.101",
        },
        "scrapeUrl": "http://bob.lab.local:9100/metrics",
        "health": "up", "lastScrape": "2024-03-15T08:00:06Z", "lastScrapeDuration": 0.009,
    },
    {
        "discoveredLabels": {"__address__": "web.lab.local:80"},
        "labels": {
            "hostname": "web", "instance": "web.lab.local:80",
            "job": "blackbox", "zone": "dmz", "role": "web-server",
            "ip": "172.16.1.10",
        },
        "scrapeUrl": "http://web.lab.local/metrics",
        "health": "up", "lastScrape": "2024-03-15T08:00:07Z", "lastScrapeDuration": 0.015,
    },
    {
        "discoveredLabels": {"__address__": "mail.lab.local:25"},
        "labels": {
            "hostname": "mail", "instance": "mail.lab.local:25",
            "job": "blackbox", "zone": "dmz", "role": "mail-relay",
            "ip": "172.16.1.30",
        },
        "scrapeUrl": "http://mail.lab.local:9100/metrics",
        "health": "unknown", "lastScrape": "2024-03-15T08:00:08Z", "lastScrapeDuration": 0.003,
    },
    {
        "discoveredLabels": {"__address__": "firewall.lab.local:161"},
        "labels": {
            "hostname": "firewall", "instance": "firewall.lab.local:161",
            "job": "snmp", "zone": "mgmt", "role": "firewall",
            "snmp_community": "public", "ip": "192.168.10.1",
        },
        "scrapeUrl": "snmp://firewall.lab.local",
        "health": "up", "lastScrape": "2024-03-15T08:00:09Z", "lastScrapeDuration": 0.025,
    },
]

NODE_EXPORTER_METRICS = """\
# HELP node_uname_info Labeled system information
# TYPE node_uname_info gauge
node_uname_info{domainname="lab.local",machine="x86_64",nodename="monitor.lab.local",release="5.15.0-101-generic",sysname="Linux",version="#111-Ubuntu SMP"} 1
# HELP node_logged_in_users Logged in users
# TYPE node_logged_in_users gauge
node_logged_in_users 1
# HELP node_load1 1m load average
# TYPE node_load1 gauge
node_load1 0.42
# HELP node_cpu_seconds_total CPU time
# TYPE node_cpu_seconds_total counter
node_cpu_seconds_total{cpu="0",mode="idle"} 42312.5
node_cpu_seconds_total{cpu="0",mode="user"} 821.3
# HELP node_filesystem_size_bytes Filesystem size
# TYPE node_filesystem_size_bytes gauge
node_filesystem_size_bytes{device="/dev/sda1",fstype="ext4",mountpoint="/"} 107374182400
node_filesystem_size_bytes{device="//FILESERVER/backup",fstype="cifs",mountpoint="/mnt/backup"} 1099511627776
node_filesystem_size_bytes{device="//DC01/SYSVOL",fstype="cifs",mountpoint="/mnt/sysvol"} 10737418240
# HELP node_network_info Network interface info
# TYPE node_network_info gauge
node_network_info{address="192.168.10.50",broadcast="192.168.10.255",device="eth1",duplex="full"} 1
"""

INDEX_HTML = """\
<!DOCTYPE html>
<html>
<head>
  <title>Prometheus - Acme Corp Monitoring</title>
  <style>
    body { font-family: sans-serif; margin: 20px; background: #f5f5f5; }
    h2 { color: #e6522c; }
    table { border-collapse: collapse; width: 100%; background: white; }
    td, th { border: 1px solid #ddd; padding: 8px 14px; font-size: 0.9em; }
    th { background: #e6522c; color: white; }
    tr:nth-child(even) { background: #f9f9f9; }
    .up { color: green; font-weight: bold; }
    .down { color: red; }
    footer { margin-top: 20px; font-size: 0.8em; color: #999; }
  </style>
</head>
<body>
  <h2>Prometheus — Acme Corp AG Internal Monitoring</h2>
  <p>Version: 2.47.0 / Build: go1.21.4 / Environment: production / Domain: lab.local</p>
  <ul>
    <li><a href="/targets">Targets</a></li>
    <li><a href="/api/v1/targets">API: /api/v1/targets</a></li>
    <li><a href="/metrics">Own Metrics</a></li>
    <li><a href="/graph">Expression Browser</a></li>
    <li><a href="/config">Config</a></li>
  </ul>
  <h3>Quick Target Overview</h3>
  <table>
    <tr><th>Host</th><th>Zone</th><th>Role</th><th>IP</th><th>Health</th></tr>
    <tr><td>dc01.lab.local:9100</td><td>lan</td><td>domain-controller</td><td>192.168.10.5</td><td class="up">UP</td></tr>
    <tr><td>db.lab.local:9100</td><td>lan</td><td>database</td><td>192.168.10.10</td><td class="up">UP</td></tr>
    <tr><td>fileserver.lab.local:9100</td><td>lan</td><td>file-server</td><td>192.168.10.20</td><td class="up">UP</td></tr>
    <tr><td>wiki.lab.local:3000</td><td>lan</td><td>devops</td><td>192.168.10.30</td><td class="up">UP</td></tr>
    <tr><td>alice.lab.local:9100</td><td>lan</td><td>workstation/finance</td><td>192.168.10.100</td><td class="up">UP</td></tr>
    <tr><td>bob.lab.local:9100</td><td>lan</td><td>workstation/it</td><td>192.168.10.101</td><td class="up">UP</td></tr>
    <tr><td>web.lab.local:80</td><td>dmz</td><td>web-server</td><td>172.16.1.10</td><td class="up">UP</td></tr>
    <tr><td>mail.lab.local:25</td><td>dmz</td><td>mail-relay</td><td>172.16.1.30</td><td>UNKNOWN</td></tr>
    <tr><td>firewall.lab.local:161</td><td>mgmt</td><td>firewall/snmp</td><td>192.168.10.1</td><td class="up">UP</td></tr>
  </table>
  <footer>Prometheus 2.47.0 | Acme Corp AG | monitor.lab.local | Unauthorized access prohibited</footer>
</body>
</html>"""

CONFIG_YAML = """\
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    environment: production
    domain: lab.local

scrape_configs:
  - job_name: node
    static_configs:
      - targets:
          - dc01.lab.local:9100
          - db.lab.local:9100
          - fileserver.lab.local:9100
          - alice.lab.local:9100
          - bob.lab.local:9100
        labels:
          zone: lan

  - job_name: gitea
    static_configs:
      - targets: [wiki.lab.local:3000]
        labels: {zone: lan, role: devops}

  - job_name: blackbox
    static_configs:
      - targets: [web.lab.local:80, mail.lab.local:25]
        labels: {zone: dmz}

  - job_name: snmp
    static_configs:
      - targets: [firewall.lab.local]
        labels: {snmp_community: public, zone: mgmt}
"""


def handle(conn: socket.socket, port: int) -> None:
    try:
        req = conn.recv(4096).decode(errors="ignore")
        path = req.split(" ")[1].split("?")[0] if " " in req else "/"

        if path == "/api/v1/targets":
            body = json.dumps({"status": "success", "data": {
                "activeTargets": ACTIVE_TARGETS,
                "droppedTargets": [],
            }})
            ct = "application/json"
        elif path == "/metrics" and port == 9100:
            body = NODE_EXPORTER_METRICS
            ct = "text/plain; version=0.0.4"
        elif path == "/metrics":
            body = '# Prometheus internal metrics\nprometheus_build_info{version="2.47.0",goversion="go1.21.4"} 1\n'
            ct = "text/plain; version=0.0.4"
        elif path == "/config":
            body = CONFIG_YAML
            ct = "text/plain"
        else:
            body = INDEX_HTML
            ct = "text/html; charset=UTF-8"

        resp = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: {ct}\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
            f"Server: Prometheus/2.47.0\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        ) + body
        conn.sendall(resp.encode())
    except (BrokenPipeError, ConnectionResetError, OSError):
        pass
    finally:
        conn.close()


def serve(port: int) -> None:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", port))
    srv.listen(20)
    print(f"[monitor] Listening on :{port}", flush=True)
    while True:
        conn, _ = srv.accept()
        threading.Thread(target=handle, args=(conn, port), daemon=True).start()


if __name__ == "__main__":
    for p in [9090, 9100]:
        threading.Thread(target=serve, args=(p,), daemon=True).start()
    while True:
        time.sleep(60)
