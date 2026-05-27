# Bachelor Thesis Improvement Report

> Analyzed: 2026-05-27
> Thesis: "Nsak as Framework for Scenario Based Network Security"
> Authors: Frank Gauss (gausf1) & Lukas von Allmen (vonal3)

---

## Priority 1 — Critical: Missing Chapters

### 1.1 Write Chapter 4: Methodology (EMPTY)
**File**: `content/04-methodology.tex` — currently 3 lines, chapter heading only.

A research thesis requires a methodology chapter. It should cover:
- Research design: what questions were investigated and how
- Evaluation approach: how AI agent performance was measured (speed, token usage, completeness, hallucination rate)
- Data collection: how benchmark runs were structured (single-agent vs. multi-agent, containerlab vs. BFH Cyber Lab)
- Reproducibility: how the test environment ensures consistent results
- Metrics definition: define formally what "correctness", "hallucination", "completeness" mean before they appear in Chapter 6

Without this chapter the evaluation results in Chapter 6 lack methodological grounding.

---

### 1.2 Write Chapter 7: Discussion (EMPTY)
**File**: `content/07-discussion.tex` — currently 3 lines, chapter heading only.

This is arguably the most important analytical chapter. Must include:
- Interpretation of benchmark results: what do the numbers mean for the hypothesis?
- Answer the research question: does AI enhance red/blue team simulations?
- Compare models: Opus 4.7 vs. qwen3:30b vs. gpt-oss:120b — trade-offs, insights
- Limitations: context window issues (already noted as TODO in 5.3), token costs, hallucination rates
- Threats to validity: is the containerlab environment representative of real networks?
- Why MCP context window issues matter for agentic security tools

---

### 1.3 Complete Chapter 8: Conclusion (NEARLY EMPTY)
**File**: `content/08-conclusion.tex` — 5 lines, only "Future Work" section header exists.

Must include:
- Summary of contributions (framework improvements + AI integration)
- Answer to the central hypothesis
- Key findings in 3–5 bullet points
- Recommendations for practitioners
- Expand "Future Work" section (web GUI, REST API, more scenarios, better MCP tooling)

---

## Priority 2 — High: Incomplete Evaluation

### 2.1 Complete Section 6.2: BFH Cyber Lab Evaluation
**File**: `content/06-evaluation.tex` (BFH section)

Current state: overview data table exists, but narrative analysis and qualitative evaluation table are not filled in.
- Fill in the qualitative criteria table (correctness, hallucination, tool use quality per model)
- Write narrative analysis comparing BFH Cyber Lab results to containerlab results
- BFH agents write findings to separate text files and generate recommendations — this interesting behavior needs commentary
- The BFH environment is a real network, making these results more significant than containerlab — emphasize this

---

### 2.2 Abstract: Add Conclusion Sentence
**File**: `content/00-abstract.tex` — marked with TODO at end.

The abstract currently summarizes approach and models tested but lacks a conclusion sentence. Add 1–2 sentences: what the results showed, whether the hypothesis was confirmed/partially confirmed.

---

## Priority 3 — Medium: Content Quality and Coherence

### 3.1 Introduction: Sharpen Research Question and Fix Structure Overview
**File**: `content/01-introduction.tex`

- TODO 1: "Sharpen research question and contribution" — the thesis needs a clear, explicit RQ (e.g., "To what extent can LLM-based agents replace manually scripted red/blue team scenarios?"). Currently the hypothesis is implied but not stated as a formal research question.
- TODO 2: "Match the structure overview to the actual structure" — the chapter outline at the end of the introduction must reflect the actual chapter sequence (Chapter 4 Methodology is likely missing from the overview).

---

### 3.2 Section 5.1 Redundancy with Chapter 3
**File**: `content/05-1-configuration-management.tex`

A TODO notes: "This section is repeating what's already stated in the concepts chapter." Options:
- Remove duplicate conceptual explanations from 5.1, keeping only the implementation details
- Or shorten 5.1 to implementation-only content and add forward references from Chapter 3

---

