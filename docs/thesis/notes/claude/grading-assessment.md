# Thesis Grading Assessment
**Date:** 2026-06-04
**Scale:** Swiss 1–6 (4.0 = minimum pass, 6.0 = excellent)
**Method:** Seven weighted criteria, scored independently in current state and after all
improvements from `improvement-assessment.md` are applied.

---

## Grading Rubric & Criteria Weights

| # | Criterion | Weight | Rationale |
|---|-----------|--------|-----------|
| G1 | Problem definition & objectives | 10 % | Clarity of RQs, scope, and relation to prior work |
| G2 | State of the art / related work | 15 % | Coverage, depth, and proper attribution of literature |
| G3 | Methodology | 10 % | Soundness of evaluation design, reproducibility |
| G4 | Technical implementation | 20 % | Engineering quality, architecture, completeness |
| G5 | Evaluation & results | 20 % | Validity, completeness, honest presentation of data |
| G6 | Discussion & interpretation | 10 % | Answering RQs, acknowledging limitations, recommendations |
| G7 | Documentation quality | 15 % | Language, structure, citations, academic style |

---

## Criterion Scores

### G1 — Problem definition & objectives (10 %)

| | Score |
|---|---|
| **Current** | **5.0 / 6** |
| **After fixes** | **5.0 / 6** |

**Justification:**
The three research questions are concrete and measurable. The motivation is well-grounded
in real-world reports (WEF, CrowdStrike) and properly bridges to the predecessor project.
The central hypothesis — that agentic AI improves adaptability over static scenarios — is
stated clearly and directly tested.

The thesis does not oversell its scope: it focuses on reconnaissance, explicitly scopes out
blue-team evaluation as a "should" goal, and consistently refers back to the RQs.

