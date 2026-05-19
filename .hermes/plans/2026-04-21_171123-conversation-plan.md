# Plan: `bible-study` Skill + Repo Refactor

## Goal

Build a first-class Hermes skill named `bible-study` that, when invoked with a
passage or topic, orchestrates research → personalization → writing and emits
**two** well-formatted Markdown documents for Erik Zettersten:

1. `study.md` — the clean study (questions, no answers)
2. `study-answered.md` — same study, with full answers in Erik's voice

The skill owns the entire workflow currently described inline in `CLAUDE.md`.
The repo is refactored so `CLAUDE.md` becomes a thin pointer that loads the
skill, and `README.md` documents invocation.

## Current context / assumptions

- Repo already has two templates (exegetical + topical) — the skill will
  reuse and render them, not replace them.
- Erik's primary translation is ESV. Full-text ESV requires api.esv.org
  (free token, required by copyright). No API key → skill prompts user
  to set `ESV_API_TOKEN` once.
- Erik's voice is not captured anywhere yet — the skill needs a
  `voice.md` sample file (written by Erik, or bootstrapped from this session)
  so personal applications don't sound generic.
- Personal profile (family, birthdays, etc.) is sensitive and should live
  in the **repo**, not the shared skill directory — so it stays under
  Erik's control and is gitignored.
- Skill conventions: `skill_manage(action='create')` puts the skill at
  `~/.hermes/skills/<category>/bible-study/` with `SKILL.md` + optional
  `references/`, `templates/`, `scripts/`, `assets/` subdirs.

## Proposed architecture

```
┌─ user: "/bible-study Proverbs 18:22, 15:1, 31:11-12 on being a husband" ─┐
│                                                                          │
│  Skill loads SKILL.md → orchestrator pattern                             │
│                                                                          │
│  Phase 1 — PARSE                                                         │
│    • classify Type A (exegetical) vs Type B (topical)                    │
│    • extract references, themes, questions                               │
│                                                                          │
│  Phase 2 — CONTEXT (parallel sub-agents via delegate_task)               │
│    ├─ profile_agent   → scripts/ensure_profile.py (Erik + family)        │
│    ├─ verses_agent    → scripts/fetch_verses.py  (ESV full text +        │
│    │                       1–2 correlating verses per reference)         │
│    ├─ history_agent   → historical / geopolitical / cultural context     │
│    └─ words_agent     → 1–2 Greek/Hebrew word studies per question       │
│                                                                          │
│  Phase 3 — WRITE                                                         │
│    • render study.md           (clean, questions only)                   │
│    • render study-answered.md  (answers in Erik's voice + verses +       │
│                                 word study + personal application)       │
│    • update README.md Study Index                                        │
│                                                                          │
│  Phase 4 — REPORT                                                        │
│    • print folder path, missing-profile gaps, any ESV-API fallbacks      │
└──────────────────────────────────────────────────────────────────────────┘
```

## Skill layout (to be created via `skill_manage`)

```
~/.hermes/skills/personal/bible-study/
├── SKILL.md                     # Orchestration instructions (main entry)
├── references/
│   ├── study-types.md           # Type A vs Type B classifier + signals
│   ├── voice-guide.md           # How to write in Erik's voice (rules)
│   ├── reformed-framework.md    # Theological guardrails (short)
│   ├── word-study-howto.md      # Strong's / lemma lookup conventions
│   └── output-contract.md       # Exact required sections in each .md
├── templates/
│   ├── study-exegetical.md      # Type A (mirrors repo template)
│   ├── study-topical.md         # Type B (mirrors repo template)
│   └── study-answered-addendum.md  # How answers are layered in
├── scripts/
│   ├── ensure_profile.py        # Load/update profile.yaml; web-search gaps
│   ├── fetch_verses.py          # ESV API → full text JSON
│   ├── fetch_correlates.py      # Given a verse, return 1–2 thematic parallels
│   └── word_study.py            # Ref + keyword → Strong's / Greek / Hebrew
└── assets/
    └── example-study/           # One worked example as reference
        ├── study.md
        └── study-answered.md
```

## Repo layout after refactor

```
bible-study/
├── README.md                    # Invocation docs (updated)
├── CLAUDE.md                    # Thin pointer: "load bible-study skill"
├── AGENTS.md                    # Same pointer for non-Claude agents
├── .gitignore                   # Adds profile.yaml, .bible-study/
├── profile.yaml                 # Erik's personal profile (gitignored)
├── voice.md                     # Erik's voice samples (gitignored or tracked)
├── templates/                   # Kept for reference / direct editing
│   ├── study-template.md
│   └── topical-study-template.md
└── studies/
    └── YYYY-MM-DD-topic/
        ├── questions.md
        ├── study.md             # NEW: clean version
        ├── study-answered.md    # NEW: answers-included version
        └── notes.md             # Optional, user-written
```

