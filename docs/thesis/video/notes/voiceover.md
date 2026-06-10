# NSAK Video — Voiceover Script

**Total target:** ~83s content (excl. BFH intro/outro)
**Speaking pace:** ~120 wpm — measured, clear delivery

---

## The Challenge

Red and blue team security exercises are essential — but they demand technical expertise
and recurring effort, putting them out of reach. Meanwhile, adversaries are accelerated by AI.

---

## Hypothesis & Research Questions

We hypothesized that integrating an AI agent would make security scenario execution
more adaptive and flexible, while lowering the barrier for operators.
We evaluated this with three concrete research questions.

---

## Our Approach

Building on NSAK — our existing modular network security framework — we integrated
an AI agent with tool-calling capabilities, and benchmarked it against
a hand-crafted scenario across three language models and two network environments.

---

## What We Built

The thesis produced four key deliverables: an AI-driven reconnaissance scenario,
a static reference scenario, a reproducible Containerlab test environment,
and a benchmark suite for automated metric collection.

---

## Evaluation Highlights

In our virtual environment, all three models completed the reconnaissance
task autonomously — with multi-agent decomposition significantly improving the smaller
models. In the physical BFH network security lab, the frontier model navigated a live
network with over 35 hosts.

---

## Demo: Interactive AI Agent

Let's see the agent in action.
The operator types a prompt, the AI executes tools, and pauses for approval at each step.

---

## Prompt - Vulnerable Services

The operator starts with a simple prompt:
"Help me to find all vulnerable services"

The agent uses nmap the command line tool, summarizes the findings and suggests next steps.

---

## [Clip 1]

[Video placeholder — ~10s clip showing the agent scanning for vulnerable services on eth1]

---

## Prompt - Further investigation

The operator follows up on the suggestion and instructs the agent to investigate SMB and LDAP.

The agent lists several critical findings with recommendations for resolution.

---

## [Clip 2]

[Video placeholder — ~10s clip showing the agent analyzing the contents of leaked documents]

---

## Prompt - Summary & Email Report

The operator has gathered thinks he has enough information for now and asks for an email report.

The agent creates the Markdown report and sends it via email by calling another tool.

---

## [Clip 3]

[Video placeholder — ~10s clip showing the email report being generated and sent]

---

## Key Findings

While the test in the BFH network security lab showed the limits of most models,
the AI agent is able to deliver valuable reports and suggestions which was not possible with a static scenario.
Together they show that AI and scripted automation are complementary: AI excels at exploration and reporting; scripted scenarios excel
at reliability and speed.
