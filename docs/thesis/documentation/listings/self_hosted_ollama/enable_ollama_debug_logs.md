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
# Truncated
WARNING:root:[Human]

You are analyzing network traffic for intrusion detection on interface eth1.

Network Discovery Result Map:
| Interface   | MAC               | IP           | Port   | Protocol   | State   | Service   | Product   | Version   |
|-------------|-------------------|--------------|--------|------------|---------|-----------|-----------|-----------|
| eth1        | ea:35:69:e3:1d:1a | 10.10.100.10 |        |            |         |           |           |           |
# Truncated

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