## Output contract (enforced by `references/output-contract.md`)

Every study must satisfy:

1. **Every verse reference quoted in full (ESV).**
2. **Every verse reference followed by 1–2 correlating verses, also in full.**
3. **In `study-answered.md`, every question answered with the four-part block:**
   - Erik-voice answer (2–5 sentences, first person, direct, pastoral,
     no sermonizing, no exclamation-point stacking, no "my friend" filler)
   - Supporting Bible verses (refs + full text)
   - Word study (1–2 Greek or Hebrew terms, with transliteration + gloss)
   - Personal application to Erik (concrete, mentions real family/life detail
     from `profile.yaml` when it fits — e.g., wife's name, kids, location —
     without forcing it)
4. **Simple Summary** line on Type B studies (daily posture, one sentence).
5. **Reformed-framework** guardrail: no Arminian free-will framing on disputed
   passages; gospel-centered, not moralistic.

## Sub-agent delegation plan

Using `delegate_task` batch mode (parallel) once Phase 1 is done:

| Agent | Toolsets | Responsibility |
|-------|----------|----------------|
| profile_agent | terminal, web, file | Run `ensure_profile.py`, report gaps |
| verses_agent | terminal, web | Run `fetch_verses.py` for all refs |
| history_agent | web | Historical / geopolitical / cultural notes |
| words_agent | web, terminal | Greek/Hebrew word studies (1–2 per Q) |

Main agent synthesizes and writes the two markdown files. No sub-agent writes
output files directly — they return structured summaries to the orchestrator.

## Scripts — responsibilities

### `scripts/ensure_profile.py`
- Reads `./profile.yaml` from the active repo (creates if missing).
- Schema: `name, age, location, marital_status, spouse:{name,age,birthday},
  children:[{name,age,birthday}], occupation, church, interests`.
- For missing fields: `web_search` Erik's name + corroborating terms; fill
  only high-confidence matches; never invent.
- Prints a JSON report of `found`, `filled_from_web`, `still_missing`.
- Main agent then asks Erik for `still_missing` fields interactively.

### `scripts/fetch_verses.py`
- Input: list of references (`["Proverbs 18:22", "1 Peter 3:7", ...]`).
- Uses `ESV_API_TOKEN` → `api.esv.org/v3/passage/text/`.
- Fallback (no token): emit a clear `MISSING_TOKEN` error with install hint;
  the orchestrator then asks Erik for the token and caches it in
  `~/.hermes/secrets/esv.token` (or env).
- Output: `{reference: {text, copyright}}` JSON.

### `scripts/fetch_correlates.py`
- Input: one reference + one theme keyword.
- Uses a curated thematic index first (`references/correlates.json` — a
  hand-rolled map for top ~200 popular refs), falls back to `web_search` +
  `fetch_verses.py` for the top 2 results.
- Output: 1–2 correlating refs with full ESV text.

### `scripts/word_study.py`
- Input: reference + English word.
- Strategy: scrape biblehub.com/lexicon (or STEP Bible open API if
  available) → Strong's number → lemma, transliteration, short gloss.
- Output: `{word, lang, lemma, translit, gloss, strongs}`.

## SKILL.md — what it contains

- **Trigger**: "when Erik gives a passage, topic, or pasted teaching outline
  for bible study".
- **Inputs / outputs** (the contract above).
- **Orchestration steps** (Phases 1–4), referencing the scripts and
  references by path.
- **Voice rules** (pointer to `references/voice-guide.md`).
- **Pitfalls** section:
  - Do not flatten Type B numbered points into prose.
  - Do not fabricate family details — if `profile.yaml` is thin, ask Erik.
  - Do not skip full-text verses to save tokens.
  - Do not moralize — ground every application in the gospel.
  - Copyright: ESV text must come from the API, never pasted from training
    data; always include the `copyright` string the API returns.
- **Verification**: after writing, the skill re-opens both `.md` files and
  checks: every `REF:` reference has quoted text; every question has the
  four-part answer block; Simple Summary exists on Type B.

## Repo refactor — exact edits

1. **Create skill** via `skill_manage(action='create', name='bible-study',
   category='personal', content=<SKILL.md body>)`.
2. **Add supporting files** via `skill_manage(action='write_file', ...)` for
   each `references/*`, `templates/*`, `scripts/*`, and `assets/example-study/*`.
