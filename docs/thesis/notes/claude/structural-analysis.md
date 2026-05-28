# Thesis Structural Analysis

> Analyzed: 2026-05-28
> Scope: content placement, chapter/appendix split, ordering, and hierarchy issues
> Empty chapters (Methodology, Discussion, Conclusion) excluded per request

---

## High Priority

### H1 — Remove "Former Abstract" from Introduction
**File**: `content/01-introduction.tex` (lines 30–52)

The introduction contains a block labelled "Former abstract" that is a draft holdover. It duplicates the actual `abstract.tex` and conflicts with the introduction's purpose. It should be deleted entirely — there is nothing to move or preserve.

---

### H2 — Operational Infrastructure Details in 05.3 Belong Elsewhere
**File**: `content/05.3-ai-scenarios.tex`

At 376 lines, section 5.3 mixes scenario design with operational infrastructure that has nothing to do with AI scenarios:
- **Grafana/Loki logging setup** — belongs in `05.2-test-environment.tex` or the appendix (selfhosted-llm.tex already documents the self-hosted services stack)
- **E-Mail alerting** — belongs in appendix or test environment
- **CLI Kill Switch** — belongs in appendix or a brief note in configuration management
- **LangChain Chat UI** — a tangential feature; move to appendix or future work

These items describe the evaluation infrastructure, not the AI scenario design. Pulling them out would also make 5.3 more focused and easier to read.

---

### H3 — Self-Hosted LLM Setup Needs a Summary in the Evaluation Chapter
**File**: `appendix/selfhosted-llm.tex` → should feed `content/06-evaluation.tex`

The evaluation tests `qwen3:30b` on a self-hosted server. The full hardware specs and setup instructions are correctly in the appendix, but the evaluation chapter never introduces this environment. A short paragraph (2–4 sentences) in the evaluation setup section should describe the self-hosted environment and point to the appendix for details. Without it, the reader does not understand where the local model runs or what its resource constraints are.

---

### H4 — Variant Decisions Are Buried in Appendix but Drive Core Design Choices
**Files**: `appendix/variant-decision-thesis-goals.tex`, `appendix/variant-decision-ai-integration.tex`

Both variant decisions (AI vs. manually built scenarios; AI-agent-in-NSAK vs. NSAK-as-MCP-server) are architecturally significant and explain *why* the thesis has its current scope and design. Currently they are only in the appendix with no mention in the main text. The concepts chapter (Chapter 3) or the implementation chapter should contain a brief summary of each decision and reference the appendix for the full analysis. Otherwise a reader of the main text cannot understand why these particular approaches were chosen.

---

### H5 — Reconnaissance Code Listings Are Fully in Appendix While Main Section Has None
**Files**: `content/05.4-reconnaissance-scenario.tex`, `appendix/reconnaissance-listings.tex`

Section 5.4 describes the reconnaissance scenario but has a TODO for a missing code snippet. All five code listings (scenario.py, drill.yaml, drill.py for host discovery, port scan, service enumeration) are in the appendix only. At least one key snippet (e.g., the scenario.py orchestration) should appear inline in 5.4 to make the main text self-contained. The appendix can retain the full listings with an explicit cross-reference from 5.4.

---

## Medium Priority

### M1 — Project Goals Section is Too Detailed for an Introduction Chapter
**File**: `content/01.2-goals.tex` (215 lines)

A 215-line goals section with full S.M.A.R.T. tables and MoSCoW breakdowns is unusually long for an introduction. Standard thesis structure keeps goals concise in the introduction (10–20 lines) and moves detailed goal elaboration to a project management appendix. The S.M.A.R.T. tables and detailed scope discussion could move to an appendix section (near the existing project-management.tex), leaving a condensed 1-page version in the introduction.

---

### M2 — Benchmark Suite (05.5) Content Belongs with Methodology, Not Implementation
**File**: `content/05.5-benchmark-suite.tex`

The benchmark suite section (BenchmarkManager, BenchmarkRun, BenchmarkResult, BenchmarkReport concepts) defines the *measurement framework* used in the evaluation. This is methodology, not implementation. Once Chapter 4 (Methodology) is written, the conceptual definition of these benchmark primitives should move there. The technical implementation detail (how the code works) can stay in 5.5 or the appendix.

---

### M3 — Vulnerability Catalog in 05.2 Should Be Condensed in Main Text
**File**: `content/05.2-test-environment.tex`, `appendix/test-environment-listings.tex`

Section 5.2 documents the intentional vulnerabilities (LDAP anonymous read, SMB weak auth, AXFR zone transfer, etc.) in detail. The appendix (`test-environment-listings.tex`) already contains the full containerlab YAML and vulnerability specifications. The main text should give a structured *overview* (e.g., a table: service → vulnerability category → intentional flaw) and reference the appendix for the complete specifications. Duplicating the detail in both places inflates the main text unnecessarily.

---

### M4 — Workshop Outcomes Should Be Referenced in Main Text
**File**: `appendix/workshops.tex` → should inform `content/03-concepts.tex` or Chapter 4

The workshops defined the scenario selection (which red/blue team scenarios to build) and produced user story maps. These outcomes directly explain design decisions that appear in the concepts and implementation chapters. The main text should reference the workshops appendix at the point where scenario selection is discussed — currently there is no cross-reference, so the reader cannot trace the rationale for the chosen scenarios.

---

### M5 — Chapter 2 Ordering: AI Research Should Precede Framework Comparison
**File**: `content/02-related-work.tex`

