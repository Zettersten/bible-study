# bible-study

A structured directory for AI-assisted bible study homework using Claude Code and Hermes.

## Purpose

This project provides a consistent workflow for comprehensive bible study. Paste your study questions, and the AI will research scripture, provide theological commentary, cross-references, and practical applications—all formatted as markdown in organized study folders.

## Quick Start

1. Open this directory in Claude Code or Hermes
2. Paste your bible study questions or topics
3. The AI will automatically:
   - Create a dated study folder
   - Generate formatted study materials
   - Update this README with your new study

## How to Use

### Starting a New Study

Simply tell the AI what you want to study:
- "Study Ephesians 1:3-14, focusing on election and predestination"
- "Analyze Romans 8:28-39"
- "Help me understand the covenant in Genesis 15"

The AI will read `CLAUDE.md` for instructions and create a comprehensive study following the template.

### Study Output

Each study is saved in `studies/YYYY-MM-DD-topic-name/` and includes:
- `questions.md` - Your original questions formatted
- `study.md` - Comprehensive analysis with context, cross-references, theology, and application
- `notes.md` (optional) - Your personal notes and reflections

## Study Index

| Date | Passage/Topic | Status | Summary |
|------|---------------|--------|---------|
| 2026-04-21 | [Life as a Husband](studies/2026-04-21-life-as-a-husband/) | ✓ Complete | Honor as a daily posture in marriage - 10 practical ways to honor your wife |

## Study Formats

Two templates are supported — the AI picks the right one based on your input:

- **Exegetical Study** (`templates/study-template.md`) — single passage, verse-by-verse
  deep dive with literary/historical/canonical context. Use for things like
  "Study Ephesians 1:3-14" or "Analyze Romans 8:28-39".
- **Topical / Teaching Outline** (`templates/topical-study-template.md`) — multiple
  passages clustered around a theme, with a central discussion question and
  numbered practical points. Use for men's-group or small-group outlines like
  "Life as a Husband" or "A Father's Words".

## Features

- **Two Study Formats**: Exegetical deep-dives and topical teaching outlines
- **Comprehensive Analysis**: Historical context, original languages when illuminating
- **Rigorous Answer Format**: Every question answered with 2-3 verses written in full, 2-3 Greek/Hebrew word studies, and 1 specific practical application
- **Cross-References**: Related passages that illuminate meaning
- **Theological Insights**: Key doctrines, Reformed framework, gospel-centered
- **Practical Application**: Heart-probing reflection questions and concrete (not generic) practices
- **Teaching-Outline Voice**: Preserves pastoral tone, numbered points, and pithy takeaways
- **Primary Translation**: ESV (English Standard Version)

## Answer Format

Every study question follows this structure:
1. **Question repeated** - Clear restatement before answering
2. **Comprehensive answer** - Thoughtful response to the question
3. **Biblical support** - 2-3 verses written out in full (ESV)
4. **Word studies** - 2-3 Greek or Hebrew word studies illuminating the verses
5. **Practical application** - 1 specific, concrete action (not generic advice)

## Project Structure

```
bible-study/
├── README.md              # This file - project hub and study index
├── CLAUDE.md              # AI instructions for consistent studies
├── .gitignore             # Git configuration
├── templates/
│   ├── study-template.md          # Exegetical (single passage)
│   └── topical-study-template.md  # Topical / teaching outline
└── studies/
    └── YYYY-MM-DD-topic/  # Individual study folders
        ├── questions.md   # Original input
        ├── study.md       # Study content
        └── notes.md       # Personal notes (optional)
```

## Tips

- Studies are organized chronologically by date
- Each study folder name includes a brief topic descriptor
- The AI follows Reformed theological framework
- You can add personal notes in `notes.md` without affecting the main study
- Review `CLAUDE.md` to understand the study methodology

## Getting Help

- For Claude Code help, use `/help` command
- Check `templates/study-template.md` to see the study structure
- Read `CLAUDE.md` to understand AI behavior and workflow
