# NSAK Bachelor Thesis — Video Script (Drehbuch)

**Project:** NSAK – Network Swiss Army Knife
**Language:** English
**Target length:** ~88 seconds (5s BFH intro + 78s content + 5s BFH outro)
**Format:** Slides + screencasts (no live camera footage)
**Music:** Dark techno / Matrix-style ambient — starts at 0:05, fades at 0:83

---

## Format rationale

Slides and terminal screencasts are the right medium for this thesis:

- The subject is a CLI tool — showing it running is more compelling than talking heads
- Screen recordings are re-recordable, precisely timed, and lend a professional look
- The BFH instructions explicitly allow students not to appear on camera
- The overview → detail structure required by the BFH checklist maps directly onto:
  - **Totale** → full terminal window or overview slide
  - **Halbtotale** → zoomed-in command output
  - **Nahaufnahme** → AI finding or email report detail

---

## Sequence overview

| # | Time | Duration | Type | Audio |
|---|------|----------|------|-------|
| 0 | 0:00 – 0:05 | 5s | BFH Vorspann (provided by BFH) | — |
| 1 | 0:05 – 0:12 | 7s | Title slide | Music in |
| 2 | 0:12 – 0:28 | 16s | Problem slide | Voiceover |
| 3 | 0:28 – 0:68 | 40s | Screencast: AI workflow | Music only |
| 4 | 0:68 – 0:83 | 15s | Results slide | Voiceover |
| 5 | 0:83 – 0:88 | 5s | BFH Nachspann (provided by BFH) | Music fade |

---

## Detailed script

---

### Sequence 0 — BFH Vorspann `[0:00 – 0:05]`

> Provided by BFH. No action required.

---

### Sequence 1 — Title `[0:05 – 0:12]`

**Visual:**
Full-screen title slide with dark background.

```
[NSAK Lama logo — centered]

NSAK
Network Swiss Army Knife

Bachelor Thesis — BFH-TI 2026
```

**Audio:**
Music starts softly (dark techno / matrix ambient). No voiceover.

**Production notes:**
- Fade in from black over 0.5s
- Logo animation optional (simple fade-in)
- Music volume at ~40% here, rises to ~70% in sequence 3

---

### Sequence 2 — Problem statement `[0:12 – 0:28]`

**Visual:**
Slide with two-column layout:

```
LEFT COLUMN                          RIGHT COLUMN
─────────────────────────────────    ─────────────────────────────────
  [Icon: network/shield]               [Icon: robot/AI]

  Manual Implementation                Agentic AI

  • Deterministic                      • Adaptive
  • Reproducible                       • Human-in-the-loop
  • Domain expertise required          • Natural language interface

           3 LLMs  ×  3 Network Environments
```

Slide transitions: left column appears first, then right column, then bottom line.

**Voiceover (~16 seconds):**

> "Network penetration testing is complex and demands deep technical expertise.
> Can agentic AI automate security scenario execution — and how does it compare
> to a hand-crafted implementation?
> We evaluated three language models across three network environments."

**Audio:**
Music at ~30% under voiceover.

---

### Sequence 3 — Screencast: AI workflow `[0:28 – 0:68]`

**Visual:**
Split into four sub-shots edited together. No voiceover — music carries this section.

#### Sub-shot A — User input `[0:28 – 0:36]` (8s)

Terminal overview (Totale): full terminal window visible.
User types a scenario prompt into NSAK:

```
$ nsak scenario run ai-scenario --environment home-lab
> Starting AI-driven scenario...
> Model: claude-sonnet-4-6
```

**Cut note:** Hold on the full terminal for 2s, then slow zoom toward the command line.

---

#### Sub-shot B — AI reasoning + human-in-the-loop `[0:36 – 0:52]` (16s)

Mid-shot (Halbtotale): terminal scrolling, showing AI tool calls and the approval prompt.

```
[AI] Analyzing network topology...
[AI] Identified hosts: 192.168.1.1, 192.168.1.20, 192.168.1.45
[AI] Proposed next drill: port-scan on 192.168.1.20

? Approve drill execution? (yes/no) › yes

[DRILL] Running port-scan...
[DRILL] Open ports: 22/ssh, 80/http, 443/https, 8080/http-alt
[AI] Proceeding with service enumeration...
```

**Cut note:** Slight zoom-in on the approval prompt line to highlight human-in-the-loop moment.

---

#### Sub-shot C — Findings output `[0:52 – 0:60]` (8s)

Close-up (Nahaufnahme): zoomed in on the AI findings summary in the terminal.

```
══════════════════════════════════════
  FINDINGS SUMMARY
══════════════════════════════════════
  Critical : 1   (default SSH credentials)
  High     : 2   (outdated HTTP service, open admin panel)
  Medium   : 3
  Low      : 1
══════════════════════════════════════
```

---

#### Sub-shot D — Email report sent `[0:60 – 0:68]` (8s)

Close-up: terminal shows report generation and email disp	192.168.10.241atch, then cut to a brief preview of the generated HTML/PDF email report rendered in a mail client or browser.

```
[REPORT] Generating PDF report... 04_Text
[REPORT] Sending to vonlu3@gmail.com
[REPORT] Done. ✓
```

Brief cut to: rendered email/report in browser (2–3 seconds).

**Audio (all of sequence 3):**
Music at ~70%, no voiceover. Increase tempo feel of music at sub-shot B to match action.

---

### Sequence 4 — Results & conclusion `[0:68 – 0:83]`

**Visual:**
Split-screen slide:

```
LEFT                                RIGHT
───────────────────────────────     ───────────────────────────────
  AGENTIC AI                          IMPLEMENTATION

  ✓ Detailed natural-language         ✓ Deterministic & reproducible
    findings report                   ✓ Fast, no token cost
  ✓ Minimal technical expertise       ✓ Precise, auditable steps
    required                          ~ Findings require interpretation
  ~ Non-deterministic output
  ~ Dependent on model quality

     [Bar chart: finding coverage across 3 models × 3 environments]
```

Bottom of slide:

```
  "AI excels at exploration and reporting.
   Implementation excels at reliability and control."
```

**Voiceover (~15 seconds):**

> "The AI agent consistently produced detailed, human-readable security reports
> with minimal technical input required.
> The deterministic implementation delivered reliable, reproducible results.
> Together, they demonstrate that AI and rule-based automation are
> complementary — not competing — approaches to network security testing."

**Audio:**
Music fades from ~70% down to ~20% as voiceover ends.

---

### Sequence 5 — BFH Nachspann `[0:83 – 0:88]`

> Provided by BFH. No action required.
> Music fades to silence over the first 2 seconds of this sequence.

---

## Production checklist

| Item | Detail |
|------|--------|
| Screen resolution | 1920×1080 minimum for all screencasts |
| Terminal font size | 18–20pt — legible at video resolution |
| Terminal theme | Dark background, high-contrast text (e.g. Tokyo Night, Dracula) |
| Music track | Royalty-free: search "dark techno ambient no copyright" or use Pixabay/Freesound |
| Voiceover | Record in a quiet room; use a headset or directional mic |
| Voiceover timing | Record voiceover first, then edit visuals to match — easier than reverse |
| Slide tool | Any (Keynote, PowerPoint, or even terminal-rendered slides) — export as video or screen-capture |
| Video editor | DaVinci Resolve (free) or Kdenlive (Linux) recommended |
| Final export | MP4, H.264, 1920×1080, stereo audio |
| Filename convention | `nsak_bsc_video_2026.mp4` |
