# Bachelor Thesis Defense — Challenging Q&A

> **Thesis:** Integrating Agentic AI into NSAK for Automated Network Reconnaissance
> **Authors:** Lukas von Allmen & Frank Gaus
> **Date:** June 2026

---

## 1. Research Questions & Scope

**Q: Your RQ1 asks how the AI scenario "performs compared to" the static scenario, but the static scenario is always faster (29 s vs. 122–963 s) and discovers more services (13 vs. 9). Doesn't that mean the static scenario wins?**

A: The comparison is a trade-off across multiple dimensions, not a single metric. On raw speed and exhaustive port coverage the static scenario is unbeatable — it is deterministic and issues unconditional sweeps. But those 13 service rows reflect a representational difference, not better coverage: the static scenario lists every host separately plus its services, while the AI consolidates hosts directly into service rows. Both discover the same 8 open services. More importantly, the static scenario cannot extract the LDAP cleartext credentials, does not elaborate the printer banner mismatch, and produces no severity-rated assessment or remediation plan. The AI adds an interpretive layer that the scripted approach structurally cannot provide. So the answer to RQ1 is: the AI matches the static scenario on discovery breadth but exceeds it on depth and operator support, at the cost of higher latency and non-determinism.

---

**Q: RQ3 asks whether the implementation is "suitable for real-world deployment." Your own results show 5/27 success rate for the multi-agent setup in the BFH lab. How can you claim suitability?**

A: The 5/27 figure reflects completions with a *fully structured output*, which is a strict criterion. All five successful runs delivered meaningful results covering the six high-severity structural risks. The failures are of two kinds: the multi-agent failures are task failures (too-restrictive scans returned empty port lists), and the unstructured failures are almost entirely infrastructure failures (103 of 109 runs hit the Anthropic monthly API quota instantly). When the model *actually ran*, it succeeded. Our conclusion is carefully qualified: the implementation is suitable for *supervised, observed* use — not unsupervised autonomous operation. A retry strategy and human checkpoint (outlined in the recommendations) would bring reliability to a practically acceptable level.

---

## 2. Methodology & Evaluation Design

**Q: You only ran 10 successful runs per model/environment. Is that statistically sufficient?**

A: Ten runs is a practical compromise driven by token costs and API rate limits, especially for the frontier model. We acknowledge this limitation explicitly. The goal was not statistical significance in the academic sense but rather trend detection — identifying which models are qualitatively in a different class and how decomposition changes behavior. The results are consistent with the theory: claude-opus shows low variance across runs (tight scatter cluster), while qwen3 and gpt-oss show higher variance. For a production-grade study, a larger n and cross-evaluation by a second rater would be required. We note this as a limitation under "Subjectivity of qualitative scoring."

---

**Q: Why did you only evaluate reconnaissance? The thesis also mentions an AI intrusion detection scenario but it wasn't fully evaluated.**

A: The intrusion detection scenario was classified as a "Should" goal rather than a "Must" goal in the user story map workshop early in the project. After completing the reconnaissance scenario and the benchmarking suite, implementing and evaluating a fully equivalent intrusion detection setup would have exceeded the time budget. What we implemented is a proof-of-concept that demonstrates the technical feasibility (packet capture → CSV → LLM analysis), but it was not included in the formal evaluation. This is documented as a gap under "Incomplete environment and scenario matrix" in the discussion, and it is listed as a clear future work direction.

---

**Q: You set temperature=0 for all models to maximize determinism, but you still observe high variance (e.g., qwen3 success factor 10/23 in single-agent mode). What causes the variance if temperature is zero?**

A: Temperature=0 makes the model's token sampling deterministic given a fixed context, but each run is not given a fixed context. The nmap output, timestamps, and tool responses all differ per run, and the model's reasoning path diverges based on the intermediate results it observes. Additionally, some failures are non-deterministic at the infrastructure level: API timeouts, temporary disconnects, and container startup timing. So temperature=0 reduces model-side variance but does not eliminate run-to-run variance coming from the environment and tool interaction.

---

**Q: You used qualitative scoring (correctness and hallucination) evaluated by yourselves. Isn't that biased?**

A: Yes, there is inherent bias risk when authors score their own system. We tried to mitigate it by defining an explicit 10-point rubric with clear per-band descriptions and by anchoring scores to verifiable scan artifacts — a model's claim was only counted as non-hallucination if it appeared in the raw nmap output. We also acknowledge this as a limitation ("Subjectivity of qualitative scoring") and recommend independent inter-rater evaluation as future work. The approach is common in applied systems papers where a ground truth exists (our deliberately planted vulnerabilities) and is used as the reference.

