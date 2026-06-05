# Thesis Improvement Assessment
**Date:** 2026-06-04
**Scope:** All chapters + abstract + bibliography
**Sorted by:** Importance (critical → high → medium → minor)

---

## Priority 1 — Critical (affects academic credibility or examinability)

---

### I-1 — Abstract overstates smaller-model results
**Estimated effort: 1 h**

**File:** `content/abstract.tex`
**Issue:** "even smaller models are capable of autonomously conducting standard red team activities"
is contradicted by the data: `qwen3:8b` executes zero tool calls in the BFH lab, and
`qwen3:30b` misses the single critical LDAP finding in 9 of 10 containerlab runs.
The sentence "most failures are detectable, enabling retry logic" also overpromises — retry
logic is listed as future work, not implemented or evaluated.
**Fix:** Replace with a precise summary that reflects the actual findings. E.g., clarify that
only the frontier model reliably completed the task, that smaller models benefit from
multi-agent decomposition but remain unreliable at scale, and that retry logic remains future work.

---

### I-2 — Physical environment gap: promised but never delivered
**Estimated effort: 3 h**

**Files:** `content/04-methodology.tex` (lists 3 environments), `content/07-discussion.tex` (acknowledges gap)
**Issue:** The methodology explicitly defines three evaluation environments:
(1) containerlab, (2) physical lab, (3) BFH cyber lab. The physical lab environment
is never evaluated. This is mentioned only once in the limitations section. An examiner
will read the methodology, expect three environments, and find only two.
**Fix:** Either (a) add a short physical environment evaluation, or (b) revise the methodology
chapter to present only two environments as the planned scope, and explain in limitations
why the third was deprioritized. Option (b) takes ~1 h; option (a) takes ~3 h but strengthens the thesis.

---

### I-3 — Success rates not prominently contextualized
**Estimated effort: 2 h**

**Files:** `content/06.1-container-lab.tex`, `content/06.2-ns-lab.tex`, `content/07-discussion.tex`
**Issue:** The headline evaluation tables show n=10 successful runs, but the actual attempt
counts are buried: 5/27 for multi-agent BFH and 6/109 for unstructured BFH.
Presenting averaged results from 5 successes out of 27 attempts as representative
performance — without a clear disclaimer at the top of the evaluation section — is
misleading. The discussion addresses it briefly but not prominently enough.
**Fix:** Add a dedicated "Reliability" paragraph or row to each evaluation overview that
leads with the attempt count before the quality metrics. State the implications upfront
in the evaluation section, not only in the limitations.

---

### I-4 — All citation and bibliography fixes (see plagiarism report)
**Estimated effort: 3 h**

The plagiarism assessment (see `plagiarism-citation-assessment.md`) identified one empty
`\cite{}`, four missing concept citations (chain-of-thought, RAG, ReAct, tool calling),
and several bibliography metadata errors. All critical and moderate items from that report
should be resolved. See that report for detail; effort includes looking up DOIs, adding
bib entries, and rephrasing the near-verbatim MITRE sentence.

---

### I-5 — Grammatical errors and broken sentences throughout
**Estimated effort: 2 h**

Multiple grammatical issues identified across chapters:

| Location | Error | Fix |
|---|---|---|
| `02-related-work.tex:211` | "such as ." — sentence fragment | Remove or complete |
| `02-related-work.tex:213` | "relly on" | "rely on" |
| `03-concepts.tex:147` | "Even tough" | "Even though" |
| `05.3-ai-scenarios.tex:107` | "variants are often have the suffix" | "variants often have the suffix" |
| `06.2-ns-lab.tex:44` | "due to the fact from its tendency" | "due to its tendency" |
| `06.2-ns-lab.tex:58` | "roughly 100% higher" vs "nearly three times" — contradictory in same section | Pick one; 222,094/116,738 ≈ 1.9×, so "nearly double" is correct |
| `07-discussion.tex:183` | "While partly implemented in  we discarded" — missing reference | Fill reference or fix sentence |
| `06-evaluation.tex:53` | "For large models this could be even harmfully" | "harmful" |
| `06-evaluation.tex:63` | "we could not relly on the automation" | "rely" |
| `07-discussion.tex:211` | "teh operator" | "the operator" |

