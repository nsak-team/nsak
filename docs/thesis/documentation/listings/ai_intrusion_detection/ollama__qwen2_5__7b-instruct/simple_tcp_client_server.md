# Run in the simple tcp client server environment

## Command

```bash
❯ uv run nsak environment simulate simple_tcp_client_server ai_intrusion_detection
```

```bash
❯ sudo podman logs -f simple_tcp_client_server_ai_intrusion_detection_1
```

## Output

```bash
❯ sudo podman logs -f simple_tcp_client_server_ai_intrusion_detection_1
Please enter the PIN:
Please touch the device.
WARNING:nsak.core.scenario.scenario_manager:EXEC SCENARIO: AI Intrusion Detection
INFO:root:Starting scenario: AI Intrusion Detection
WARNING:nsak.core.drill.drill_manager:EXEC DRILL: Discover Hosts
DEBUG:httpcore.connection:connect_tcp.started host='ai.hiube.ch' port=43434 local_address=None timeout=None socket_options=None
DEBUG:httpcore.connection:connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x7f5bebb1af90>
DEBUG:httpcore.connection:start_tls.started ssl_context=<ssl.SSLContext object at 0x7f5bebb834d0> server_hostname='ai.hiube.ch' timeout=None
DEBUG:httpcore.connection:start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x7f5bebb37110>
DEBUG:httpcore.http11:send_request_headers.started request=<Request [b'POST']>
DEBUG:httpcore.http11:send_request_headers.complete
DEBUG:httpcore.http11:send_request_body.started request=<Request [b'POST']>
DEBUG:httpcore.http11:send_request_body.complete
DEBUG:httpcore.http11:receive_response_headers.started request=<Request [b'POST']>
DEBUG:httpcore.http11:receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Server', b'nginx'), (b'Date', b'Mon, 06 Apr 2026 07:57:23 GMT'), (b'Content-Type', b'application/x-ndjson'), (b'Connection', b'close')])
INFO:httpx:HTTP Request: POST https://ai.hiube.ch:43434/api/chat "HTTP/1.1 200 OK"
DEBUG:httpcore.http11:receive_response_body.started request=<Request [b'POST']>
DEBUG:httpcore.http11:receive_response_body.complete
DEBUG:httpcore.http11:response_closed.started
DEBUG:httpcore.http11:response_closed.complete
WARNING:root:[Human]

You are analyzing network traffic for intrusion detection on interface eth1.

Network Discovery Result Map:
| Interface   | MAC               | IP           | Port   | Protocol   | State   | Service   | Product   | Version   |
|-------------|-------------------|--------------|--------|------------|---------|-----------|-----------|-----------|
| eth1        | e2:c8:23:b4:e4:fa | 10.10.100.10 |        |            |         |           |           |           |
| eth1        | be:22:cf:7c:cb:59 | 10.10.100.20 |        |            |         |           |           |           |
| eth1        | c2:32:58:59:03:68 | 10.10.100.30 |        |            |         |           |           |           |
| eth1        | c2:32:58:59:03:68 | 10.10.100.20 |        |            |         |           |           |           |
| eth1        | c2:32:58:59:03:68 | 10.10.100.10 |        |            |         |           |           |           |

Captured packets (CSV):
frame.number,eth.src,eth.dst,ip.src,ip.dst,tcp.dstport,udp.dstport,frame.protocols,frame.len
1,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
2,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
3,be:22:cf:7c:cb:59,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
4,e2:c8:23:b4:e4:fa,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
5,fe:ca:7b:e6:af:1a,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
6,c2:32:58:59:03:68,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
7,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
8,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
9,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
10,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
11,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
12,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
13,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
14,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
15,e2:c8:23:b4:e4:fa,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
16,be:22:cf:7c:cb:59,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
17,c2:32:58:59:03:68,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
18,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
19,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
20,fe:ca:7b:e6:af:1a,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
21,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
22,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
23,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
24,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
25,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
26,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
27,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
28,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
29,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
30,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
31,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
32,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
33,e2:c8:23:b4:e4:fa,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
34,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
35,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
36,be:22:cf:7c:cb:59,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
37,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
38,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
39,c2:32:58:59:03:68,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
40,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
41,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
42,fe:ca:7b:e6:af:1a,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
43,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
44,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
45,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
46,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
47,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
48,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
49,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
50,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
51,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
52,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
53,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
54,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
55,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
56,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
57,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
58,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
59,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
60,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
61,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
62,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
63,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
64,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
65,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
66,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
67,e2:c8:23:b4:e4:fa,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
68,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
69,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
70,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
71,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
72,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
73,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42
74,c2:32:58:59:03:68,fe:ca:7b:e6:af:1a,,,,,eth:ethertype:arp,42

Identify at most 5 suspicious events if any. For each, output:
- src/dst IP and MAC
- protocol
- reason it is suspicious

Identify malicious hosts (MAC and/or IP) if any.

Be concise. Do not repeat packet data.


WARNING:root:[AI]
Based on the provided packet data, several suspicious events can be identified:

1. **Suspicious Event:**
   - **Src/Dst IP/MAC:** `c2:32:58:59:03:68` (Src) -> `fe:ca:7b:e6:af:1a` (Dst)
   - **Protocol:** ARP
   - **Reason:** The source MAC address `c2:32:58:59:03:68` is sending a large number of ARP requests to the destination MAC address `fe:ca:7b:e6:af:1a`. This could indicate a potential ARP spoofing attack or a network scanning activity.

2. **Suspicious Event:**
   - **Src/Dst IP/MAC:** `e2:c8:23:b4:e4:fa` (Src) -> `33:33:00:00:00:02`
   - **Protocol:** IPv6 ICMP
   - **Reason:** The source MAC address `e2:c8:23:b4:e4:fa` is sending a large number of ICMPv6 packets to the multicast address `33:33:00:00:00:02`. This could indicate an attempt to probe or scan the network for devices.

3. **Suspicious Event:**
   - **Src/Dst IP/MAC:** `c2:32:58:59:03:68` (Src) -> `fe:ca:7b:e6:af:1a` (Dst)
   - **Protocol:** ARP
   - **Reason:** Similar to the first event, this MAC address is sending a large number of ARP requests. This could be part of an ongoing attack or scanning activity.

4. **Suspicious Event:**
   - **Src/Dst IP/MAC:** `c2:32:58:59:03:68` (Src) -> `fe:ca:7b:e6:af:1a` (Dst)
   - **Protocol:** ARP
   - **Reason:** The source MAC address is sending a large number of ARP requests, which could be part of an ongoing attack or scanning activity.

5. **Suspicious Event:**
   - **Src/Dst IP/MAC:** `c2:32:58:59:03:68` (Src) -> `fe:ca:7b:e6:af:1a` (Dst)
   - **Protocol:** ARP
   - **Reason:** The source MAC address is sending a large number of ARP requests, which could be part of an ongoing attack or scanning activity.

**Malicious Hosts Identified:**
- **MAC Address:** `c2:32:58:59:03:68`
  - This MAC address is involved in multiple suspicious events and could be a potential attacker.

- **IP Address:** None explicitly identified, but the IP addresses associated with this MAC (if any) should be investigated further.

These findings suggest that there might be an ongoing ARP spoofing or network scanning activity originating from the MAC address `c2:32:58:59:03:68`. Further investigation is recommended to confirm these suspicions.
```
