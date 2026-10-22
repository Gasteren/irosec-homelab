#!/usr/bin/env python3
"""
Add or update `sidebar: { order: N }` in a Markdown file's frontmatter
without touching anything else in the file.

Usage:
    python3 set_sidebar_order.py <file> <order_number>
"""
import re
import sys
from pathlib import Path

def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    path = Path(sys.argv[1])
    order = int(sys.argv[2])

    text = path.read_text(encoding="utf-8")

    fm_match = re.match(r"^(---\s*\n)(.*?)(\n---\s*\n)", text, re.DOTALL)
    if not fm_match:
        print(f"SKIP (no frontmatter found): {path}")
        return

    open_delim, fm_body, close_delim = fm_match.groups()
    fm_body = re.sub(r"\nsidebar:\n(?:  .+\n?)*", "\n", fm_body)
    fm_body = fm_body.rstrip("\n") + f"\nsidebar:\n  order: {order}"

    new_frontmatter = open_delim + fm_body + close_delim
    new_text = new_frontmatter + text[fm_match.end():]

    path.write_text(new_text, encoding="utf-8")
    print(f"order={order}: {path}")

if __name__ == "__main__":
    main()
