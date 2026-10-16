#!/usr/bin/env python3
"""Keep shared reference files in step.

uk-deadlines needs the key deadlines calendar inside its own folder, so the skill
still works when uploaded on its own to the Claude app. The single source is the
uk-company-guide copy; this script writes the uk-deadlines copy from it, turning
links to files that only exist in uk-company-guide into plain text.

  python3 tools/sync_shared.py          write the copy
  python3 tools/sync_shared.py --check  exit 1 if the copy is out of date
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAIRS = [
    (
        "plugins/uk-business/skills/uk-company-guide/references/key-deadlines-calendar.md",
        "plugins/uk-business/skills/uk-deadlines/references/key-deadlines-calendar.md",
    ),
]
LINK = re.compile(r"\[([^\]]+)\]\(([^)#]+\.md)(#[^)]*)?\)")


def render(src: Path, dst: Path) -> str:
    text = src.read_text(encoding="utf-8")

    def fix(m: re.Match) -> str:
        target = m.group(2)
        if target.startswith("http") or (dst.parent / target).exists():
            return m.group(0)
        return m.group(1)

    header = (
        "<!-- Generated from ../../uk-company-guide/references/key-deadlines-calendar.md "
        "by tools/sync_shared.py. Edit the source, not this copy. -->\n\n"
    )
    return header + LINK.sub(fix, text)


def main() -> int:
    check = "--check" in sys.argv
    stale = []
    for s, d in PAIRS:
        src, dst = ROOT / s, ROOT / d
        want = render(src, dst)
        have = dst.read_text(encoding="utf-8") if dst.exists() else ""
        if want != have:
            stale.append(d)
            if not check:
                dst.write_text(want, encoding="utf-8")
    if check and stale:
        print("Out of date, run tools/sync_shared.py:", *stale, sep="\n  ")
        return 1
    print("Shared files in step." if check else f"Wrote {len(stale)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
