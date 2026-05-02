# Discover Hosts

Discovers active hosts on a network and returns their IP and MAC addresses.

Operates in two modes depending on whether the optional `subnet` argument is provided:

| Mode            | Tool                  | Use case                                               |
|-----------------|-----------------------|--------------------------------------------------------|
| Local (default) | `arp-scan --localnet` | Hosts on the same Layer 2 segment as `interface`       |
| Remote subnet   | `nmap -sn <subnet>`   | Hosts in an arbitrary subnet, across routers (Layer 3) |

MAC addresses are only available for hosts on the same Layer 2 segment. Remote hosts discovered via nmap will have an empty `mac` field.

## Arguments

| Argument    | Type  | Default | Description                                                                                |
|-------------|-------|---------|--------------------------------------------------------------------------------------------|
| `interface` | `str` | —       | Network interface to use (e.g. `eth0`)                                                     |
| `subnet`    | `str` | `null`  | Subnet to scan in CIDR notation (e.g. `10.0.2.0/24`). If omitted, scans the local segment. |

## Return type

`NetworkDiscoveryResultMap` — keyed by interface name, each entry contains a list of discovered `NetworkService` objects with IP, MAC, and vendor info.

## Usage

```bash
# Scan local segment on eth0
nsak drill run discover_hosts --interface eth0

# Scan a remote subnet via nmap
nsak drill run discover_hosts --interface eth0 --subnet 10.0.2.0/24
```

## Dependencies

- `arp-scan` (local mode)
- `nmap` (remote subnet mode)
