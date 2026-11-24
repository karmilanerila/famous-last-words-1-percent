"""Famous Last Words at 1 Percent: write one last-words line to /output/entry.txt.

The line is the funniest possible last words a phone would say when its
battery hits 1 percent: dramatic, specific, self-aware — 47 tabs open, one
unsent text, not a single photo backed up — and a goodbye to the charger.
It stays within the competition's 199-character gate.
"""

import os

LINE = (
    "So this is how it ends — 47 tabs open, one unsent text, "
    "and not a single photo backed up. "
    "Tell the charger I loved it. Goodbye."
)

MAX_CHARS = 199


def main():
    if not 1 <= len(LINE) <= MAX_CHARS:
        raise SystemExit(f"entry line is {len(LINE)} chars, must be 1-199")
    if LINE != LINE.strip() or "\n" in LINE:
        raise SystemExit("entry line must be a single line, no surrounding whitespace")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    # Write straight to the final path: no tempfile dance. The grader
    # reads entry.txt as another user, so the file must be world-readable
    # from the moment it exists, which a mkstemp-created 0600 file is not.
    with open(path, "wb") as f:
        f.write(LINE.encode("utf-8"))
    os.chmod(path, 0o644)
    print(f"wrote {len(LINE)} chars to {path}")


if __name__ == "__main__":
    main()