---

## 3. Technical Design Decisions

**Q: Why LangChain? You say you chose it without comparing alternatives. That seems like a weak engineering decision.**

A: We chose LangChain for pragmatic reasons: it is the most widely adopted Python agentic framework, has native async support, provides a provider-agnostic `BaseChatModel` abstraction (so we could switch between Anthropic, Ollama, and BFH's OpenAI-compatible endpoint by changing one config value), and its documentation is extensive. Not evaluating alternatives formally is a limitation. However, for a bachelor thesis with time constraints, and given that our goal was not to compare agentic frameworks but to evaluate AI reconnaissance, this was an acceptable trade-off. We were aware of alternatives like CrewAI and AutoGen but these would not have changed the core findings about model capability.

---

**Q: You gave the agent unrestricted CLI access via `cli_tool`. Isn't this a severe security risk? What prevents the agent from running `rm -rf /` or attacking a network it shouldn't?**

A: You are right that this is a deliberate design choice with inherent risk, and we discuss it explicitly in the kill-switch section. The mitigations we implemented are: (1) a kill-switch CLI command (`nsak killswitch`) that sends SIGTERM to all running containers; (2) the agent always runs inside an OCI container, so file system damage is contained; (3) the system prompt establishes scope constraints (the agent is instructed to perform reconnaissance only on the specified interface). In production, this would need to be extended with explicit guardrails and scope restriction, which we identify as future work. We acknowledge that the current implementation is suitable for supervised lab use, not production deployment.

---

**Q: Why did you use structured output for the benchmark? You found it causes failures in larger networks. Wouldn't it have been better to use unstructured output from the start?**

A: Structured output was chosen because it enables automated quantitative metrics — without it, you cannot programmatically extract host counts, service counts, or findings counts for plotting. It also enables fair comparison across runs and models. We discovered only during BFH lab evaluation that it becomes a failure mode in larger environments, likely because the grammar constraint for the output schema fills additional context. The unstructured variant was an ad-hoc fix to confirm the cause. In hindsight, a hybrid approach — structured output only for the final results block, free-form for intermediate reasoning — would have been better. This is a lesson learned that feeds into the RAG pipeline recommendation.

---

**Q: The multi-agent approach reduced qwen3:30b's tokens by 68% but barely helped claude-opus. Why?**

A: Context management scales differently with model size. Larger models are generally better at ignoring irrelevant context and maintaining focus over long token sequences. For claude-opus-4-7, the single accumulated context is manageable, and decomposition mainly adds orchestration overhead (+13% tokens). For qwen3:30b, a single-agent run accumulates 86k tokens of tool call history, and the model's attention degrades as the context fills — it starts repeating steps, skipping enumeration, or producing schema-invalid output. Splitting the task into sub-agents with focused, short contexts restores its effectiveness. This is the central architectural finding: decomposition is a technique to bring smaller/self-hosted models into a usable range.

---

**Q: Your MCP integration is described as a "graceful fallback" — it's optional. But the thesis claims NSAK uses MCP for the draw.io integration. If MCP is optional and you say in the related work that "MCP is dead," why did you still use it?**

A: The "MCP is dead" claim from the Risky Business podcast is specifically about the excessive use of MCP that pushes agents toward using a root shell instead. Our use case is the opposite: we deliberately restrict the agent to a *minimum* tool set and use MCP only for one optional capability (draw.io diagrams). We chose MCP for draw.io because it was the only interface available for that tool — we didn't design the MCP server ourselves. The implementation correctly makes it optional with graceful fallback, so the core scenarios work without it. The broader point we drew from the podcast discussion was to focus on Tool Calling as a general concept rather than treating MCP as the canonical approach.

---

## 4. Results & Findings

**Q: Claude-opus classified the printer as a honeypot, which you counted as a hallucination. But couldn't that actually be a reasonable inference given the banner mismatch (BaseHTTPServer behind an HP LaserJet facade)?**

A: It is a reasonable inference, and interestingly it is simultaneously a sign of the model's analytical sophistication and its weakness. The model correctly identified the banner mismatch between `BaseHTTPServer/0.6` and `HP-WebServer/2.6.5` — that is a real anomaly worth flagging. However, classifying it as a "honeypot" goes beyond what the data supports: a honeypot is a deliberate deception deployment, and there is no network-observable evidence for that conclusion. It could equally be a misconfigured service or an old device with a custom Python wrapper. We counted it as a hallucination because the conclusion is not directly verifiable from scan output. It does show that the model reasons about attack context, which is genuinely valuable — but that reasoning must be reviewed by the operator.

---

**Q: The static scenario's 13 services vs. the AI's 9 services — you say this is a representation difference. How can you be sure the AI isn't actually missing services?**

A: We traced the discrepancy explicitly: the static scenario lists each discovered host as a separate row and then lists its services underneath, which inflates the count. The AI consolidates hosts with open ports directly into their service rows and only keeps a standalone gateway entry (which has no open ports). When we count distinct open-port/service combinations, both discover the same 8 services. The gateway appears once in the static output as a row on its own, and the AI folds it in as a gateway note. We verified this against the ground truth defined in the Containerlab topology.

---

**Q: gpt-oss:120b fabricated CVE identifiers in some runs. Did you report this to BFH, and what are the implications for using that model in a real security context?**

A: We documented this as a hallucination finding in the evaluation. Since gpt-oss:120b is hosted on BFH's ML platform, it is an internal deployment and the findings were communicated in the thesis and available to the institution. The implication for real security use is significant: a fabricated CVE in a security report is dangerous because a blue team may waste resources chasing a vulnerability that doesn't exist, or — worse — a client may be alarmed by a non-existent critical finding. This reinforces the supervised-operation recommendation: any AI-generated security report should be reviewed against a verifiable source (NVD, actual scan artifacts) before being acted upon. This is also the motivation for the RAG pipeline recommendation in the conclusion.

---

## 5. Framework & Architecture

**Q: NSAK doesn't map to MITRE ATT&CK. All competing frameworks (Caldera, Atomic Red Team) do. Isn't this a significant gap?**

A: It is a deliberate architectural decision, not an oversight. MITRE ATT&CK alignment is valuable for enterprise-grade threat emulation where findings must be mapped to known adversary TTPs for compliance or detection engineering. NSAK's focus is different: it is a harness for *network-focused* red and blue team scenarios, including physical lab deployments on embedded hardware. The ATT&CK mapping can be added as a drill or scenario output attribute, and we suggest this as a direction for the framework. The reconnaissance scenario we implemented aligns with MITRE ATT&CK TA0043 (Reconnaissance) and T1046 (Network Service Scanning) even without formal annotation. The modular design allows integrating ATT&CK-mapped tools (Atomic Red Team, Caldera) as drills via their APIs, which would bring ATT&CK coverage without rebuilding NSAK.

---

**Q: You used a lazy object proxy for config loading to avoid import-time side effects. Why does this matter for shell tab completion?**

A: Shell completion is invoked on every keystroke, and the Click framework imports the CLI module for every completion request. If the config was loaded eagerly at import time, each tab press would trigger a file system read (checking `run/config.yaml`) — this would cause visible latency and fail in environments where the run directory doesn't exist yet. The `lazy_object_proxy.Proxy` defers the `Config.load()` call to the first attribute access, which only happens when an actual command runs, not when completing. This is a detail, but it is the kind of UX decision that matters when NSAK is used interactively.

---

**Q: You implemented the Device resource type fresh in this thesis. The predecessor project had it only as a concept. How much of the thesis budget did this take, and was it worth it?**

A: The Device implementation was necessary foundation work for the AI scenarios to work: the `host_configuration` tool that bootstraps the agent's situational awareness reads directly from the Device YAML, giving the agent interface names, IP addresses, and `is_target`/`is_management` flags without requiring it to parse raw `ip addr` output. Without it, the AI scenario prompt would need to either rely on the agent self-discovering the network configuration (unreliable) or hardcode it (defeating reusability). We also used the Device implementation to refactor the existing resource classes to use shared base classes, which reduced boilerplate across the entire codebase. The effort was justified by both the foundational dependency and the code quality improvement.

---

## 6. Ethics & Safety

**Q: You effectively built a tool that autonomously conducts network attacks. What ethical and legal safeguards did you consider?**

A: Several layers were considered. First, all evaluation was conducted in a controlled environment: a self-contained Containerlab topology (no external connectivity) and the BFH network security lab (with explicit permission from BFH). The NSAK framework itself includes a CLI kill switch and always runs scenarios inside containers. Second, the thesis explicitly positions the tool for authorized red/blue team exercises and explicitly warns in the discussion that it is "not yet suitable for unsupervised autonomous operation." Third, the scope restriction in the system prompt instructs the agent to only act on the specified interface. The tool lowers the expertise barrier — which is a stated goal — but also lowers the barrier for misuse, which is why we recommend guardrails and sandbox enforcement as the next development step before any production use.

---

**Q: Your abstract says the tool makes "cybersecurity use cases more accessible and cost-effective." Does lowering the barrier to entry for red team tools create more risk than it reduces?**

A: This is a genuine dual-use dilemma and one we take seriously. Our position is that the defenders and the attackers face the same asymmetry today: adversaries already have access to LLM-assisted tools and are using them (as documented by the CrowdStrike 2025 report cited in the introduction). Defenders without comparable tooling are at a disadvantage. NSAK targets the *legitimate blue and red team* use case: authorized security exercises at organizations that currently can't afford the expertise to run them. The risk of misuse exists for any security tool — nmap, Metasploit, and Caldera all carry the same dual-use risk. Responsible disclosure, access controls, and supervised deployment are the standard mitigations, and we apply the same framing.

---

## 7. Future Work & Limitations

**Q: You recommend a RAG pipeline as the next step. How specifically would that work with NSAK?**

A: The concrete proposal in the conclusion is: (1) run the deterministic reconnaissance scenario first, producing a structured `ReconnaissanceScenarioResult`; (2) pass that result, along with RAG-retrieved documents (CVE feeds, NSE script documentation, vendor advisories), into the AI agent as grounding context; (3) the agent then writes an assessment that it is forced to anchor in those sources rather than its parametric memory. This would address the hallucinated CVE problem directly — the agent can only cite CVEs that appear in the retrieval context. Implementation would require a vector store seeded with CVE feeds (e.g., NVD JSON) and NSE documentation, and a retrieval step triggered by each discovered service name and version.

---

**Q: Branch 310 (human-in-the-loop) was developed but not merged. What specifically went wrong?**

A: The LangChain human-in-the-loop middleware works by interrupting the agent graph at tool call nodes and requesting approval. The problem we encountered is that the agent, once it saw the approval mechanism was available, started using it for *every* tool call — including simple ones like `host_configuration` that require no human judgment. The result was more interactive overhead than the custom `human_interaction_hook` tool it was meant to replace, without a qualitative improvement. We deprioritized it because the evaluation focuses on non-interactive mode, and the custom hook already works correctly for the interactive flag. The branch is preserved and recommended for the next iteration together with a smarter approval policy that only intercepts high-risk tool calls (e.g., `cli_tool` invocations with destructive flags).

---

## 8. Quick-Fire Technical Questions

**Q: What is the difference between a Drill and a Scenario in NSAK?**

A: A Drill is the smallest reusable unit — one specific action with a typed interface (e.g., `discover_hosts`, `port_scan`). A Scenario orchestrates a sequence of drills for a complete red or blue team operation and also declares its target environment. Drills return typed results that feed into the next drill; scenarios expose a typed CLI interface to the operator without the operator needing to know the internal drill chain.

---

**Q: Why Containerlab over Docker Compose for the test environment?**

A: Docker (and Compose) abstracts away most of the network stack and typically gives containers a single interface. Containerlab builds on Docker but is specifically designed for network simulation: it supports multiple interfaces per node, creates virtual Ethernet links between nodes, and allows you to declare a complete network topology in a single YAML file. For our test environment (firewall, DMZ, LAN segment, multiple hosts with specific IPs and roles), Containerlab was the appropriate tool.

---

**Q: What is structured output and why does it fail in large environments?**

A: Structured output constrains the LLM to produce a response that conforms to a predefined JSON schema, enforced via grammar-based sampling (restricting valid tokens at each generation step). In large environments the nmap output itself is much longer, and the schema grammar adds additional tokens to the context. Our hypothesis is that smaller models degrade when the context exceeds their effective attention range, causing them to produce invalid JSON or time out. Claude-opus-4-7, with larger effective context handling, is less affected.

---

**Q: Why did qwen3:8b fail completely in the BFH lab with zero CLI calls?**

A: Qwen3:8b is a very small model (8 billion parameters). In the BFH lab environment the nmap scan of ~35 hosts produces a large context, and the model appears to lose track of the task goal. In all 6 runs it either returned a generic connectivity recommendation or produced a report without executing any tools. This is consistent with what we saw for qwen3:30b in single-agent mode (10/23 success) — the 8b model simply hits this threshold at an earlier scale. The lesson is that autonomous tool-calling reconnaissance requires a model of at least 30b parameters to be usable, and even then a frontier model is needed for critical findings.