### 3.3 Add Missing Code Snippet in Section 5.4
**File**: `content/05-4-reconnaissance-scenario.tex` — TODO: "Add Snippet"

The output artifacts section (NetworkDiscoveryResultMap) is missing a code example. Add the data structure definition or a sample output to make the section concrete.

---

### 3.4 Related Research: Clarify MCP Section Relevance and "MCP is dead" Content
**File**: `content/02-related-research.tex`

- Several TODOs question whether sections are relevant to the thesis
- The "MCP is dead" discussion from the Risky Business podcast needs framing: does it affect the thesis's use of MCP, or is it tangential?
- The AI evolution (SLM → NLM → PLM → LLM) section may be too broad — consider condensing

---

## Priority 4 — Medium: Tense and Writing Quality

### 4.1 Risk Assessment: Rewrite in Past Tense
**File**: `appendix/risk-assessment.tex` — line 2 TODO.

The risk assessment was conducted during the project and should be written in past tense throughout.

---

### 4.2 Self-Hosted LLM: Refactor into Subsections
**File**: `appendix/selfhosted-llm.tex` — line 10 TODO.

Currently a flat structure. The content covers hardware, Ollama, SWAG proxy, OpenWebUI, DynDNS, firewall, and additional services — each deserves its own subsection heading.

---

### 4.3 Proof-Read Section 1.1 (Motivation)
**File**: `content/01-1-motivation.tex` — TODO: "Proof Reading"

Flagged for general proof-reading. Verify grammar, tense consistency, and that NSAK concepts are explained clearly for readers unfamiliar with the predecessor project.

---

## Priority 5 — Low: Polish and Completeness

### 5.1 Complete Meeting Notes 7–9
**File**: `appendix/meetings/` — meetings 7–9 are 1 line each (empty).

Fill in with actual meeting content or remove references to them.

### 5.2 Variant Decision: Clarify LangChain vs MCP Tool Abstraction
**File**: `appendix/variant-decision-ai-integration.tex` — lines 60, 63.

The text may still mention MCP for tool calling, but the project uses LangChain Tools. Correct to avoid misleading the reader about the architectural choice.

### 5.3 Add Checkpoint 1 Slides to Meeting Notes
**File**: `appendix/meetings/meeting-1.tex` — TODO: "Add slides if we can reproduce them"

Add slides from Checkpoint 1 if they can be reconstructed or exported.

---

## Summary Table

| # | Area | File(s) | Priority | Effort |
|---|------|---------|----------|--------|
| 1.1 | Write Methodology chapter | `content/04-methodology.tex` | CRITICAL | High |
| 1.2 | Write Discussion chapter | `content/07-discussion.tex` | CRITICAL | High |
| 1.3 | Complete Conclusion chapter | `content/08-conclusion.tex` | CRITICAL | Medium |
| 2.1 | Complete BFH Cyber Lab evaluation | `content/06-evaluation.tex` | High | Medium |
| 2.2 | Abstract conclusion sentence | `content/00-abstract.tex` | High | Low |
| 3.1 | Sharpen RQ + fix structure overview | `content/01-introduction.tex` | Medium | Low |
| 3.2 | Remove 5.1 redundancy with Ch. 3 | `content/05-1-*.tex` | Medium | Low |
| 3.3 | Add missing code snippet in 5.4 | `content/05-4-*.tex` | Medium | Low |
| 3.4 | Clarify MCP section relevance | `content/02-related-research.tex` | Medium | Low |
| 4.1 | Rewrite risk assessment in past tense | `appendix/risk-assessment.tex` | Medium | Low |
| 4.2 | Refactor selfhosted-llm into subsections | `appendix/selfhosted-llm.tex` | Low | Low |
| 4.3 | Proof-read motivation section | `content/01-1-motivation.tex` | Low | Low |
| 5.1 | Complete meeting notes 7–9 | `appendix/meetings/` | Low | Low |
| 5.2 | Fix LangChain vs MCP description | `appendix/variant-decision-ai-integration.tex` | Low | Low |
| 5.3 | Add Checkpoint 1 slides | `appendix/meetings/meeting-1.tex` | Low | Low |
