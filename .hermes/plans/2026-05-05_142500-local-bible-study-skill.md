# Plan — Local `bible-study` Skill (in-repo, agentskills.io spec)

## Goal

Create an in-repo skill that captures the exact workflow used to convert the Colossians 2 class outline (a `.docx` Word doc) into a `questions.md` + `study.md` pair under `studies/YYYY-MM-DD-<slug>/`. Future runs of `/skill bible-study` (or any agent that reads `.skills/`) should produce the same caliber of output without me having to re-derive the steps.

## Context / Assumptions

- Repo: `~/Projects/bible-study/` (git remote `Zettersten/bible-study` on GitHub).
- Existing artifacts that the skill must respect:
  - `CLAUDE.md` — project-level instructions (Reformed framework, study types A/B, Erik-voice answer format).
  - `templates/study-template.md` and `templates/topical-study-template.md` — existing templates.
  - `studies/2026-04-21-life-as-a-husband/` and `studies/2026-05-05-colossians-2-christ-sufficient/` — reference studies showing the canonical output shape.
- `bible-study/` empty nested dir with its own `.git` is orphan scaffolding from an earlier abandoned attempt — leave alone.
- Translation: default to **CSB** going forward (matches user's most recent invocation and how the chapter was published in the latest study). `CLAUDE.md` still says ESV; the skill notes this and treats translation as a per-run override.
- Required input is **a `.docx` Word document**. Pasted text is *not* the supported entry point — the skill is built around docx parsing.

## Audit findings

| Concern | Status | Action |
|---|---|---|
| Skill file location convention | Prior session settled on `bible-study/.skills/bible-study/` (tracked, in-repo). Per agentskills.io v1, the parent dir name must equal `name`. | Use `.skills/bible-study/` at repo root. |
| Spec compliance | agentskills.io v1: SKILL.md with YAML frontmatter (`name`, `description` required); optional `scripts/`, `references/`, `assets/`. SKILL.md ≤ ~500 lines; offload depth to `references/`. | Honor — keep SKILL.md tight, push voice/word-study/answer-format depth into references. |
| docx parsing | Earlier ad-hoc attempt used `unzip -p word/document.xml | python3 -c …`. Brittle and gets flagged by the security scanner. | Ship a real `scripts/parse_docx.py` (stdlib only, zipfile + xml.etree). |
| Translation source | User confirmed CSB; no API key for CSB. ESV API token (`ESV_API_TOKEN`) was previously discussed for ESV. | For CSB, use Bible Gateway / Bible.com extraction via `web_extract` (no API). For ESV, optional `ESV_API_TOKEN`. Document both paths in references. |
| README index update | Manually maintained today. | Skill step explicitly includes README index update — already done for Col 2, document the rule. |
| File naming | Existing studies use `study.md` (not `answers.md`). User asked for "answers.md" in the request, but the project convention is `study.md`. | Skill produces `study.md` (matches existing studies); note in references that `answers.md` is an acceptable alias if the user explicitly asks for it. |

## Design contracts (UX/feel layer)

These are required behaviors the skill must encode, not nice-to-haves:

- Every verse referenced anywhere in either output file is printed in full CSB (or chosen translation), never bare reference.
- Each answer block has the four parts in this order: **Answer (Erik voice) → Biblical Support (full-text verses) → Word Studies (Greek/Hebrew, with original script + transliteration) → Personal Application (concrete, names Erin/kids when fitting)**.
- Erik voice: Reformed, gospel-anchored, plainspoken, engineer-skeptical-of-frameworks. Not academic-paragraph mode.
- Topical/teaching outlines preserve the user's structure — same number of points, same numbered ordering, same pithy takeaway lines.
- README index gets updated in the same commit as the new study.

## Proposed structure

```
.skills/bible-study/
├── SKILL.md                          # YAML frontmatter + tight workflow
├── scripts/
│   └── parse_docx.py                 # stdlib docx → structured outline (JSON to stdout)
├── references/
│   ├── ANSWER_FORMAT.md              # canonical 4-part answer block, deep
│   ├── VOICE.md                      # Erik-voice rules (with examples)
│   ├── WORD_STUDIES.md               # how to pick & format Greek/Hebrew studies
│   └── TRANSLATIONS.md               # CSB (web_extract) and ESV (api.esv.org) paths
└── assets/
    └── (templates already live in /templates — reference, do not duplicate)
```

## Step-by-step execution

1. Create `.skills/bible-study/` directory tree.
2. Write `SKILL.md` (frontmatter: `name: bible-study`, description specifying docx as required input, compatibility note, allowed-tools left off).
3. Write `scripts/parse_docx.py` (stdlib only; emits JSON: topic, intro, sections[], where each section has a `read_passage` and ordered `questions[]`).
4. Write `references/ANSWER_FORMAT.md`, `references/VOICE.md`, `references/WORD_STUDIES.md`, `references/TRANSLATIONS.md`.
5. Patch `CLAUDE.md` so it points at the skill as the canonical workflow (don't duplicate detail; redirect).
6. Patch `README.md` Project Structure block to include `.skills/`.
7. Smoke-validate `parse_docx.py` against `~/Downloads/Colossians 2class.docx` to confirm it produces the structured outline this session worked from.
8. `git add` skill + doc updates → commit → push.

## Files likely to change

- **NEW**: `.skills/bible-study/SKILL.md`
- **NEW**: `.skills/bible-study/scripts/parse_docx.py`
- **NEW**: `.skills/bible-study/references/{ANSWER_FORMAT,VOICE,WORD_STUDIES,TRANSLATIONS}.md`
- **MODIFIED**: `CLAUDE.md` (point at skill)
- **MODIFIED**: `README.md` (add `.skills/` to project structure)

## Validation

- `python3 .skills/bible-study/scripts/parse_docx.py "~/Downloads/Colossians 2class.docx"` returns a JSON object with `topic`, `intro`, and 5 sections containing 6 questions total, matching what was hand-extracted this session.
- `SKILL.md` parses as valid YAML frontmatter + Markdown body.
- `name` field equals parent dir name (`bible-study`) and matches all spec constraints.

## Risks & open questions

- **Risk**: The skill name `bible-study` collides with the repo name. Acceptable — agentskills.io only requires the *skill dir name* to match the `name` field, not anything else. The skill dir is `.skills/bible-study/`, distinct from the repo root.
- **Open**: `CLAUDE.md` says ESV; latest study uses CSB. The skill defaults to CSB and treats translation as per-run override, but `CLAUDE.md` still says ESV in two spots. I'll patch the "Primary Translation" line to `CSB (override per-study)` rather than scrub all ESV references — preserves history of older studies and avoids invalidating the existing checklist.
- **Open**: Should `.skills/` be added to `.gitignore` exclusions or tracked? Tracked — the whole point is in-repo discoverability for future agents and humans.
