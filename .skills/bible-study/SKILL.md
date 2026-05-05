---
name: bible-study
description: Convert a class/teaching-outline Word document (.docx) into a paired questions.md + study.md under studies/YYYY-MM-DD-<slug>/, with full-text scripture, Greek/Hebrew word studies, and Erik-voice personal application. Use whenever the user provides a .docx bible study outline (or asks to "produce a new study" from one) for this repo.
license: Proprietary — internal to Zettersten/bible-study
compatibility: Requires Python 3 (stdlib only) for docx parsing. Optional ESV_API_TOKEN for ESV passages; CSB passages are pulled via web_extract.
metadata:
  author: erik.zettersten
  version: "1.0"
  primary_translation: CSB
  framework: Reformed
---

# bible-study

Turn a class outline `.docx` into a fully-researched, voice-correct, gospel-anchored bible study under `studies/`.

## When to use

Trigger on **any** of:
- User attaches a `.docx` and asks for a "new study" / "produce a study" / "answers and questions."
- User pastes a class outline that looks like the Type B teaching format described in `CLAUDE.md` (anchor passages, `READ` tags, `Q.` prompts, "tune in next week …").
- User says "use the bible study skill / project."

## Required inputs

1. **A `.docx` file path.** Pasted text is *not* the supported entry point — bounce back and ask for the docx if not provided. Reasoning: the docx is the source of truth for the class; reformatted text loses the structure parser keys on (`READ <ref>`, blank-line separators, `Q.` prompts).
2. **Translation** (optional). Default **CSB**. User may override per run (ESV, NASB, etc.). If ESV, expect `ESV_API_TOKEN` in env; otherwise use `web_extract` against Bible Gateway.
3. **Date** (optional). Default to today (`YYYY-MM-DD`).

## Output contract

Two files under `studies/YYYY-MM-DD-<slug>/`:

- **`questions.md`** — the class outline reformatted in markdown. Full chapter (or all referenced passages) printed in full in the chosen translation. Original `READ` blocks preserved. Original `Q.` numbered. **No answers.**
- **`study.md`** — same questions, with the canonical four-part answer block under each (see `references/ANSWER_FORMAT.md`). All cross-referenced verses printed in full. Topical/teaching-outline structure preserved.

Plus:
- **README.md** — add a row to the Study Index table in the same commit.

> Filename note: this project standardized on `study.md` (not `answers.md`) — see `studies/2026-04-21-life-as-a-husband/`. Use `study.md` unless the user explicitly insists on `answers.md`.

## Workflow

### 1. Parse the docx

```bash
python3 .skills/bible-study/scripts/parse_docx.py "<path-to-docx>"
```

Emits JSON to stdout:

```json
{
  "topic": "Colossians 2",
  "intro": "...",
  "sections": [
    {"read": "Col 2:2-3", "questions": ["Why is God's plan mysterious?", "..."]},
    ...
  ],
  "closing": "Tune in next week – Colossians 3"
}
```

If the parser returns 0 sections or 0 questions, the docx is not in the expected outline shape — surface that to the user before proceeding, do not silently invent structure.

### 2. Choose study type

Almost all class docs are **Type B (topical / teaching outline)** in `CLAUDE.md` terms. Use `templates/topical-study-template.md` as the reference shape, but adapt: when the doc walks one chapter section-by-section (like Colossians 2), make the chapter itself the anchor and use the `READ` blocks as the natural section breaks.

### 3. Pull scripture in full

Default = **CSB** via `web_extract` against `https://www.biblegateway.com/passage/?search=<ref>&version=CSB`. See `references/TRANSLATIONS.md` for the exact retrieval pattern, ESV API path, and how to cope with rate limiting.

Print every verse in full — chapter passage, every cross-reference, every supporting verse cited in word studies. Bare references are a bug.

### 4. Build `questions.md`

Reformat the class outline in markdown:
- H1 with topic + "Study Input" suffix
- Topic, introduction context (pulled from the docx intro paragraph)
- Full passage printed under section headers matching the `READ` boundaries
- Each section ends with a blockquote of the original `Q.` prompts, numbered (Q1, Q2, …)
- Closing note ("Tune in next week …") if the docx had one

### 5. Build `study.md`

For each question, write the **four-part answer block** (see `references/ANSWER_FORMAT.md`):

1. **Answer** — Erik voice, 2–4 paragraphs. See `references/VOICE.md`.
2. **Biblical Support** — 2–4 verses, **printed in full**, with reference and translation tag.
3. **Word Studies** — 1–3 entries. Greek/Hebrew root, original script, transliteration, gloss, theological payload. See `references/WORD_STUDIES.md`.
4. **Personal Application** — One concrete, specific action this week. Name Erin and the kids by name where it fits. No platitudes.

Add the standard envelope sections from `templates/topical-study-template.md`: Intro, Core Passages, Anchor Text, Context & Theological Grounding (compact), Cross-References, Simple Summary, Personal Reflection Questions, Notes.

### 6. Update README.md

Add one row to the **Study Index** table:

```
| YYYY-MM-DD | [Title](studies/YYYY-MM-DD-<slug>/) | ✓ Complete | One-line summary |
```

### 7. Verify before commit

Run through `references/ANSWER_FORMAT.md` checklist:

- [ ] All verses (everywhere in either file) printed in full — no bare references.
- [ ] Each answer has all four parts in the correct order.
- [ ] Word studies include both original script and transliteration.
- [ ] Personal applications are concrete (specific action, often this-week-scoped).
- [ ] README Study Index updated.
- [ ] Translation tag (CSB/ESV) consistent across both files.

### 8. Commit & push

```bash
git add README.md studies/YYYY-MM-DD-<slug>/
git commit -m "Add <topic> study"
git push origin main
```

If the user said "commit and push when done," do it. If not, ask first.

## Voice & framework (quick rules — full detail in references/VOICE.md)

- **Reformed**, gospel-anchored. Indicatives before imperatives. No moralism.
- **Plainspoken engineer**. Skeptical of frameworks dressed as wisdom. Comfortable naming current cultural counterfeits (therapeutic deism, prosperity gospel, scientism, AI-as-oracle).
- **Family-grounded**. Erin (wife) and the kids appear in personal applications by name where fitting.
- **No academic paragraphs**. Punchy, pastoral, direct.

## Anti-patterns

- ❌ Inventing questions the docx didn't ask. Parse, don't paraphrase the structure.
- ❌ Bare verse references. Every one in full.
- ❌ Generic application ("pray more, read your Bible"). Concrete or it doesn't ship.
- ❌ Word studies that just transliterate without payload — the *theological why* is mandatory.
- ❌ Treating Type B teaching outlines like Type A exegetical studies — voice flattens, structure breaks.
- ❌ Updating CLAUDE.md or templates when the user only asked for a new study. Scope discipline.

## Reference files

- `references/ANSWER_FORMAT.md` — canonical four-part answer block, with full example.
- `references/VOICE.md` — Erik-voice rules with do/don't pairs.
- `references/WORD_STUDIES.md` — how to choose words and format the entry.
- `references/TRANSLATIONS.md` — CSB and ESV retrieval, with fallbacks.

## Scripts

- `scripts/parse_docx.py` — stdlib-only docx → JSON outline.
