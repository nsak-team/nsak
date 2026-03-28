# NSAK Scenario: Network Discovery - Red Team

GitLab: https://gitlab.ti.bfh.ch/groups/gausf1-vonal3/-/milestones/7
Start date: 02.04.2026
Due date: 16.04.2026

Network discovery is one of the most essential Red Team activities in the reconnaissance phase. Participants and services are identified and interesting targets can be evaluated. The resulting network map can then be used in later phases, for example an ARP spoofing attack can be executed to intercept traffic more efficiently.

Goals:
- [ ] The scenario correctly identifies the setup it can use for network discovery (ports and interfaces)
- [ ] The scenario is able to discover the available subnets
- [ ] The scenario can get valid IP addresses for the discovered subnets
- [ ] The scenario provides different modes on how the network discovery is done (selective, slow, fast)
- [ ] The scenario is able to identify clients, servers and services participating in the networks
- [ ] The scenario returns a map of the scanned networks

Tasks (Must):
- [ ] Physical Ports / Interfaces: List ports, list interfaces, filter interfaces
- [ ] Subnets: Scan subnets, filter subnets
- [ ] IP Address Assignment: DHCP (request dynamic IP), Static (assign static IP)
- [ ] Mode: Fast full search
- [ ] Devices: Discover MAC Addresses, discover IP Addresses
- [ ] Services: Port Scan
- [ ] Mapping: Network map as datastructure

Tasks (Could):
- [ ] Human Interface Hook: Select mode
- [ ] Mode: Slow full search, distinct search
