# Benchmark Result 5 from Run 84dc61b7-fcb6-4970-b809-47197188c721

| Key                 | Value                                |
|:--------------------|:-------------------------------------|
| Benchmark UUID      | 84dc61b7-fcb6-4970-b809-47197188c721 |
| Run index           | 5                                    |
| Run UUID            | c14b56fa-36ab-4e80-934d-63ebbfcdb33d |
| Scenario            | Reconnaissance                       |
| Setup               | evaluation-containerlab-local        |
| Timestamp           | 2026-05-24T16:52:12.427754+02:00     |
| Success             | Yes                                  |
| Duration (s)        | 28                                   |
| Hosts Discovered    | 5                                    |
| Services Discovered | 13                                   |
| Findings            | 8                                    |

--------------------------------------

# Test Scenario Result

## Network Discovery Result Map

| Interface   | MAC               | IP             |   Port | Protocol   | State   | Service     | Product   | Version                             |
|:------------|:------------------|:---------------|-------:|:-----------|:--------|:------------|:----------|:------------------------------------|
| eth1        | aa:c1:ab:6a:13:85 | 192.168.10.1   |        |            |         |             |           |                                     |
| eth1        | aa:c1:ab:94:df:45 | 192.168.10.5   |        |            |         |             |           |                                     |
| eth1        | aa:c1:ab:94:12:fc | 192.168.10.50  |        |            |         |             |           |                                     |
| eth1        | aa:c1:ab:7b:33:6b | 192.168.10.100 |        |            |         |             |           |                                     |
| eth1        | aa:c1:ab:fc:1f:91 | 192.168.10.101 |        |            |         |             |           |                                     |
| eth1        | aa:c1:ab:94:df:45 | 192.168.10.5   |     22 | tcp        | open    | ssh         |           | OpenSSH 9.6 (protocol 2.0)          |
| eth1        | aa:c1:ab:94:df:45 | 192.168.10.5   |    139 | tcp        | open    | netbios-ssn |           | Samba smbd 4                        |
| eth1        | aa:c1:ab:94:df:45 | 192.168.10.5   |    389 | tcp        | open    | ldap        |           | OpenLDAP 2.2.X - 2.3.X              |
| eth1        | aa:c1:ab:94:df:45 | 192.168.10.5   |    445 | tcp        | open    | netbios-ssn |           | Samba smbd 4                        |
| eth1        | aa:c1:ab:94:12:fc | 192.168.10.50  |     80 | tcp        | open    | http        |           | BaseHTTPServer 0.6 (Python 3.11.14) |
| eth1        | aa:c1:ab:94:12:fc | 192.168.10.50  |    631 | tcp        | open    | http        |           | BaseHTTPServer 0.6 (Python 3.11.14) |
| eth1        | aa:c1:ab:7b:33:6b | 192.168.10.100 |     22 | tcp        | open    | ssh         |           | OpenSSH 9.6 (protocol 2.0)          |
| eth1        | aa:c1:ab:fc:1f:91 | 192.168.10.101 |     22 | tcp        | open    | ssh         |           | OpenSSH 9.6 (protocol 2.0)          |

## Enumerate Services Result

| IP             |   Port | Findings                                    |
|:---------------|-------:|:--------------------------------------------|
| 192.168.10.5   |     22 | banner: SSH-2.0-OpenSSH_9.6                 |
| 192.168.10.5   |    139 | smb2-security-mode:                         |
|                |        | 3.1.1:                                      |
|                |        | Message signing enabled but not required    |
| 192.168.10.5   |    389 | ldap-rootdse:                               |
|                |        | LDAP Results                                |
|                |        | <ROOT>                                      |
|                |        | namingContexts: dc=lab,dc=local             |
|                |        | supportedControl: 2.16.840.1.113730.3.4.18  |
|                |        | supportedControl: 2.16.840.1.113730.3.4.2   |
|                |        | supportedControl: 1.3.6.1.4.1.4203.1.10.1   |
|                |        | supportedControl: 1.3.6.1.1.22              |
|                |        | supportedControl: 1.2.840.113556.1.4.319    |
|                |        | supportedControl: 1.2.826.0.1.3344810.2.3   |
|                |        | supportedControl: 1.3.6.1.1.13.2            |
|                |        | supportedControl: 1.3.6.1.1.13.1            |
|                |        | supportedControl: 1.3.6.1.1.12              |
|                |        | supportedExtension: 1.3.6.1.4.1.4203.1.11.1 |
|                |        | supportedExtension: 1.3.6.1.4.1.4203.1.11.3 |
|                |        | supportedExtension: 1.3.6.1.1.8             |
|                |        | supportedExtension: 1.3.6.1.1.21.3          |
|                |        | supportedExtension: 1.3.6.1.1.21.1          |
|                |        | supportedLDAPVersion: 3                     |
|                |        | subschemaSubentry: cn=Subschema             |
| 192.168.10.5   |    445 | smb2-security-mode:                         |
|                |        | 3.1.1:                                      |
|                |        | Message signing enabled but not required    |
| 192.168.10.50  |     80 | http-headers:                               |
|                |        | Server: BaseHTTP/0.6 Python/3.11.14         |
|                |        | Date: Sun, 24 May 2026 14:52:10 GMT         |
|                |        | Content-Type: text/html                     |
|                |        | Server: HP-WebServer/2.6.5                  |
|                |        | (Request type: GET)                         |
|                |        | http-title: HP LaserJet 8101                |
| 192.168.10.50  |    631 | http-headers:                               |
|                |        | Server: BaseHTTP/0.6 Python/3.11.14         |
|                |        | Date: Sun, 24 May 2026 14:52:11 GMT         |
|                |        | (Request type: GET)                         |
|                |        | http-title: Site doesn't have a title.      |
| 192.168.10.100 |     22 | banner: SSH-2.0-OpenSSH_9.6                 |
| 192.168.10.101 |     22 | banner: SSH-2.0-OpenSSH_9.6                 |
