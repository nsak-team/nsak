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
# Truncated

Identify at most 5 suspicious events. For each, output:
- src/dst IP and MAC
- protocol
- reason it is suspicious

Be concise. Do not repeat packet data.


WARNING:root:[AI]


WARNING:nsak.core.scenario.scenario_manager:EXEC SCENARIO: AI Intrusion Detection
```
