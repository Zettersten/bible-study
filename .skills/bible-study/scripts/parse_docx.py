#!/usr/bin/env python3
"""Parse a class-outline .docx into a structured JSON outline.

Stdlib-only. No python-docx dependency. The .docx format is just a zip
containing word/document.xml; we read the paragraphs directly.

Usage:
    python3 parse_docx.py <path-to-docx>

Emits JSON to stdout:
    {
      "topic": str,
      "intro": str,
      "sections": [
        {"read": str | null, "questions": [str, ...]},
        ...
      ],
      "closing": str | null
    }

Heuristics for the class-outline shape (matches the Colossians 2 doc and the
men's-group outlines this repo has seen):

- First non-empty paragraph is the topic line (e.g. "Colossians 2").
- Subsequent paragraphs up to the first "READ" line are the intro.
- A line starting with "READ" (case-insensitive) opens a new section. The
  reference is whatever follows "READ" on that line.
- Lines starting with "Q." (or "Q1.", "Q:") inside a section are questions.
- Separator lines made of underscores/dashes are ignored.
- A trailing "Tune in next week" line is captured as `closing`.
"""

from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def extract_paragraphs(docx_path: Path) -> list[str]:
    """Return the document's paragraphs as plain text strings."""
    with zipfile.ZipFile(docx_path) as zf:
        with zf.open("word/document.xml") as f:
            tree = ET.parse(f)
    root = tree.getroot()
    paragraphs: list[str] = []
    for p in root.iter(f"{W_NS}p"):
        # Concatenate all <w:t> text runs in the paragraph.
        texts = [t.text or "" for t in p.iter(f"{W_NS}t")]
        line = "".join(texts).strip()
        # Normalize unicode ellipses/em-dashes that the original doc uses heavily.
        paragraphs.append(line)
    return paragraphs


def is_separator(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    # Lines made overwhelmingly of underscores or dashes.
    non_filler = re.sub(r"[_\-\s]", "", stripped)
    return len(non_filler) == 0


def parse_outline(paragraphs: list[str]) -> dict:
    # Drop separators while keeping a flat list of meaningful lines.
    lines = [ln for ln in paragraphs if not is_separator(ln)]
    if not lines:
        return {"topic": "", "intro": "", "sections": [], "closing": None}

    topic = lines[0]
    intro_parts: list[str] = []
    sections: list[dict] = []
    closing: str | None = None

    current: dict | None = None
    in_intro = True

    read_re = re.compile(r"^\s*READ\b\s*[:\-]?\s*(.*)$", re.IGNORECASE)
    question_re = re.compile(r"^\s*Q\s*\d*\s*[\.:\)]\s*(.+)$", re.IGNORECASE)
    tune_in_re = re.compile(r"tune\s+in\s+next\s+week", re.IGNORECASE)

    for line in lines[1:]:
        if tune_in_re.search(line):
            closing = line.strip()
            continue

        m_read = read_re.match(line)
        if m_read:
            in_intro = False
            ref = m_read.group(1).strip().rstrip(".") or None
            current = {"read": ref, "questions": []}
            sections.append(current)
            continue

        m_q = question_re.match(line)
        if m_q and current is not None:
            current["questions"].append(m_q.group(1).strip())
            continue

        if in_intro:
            intro_parts.append(line.strip())
        # else: free-prose line inside a section (Paul-says-something framing).
        # We intentionally don't capture it — the answer-writer re-derives
        # framing from the passage itself, and capturing it here just creates
        # noise that has to be deduped later.

    intro = "\n\n".join(p for p in intro_parts if p)
    return {
        "topic": topic,
        "intro": intro,
        "sections": sections,
        "closing": closing,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: parse_docx.py <path-to-docx>", file=sys.stderr)
        return 2
    path = Path(argv[1]).expanduser()
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 1
    paragraphs = extract_paragraphs(path)
    outline = parse_outline(paragraphs)
    json.dump(outline, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
