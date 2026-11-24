#!/usr/bin/env python3
"""Famous last words at 1% battery.

Writes one farewell line to $MAKEFUN_OUTPUT_DIR/entry.txt.
Stdlib only.
"""

import os
import sys

# --- tunables ------------------------------------------------------------
MIN_CHARS = 1
MAX_CHARS = 199
FILE_NAME = "entry.txt"
FILE_MODE = 0o644
FALLBACK_DIR = "/output"

# --- the line, assembled from its two halves ----------------------------
_OPENING = "So this is how it ends"
_REST = (
    "47 tabs open, one unsent text, "
    "and not a single photo backed up. "
    "Tell the charger I loved it. Goodbye."
)
_DASH = "\u2014"


def build_line():
    """Join opening and body around an em dash."""
    return " ".join((_OPENING, _DASH, _REST))


def check_line(line):
    """Reject anything outside 1-199 chars or spanning more than one line."""
    if not isinstance(line, str):
        raise TypeError("line must be str")
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        raise ValueError(
            "line must be %d-%d chars, got %d" % (MIN_CHARS, MAX_CHARS, len(line))
        )
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    return line


def output_path():
    """Resolve the destination file from the environment."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_DIR
    return os.path.join(directory, FILE_NAME)


def write_entry(line):
    """Write the line bytes directly, then fix the file mode."""
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(line.encode("utf-8"))
    os.chmod(path, FILE_MODE)
    actual_mode = os.stat(path).st_mode & 0o777
    if actual_mode != FILE_MODE:
        raise OSError("mode of %s is %o, expected %o" % (path, actual_mode, FILE_MODE))
    return path


def main():
    try:
        line = check_line(build_line())
        path = write_entry(line)
    except (TypeError, ValueError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    print("wrote %d chars to %s" % (len(line), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
