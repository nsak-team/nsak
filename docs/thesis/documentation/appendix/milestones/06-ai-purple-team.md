# NSAK Scenario: AI - Purple Team

GitLab: https://gitlab.ti.bfh.ch/groups/gausf1-vonal3/-/milestones/18
Start date: 19.03.2026
Due date: 16.04.2026

The usage of AI in network security is still subject of recent research. With the advent of agentic AI the question arises: what happens and what are the possibilities when we give an AI full access to the NSAK framework?

Goals:
- [ ] The operator can provide an initial prompt or use a predefined Red or Blue Team prompt
- [ ] The scenario runs an AI agent with a remote connection
- [ ] An operator can interact with the agent, ideally at all times
- [ ] The scenario logs all relevant actions and network traffic
- [ ] The AI is able to trigger an alert to notify an operator depending on the prompt
- [ ] The scenario has a kill switch, so that the operator can stop it at all times

Tasks (Must):
- [ ] Initial Prompt: Custom Prompt, Red Team Prompt, Blue Team Prompt
- [ ] Run: AI Agent with remote connection
- [ ] Human Interaction Hook: CLI
- [ ] Logging / Sniffing: Local
- [ ] Alerting: E-Mail
- [ ] Kill Switch: Stop Scenario

Tasks (Should):
- [ ] Human Interaction Hook: Web GUI
- [ ] Logging / Sniffing: Remote
- [ ] Kill Switch: Shutoff

Tasks (Could):
- [ ] Human Interaction Hook: Messenger, Chats
- [ ] Alerting: SMS, Phone, Pager, Messenger, Chats, Scheduling
- [ ] Logging / Sniffing: Dashboard
