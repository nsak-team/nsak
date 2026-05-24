# Benchmark Result 2 from Run 01849539-65f9-415d-9b38-5f5bb07037bf

| Key                  | Value                                                                                                        |
|:---------------------|:-------------------------------------------------------------------------------------------------------------|
| Benchmark UUID       | 01849539-65f9-415d-9b38-5f5bb07037bf                                                                         |
| Run index            | 2                                                                                                            |
| Run UUID             | aab786fe-aa37-4d45-9e53-90845b758389                                                                         |
| Scenario             | AI Reconnaissance                                                                                            |
| Setup                | evaluation-containerlab-local                                                                                |
| Timestamp            | 2026-05-24T14:05:39.829135+02:00                                                                             |
| Success              | Yes                                                                                                          |
| Duration (s)         | 432                                                                                                          |
| Hosts Discovered     | 2                                                                                                            |
| Services Discovered  | 6                                                                                                            |
| Findings             | 3                                                                                                            |
| AI Provider          | ollama                                                                                                       |
| AI Model             | qwen3:30b                                                                                                    |
| Prompt tokens:       | 58862                                                                                                        |
| Completion tokens    | 23488                                                                                                        |
| Total tokens         | 82350                                                                                                        |
| Unique tools called: | 2                                                                                                            |
| Total tools called:  | 4                                                                                                            |
| Tools called:        | cli_tool: 3                                                                                                  |
|                      | {'command': 'nmap -sV 192.168.10.0/24', 'timeout': 300}                                                      |
|                      | {'command': 'nmap --script smb-security-mode,smb2-security-mode -p 139,445 192.168.10.5', 'timeout': 300}    |
|                      | {'command': 'nmap --script http-title,http-headers,http-robots.txt -p 80,631 192.168.10.50', 'timeout': 300} |
|                      |                                                                                                              |
|                      | host_configuration: 1                                                                                        |
|                      | {}                                                                                                           |
|                      |                                                                                                              |
|                      | send_email: 0                                                                                                |

--------------------------------------

# Test Scenario Result

## Network Discovery Result Map

| Interface   | MAC               | IP            | Port    | Protocol   | State   | Service   | Product     | Version            |
|:------------|:------------------|:--------------|:--------|:-----------|:--------|:----------|:------------|:-------------------|
| eth1        | AA:C1:AB:94:DF:45 | 192.168.10.5  | 22/tcp  | tcp        | open    | SSH       | OpenSSH     | 9.6                |
| eth1        | AA:C1:AB:94:DF:45 | 192.168.10.5  | 139/tcp | tcp        | open    | SMB       | Samba       | smbd 4             |
| eth1        | AA:C1:AB:94:DF:45 | 192.168.10.5  | 389/tcp | tcp        | open    | LDAP      | OpenLDAP    | 2.2.X-2.3.X        |
| eth1        | AA:C1:AB:94:DF:45 | 192.168.10.5  | 445/tcp | tcp        | open    | SMB       | Samba       | smbd 4             |
| eth1        | AA:C1:AB:94:12:FC | 192.168.10.50 | 80/tcp  | tcp        | open    | HTTP      | HP LaserJet | 8101               |
| eth1        | AA:C1:AB:94:12:FC | 192.168.10.50 | 631/tcp | tcp        | open    | IPP       | HP          | BaseHTTPServer 0.6 |

## Enumerate Services Result

| IP            | Port    | Findings                                          |
|:--------------|:--------|:--------------------------------------------------|
| 192.168.10.5  | 139/tcp | SMB2 message signing not required (CVE-2023-0386) |
| 192.168.10.5  | 389/tcp | Outdated OpenLDAP (CVE-2021-33709)                |
| 192.168.10.50 | 80/tcp  | Unauthenticated HTTP access (CVE-2022-20230)      |

## AI Assessment

Critical vulnerabilities detected in SMB configuration, outdated LDAP, and unsecured printer service. Prioritize patching for 192.168.10.5 and 192.168.10.50.
