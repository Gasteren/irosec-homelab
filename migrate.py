#!/usr/bin/env python3
"""
Migrate a Wiki.js markdown export into a Starlight content tree.

Usage:
    python3 migrate.py <wikijs_export_dir> <starlight_docs_dir>
"""

import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def parse_existing_frontmatter(fm_text: str) -> dict:
    data = {}
    for line in fm_text.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        data[key] = value
    return data


def derive_title(text: str, fallback: str) -> tuple[str, str]:
    match = H1_RE.search(text)
    if match and text.lstrip().startswith("#"):
        title = match.group(1).strip()
        body = text[: match.start()] + text[match.end():]
        return title, body.lstrip("\n")
    return fallback, text


def slug_to_title(name: str) -> str:
    name = name.replace("-", " ").replace("_", " ")
    return name.strip().title() or "Untitled"


def make_description(body: str) -> str:
    for line in body.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("!["):
            desc = re.sub(r"[#*_`>]", "", line).strip()
            return (desc[:117] + "...") if len(desc) > 120 else desc
    return "Migrated from Wiki.js."


def yaml_escape(s: str) -> str:
    return s.replace('"', '\\"')


def migrate_file(src: Path, dst: Path) -> None:
    text = src.read_text(encoding="utf-8", errors="replace")

    existing_title = ""
    existing_description = ""

    fm_match = FRONTMATTER_RE.match(text)
    if fm_match:
        existing = parse_existing_frontmatter(fm_match.group(1))
        existing_title = existing.get("title", "")
        existing_description = existing.get("description", "")
        text = text[fm_match.end():]

    fallback_title = slug_to_title(src.stem)
    derived_title, body = derive_title(text, fallback_title)
    description = make_description(body)

    title = existing_title or derived_title
    description = existing_description or description

    frontmatter = (
        "---\n"
        f'title: "{yaml_escape(title)}"\n'
        f'description: "{yaml_escape(description)}"\n'
        "---\n\n"
    )

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(frontmatter + body.lstrip("\n"), encoding="utf-8")
    print(f"migrated: {src} -> {dst}  (title: {title!r})")


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    src_root = Path(sys.argv[1]).resolve()
    dst_root = Path(sys.argv[2]).resolve()

    if not src_root.is_dir():
        print(f"Source directory not found: {src_root}")
        sys.exit(1)

    md_files = list(src_root.rglob("*.md"))
    if not md_files:
        print(f"No .md files found under {src_root}")
        sys.exit(1)

    for src in md_files:
        rel = src.relative_to(src_root)
        dst = dst_root / rel
        migrate_file(src, dst)

    print(f"\nDone. Migrated {len(md_files)} file(s) into {dst_root}")


if __name__ == "__main__":
    main()