---

## Priority 2 — High (significantly weakens quality)

---

### I-6 — Inverted/confusing Hallucination scale in methodology
**Estimated effort: 0.5 h**

**File:** `content/04-methodology.tex`, Table 2 (`tab:qualitative-scale`)
**Issue:** The Correctness scale runs 1–2 = Insufficient up to 9–10 = Excellent (low is bad).
The Hallucination scale runs 9–10 = Severe down to 1–2 = None (low is good).
This inverted direction is non-obvious, will confuse readers, and risks misinterpretation
when comparing scores across the two criteria.
**Fix:** Either (a) re-define Hallucination so that higher = better (rename to "Accuracy of Claims"
and flip the descriptions), making both scales consistent; or (b) add a prominent note
that Hallucination scores are intentionally inverted with an explicit callout at first use.

---

### I-7 — BFH results table missing static scenario numbers
**Estimated effort: 0.5 h**

**File:** `content/06.2-ns-lab.tex`, Table (`tab:overview-nslab`)
**Issue:** The static scenario row shows `--` for hosts, services, and findings, but the
discussion (Chapter 7) states it found 130 services and 58 findings, and the duration
was 1780 s. The table is therefore incomplete and inconsistent with the text.
**Fix:** Fill in the known numbers (1780 s, 130 services, 58 findings) for the static scenario
row. Where host count is unknown/undefined, explain in a footnote.

---

### I-8 — Bare `\ref{}` calls without surrounding text
**Estimated effort: 1 h**

**Files:** Multiple chapters
Multiple places use raw `\ref{}` or `\ref{}\ref{}\ref{}` concatenated without any
surrounding language (e.g., `02-related-work.tex:95`, `03-concepts.tex:98`, `03-concepts.tex:136`).
These render as orphaned section numbers in the PDF and look unfinished to any reviewer.
**Fix:** Replace all bare references with "Section~\ref{}", "see~\ref{}", or
"as described in~\ref{}". Do a full-document grep for `}}\ref` and `.\ref` to catch
all instances.

---

### I-9 — "We didn't do X" sections belong in Future Work, not Implementation
**Estimated effort: 1 h**

**File:** `content/05.3-ai-scenarios.tex`
Two subsections in the Implementation chapter describe things that were started but
deliberately not merged:
- §5.3.3.3 "LangChain Middleware: Human in the Loop (HITL)" — describes a proof-of-concept
  that didn't work well enough and was discarded
- §5.3.3.4 "LangChain Agent Chat UI" — describes something not implemented at all

Both of these read as implementation notes to a future developer rather than academic
content. They weaken the impression of the chapter.
**Fix:** Move these to the Future Work section (§8.3) with a one-sentence note each.
Replace the space in §5.3 with a brief paragraph summarizing the human-interaction
design decision and why the simple hook was kept.

---

### I-10 — Qualitative scoring subjectivity not adequately mitigated
**Estimated effort: 1.5 h**

