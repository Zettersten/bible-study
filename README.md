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
| | | | *No studies yet - start your first study!* |

## Features

- **Comprehensive Analysis**: Deep exegetical study with historical context and original languages
- **Cross-References**: Related passages that illuminate meaning
- **Theological Insights**: Key doctrines and principles
- **Practical Application**: Personal reflection questions and life applications
- **Consistent Format**: All studies follow the same template structure
- **Primary Translation**: ESV (English Standard Version)

## Project Structure

```
bible-study/
├── README.md              # This file - project hub and study index
├── CLAUDE.md              # AI instructions for consistent studies
├── .gitignore             # Git configuration
├── templates/
│   └── study-template.md  # Template for all studies
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
