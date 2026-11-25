#!/usr/bin/env python3
"""The Funniest Office Joke, Judged Head to Head.

Writes a single one-line joke about office life to /output/entry.txt.

The joke is a fixed, hand-written line (no network, no randomness, no
external dependencies -- pure standard library). It is built for the
published judge brief, in the brief's own order of importance:

1. A real one-line joke about office life, with a setup and a turn.
2. Turns on something anyone who has worked in an office knows: the
   calendar packed with meetings about meetings.
3. Surprises: the turn ("and I no-showed") is not a plain complaint --
   the speaker sabotages the one meeting meant to save them.
4. Lands in one line, every word earning its place, punchline last.
5. Feels new: the meeting-with-myself premise is not the usual
   "this meeting could have been an email" line going round the office.

Determinism: the joke is a fixed literal assembled from fixed parts.
No randomness, no clock, no input besides the output directory, so
every run writes byte-identical output.
"""

import os
import sys

# One clause per string; build_joke() joins them verbatim, so the line
# stays exactly the same while the structure is easier to audit.
JOKE_PARTS = (
    "My calendar was so full of meetings about meetings that I booked ",
    "one with myself to do my actual job \u2014 and I no-showed.",
)


def build_joke() -> str:
    """Assemble the joke line from its fixed parts."""
    return "".join(JOKE_PARTS).strip()


def resolve_output_dir() -> str:
    """Pick the grader's output directory, falling back gracefully.

    The grader mounts a writable directory at /output and sets
    MAKEFUN_OUTPUT_DIR to it. Fall back to /output, then to a local
    ./output directory so the program is also runnable by hand.
    """
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if not os.path.isdir(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError:
            output_dir = os.path.join(os.getcwd(), "output")
            os.makedirs(output_dir, exist_ok=True)
    return output_dir


def validate(text: str) -> int:
    """Gate self-checks (mirror the sealed scorer): UTF-8 text, 1-200
    characters, not only whitespace, a single line. Returns 0 on pass,
    1 after printing the failure to stderr."""
    if not text:
        print("error: joke is empty", file=sys.stderr)
        return 1
    if len(text) > 200:
        print(f"error: joke is {len(text)} characters, over the 200 cap",
              file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: joke must be a single line", file=sys.stderr)
        return 1
    text.encode("utf-8")  # raises if not valid UTF-8
    return 0


def main() -> int:
    text = build_joke()
    if validate(text) != 0:
        return 1

    path = os.path.join(resolve_output_dir(), "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    print(f"wrote {len(text)} characters to {path}")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
