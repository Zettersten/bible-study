#!/usr/bin/env python3
"""Dump a .docx file's paragraphs as plain UTF-8 text, one per line.

This is intentionally NOT a parser. The .docx format has no consistent
class-outline template across teachers, so structural interpretation
(what's an intro, what's a question, what's filler) is the agent's job —
not a regex's. This helper only does the one mechanical thing the agent
can't do directly: extract readable text from the binary .docx.

Stdlib-only. No python-docx dependency.

Usage:
    python3 dump_docx_text.py <path-to-docx>

Output:
    Each non-empty paragraph from word/document.xml on its own line,
    in document order. UTF-8.
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def dump(docx_path: Path) -> int:
    if not docx_path.exists():
        print(f"file not found: {docx_path}", file=sys.stderr)
        return 1
    with zipfile.ZipFile(docx_path) as zf:
        with zf.open("word/document.xml") as f:
            tree = ET.parse(f)
    for p in tree.getroot().iter(f"{W_NS}p"):
        line = "".join((t.text or "") for t in p.iter(f"{W_NS}t")).strip()
        if line:
            print(line)
    return 0


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: dump_docx_text.py <path-to-docx>", file=sys.stderr)
        return 2
    return dump(Path(argv[1]).expanduser())


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
