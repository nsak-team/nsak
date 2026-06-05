# Plagiarism & Citation Assessment
**Date:** 2026-06-04
**Scope:** All main content chapters (`01`–`08`) + `references.bib`
**Assessor:** Claude Sonnet 4.6

---

## Overall Assessment

The thesis demonstrates clearly original work throughout the implementation and evaluation
chapters, which describe the authors' own system, experiments, and results. The plagiarism
risk is **low**. No verbatim or near-verbatim copying was found that lacked a corresponding
citation. The citation problems identified are:

1. One broken/empty citation placeholder (`\cite{}`)
2. Several concepts introduced without any citation at all
3. A handful of passages whose phrasing closely mirrors the language of the cited source
   (paraphrasing that should be re-worded or explicitly quoted)
4. Multiple bibliographic entries with incomplete or incorrect metadata
5. One incomplete sentence left in the text

---

## Critical Issues (must fix before submission)

### C1 — Empty citation placeholder
**File:** `content/03-concepts.tex`, line 135
**Passage:**
```
This is typically enforced through grammar-based sampling or constrained decoding,
which restricts the set of valid tokens at each generation step to those that keep
the output consistent with the target schema~\cite{}.
```
An empty `\cite{}` will cause a LaTeX warning / blank reference in the PDF.
**Fix:** Fill in the appropriate citation. Suitable candidates:
- Willard & Louf (2023) "Efficient Guided Generation for Large Language Models" (arXiv:2307.09702)
- Beurer-Kellner et al. (2023) "Prompting Is Programming: A Query Language for Large Language Models"
- Or cite the LangChain structured-output docs (`langchain_structured_output`) that is already in the bibliography.

---

### C2 — Incomplete sentence
**File:** `content/02-related-work.tex`, lines 211–212
**Passage:**
```
Recently, other concepts for calling tools were established, such as .
```
The sentence ends with "such as ." — the concept name was removed but the sentence frame
was left. This will confuse readers and reviewers.
**Fix:** Either name the concept(s) (e.g., OpenAI function calling, ACI, etc.) or delete the
sentence entirely.

---

### C3 — MITRE ATT&CK definition verbatim from source
**File:** `content/02-related-work.tex`, line 15
**Passage:**
```
The MITRE ATT&CK framework is a globally accessible knowledge base of adversary
tactics and techniques based on real-world observations~\cite{mitreattack}.
```
This sentence is essentially word-for-word from MITRE's official description. The citation
is present, but automated plagiarism detectors will flag this as verbatim copying.
**Fix:** Either wrap in `\enquote{...}` to quote it explicitly, or paraphrase in your own words.

---

## Moderate Issues (strongly recommended to fix)

### M1 — Chain-of-thought: concept used without original citation
**File:** `content/03-concepts.tex`, lines 151–153
**Passage:**
```
This is typically achieved through prompting strategies such as chain-of-thought,
where the model is instructed to think step by step before producing a final answer.
```
Chain-of-thought prompting is a specific technique introduced by Wei et al. (2022). No
citation is given.
**Fix:** Add `\cite{}` pointing to:
Wei et al. (2022) "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (NeurIPS 2022).

---

### M2 — RAG: definition without citation
**File:** `content/03-concepts.tex`, lines 157–161
**Passage:**
```
Retrieval Augmented Generation is a technique that extends an LLM by retrieving
relevant documents or knowledge at inference time and including them in the context
window alongside the user prompt.
```
No citation for RAG.
**Fix:** Add citation to Lewis et al. (2020) "Retrieval-Augmented Generation for
Knowledge-Intensive NLP Tasks" (NeurIPS 2020), arXiv:2005.11401.

---

### M3 — Tool calling definition: no citation
**File:** `content/05.3-ai-scenarios.tex`, lines 80–85
**Passage:**
```
Tool calling is the mechanism by which the LLM declares that it wants to invoke an
external function. The framework intercepts the model's output, parses the tool call,
executes the corresponding Python function, MCP, or Skill, and appends the result to
the message history before asking the model to continue.
```
This is a general technical description but no citation is given.
**Fix:** Cite a foundational reference, e.g., the Anthropic or OpenAI API documentation for
tool use, or the LangChain docs (`langchain_docs` already in bibliography).

---

### M4 — ReAct agent: foundational paper not cited
**File:** `content/05.3-ai-scenarios.tex`, line 68
**Passage:**
```
\mintinline{python}{create_agent()} - builds a LangGraph-based ReAct agent graph
```
The ReAct reasoning strategy was introduced in a specific paper that should be cited when
naming the paradigm.
**Fix:** Add: Yao et al. (2022) "ReAct: Synergizing Reasoning and Acting in Language Models"
(ICLR 2023), arXiv:2210.03629.

---

### M5 — MCP description closely mirrors source language
**File:** `content/02-related-work.tex`, lines 172–173
**Passage:**
```
The MCP was introduced as an open source standard that enables AI assistants to
connect to external systems, including databases, business tools, and development
environments~\cite{anthropic-mcp}.
```
This phrasing is very close to Anthropic's own blog announcement text. The citation is
present, but the sentence should be paraphrased more thoroughly.
**Fix:** Rephrase in your own words, keeping `\cite{anthropic-mcp}`.

---

