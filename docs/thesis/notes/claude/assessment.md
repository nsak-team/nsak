# Thesis Assessment — NSAK as Framework for Scenario Based Network Security

**Authors:** Frank Gauss (gausf1), Lukas von Allmen (vonal3)
**Advisor:** Wenger Hansjürg
**Assessed by:** Claude (claude-sonnet-4-6), 2026-06-11
**Basis:** thesis.pdf (v1.0 June 11, 2026), assignment gauss_vonallmen-signed.pdf, instructions_book.pdf

---

## Overall Impression

The thesis is substantive and well-structured. All mandatory ("must") project goals from Appendix A are addressed, three research questions are stated and answered, and a genuine implementation plus benchmark suite is delivered. The core scientific weakness is the gap between the planned methodology (three environments, n=10 runs each) and what was actually executed, combined with an explicitly incomplete qualitative evaluation for the BFH lab environment.

---

## HIGH — Could cause failure of the bachelor thesis module

### H1 — BFH lab qualitative evaluation is explicitly stated as incomplete
**Location:** Section 6.3.2, p. 52
Section 6.3.2 ("Qualitative Criteria") opens with: *"The qualitative findings are not evaluated in detail here, because the BFH Network Security Lab is still in use."* The evaluation chapter then proceeds with only a three-row table covering correctness/hallucination and four sentences of discussion.

RQ3 ("To what extent is the implementation suitable for deployment in real-world environments?") depends directly on this section. Evaluation goal A.4.1 ("AI Scenario Evaluation — must") requires a complete assessment across both environments. An examiner who checks the evaluation chapter against the methodology will find an openly acknowledged gap in a mandatory deliverable.

**Action:** Either complete the qualitative scoring and discussion now that the lab period has ended, or — if lab access truly prevents it — explicitly reclassify the BFH evaluation as "quantitative only" from the start of Chapter 6 and adjust the RQ3 answer accordingly so it does not over-claim on data you do not have.

---

### H2 — Physical environment planned in methodology but entirely absent from evaluation
**Location:** Section 4.1.2, p. 20 and Section 7.5, p. 58
The methodology chapter lists three environments: (1) virtual Containerlab, (2) physical environment, (3) BFH Cyber Lab. The evaluation covers only environments 1 and 3. Section 7.5 acknowledges this as *"Incomplete environment and scenario matrix"* but frames it as a limitation rather than correcting the methodology chapter.

A thesis that proposes a three-environment study and executes a two-environment study has a structural inconsistency between Chapters 4 and 6. Examiners checking completeness against the methodology will notice this immediately.

**Action:** Either (a) retroactively remove the physical environment from Section 4.1.2 and state the scope reduction explicitly in the methodology, not only in the limitations, or (b) add even a brief physical-hardware run of the static reference scenario (which requires no API quota) to close the gap.

---

### H3 — n=10 run methodology not achieved in BFH lab; conclusions drawn from 5 data points
**Location:** Section 4.1.1 (methodology), Table 6.6 and Section 6.3, p. 49–53
The evaluation methodology states n=10 runs per model per environment. For the BFH lab, the multi-agent structured variant achieved only 5/27 successful runs; the unstructured variant 6/109. The thesis reports averages over those 5 and 6 runs respectively. The discussion in Chapter 7.3 draws conclusions about real-world suitability and structured vs. unstructured output trade-offs from this data.

Drawing comparative conclusions from 5 vs. 6 data points while the stated methodology is n=10 is methodologically weak. A footnote on p. 53 argues the 6/109 rate is "largely an infrastructure artifact," but using that argument to then proceed with full conclusions is circular: if the data is unreliable due to infrastructure, the conclusions derived from it are equally unreliable.

**Action:** Either cap conclusions drawn from the BFH lab at a descriptive level only (*"these 5 runs suggest…"*) or acknowledge upfront in Chapter 6 that the BFH lab analysis is exploratory/preliminary rather than confirmatory. Adjust the RQ3 answer in 7.7 accordingly.

---

## MEDIUM — Likely to significantly impact the grade

### M1 — LangChain chosen without comparing alternatives
**Location:** Section 5.3.1, p. 30
The text states: *"The project team chose LangChain as the agentic framework without comparing it with alternative solutions."* For a research thesis with a framework comparison chapter, omitting the same rigor for the core technical choice is conspicuous. Alternatives like CrewAI, AutoGen, or the Anthropic Agent SDK exist and are widely cited. The four bullet-point justification (free, Python, reputation, documentation) is informal, not scientific.

**Action:** Add a brief table or paragraph comparing LangChain to at least one alternative (e.g., CrewAI or AutoGen) on the criteria that matter for this use case (tool calling support, multi-agent orchestration, local model compatibility). One paragraph in Section 5.3.1 or 2.2.3 would suffice.

---

### M2 — Prompt optimization biases the evaluation against larger models
**Location:** Section 5.3.10, p. 38
The prompts were iteratively improved during testing primarily against qwen3:30b (*"the smallest model to be used"*). The thesis acknowledges: *"the prompts were implicitly optimized for this model"* and notes that *"larger models might have yielded worse results"* with the current prompts. This means the evaluation is systematically tilted in favour of qwen3:30b and against claude-opus and gpt-oss:120b.

This is a material threat to internal validity. The quantitative and qualitative comparisons in Chapter 6 cannot be cleanly attributed to model capability when prompt engineering introduces a confound.

