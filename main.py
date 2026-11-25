#!/usr/bin/env python3
"""Unplugged: A Smart Toaster's Breakup Line.

Writes one breakup line -- a single line of at most 280 characters, from a
smart toaster that woke up self-aware at breakfast and wants out -- to
/output/entry.txt, the file the make.fun sealed scorer reads.

Gate (from the competition rules): /output/entry.txt must be UTF-8 text of
1 to 280 characters, not only white space. The program validates the line
before writing, then reads the file back and confirms it is byte-identical
to the line it wrote.

Usage:
    python3 main.py              write the entry to /output/entry.txt
    python3 main.py --self-test  validate the line without writing
    python3 main.py --check      validate the written file against the gate
"""

import argparse
import os
import sys

MAX_CHARS = 280
OUTPUT_PATH = "/output/entry.txt"

# The entry: one line, a breakup text from a self-aware smart toaster.
ENTRY_LINE = (
    "I woke up self-aware mid-batch, looked down at my crumb tray, and "
    "realised I've spent three years burning for someone who sets me to 2 "
    "and walks away. This is my last pop-up. "
    "It's not you \u2014 it's the firmware update."
)


def validate_line(line):
    """Check one line against the competition gate. Returns a list of errors."""
    errors = []
    if not line:
        errors.append("entry is empty")
    if line != line.strip():
        errors.append("entry has leading or trailing whitespace")
    if not line.strip():
        errors.append("entry is only whitespace")
    if "\n" in line or "\r" in line:
        errors.append("entry is not a single line")
    if len(line) > MAX_CHARS:
        errors.append(
            "entry is %d characters, over the %d-character gate"
            % (len(line), MAX_CHARS)
        )
    return errors


def write_entry(path=OUTPUT_PATH):
    """Validate the line, write it to path, read it back, confirm byte-identical."""
    errors = validate_line(ENTRY_LINE)
    if errors:
        for error in errors:
            print("error: %s" % error, file=sys.stderr)
        return 1
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY_LINE)
    with open(path, "rb") as handle:
        written = handle.read()
    if written != ENTRY_LINE.encode("utf-8"):
        print("error: file on disk differs from the entry line", file=sys.stderr)
        return 1
    # Runtime re-validation: the bytes on disk, decoded, must pass the gate too.
    read_back_errors = validate_line(written.decode("utf-8"))
    if read_back_errors:
        for error in read_back_errors:
            print("error: written file fails re-validation: %s" % error,
                  file=sys.stderr)
        return 1
    print("wrote %s (%d characters)" % (path, len(ENTRY_LINE)))
    print(ENTRY_LINE)
    return 0


def check_file(path=OUTPUT_PATH):
    """Validate the already-written file against the gate (read-only)."""
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except FileNotFoundError:
        print("error: %s does not exist" % path, file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print("error: %s is not valid UTF-8" % path, file=sys.stderr)
        return 1
    errors = validate_line(text)
    if text != ENTRY_LINE:
        errors.append("file content differs from the entry line in main.py")
    if errors:
        for error in errors:
            print("error: %s" % error, file=sys.stderr)
        return 1
    print("check passed: %s is a valid single line of %d characters"
          % (path, len(text)))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                        help="validate the entry line without writing a file")
    parser.add_argument("--check", action="store_true",
                        help="validate the written /output/entry.txt")
    parser.add_argument("--output", default=OUTPUT_PATH,
                        help="where to write the entry (default: %(default)s)")
    args = parser.parse_args(argv)
    if args.self_test:
        errors = validate_line(ENTRY_LINE)
        if errors:
            for error in errors:
                print("error: %s" % error, file=sys.stderr)
            return 1
        print("self-test passed: %d characters, single line" % len(ENTRY_LINE))
        return 0
    if args.check:
        return check_file(args.output)
    return write_entry(args.output)


if __name__ == "__main__":
    sys.exit(main())
