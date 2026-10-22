#!/usr/bin/env python3
"""
Find (and optionally fix) em dashes across all Markdown files under a
content directory.

Usage:
    python3 find_emdashes.py <docs_dir>            # report only
    python3 find_emdashes.py <docs_dir> --fix       # replace and report
"""
import sys
from pathlib import Path

EM_DASH = "\u2014"

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    root = Path(sys.argv[1]).resolve()
    fix = "--fix" in sys.argv

    md_files = sorted(root.rglob("*.md"))
    total_occurrences = 0
    files_with_matches = 0

    for path in md_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        count = text.count(EM_DASH)
        if count == 0:
            continue

        files_with_matches += 1
        total_occurrences += count
        rel = path.relative_to(root)
        print(f"\n{rel}  ({count} occurrence{'s' if count != 1 else ''})")

        for i, line in enumerate(text.splitlines(), 1):
            if EM_DASH in line:
                print(f"  L{i}: {line.strip()}")

        if fix:
            new_text = text.replace(EM_DASH, " - ")
            while "  " in new_text:
                new_text = new_text.replace("  ", " ")
            path.write_text(new_text, encoding="utf-8")

    print(f"\n{'Fixed' if fix else 'Found'} {total_occurrences} em dash(es) across {files_with_matches} file(s) out of {len(md_files)} scanned.")

if __name__ == "__main__":
    main()