3. **Rewrite `CLAUDE.md`** to a thin pointer (~20 lines):
   > "For any bible study request, load the `personal/bible-study` skill
   > and follow its SKILL.md. Primary translation: ESV. Framework: Reformed.
   > Subject: Erik Zettersten (see `profile.yaml`)."
4. **Add `AGENTS.md`** mirroring CLAUDE.md so non-Claude Hermes agents see
   the same pointer.
5. **Update `README.md`**:
   - New "Invocation" section with exact commands
     (`/bible-study <topic>`, paste-outline workflow, etc.)
   - Prerequisites (ESV_API_TOKEN, profile.yaml bootstrap)
   - Output shape (questions.md + study.md + study-answered.md)
   - Brief skill overview + link to `~/.hermes/skills/personal/bible-study/`
6. **Update `.gitignore`** to exclude `profile.yaml` and any cached secrets.
7. **Bootstrap `profile.yaml.example`** (tracked) so a fresh clone knows
   the schema.

## Files likely to change

Created:
- `~/.hermes/skills/personal/bible-study/SKILL.md`
- `~/.hermes/skills/personal/bible-study/references/*.md` (5 files)
- `~/.hermes/skills/personal/bible-study/templates/*.md` (3 files)
- `~/.hermes/skills/personal/bible-study/scripts/*.py` (4 files)
- `~/.hermes/skills/personal/bible-study/assets/example-study/*.md` (2 files)
- `bible-study/AGENTS.md`
- `bible-study/profile.yaml.example`

Modified:
- `bible-study/CLAUDE.md` (rewritten as pointer)
- `bible-study/README.md` (invocation + skill docs)
- `bible-study/.gitignore` (add profile.yaml, secrets cache)

Possibly retired (kept for now, re-evaluated after first run):
- `bible-study/templates/study-template.md`
- `bible-study/templates/topical-study-template.md`
  (the skill templates become canonical; repo copies become reference-only)

## Validation / tests

- **Dry-run on tonight's study** ("Life as a Husband", Prov 18:22 / 15:1 /
  31:11–12 / 1 Pet 3:7) and confirm:
  - Correct Type B classification
  - All 4 refs fetched with full ESV text + 2 correlates each
  - All 10 numbered points preserved (not flattened)
  - `study-answered.md` has 4-part answer block on each question
  - Simple Summary present
- **Missing-profile path**: temporarily rename `profile.yaml`, confirm skill
  asks Erik for gaps instead of fabricating.
- **Missing-token path**: unset `ESV_API_TOKEN`, confirm skill errors
  cleanly and prompts for it.
- **Voice check**: spot-read 2–3 personal applications — do they sound like
  Erik (direct, dry, no sermon voice) or like a generic devotional?

## Risks, tradeoffs, open questions

1. **ESV API token** — requires a free signup at crossway.org/api. Is Erik
   okay setting this up once? Without it we cannot legally reproduce ESV
   text; WEB/KJV fallback changes the study's translation.
2. **Erik's voice sample** — the quality of personal applications is bounded
   by how much voice data we feed the skill. Open question: does Erik want
   to paste 3–5 paragraphs of his own writing into `voice.md` as ground
   truth, or have the skill bootstrap from our session history?
3. **Word study source** — biblehub.com scraping is fragile; STEP Bible has
   a proper API but limited coverage. Tradeoff: scrape for breadth vs. use
   STEP for reliability. Proposal: STEP first, biblehub fallback.
4. **Personal profile in git** — recommending `profile.yaml` be gitignored.
   If Erik wants it tracked (e.g., private repo), we flip one line.
5. **Skill location** — `personal/bible-study` vs top-level. `personal/`
   signals "Erik-specific" which matches the brief; happy to change if
   Erik prefers `research/` or a new category.
6. **Answered vs clean as separate files** — confirmed by spec. Alt would be
   a single file with collapsible sections, but two files are simpler for
   printing / group handouts.

## Open questions for Erik before execution

1. ESV API token — will you create one, or should the skill fall back to
   WEB/KJV and call that out explicitly in each study?
2. Voice sample — paste some of your own writing into `voice.md`, or let the
   skill infer your voice from this conversation?
3. `profile.yaml` — gitignored (my default) or tracked?
4. Skill category — `personal/bible-study` okay, or somewhere else?
5. Keep the two repo templates as reference copies, or retire them once the
   skill-internal ones become canonical?

---

Saved plan: `.hermes/plans/2026-04-21_171123-conversation-plan.md`
