# Enable Ollama debug logs

During the development of the AI intrusion detection scenario, Ollama suddenly sent an empty response terminating the agent.
For investigation, I enabled the debug logs on the AI server.

```bash
sudo systemctl edit --full ollama.service

# Add the following line
Environment="OLLAMA_DEBUG=2"

# Restart the service
sudo systemctl restart ollama.service

# The logs can now be listed with:
journalctl -f -b -u ollama
```

## Container logs of the empty Ollama response:

-> The last log indicates a container restart (scenario was terminated by empty response)

```bash
❯ sudo podman logs -f simple_tcp_client_server_ai_intrusion_detection_1
WARNING:nsak.core.scenario.scenario_manager:EXEC SCENARIO: AI Intrusion Detection
INFO:root:Starting scenario: AI Intrusion Detection
WARNING:nsak.core.drill.drill_manager:EXEC DRILL: Discover Hosts
DEBUG:httpcore.connection:connect_tcp.started host='ai.hiube.ch' port=43434 local_address=None timeout=None socket_options=None
DEBUG:httpcore.connection:connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x7f6434e86f90>
DEBUG:httpcore.connection:start_tls.started ssl_context=<ssl.SSLContext object at 0x7f6434eff4d0> server_hostname='ai.hiube.ch' timeout=None
DEBUG:httpcore.connection:start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x7f6434eab110>
DEBUG:httpcore.http11:send_request_headers.started request=<Request [b'POST']>
DEBUG:httpcore.http11:send_request_headers.complete
DEBUG:httpcore.http11:send_request_body.started request=<Request [b'POST']>
DEBUG:httpcore.http11:send_request_body.complete
DEBUG:httpcore.http11:receive_response_headers.started request=<Request [b'POST']>
DEBUG:httpcore.http11:receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Server', b'nginx'), (b'Date', b'Mon, 06 Apr 2026 07:22:02 GMT'), (b'Content-Type', b'application/x-ndjson'), (b'Connection', b'close')])
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
| eth1        | ea:35:69:e3:1d:1a | 10.10.100.10 |        |            |         |           |           |           |
| eth1        | 72:31:39:c6:67:e6 | 10.10.100.20 |        |            |         |           |           |           |
| eth1        | f2:f7:61:1a:62:f5 | 10.10.100.30 |        |            |         |           |           |           |
| eth1        | f2:f7:61:1a:62:f5 | 10.10.100.20 |        |            |         |           |           |           |
| eth1        | f2:f7:61:1a:62:f5 | 10.10.100.10 |        |            |         |           |           |           |

Captured packets (CSV):
frame.number,eth.src,eth.dst,ip.src,ip.dst,tcp.dstport,udp.dstport,frame.protocols,frame.len
1,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
2,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
3,42:0a:f1:34:e7:5b,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
4,72:31:39:c6:67:e6,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
5,f2:f7:61:1a:62:f5,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
6,ea:35:69:e3:1d:1a,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
7,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
8,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
9,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
10,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
11,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
12,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
13,42:0a:f1:34:e7:5b,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
14,72:31:39:c6:67:e6,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
15,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
16,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
17,f2:f7:61:1a:62:f5,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
18,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
19,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
20,ea:35:69:e3:1d:1a,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
21,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
22,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
23,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
24,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
25,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
26,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
27,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
28,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
29,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
30,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
31,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
32,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
33,72:31:39:c6:67:e6,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
34,42:0a:f1:34:e7:5b,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
35,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
36,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
37,f2:f7:61:1a:62:f5,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
38,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
39,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
40,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
41,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
42,ea:35:69:e3:1d:1a,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
43,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
44,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
45,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
46,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
47,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
48,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
49,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
50,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
51,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
52,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
53,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
54,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
55,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
56,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
57,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
58,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
59,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
60,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
61,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
62,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
63,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
64,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
65,72:31:39:c6:67:e6,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
66,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
67,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
68,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
69,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
70,42:0a:f1:34:e7:5b,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
71,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
72,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
73,f2:f7:61:1a:62:f5,33:33:00:00:00:02,,,,,eth:ethertype:ipv6:icmpv6,70
74,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
75,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42
76,f2:f7:61:1a:62:f5,42:0a:f1:34:e7:5b,,,,,eth:ethertype:arp,42

Identify at most 5 suspicious events. For each, output:
- src/dst IP and MAC
- protocol
- reason it is suspicious

Be concise. Do not repeat packet data.


WARNING:root:[AI]


WARNING:nsak.core.scenario.scenario_manager:EXEC SCENARIO: AI Intrusion Detection
```