### M6 — BIND: no citation
**File:** `content/05.2-containerlab-environment.tex`, line 28
**Passage:**
```
BIND is a complete implementation of the DNS protocol that can be configured through
the named.conf file as an authoritative name server and resolver.
```
No citation for BIND (ISC BIND9).
**Fix:** Add a `@misc` entry for the ISC BIND documentation (https://www.isc.org/bind/) and
cite it here.

---

### M7 — Containerlab: citation missing in concepts section
**File:** `content/03-concepts.tex`, lines 100–111
The `containerlab` bib entry exists but is not cited anywhere in the concepts section where
Containerlab is first introduced and compared to Docker/Podman. It only appears (if at all)
in the implementation chapter.
**Fix:** Add `~\cite{containerlab}` at the first substantive mention of Containerlab in Section 3.4.

---

## Minor Issues (should fix)

### m1 — Bibliography: chapter1 and chapter3 share the same title
**File:** `references.bib`, entries `chapter1` and `chapter3`
Both entries carry the title "Define AI Agent" from the book *Agentic AI: Theories and
Practices* (Huang, 2025). Chapter 3 appears to be a different chapter (co-authored by
K Huang and J Huang) and should have its own correct title.
**Fix:** Verify the actual chapter titles from the book and update both entries to include
correct `title` and `pages` fields.

---

### m2 — `riskybiz_mcp`: incomplete podcast citation
**File:** `references.bib`, entry `riskybiz_mcp`
```bibtex
title        = {...MCP is Dead},
note         = {Podcast episode , Accessed: 2026-03-18}
```
Missing: episode number/title, date, and the note says "Podcast episode ," (trailing comma
with nothing after it).
**Fix:** Add the specific episode number, air date, and a direct URL to the episode.

---

### m3 — AI-generated artifact comments in bib entries
**File:** `references.bib`, entries `fastapi` and `vuejs`
```bibtex
howpublished = {\url{https://fastapi.tiangolo.com/}} % official docs and site :contentReference[oaicite:0]{index=0}
howpublished = {\url{https://vuejs.org/}} % official site for Vue.js :contentReference[oaicite:1]{index=1}
```
The `:contentReference[oaicite:0]{index=0}` comments are artifacts from an AI-assisted
citation generation tool and should be removed before submission.
**Fix:** Delete the inline comments from both entries.

---

### m4 — Several `@misc` tool entries missing author/year/urldate
**File:** `references.bib` — entries for `python`, `uv`, `ruff`, `mypy`, `pytest`, `yaml`,
`pyyaml`, `scapy`, `precommit`, `git`, `iptables`, `nftables`, `podman`, `podman_compose`,
`curl`, `sudo`, `pip`, `click`
These entries are missing `author`, `year`, and `urldate` fields, which is acceptable for
software tools but will produce incomplete bibliography entries.
**Fix:** Add at minimum `year = {accessed year}` and `urldate = {2026-xx-xx}` to each.

---

### m5 — Bare `\ref{}` calls without surrounding text
**File:** `content/02-related-work.tex`, line 95
```latex
Further details of the frameworks are presented in the following sections.
\ref{subsec:atomic-red-team-evaluation}\ref{subsec:caldera-evaluation}\ref{subsec:metasploit-evalutaion}
```
Three bare `\ref{}` calls are placed inline with no labels, parentheses, or "See Section X"
language. They will render as raw section numbers in the PDF and look unfinished.
**Fix:** Rewrite as: "Further details are presented in Sections~\ref{...}, \ref{...},
and~\ref{...}."

---

### m6 — WEF bib key says 2025 but report is 2026 edition
**File:** `references.bib`, entry `WEF2025GlobalRisks`
The bib key suffix `2025` is inconsistent with `year = {2026}` and `title = {The Global
Risks Report 2026}`. The 21st edition was published in January 2026.
**Fix:** Either rename the key to `WEF2026GlobalRisks` (and update all `\cite{}` calls) or
clarify the year in the entry.

---

### m7 — `Figueredo2024RCVaR`: year mismatch
**File:** `references.bib`, entry `Figueredo2024RCVaR`
The entry has `year = {2023}` but the bib key suffix says `2024`.
**Fix:** Verify the actual publication year and align the key and field.

---

### m8 — `nsakRepository2026`: GitHub URL not verifiable
**File:** `references.bib`, entry `nsakRepository2026`
URL points to `https://github.com/nsak-team/nsak` which may not be a public repository.
Reviewers and plagiarism tools may flag an inaccessible or private URL.
**Fix:** Update to the actual public GitLab URL of the project, or add a note that the
repository is currently private.

---

## Plagiarism Risk Summary

| Risk | Count | Verdict |
|------|-------|---------|
| Verbatim copying without citation | 0 | None found |
| Verbatim / near-verbatim with citation but no quotation marks | 2 | C3, M5 — should be re-worded or quoted |
| Missing citation for original concept | 4 | M1, M2, M3, M4 |
| Empty citation placeholder | 1 | C1 — critical |
| Broken/incomplete text | 1 | C2 — critical |
| Bibliography metadata errors | 6+ | m1–m8 |

**Overall plagiarism risk: LOW.** The implementation chapters (5–8) are clearly original
work describing the authors' own design decisions, code, experiments, and results. The
background chapters (2–3) properly cite most claims. The issues above are quality problems
typical of a first submission draft, not intentional academic misconduct.

---

## Recommended Action Priority

1. **Before any external review / submission:**
   - Fix C1 (empty cite), C2 (broken sentence), C3 (MITRE verbatim)
   - Fix m3 (remove AI artifact comments from bib)

2. **Before final submission:**
   - Add M1 (chain-of-thought), M2 (RAG), M3 (tool calling), M4 (ReAct) citations
   - Fix M5 (rephrase MCP sentence), M6 (BIND citation), M7 (Containerlab cite)
   - Fix bibliography issues m1, m2, m4, m5, m6, m7, m8
