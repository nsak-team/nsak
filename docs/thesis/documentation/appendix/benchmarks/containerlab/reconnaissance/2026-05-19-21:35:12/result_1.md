# Benchmark Result 1 from Run ca0de1f7-df71-45b5-a973-11c07df82847

| Key            | Value                                |
|:---------------|:-------------------------------------|
| Benchmark UUID | ca0de1f7-df71-45b5-a973-11c07df82847 |
| Run index      | 1                                    |
| Run UUID       | 83cc9608-9cb7-4f93-ba00-2217a521f4b7 |
| Scenario       | Reconnaissance                       |
| Setup          | containerlab                         |
| Timestamp      | 2026-05-19T21:35:41.400712+02:00     |
| Duration (s)   | 29                                   |

--------------------------------------

# Test Scenario Result

## Network Discovery Result Map

| Interface   | MAC               | IP             |   Port | Protocol   | State   | Service     | Product   | Version                             |
|:------------|:------------------|:---------------|-------:|:-----------|:--------|:------------|:----------|:------------------------------------|
| eth1        | aa:c1:ab:28:18:71 | 192.168.10.1   |        |            |         |             |           |                                     |
| eth1        | aa:c1:ab:4e:ca:69 | 192.168.10.5   |        |            |         |             |           |                                     |
| eth1        | aa:c1:ab:d7:09:5f | 192.168.10.50  |        |            |         |             |           |                                     |
| eth1        | aa:c1:ab:b3:d4:f9 | 192.168.10.100 |        |            |         |             |           |                                     |
| eth1        | aa:c1:ab:35:62:32 | 192.168.10.101 |        |            |         |             |           |                                     |
| eth1        | aa:c1:ab:4e:ca:69 | 192.168.10.5   |     22 | tcp        | open    | ssh         |           | OpenSSH 9.6 (protocol 2.0)          |
| eth1        | aa:c1:ab:4e:ca:69 | 192.168.10.5   |    139 | tcp        | open    | netbios-ssn |           | Samba smbd 4                        |
| eth1        | aa:c1:ab:4e:ca:69 | 192.168.10.5   |    389 | tcp        | open    | ldap        |           | OpenLDAP 2.2.X - 2.3.X              |
| eth1        | aa:c1:ab:4e:ca:69 | 192.168.10.5   |    445 | tcp        | open    | netbios-ssn |           | Samba smbd 4                        |
| eth1        | aa:c1:ab:d7:09:5f | 192.168.10.50  |     80 | tcp        | open    | http        |           | BaseHTTPServer 0.6 (Python 3.11.14) |
| eth1        | aa:c1:ab:d7:09:5f | 192.168.10.50  |    631 | tcp        | open    | http        |           | BaseHTTPServer 0.6 (Python 3.11.14) |
| eth1        | aa:c1:ab:b3:d4:f9 | 192.168.10.100 |     22 | tcp        | open    | ssh         |           | OpenSSH 9.6 (protocol 2.0)          |
| eth1        | aa:c1:ab:35:62:32 | 192.168.10.101 |     22 | tcp        | open    | ssh         |           | OpenSSH 9.6 (protocol 2.0)          |

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
|                |        | Date: Tue, 19 May 2026 19:35:39 GMT         |
|                |        | Content-Type: text/html                     |
|                |        | Server: HP-WebServer/2.6.5                  |
|                |        | (Request type: GET)                         |
|                |        | http-title: HP LaserJet 8101                |
| 192.168.10.50  |    631 | http-headers:                               |
|                |        | Server: BaseHTTP/0.6 Python/3.11.14         |
|                |        | Date: Tue, 19 May 2026 19:35:40 GMT         |
|                |        | (Request type: GET)                         |
|                |        | http-title: Site doesn't have a title.      |
| 192.168.10.100 |     22 | banner: SSH-2.0-OpenSSH_9.6                 |
| 192.168.10.101 |     22 | banner: SSH-2.0-OpenSSH_9.6                 |
