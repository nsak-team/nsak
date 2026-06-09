# Flaws & Corrections Assessment
**Date:** 2026-06-09
**Scope:** All content chapters/sub-files in `docs/thesis/documentation/content/`
(`abstract`, `01`–`08`, `05.1`–`05.5`, `06.1`–`06.2`) + cross-checks against
`references.bib`. This is a full read-through scan, complementary to
`plagiarism-citation-assessment.md` (citation issues are not repeated here).
**Assessor:** Claude Opus 4.8

---

## Overall

The argument and results are solid and the structure is sound. The problems are
almost entirely **mechanical**: a couple of genuine LaTeX/data bugs that must be
fixed before submission, one pervasive cross-referencing style issue that appears
dozens of times, a few number/model inconsistencies between chapters, and the usual
crop of grammar slips. Nothing indicates a content or methodology problem — these
are draft-polish items.

---

## Critical (must fix — render/compile or wrong data)

### F1 — Broken `\mintinline` delimiter swallows a whole sentence
**File:** `content/05.2-containerlab-environment.tex`, line 48
```
a file named \mintinline{bash}|{secret.txt} containing sensitive data is placed on the server.|
```
The verbatim region runs from the first `|` to the `|` at the **end of the sentence**,
so "containing sensitive data is placed on the server." is typeset as monospaced code,
and the `{ }` render literally.
**Fix:** `a file named \mintinline{bash}|secret.txt| containing sensitive data is placed on the server.`
**Also check (same file):** line 80 `\mintinline{bash}| {/jobs}|` (leading space + stray
braces) and line 81 `\mintinline{bash}|{/var/logs/printer_sim_logs}|` — the `{ }` are
almost certainly not wanted and will print verbatim.

### F2 — Token-cost figure contradicts itself
The BFH benchmark table gives the multi-agent mean as **116,738** tokens
(`content/06.2-ns-lab.tex`, line 19; repeated 06.2:57–58, and `07-discussion.tex`:49).
But `07-discussion.tex`, line 117 says:
```
roughly three times the token cost (222,094 vs.\ 81,453).
```
`81,453` appears nowhere else in the thesis.
**Fix:** Use one source of truth (the table). Replace `81,453` with `116,738`.

### F3 — "Three times" vs "100 % higher" — same ratio described two ways
222,094 vs 116,738 ≈ **1.9×** (~90 % more). The text variously calls this
"nearly three times" (`06.2`:57), "roughly three times" (`07`:49, `07`:117) and
"roughly 100\% higher" (`06.2`:58) — within a few lines of each other.
**Fix:** Standardize to "nearly twice" / "~90 % higher". Drop the "three times" wording
(it only fits the erroneous 81,453 value from F2).

### F4 — Incomplete sentence (unbalanced parenthesis)
**File:** `content/06.2-ns-lab.tex`, line 140
```
\textbf{Qwen3:8b} is not further assessed due to its low success rate, (close to 0\%.
```
Sentence is cut off and the `(` is never closed.
**Fix:** e.g. "… due to its low success rate (close to 0\%)."

### F5 — Incomplete sentence (missing reference/word)
**File:** `content/07-discussion.tex`, line 187
```
While partly implemented in  we discarded the branch,
```
Double space where a branch name / section reference was removed.
**Fix:** name the branch ("on branch 310") or rephrase. Compare with the parallel
(also awkward) sentence in `08-conclusion.tex`:56 "While partly implemented on branch
310 in the project, but rejected …" — drop either "While" or "but".

---

## Structural / Consistency

### S1 — Local model named `qwen3:30b` in methodology but `qwen3:8b` in the BFH results
Methodology defines the self-hosted model as **qwen3:30b**
(`04-methodology.tex`:14 and Table 04:61). The BFH lab evaluation and discussion use
**qwen3:8b** (`06.2`:19,110,140; `07`:50,118,129,165). `qwen3:8b` is never introduced.
**Fix:** Either state explicitly that a smaller `qwen3:8b` was used for the larger BFH
network (and why), or align the names. As written it reads like a typo.

### S2 — "3 environments / 120 measurements" never realized
`04-methodology.tex`:37 claims "3 models × 3 environments … yields 120 measurements".
Only **two** environments were evaluated; the physical environment was dropped
(acknowledged in `07`:144–148).
**Fix:** Soften the methodology sentence or add a forward reference to the limitation,
so the planned matrix and the executed matrix don't silently disagree.

### S3 — "four drills" but only three are listed
**File:** `content/05.4-reconnaissance-scenario.tex`, line 5
```
It chains four drills in sequence: host discovery, port scanning, and service enumeration.
```
Three are named (and elsewhere only `arp-scan, nmap` are mentioned, `06`:36).
**Fix:** Make the count match the list (the scenario has 3 drills:
discover-hosts, port-scan, enumerate-services).

