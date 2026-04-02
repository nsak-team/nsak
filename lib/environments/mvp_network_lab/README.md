# Enterprise Network Lab (MVP – Stage 1)

Simulated enterprise network with three segments (WAN / DMZ / LAN) for
reproducible network attack scenarios with NSAK.

## Topology

```
internet-client (203.0.113.100)
        │
   [wan-br]  WAN 203.0.113.0/24
        │
   [firewall]  .1 on all three segments
        │                    │
   [dmz-br] 172.16.1.0/24   [lan-br] 192.168.10.0/24
      ├─ web         172.16.1.10    ├─ db          192.168.10.10
      ├─ dns         172.16.1.20    ├─ ws1         192.168.10.100
      └─ nsak (eth2) 172.16.1.50   ├─ ws2         192.168.10.101
                                   └─ nsak (eth1) 192.168.10.50
```

### Nodes

| Node | Image | IP(s) | Role |
|---|---|---|---|
| `firewall` | alpine:3.19 | .1 on WAN/DMZ/LAN | iptables, IP forwarding, NAT |
| `internet-client` | alpine:3.19 | 203.0.113.100 | External attacker / user |
| `dns` | alpine:3.19 | 172.16.1.20 | dnsmasq, zone `lab.local` |
| `web` | nginx:alpine | 172.16.1.10 | HTTP server in DMZ |
| `db` | mariadb:lts | 192.168.10.10 | MariaDB, database `appdb` |
| `ws1` | alpine:3.19 | 192.168.10.100 | Internal client 1 |
| `ws2` | alpine:3.19 | 192.168.10.101 | Internal client 2 |
| `nsak` | nsak:latest | 192.168.10.50 / 172.16.1.50 | NSAK (LAN + DMZ) |

### Firewall Rules (Default DENY FORWARD)

| From | To | Allowed |
|---|---|---|
| LAN / DMZ | WAN | all (NAT masquerade) |
| LAN | DMZ | all (workstations → web/dns) |
| WAN | DMZ | TCP:80 (web), UDP/TCP:53 (dns) |
| DMZ | LAN | TCP:3306 (web backend → db) |

### DNS (`lab.local`)

| Hostname | IP |
|---|---|
| `firewall.lab.local` | 172.16.1.1 |
| `web.lab.local` | 172.16.1.10 |
| `dns.lab.local` | 172.16.1.20 |
| `db.lab.local` | 192.168.10.10 |
| `ws1.lab.local` | 192.168.10.100 |
| `ws2.lab.local` | 192.168.10.101 |

## Prerequisites

- [ContainerLab](https://containerlab.dev/install/) installed
- Docker or Podman
- NSAK image built locally (once, from the project root):

```bash
docker build -t nsak:latest .
```

## Deploy the lab

ContainerLab's `bridge` kind references existing Linux bridges — it does not
create them. Create the three segment bridges once before the first deploy
(they are lost on reboot):

```bash
sudo ip link add wan-br type bridge && sudo ip link set wan-br up
sudo ip link add dmz-br type bridge && sudo ip link set dmz-br up
sudo ip link add lan-br type bridge && sudo ip link set lan-br up
```

Then deploy:

```bash
# From the project root
sudo containerlab deploy -t lib/environments/enterprise_network_lab/topology.clab.yaml
# To --destroy the container and deploy new 
sudo containerlab deploy -t lib/environments/enterprise_network_lab/topology.clab.yaml --reconfigure
```

## Destroy the lab

```bash
sudo containerlab destroy -t lib/environments/enterprise_network_lab/topology.clab.yaml
```

## Using NSAK

The NSAK container sits on both **LAN** (`eth1`) and **DMZ** (`eth2`), mirroring
the `is_target` interfaces of the physical BananaPI R4 device.

```bash
# Open a shell in the NSAK container
docker exec -it clab-enterprise-network-lab-nsak bash

# List available scenarios
nsak scenario list

# Execute a scenario
nsak scenario execute <scenario> [--option value]
```

### Example: MITM on the LAN (ws1 ↔ ws2)

The MITM scenario runs three drills in sequence:
1. **discover_hosts** — ARP scan to find all hosts on the segment
2. **transparent_tcp_proxy** — sets up a proxy to intercept TCP traffic
3. **arp_spoof** — poisons the ARP caches of all discovered hosts

```bash
docker exec -it clab-enterprise-network-lab-nsak bash

# Run MITM on the LAN segment (eth1)
# NSAK will intercept traffic between ws1 (192.168.10.100)
# and ws2 (192.168.10.101)
nsak scenario execute mitm --interface eth1
```

To run MITM on the DMZ segment instead (web ↔ dns):

```bash
nsak scenario execute mitm --interface eth2
```

### Simulating Traffic Between ws1 and ws2

Open two terminals — one per workstation.

**Terminal 1 — ws2 (server):**

```bash
docker exec -it clab-enterprise-network-lab-ws2 sh

# Start a simple HTTP server on port 8080
mkdir -p /srv && echo "Hello from ws2" > /srv/index.html
busybox-extras httpd -f -p 8080 -h /srv
```

**Terminal 2 — ws1 (client):**

```bash
docker exec -it clab-enterprise-network-lab-ws1 sh

# Send a request every second — keep this running while NSAK executes MITM
while true; do wget -qO- http://192.168.10.101:8080; sleep 1; done
```

With both running, start the MITM scenario in the NSAK container:

```bash
docker exec -it clab-enterprise-network-lab-nsak bash
nsak scenario execute mitm --interface eth1
```

The NSAK will discover both hosts, intercept the TCP stream between ws1 and ws2,
and you will see the HTTP responses passing through the proxy.

## Connecting to other containers

```bash
docker exec -it clab-enterprise-network-lab-ws1 sh
docker exec -it clab-enterprise-network-lab-ws2 sh
docker exec -it clab-enterprise-network-lab-internet-client sh

# Verify connectivity (from ws1)
ping 172.16.1.10
curl http://web.lab.local
dig @172.16.1.20 web.lab.local
mysql -h 192.168.10.10 -u appuser -papppass appdb
```

## Sniffing traffic on the host

ContainerLab creates a Linux bridge on the host for each network segment:

```bash
# List bridges
ip link show type bridge

# Capture traffic on a segment (e.g. LAN)
sudo tcpdump -i lan-br -n
```