No significant improvement is expected from the identified fixes, since this criterion is
already strong. The only minor gap is the absence of an explicit definition of "success" for
each RQ at the outset (e.g., what correctness score would count as "AI supports operators
sufficiently?"), which would make the RQ answers in Chapter 7 more decisive.

---

### G2 — State of the art / related work (15 %)

| | Score |
|---|---|
| **Current** | **3.5 / 6** |
| **After fixes** | **4.5 / 6** |

**Justification (current):**
The framework comparison (Metasploit, Caldera, Atomic Red Team) is thorough, well-cited,
and clearly positioned against NSAK. The MCP integration survey of all three frameworks is
a genuine contribution.

The AI background, however, is the weakest part of the thesis academically. The language
model history (SLM → LLM) covers four sentences and cites only a 2023 survey and a 2020
training-parallelism paper. The following foundational papers are entirely absent:
- Vaswani et al. (2017), "Attention Is All You Need" — the architectural basis for all
  modern LLMs
- Brown et al. (2020), "Language Models are Few-Shot Learners" — established the LLM
  paradigm at scale
- Wei et al. (2022), chain-of-thought prompting — directly relevant to agent reasoning
- Yao et al. (2022), ReAct — the specific paradigm used by LangGraph agents in this thesis
- Lewis et al. (2020), RAG — described in the concepts chapter without citation

The agentic AI section relies heavily on chapters from a single edited book (Huang 2025)
whose bib entries share an identical title ("Define AI Agent"), raising quality concerns.
The informal podcast citation (Risky Business) for the claim "MCP is dead" is not
acceptable as an academic source for a factual claim.

**After fixes (I-4, I-11):** Adding the five foundational papers and replacing or
supplementing the podcast claim with a peer-reviewed source would raise this to ~4.5.
A 5.0 would require a more systematic review of AI-driven penetration testing literature
(e.g., Applebaum et al. 2016 is in the bibliography but never cited in the text).

---

### G3 — Methodology (10 %)

| | Score |
|---|---|
| **Current** | **4.0 / 6** |
| **After fixes** | **5.0 / 6** |

**Justification (current):**
The evaluation design is clear: three models, two agent architectures, a static baseline,
n=10 runs per configuration, a reproducible containerlab environment, and an explicit
qualitative rubric. The benchmark suite automating quantitative metrics is a genuine
methodological contribution.

Weaknesses:
- The methodology defines three evaluation environments; only two are evaluated. This
  represents a material deviation from the stated plan that is only acknowledged in
  limitations (I-2).
- The qualitative scoring scale has an inverted Hallucination axis (high score = bad)
  compared to Correctness (high score = good), creating a systematic reading risk (I-6).
- Correctness and hallucination were scored by the thesis authors themselves against a
  ground truth they also defined, with no inter-rater validation, no rubric calibration
  examples, and no mention of how disagreements between co-authors were resolved (I-10).
- The selection of three specific models (one frontier, one mid-tier, one local) is not
  justified against alternatives — no explanation why no other frontier model was compared.

**After fixes (I-2, I-6, I-10, I-12):** Addressing the environment gap, adding a rubric
calibration example, and providing the model selection rationale would bring this to 5.0.

---

### G4 — Technical implementation (20 %)

| | Score |
|---|---|
| **Current** | **5.0 / 6** |
| **After fixes** | **5.2 / 6** |

**Justification (current):**
This is the strongest part of the thesis. The LangChain/LangGraph agent integration is
well-engineered: provider abstraction via a single `PROVIDER_MAP`, async refactoring for
MCP support, deterministic temperature-zero configuration, structured vs. unstructured
output variants, and a kill switch for safety. The multi-agent decomposition approach is
a principled design decision with measurable payoff.

The three-layer configuration system (static / runtime / resource) is architecturally clean
and cleanly described. The containerlab test environment with deliberately misconfigured
services (anonymous LDAP bind, exposed credentials, banner mismatches) is a well-designed
evaluation artifact.

Minor weaknesses:
- Two subsections describe abandoned implementations (LangChain HITL middleware, Chat UI)
  that do not belong in the Implementation chapter (I-9).
- The transition from the initial test model (`qwen2.5:7b-coder`) to the final evaluated
  models (`qwen3:30b`, etc.) is mentioned in passing without a clear explanation.
- The tool calling section lacks a citation (I-4 / M3).

**After fixes (I-9):** Cleaning the chapter of "didn't do X" content would improve
coherence. The score ceiling here is not a 6 because the implementation did not fully
achieve all stated goals (blue-team scenario is only proof-of-concept; physical environment
not deployed).

---

### G5 — Evaluation & results (20 %)

| | Score |
|---|---|
| **Current** | **4.0 / 6** |
| **After fixes** | **5.0 / 6** |

**Justification (current):**
The quantitative evaluation is well-executed: duration, token usage, host/service/finding
counts, scatter plots, and a success factor are all reported. The vulnerability coverage
table (Table 5 in Chapter 6) is particularly strong — it maps each ground-truth
vulnerability against what each configuration actually found, which is exactly the right
level of rigor.

The qualitative comparison in the containerlab (Table 4) is honest and specific, including
the concrete misclassification of the printer as a honeypot.

Significant weaknesses:
- The success rate framing is misleading: headline tables present n=10 successful runs
  without the denominator visible in the same view. The 5/27 and 6/109 attempt counts
  are buried in the text and discussion. A reader scanning the tables will form an
  overly optimistic picture (I-3).
- The BFH results table (Table in §6.2) shows `--` for hosts, services, and findings
  for the static scenario, but the discussion text states it found 130 services and 58
  findings. The table is factually incomplete (I-7).
- The abstract claims "even smaller models are capable of autonomously conducting standard
  red team activities," directly contradicted by qwen3:8b (0 tool calls, all runs) and
  qwen3:30b (misses the single critical finding in 9/10 runs) (I-1).
- The static vs. AI comparison is framed as if both approaches compete on the same axis,
  when they are fundamentally asymmetric (breadth vs. depth). This makes the comparison
  harder to interpret than it needs to be (I-15).
- The qualitative BFH evaluation is deliberately thin ("because the lab is still in use"),
  which is understandable but limits the evidentiary value of the BFH section.

**After fixes (I-1, I-3, I-7, I-15):** Fixing the denominator visibility, the incomplete
table, the abstract, and explicitly framing the asymmetric comparison would bring this to 5.0.

---

### G6 — Discussion & interpretation (10 %)

| | Score |
|---|---|
| **Current** | **4.5 / 6** |
| **After fixes** | **5.0 / 6** |

**Justification (current):**
All three research questions are answered in dedicated paragraphs with concrete references
to evaluation results. The recommendations section is practical and grounded. The
limitations section honestly acknowledges the missing environment, low success rates, and
subjectivity of scoring.

The discussion correctly identifies the central finding: the AI scenario adds an
interpretive layer that complements rather than replaces the static scenario, and
multi-agent decomposition improves smaller models disproportionately.

Weaknesses:
- The "Unexpected Results" section is only two short paragraphs and reads as an appendix
  rather than a substantive finding. A 68 % token reduction and a complete model failure
  are significant enough results to deserve more analysis.
- One sentence in the recommendations has a broken reference: "While partly implemented
  in  we discarded the branch" (I-5).
- The technical conclusion (§8.2) is ~150 words — too brief to synthesize the work and
  position it relative to related work reviewed in Chapter 2 (I-13).

**After fixes (I-5, I-13):** Expanding the conclusion and fixing the broken reference
would bring this to 5.0. A 5.5 would require deeper analysis in "Unexpected Results"
and a stronger connection between the findings and the related-work landscape.

---

### G7 — Documentation quality (15 %)

| | Score |
|---|---|
| **Current** | **3.5 / 6** |
| **After fixes** | **5.0 / 6** |

**Justification (current):**
This criterion is the main drag on the current overall grade. The problems are numerous:

**Language errors (I-5):**
"Even tough" (should be "though"), "relly on" (twice — should be "rely"), "the tool calling
variants are often have the suffix", "due to the fact from its tendency", "teh operator",
"For large models this could be even harmfully."

**Structural issues:**
- One empty `\cite{}` placeholder that will render as a blank in the PDF (I-4 / C1)
- One broken sentence "such as ." (I-4 / C2)
- One sentence with a missing reference "While partly implemented in  we discarded" (I-5)
- Multiple bare `\ref{}` calls rendering as orphaned numbers (I-8)

**Citation issues:**
- No citation for chain-of-thought prompting, RAG, or the ReAct paradigm (I-11 / M1–M4)
- MITRE ATT&CK definition is near-verbatim from the source without quotation marks (I-4 / C3)
- AI-generated `:contentReference[oaicite:0]{index=0}` artifacts remain in two bib entries

**Style:**
- Inconsistent tense within chapters (I-18)
- Inline YouTube and GitLab branch URLs in academic text (I-16)
- `\gls{}` vs. `\glsxtrshort{}` used inconsistently for NSAK, YAML, CLI (I-19)
- Model name `claude-opus-4-7` vs. "Claude Opus 4.7" mixed in running prose (I-20)

The implementation and evaluation chapters are well-structured and mostly readable. The
documentation problems are concentrated in Chapters 2, 3, and the bibliography, and in
scattered errors throughout.

**After fixes (I-4 through I-20):** Resolving all language, citation, and formatting issues
would bring this to 5.0. A 5.5 would require a more consistently polished academic voice,
particularly in transition passages and the conclusion.

---

## Overall Grade

### Weighted Score Calculation

| Criterion | Weight | Current Score | Current Contribution | Fixed Score | Fixed Contribution |
|-----------|--------|---------------|---------------------|-------------|-------------------|
| G1 Problem definition | 10 % | 5.0 | 0.50 | 5.0 | 0.50 |
| G2 Related work | 15 % | 3.5 | 0.53 | 4.5 | 0.68 |
| G3 Methodology | 10 % | 4.0 | 0.40 | 5.0 | 0.50 |
| G4 Implementation | 20 % | 5.0 | 1.00 | 5.2 | 1.04 |
| G5 Evaluation | 20 % | 4.0 | 0.80 | 5.0 | 1.00 |
| G6 Discussion | 10 % | 4.5 | 0.45 | 5.0 | 0.50 |
| G7 Documentation | 15 % | 3.5 | 0.53 | 5.0 | 0.75 |
| **Weighted total** | 100 % | | **4.2 / 6** | | **5.0 / 6** |

---

### Grade in Context

| State | Weighted Score | Swiss Grade | Interpretation |
|-------|----------------|-------------|----------------|
| **Current** | 4.2 / 6 | **4.0–4.5** | Sufficient — passes, but with notable gaps |
| **After Priority 1–2 fixes** (I-1 to I-10) | ~4.6 / 6 | **4.5** | Adequate — meets requirements |
| **After all fixes** (I-1 to I-20) | ~5.0 / 6 | **5.0** | Good — meets all requirements with above-average elements |

---

## Key Observations

**Why the gap is so large (4.2 → 5.0):**
The core engineering work is genuinely strong (G4 = 5.0) and the problem is
well-defined (G1 = 5.0). However, 35 % of the weight sits in G2 (related work, 3.5)
and G7 (documentation, 3.5) — both of which are below passing quality in their current
state. These criteria are also the cheapest to fix: the documentation issues are
~11 h of writing/editing work, not new experiments.

**What cannot be fixed without new experiments:**
- G3 methodology: The physical environment is simply missing. Even with the narrative fix
  (I-2 option b), a strict examiner will penalize the deviation from the stated plan.
- G5 evaluation: The BFH qualitative assessment is thin by necessity (lab still in use),
  and the 5.5 % success rate of the unstructured configuration is a real limitation.
- G4 implementation ceiling: The blue-team IDS scenario being proof-of-concept and the
  dynamic tool selection not being fully integrated keep this below 5.5.

**What would push the thesis to 5.5:**
1. Adding the five missing foundational AI papers to G2 (I-11) + a proper related-work
   paragraph on AI-driven penetration testing (Applebaum 2016 is already in the bib
   but never cited in text)
2. Physical environment evaluation or a formal written justification for descoping it
3. Inter-rater agreement on at least a subset of qualitative scores
4. Expanding the conclusion to synthesize the contribution against the related work reviewed