### S4 — Garbled static-services count
**File:** `content/06.1-container-lab.tex`, line 260
```
The static scenario discovers all 13 (minus the 5 hosts) 8 \gls{LAN} services …
```
Reads as a mid-edit fragment.
**Fix:** Rephrase, e.g. "… discovers all 8 LAN services (the table lists 13 rows because
each host is also counted) …".

### S5 — `\todo{}` notes still in the body
Will render as visible margin notes (or break a non-todonotes build):
- `03-concepts.tex`:115 `\todo{warum braucht es den satz???}`
- `05.1-configuration-management.tex`:126 `\todo{PRESENT???? }`
- `07-discussion.tex`:17 `\todo{Allgemein … RQs habtcla}`
**Fix:** Resolve and delete all three before submission.

---

## Pervasive style issue (high count)

### P1 — Bare `~\ref{}` used as a noun reference (no "Section/Listing/Figure" word)
Appears **throughout** the thesis; it renders as a bare number, e.g.
"defined in the **1**", "the order of drills **3.1.3**". This is the same defect as
`m5` in the plagiarism notes, but far more widespread. Representative locations:
- `06-evaluation.tex`:5 `defined in the~\ref{ch:introduction}`, 06:7, 06:8, 06:11, 06:36
- `03-concepts.tex`:97 (two), `01-introduction.tex`:14
- `07-discussion.tex`:67, 212, 221
- `05.1-…`:5,6,71,102,105,108,113,118,129,139 (and the `\enquote{Project 2}\ref{…}` joins)
- `05.2-…`:5,28,34,62,72,81  ·  `05.3-…`:3,4,7,8,9,96  ·  `05.4-…`:21  ·  `05.5-…`:3
**Fix:** Prefix each with the referenced object and a non-breaking space, e.g.
`Section~\ref{…}`, `Listing~\ref{…}`, `Figure~\ref{…}`. A grep for `[a-z]~?\\ref{`
without a leading keyword finds them all.

### P2 — Adjacent `\ref` with no separator
- `05.2-…`:72 `…respective roles~\ref{…alice}\ref{…bob}` → add "and"/comma.
- `02-related-work.tex`:94 was fixed (m5); the same pattern remains in the `05.2`:90–99
  listing block and could read as "Listings~\ref…, \ref…, and~\ref…".

### P3 — Inconsistent capitalization of proper/model names
Mixed within prose: `containerlab` vs `Containerlab`; `qwen3` vs `Qwen3`;
`gpt-oss` vs `Gpt-oss`; `claude-opus-4-7` vs `Claude-opus-4-7` (e.g. `07`:20,29,42;
`06.1`:195; `06.2`:140). Sentence-initial casing of a lowercase model id looks
inconsistent.
**Fix:** Decide one convention (recommended: keep model ids verbatim/lowercase and
reword so they never start a sentence, or wrap in `\textit{}` consistently).

---

## Grammar / typos (representative, not exhaustive)

| File:line | Issue | Suggestion |
|-----------|-------|------------|
| `02`:153 | "and led limited success" | "and led **to** limited success" |
| `02`:188 | missing trailing period | add "." |
| `03`:146 | "Even tough" | "Even **though**" |
| `06`:53 | "could be even harmfully" | "could be even **harmful**" |
| `06.1`:124 | "allowing to compares the models" | "allowing **to compare**" |
| `06.1`:127 | stray "; " → "and \textit{gpt-oss:120b}; spreads" | remove the semicolon |
| `06.2`:44 | "due to the fact from its tendency" | "due to its tendency" |
| `07`:62 | "the AI frontier model extract" | "extract**s**" |
| `07`:150 | "where rated more critical" | "**were** rated" |
| `07`:215 | "teh operator" | "the operator" |
| `05.5`:53 | line begins with ", saves a Markdown…" | merge into previous clause |
| `08`:56 | "While … , but rejected" | drop "While" or "but" |

(There are more agreement/article slips of the same kind across `07` especially; a
dedicated language pass is advisable.)

---

## Minor / already tracked elsewhere

- **WEF citation key** `WEF2025GlobalRisks` still cited in `01`:7 although the report is
  the 2026 edition. Decision was to **leave the key as-is** (entry fields already say
  2026); noted here only for completeness.
- **Repository URL placeholder** `nsakRepository2026` →
  `https://github.com/nsak-team/nsak` (cited at `03`:23,37,45,55,144). Looks like a
  placeholder; replace with the real public URL. (= `m8` in the plagiarism notes.)
- **Bib chapter titles** `chapter1`/`chapter3` carry the placeholder "Define AI Agent"
  (`02`:183,188). Left untouched per your decision; confirm against the book.

---

## Suggested fix order
1. F1–F5 (bugs / broken text) — blocking.
2. S1–S5 (consistency + remove `\todo`s).
3. P1 (the bare-`\ref` sweep) — biggest visual-quality win; mechanical.
4. P2–P3, then the grammar pass.