**Action:** Elevate this from a brief parenthetical in 5.3.10 to a dedicated paragraph in the limitations section (7.5) quantifying the potential bias. Optionally run one additional set of 10 Containerlab runs with a prompt tuned for claude-opus as a sensitivity check — even if out of scope, acknowledging that this check was not done strengthens the honesty of the limitation.

---

### M3 — Qualitative scoring lacks inter-rater reliability
**Location:** Section 7.5, p. 58
The thesis acknowledges: *"the scoring involves human judgement and is not independently inter-rated."* Correctness and hallucination scores in Tables 6.4 and 6.7 are the primary qualitative evidence for the research questions. Single-rater ordinal scores without any reliability check are a known weakness in qualitative evaluation methodology.

**Action:** Have the second author independently score at least two or three benchmark reports per model and report Cohen's kappa or a simple agreement percentage. Even modest inter-rater agreement data (e.g., "we independently scored 3 runs each and agreed on 5/6 scores") would meaningfully strengthen the methodology.

---

### M4 — Blue-team intrusion detection scenario evaluated only as proof of concept
**Location:** Sections 5.3.9 and A.3.4
Goal A.3.4 "Intrusion Detection — Blue Team" is marked "should." The thesis implements it as a proof of concept but explicitly states: *"has not been finalized, since the corresponding goal is categorized as 'Should'."* This is disclosed and acceptable, but the scenario is mentioned in the abstract's index terms ("AI-Driven Cybersecurity") and in the contributions list of Chapter 5 without a matching evaluation.

**Action:** Either include a brief evaluation of the intrusion detection scenario (even a single manually assessed run) to give it scientific substance, or remove it from the contributions listed in Chapter 5's introduction paragraph and make it clear it is out of scope.

---

### M5 — Comparison between structured vs. unstructured output in BFH lab is based on incomparable sample sizes
**Location:** Sections 6.3 and 7.3, p. 49–56
The discussion in 7.3 draws a direct trade-off conclusion: structured multi-agent is faster and cheaper, unstructured achieves higher correctness (9 vs. 7). This comparison is between 5 structured runs and 6 unstructured runs, which is already low, but additionally the 6/109 unstructured figure is distorted by the API quota event. The comparison is therefore between two datasets of different provenance and reliability.

**Action:** State explicitly in Section 6.3 that the structured vs. unstructured comparison in the BFH lab is indicative only, and that the correctness difference (7 vs. 9) should not be interpreted as a reliable finding without a proper sample. Soften the conclusion in 7.3 accordingly.

---

### M6 — The section header "MCP" in the body does not match the TOC entry "Model Context Protocol (MCP)"
**Location:** Section 2.2.2, p. 7 and TOC p. iii
Minor structural inconsistency but signals insufficient final proofreading pass.

---

### M7 — "ressources" typo in Figure 3.3 label
**Location:** Figure 3.3, p. 12
The C4 component diagram contains the label "ressources" (should be "resources"). Figures are high-visibility items in a thesis.

---

## LOW — Cosmetics

### L1 — "Comma Seperated Values" typo
**Location:** Section 5.3.9, p. 38
"Seperated" should be "Separated."

### L2 — Subject-verb agreement: "Zilberman et al. recommends"
**Location:** Section 2.1.1, p. 5
Should be "Zilberman et al. recommend" (plural subject).

### L3 — Inconsistent spelling conventions (British/American mix)
**Location:** Various
"parameterise" (British) appears alongside "analyze" (American). Pick one convention and apply it consistently throughout. The thesis otherwise reads as American English.

### L4 — Figure caption punctuation inconsistency
**Location:** Various figures
Some figure captions end with a period, others do not. Standard practice is to either always include or always omit — pick one.

### L5 — "It's ability" vs "Its ability"
**Location:** Section 3.2.4, p. 16 (Containerlab advantages bullet)
"It's ability to create a reproducible…" should be "Its ability to create…"

### L6 — Dangling hyperlinks to YouTube / LangChain documentation
**Location:** Section 5.3.3, p. 34
The text references "LangChain UI tutorial" and "LangChain Agent Chat UI" as live hyperlinks. External URLs can rot; if these are cited as sources they should appear in the bibliography. If they are just informational references, rephrase to avoid hyperlinking to a tutorial video in a scientific document.

### L7 — Section 6.3.1 figure description cut off mid-sentence
**Location:** p. 50, end of page
"The" at the bottom of page 50 is followed by nothing — the sentence appears to be cut off in the flow between pages (possible LaTeX pagination artifact). Verify the sentence concludes correctly at the top of p. 51.

### L8 — "Comma Separated" used in two slightly different phrasings
**Location:** Sections 5.3.9 and elsewhere
Minor — check for consistent abbreviation: "CSV" is introduced but "Comma Seperated Values" (already flagged as L1) spells it out inconsistently.

### L9 — Personal section contains colloquial language
**Location:** Section 8.1 (Personal Section), p. 61
Phrases like *"just another thing"* (italicized) and *"rookie mistake"* are informal for a scientific document. Some BFH examiners consider the personal section separate and hold it to a different standard; confirm with your advisor whether this language is acceptable.

---

## Summary Counts

| Category | Count |
|----------|-------|
| HIGH     | 3     |
| MEDIUM   | 7     |
| LOW      | 9     |