The chapter currently opens with the framework comparison (Metasploit, Atomic Red Team, Caldera vs. NSAK) and then moves to AI research. Since the central contribution of the thesis is AI integration, the AI background (LLM evolution, agentic AI, MCP) should come first to establish the conceptual foundation. The framework comparison is supporting context. Reordering would better reflect the thesis's priorities and make the narrative flow from "what AI can do" → "what existing security frameworks do" → "gap this thesis fills."

---

### M6 — Configuration Management Duplication Between Chapter 3 and Section 5.1
**Files**: `content/03-concepts.tex`, `content/05.1-configuration-management.tex`

There is an acknowledged TODO in 5.1: "this section is repeating what's already stated in the concepts chapter." Chapter 3 explains the three-layer configuration model (static, runtime, resource) conceptually. Section 5.1 then re-explains the same model before showing implementation. The conceptual explanation in 5.1 should be removed (not moved to appendix — it already exists in Chapter 3). Section 5.1 should open with a direct reference to Chapter 3 and proceed immediately to implementation details.

---

### M7 — Test Environment Description Placement is Ambiguous
**File**: `content/05.2-test-environment.tex` (line 23 TODO)

The TODO questions whether the test environment description belongs in the predecessor project section rather than the implementation chapter. The test environment was built *for this thesis's evaluation*, so it belongs in implementation. However, the introductory framing of section 5.2 should make clear that this is a newly created environment (not inherited from Project 2). Currently the framing is ambiguous. The fix is editorial (a sentence or two), not a structural move.

---

## Low Priority

### L1 — project-management.tex Uses \chapter{} in the Appendix
**File**: `appendix/project-management.tex`

This file uses `\chapter{}` rather than `\section{}`, which is inconsistent with all other appendix files. In the BFH thesis template the appendix sections should use `\section{}` to avoid incorrect chapter numbering. Change the heading command to match the appendix structure.

---

### L2 — sprints.tex Is a Near-Empty Wrapper
**File**: `appendix/sprints.tex`

The file contains only a comment (`% Time form: Past tense`) with no content. Sprint content lives in the `appendix/sprints/` subdirectory but is never `\input{}`-ed from sprints.tex. Either add the `\input{}` calls for the sprint subdirectory files, or consolidate all sprint content into project-management.tex under a "Sprint Ceremonies" subsection (where it logically belongs).

---

### L3 — runs-tempo.tex Is a Thin One-Line Wrapper
**File**: `appendix/runs-tempo.tex`

This file contains a single `\input{}` reference to one benchmark result file. If benchmark run results are part of the appendix, they should be organized under a dedicated appendix section (e.g., "Benchmark Run Results") rather than as an orphan wrapper file. Either expand it to include all relevant run results, or integrate it into the evaluation appendix structure.

---

### L4 — "Out of Scope" at the End of Goals Section
**File**: `content/01.2-goals.tex` (line 208)

The "Out of Scope" content is currently at the end of the goals subsection inside the introduction. It fits better as the last paragraph of the introduction itself (after the goals subsection), or as a note in the project management appendix. Placing it inside a subsection makes it easy to miss.

---

### L5 — Glossary Contains Hardware/Infrastructure Terms Unrelated to the Thesis
**File**: `content/glossary.tex`

The glossary includes entries like `Zynq`, `SoC`, `ASIC`, `RTOS`, `BananaPI R4`, `FRITZ!Box`, and `Infomaniak` — hardware and infrastructure terms carried over from the predecessor project or self-hosted setup. Unless these terms appear in the thesis text, they add noise to the glossary. Prune entries that are not actually referenced in the document.

---

## Summary Table

| ID | Issue | From | To / Action | Priority |
|----|-------|------|-------------|----------|
| H1 | "Former abstract" in introduction | `01-introduction.tex` | Delete | High |
| H2 | Logging/alerting/kill switch in 05.3 | `05.3-ai-scenarios.tex` | Move to appendix / test env | High |
| H3 | Self-hosted LLM not introduced in evaluation | appendix only | Add summary to `06-evaluation.tex` | High |
| H4 | Variant decisions not referenced in main text | appendix only | Add summary + reference in Ch. 3 | High |
| H5 | Reconnaissance code only in appendix | `appendix/reconnaissance-listings.tex` | Add key snippet to `05.4` | High |
| M1 | Goals section too long for introduction | `01.2-goals.tex` | Condense; detail → appendix | Medium |
| M2 | Benchmark concepts in implementation, not methodology | `05.5-benchmark-suite.tex` | Move concept part to Ch. 4 | Medium |
| M3 | Vulnerability detail duplicated in main + appendix | `05.2-test-environment.tex` | Condense main text; appendix stays | Medium |
| M4 | Workshop outcomes not referenced in main text | `appendix/workshops.tex` | Add cross-reference in Ch. 3 | Medium |
| M5 | Framework comparison before AI research in Ch. 2 | `02-related-work.tex` | Swap section order | Medium |
| M6 | Config management concepts duplicated in Ch. 3 and 5.1 | `05.1-configuration-management.tex` | Remove duplicate from 5.1 | Medium |
| M7 | Test environment framing ambiguous vs. Project 2 | `05.2-test-environment.tex` | Editorial fix (1–2 sentences) | Medium |
| L1 | `\chapter{}` used in appendix file | `appendix/project-management.tex` | Change to `\section{}` | Low |
| L2 | sprints.tex has no content or inputs | `appendix/sprints.tex` | Add inputs or merge into PM section | Low |
| L3 | runs-tempo.tex is orphan wrapper | `appendix/runs-tempo.tex` | Integrate into a benchmark results section | Low |
| L4 | "Out of scope" buried in goals subsection | `01.2-goals.tex` | Move to end of introduction | Low |
| L5 | Glossary has unrelated hardware terms | `content/glossary.tex` | Prune unused entries | Low |