**File:** `content/07-discussion.tex` (limitations section)
**Issue:** The correctness and hallucination scores were assigned by the authors themselves
against a known ground truth they also defined. The thesis acknowledges the subjectivity
but presents no mitigation (no inter-rater agreement, no rubric examples, no second scorer).
This is an easy target for examiners.
**Fix:** Either (a) have a second independent person score a subset of runs and report the
agreement (Cohen's κ or simple % agreement) — this takes ~2 h; or (b) provide 2–3
concrete scoring examples in the methodology chapter that ground the rubric, demonstrating
calibration. Option (b) takes ~1.5 h and is more realistic before submission.

---

## Priority 3 — Medium (improves academic depth and completeness)

---

### I-11 — LLM/Agent background is thin; foundational papers missing
**Estimated effort: 2 h**

**File:** `content/02-related-work.tex`, AI Research section
The language model history (SLM → NLM → PLM → LLM) is covered in four sentences and only
cites Zhao et al. (2023 survey) and Shoeybi et al. (2020) for the parameter size statement.
The Agentic AI section cites chapters from a single book (Huang 2025).
For an AI-focused thesis, reviewers will expect citations to canonical papers:
- Attention/Transformers: Vaswani et al. (2017) "Attention Is All You Need"
- GPT-scale language models: Brown et al. (2020) "Language Models are Few-Shot Learners" (GPT-3)
- Chain-of-thought: Wei et al. (2022)
- ReAct: Yao et al. (2022)
- RAG: Lewis et al. (2020)
**Fix:** Add 3–5 foundational citations in the AI background, replacing or supplementing the
Huang book chapters where appropriate.

---

### I-12 — Model choice not justified: no GPT-4o, Gemini, or newer Claude
**Estimated effort: 1 h**

**File:** `content/04-methodology.tex`, §4.3 Models
**Issue:** The thesis evaluates one frontier API model (claude-opus-4-7) and two open-weight
models, but does not explain why no other frontier model (GPT-4o, Gemini 1.5 Pro,
Llama-3-70B) was included for comparison. This limits the generalizability of the findings.
**Fix:** Add 2–3 sentences in the methodology explaining the selection rationale:
institutional API access, cost constraints, reproducibility, or scope limitation.
This makes the choice defensible without requiring additional experiments.

---

### I-13 — Conclusion chapter is too brief
**Estimated effort: 1.5 h**

**File:** `content/08-conclusion.tex`
The technical conclusion (§8.2) is approximately 150 words and reads as a bullet-point
summary of the abstract. It does not synthesize the findings into a coherent intellectual
contribution or position the work in relation to the related work reviewed in Chapter 2.
**Fix:** Expand §8.2 to ~400–500 words that: (1) revisit the central hypothesis stated in
the introduction and evaluate whether it was confirmed, (2) state what was genuinely
novel compared to prior work, and (3) identify the most important open question for future work.

---

### I-14 — Complete the bibliography metadata
**Estimated effort: 1.5 h**

As noted in the plagiarism report (m1–m8), several `@misc` entries are missing `year`,
`urldate`, and `author` fields. Additionally, the `chapter1`/`chapter3` bib entries need
correct chapter titles. This is mechanical but important for a publishable thesis.
**Fix:** Add `urldate`, `year`, and `author` to all tool/software entries. Verify and correct
the Huang book chapter titles.

---

### I-15 — AI reconnaissance scenario comparison is asymmetric
**Estimated effort: 1.5 h**

**File:** `content/06-evaluation.tex`, `content/07-discussion.tex`
**Issue:** The comparison between static and AI scenarios conflates two different things:
(a) raw coverage of hosts and services, and (b) depth/quality of findings. The evaluation
shows the static scenario discovers more services (13 vs 9) while AI finds deeper
findings (LDAP credentials). But this is never framed as an explicitly asymmetric
comparison where the two approaches are good at different things. Instead, the thesis
switches between comparing them on the same scale and noting they're incomparable.
**Fix:** Add a short "Comparison Framework" paragraph early in the evaluation that explicitly
states: the two scenarios are not competing on the same metric (breadth vs. depth) and
defines which metrics are appropriate for each. This pre-empts the most likely examiner
objection.

---

## Priority 4 — Minor (polish and professional presentation)

---

### I-16 — Inline `\href{}` URLs should be footnotes or citations
**Estimated effort: 0.5 h**

**File:** `content/05.3-ai-scenarios.tex` (lines 161, 167, 171, 174)
Several URLs appear as inline hyperlinks in the main text body, including YouTube tutorials
and branch links. These are non-citable sources (YouTube tutorial, a GitLab branch). In
an academic thesis they should appear in footnotes or be removed.
**Fix:** Convert the YouTube tutorial link and GitLab branch references to `\footnote{}`.
Remove the LangChain UI link if the section is moved to Future Work per I-9.

---

### I-17 — Personal section tone inconsistency
**Estimated effort: 0.5 h**

**File:** `content/08-conclusion.tex`
The personal section (§8.1) is written in a casual, reflective style that differs markedly
from the rest of the document. Specific phrases ("rookie mistake", "walking the extra mile",
"just another thing") are colloquial. Whether this is appropriate depends on BFH's thesis
guidelines — some schools require formal language throughout.
**Fix:** Review BFH thesis guidelines and adjust tone if required. At minimum, replace
contractions and highly colloquial phrases with professional equivalents.

---

### I-18 — Tense inconsistencies between and within chapters
**Estimated effort: 1 h**

Each chapter has a tense marker comment (e.g., `% Time form: Present tense`) but the
writing occasionally switches tense mid-paragraph. The discussion chapter uses both present
and past tense in the same paragraph. The implementation chapter (past tense) sometimes
uses present tense for current-state descriptions.
**Fix:** Do a focused read-through of chapters 5, 6, and 7 with tense as the single focus,
correcting violations of the declared tense for each chapter.

---

### I-19 — `\gls{}` vs. `\glsxtrshort{}` used inconsistently
**Estimated effort: 0.5 h**

Throughout the document, the acronym `NSAK` is sometimes written as `\gls{NSAK}` (which
expands on first use) and sometimes as `\glsxtrshort{NSAK}` (always short form). Similarly
for YAML, CLI, and a few others. This is inconsistent.
**Fix:** Standardize all acronym references to `\gls{}` and let the glossary system handle
expansion vs. abbreviation automatically.

---

### I-20 — Methodology model table: `Claude Opus 4.7` vs `claude-opus-4-7` inconsistency
**Estimated effort: 0.5 h**

**File:** `content/04-methodology.tex`, line 12 and Table 3
In the methodology text, the model is called "Claude Opus 4.7" (proper noun), but in the
table it appears as `claude-opus-4-7` (API identifier). The discussion chapter uses
"claude-opus-4-7" in running text, which reads awkwardly as a prose word.
**Fix:** Establish a consistent convention: use the API identifier `\texttt{claude-opus-4-7}`
only in code/table contexts, and "Claude Opus 4.7" in running prose.

---

## Summary Table

| ID | Area | Description | Effort |
|----|------|-------------|--------|
| I-1 | Abstract | Overstated smaller-model claims | 1 h |
| I-2 | Methodology/Evaluation | Physical environment gap | 3 h |
| I-3 | Evaluation | Success rates not prominently contextualized | 2 h |
| I-4 | Citations | All citation/bib fixes (see plagiarism report) | 3 h |
| I-5 | Language | Grammatical errors and broken sentences | 2 h |
| I-6 | Methodology | Inverted Hallucination scale confusing | 0.5 h |
| I-7 | Evaluation | BFH table missing static scenario numbers | 0.5 h |
| I-8 | Cross-cutting | Bare `\ref{}` calls without surrounding text | 1 h |
| I-9 | Implementation | "Didn't implement X" sections → Future Work | 1 h |
| I-10 | Methodology | Qualitative scoring lacks calibration evidence | 1.5 h |
| I-11 | Related Work | LLM background thin; foundational papers missing | 2 h |
| I-12 | Methodology | Model selection not justified | 1 h |
| I-13 | Conclusion | Technical conclusion too brief | 1.5 h |
| I-14 | Bibliography | Missing bib metadata (year, urldate, author) | 1.5 h |
| I-15 | Evaluation | Asymmetric static vs AI comparison not framed | 1.5 h |
| I-16 | Formatting | Inline URLs → footnotes | 0.5 h |
| I-17 | Style | Personal section: colloquial tone | 0.5 h |
| I-18 | Language | Tense inconsistencies within chapters | 1 h |
| I-19 | Formatting | `\gls{}` vs `\glsxtrshort{}` inconsistency | 0.5 h |
| I-20 | Formatting | Model name formatting inconsistency | 0.5 h |
| | | **Total estimated effort** | **~27 h** |

---

## Recommended Focus Sessions

Given the estimates above, a realistic revision plan:

| Session | Items | Hours |
|---------|-------|-------|
| Session 1 — Academic integrity | I-4 (citations + bib) | 3 h |
| Session 2 — Credibility fixes | I-1, I-3, I-6, I-7 | 4 h |
| Session 3 — Structural fixes | I-2, I-9, I-13 | 5.5 h |
| Session 4 — Language pass | I-5, I-8, I-18 | 4 h |
| Session 5 — Depth improvements | I-10, I-11, I-12, I-15 | 6 h |
| Session 6 — Polish | I-14, I-16, I-17, I-19, I-20 | 3 h |
| **Total** | | **~26 h** |
