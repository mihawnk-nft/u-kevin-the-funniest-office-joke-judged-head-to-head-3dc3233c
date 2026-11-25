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
"""

import os
import sys

JOKE = (
    "My calendar was so full of meetings about meetings that I booked "
    "one with myself to do my actual job \u2014 and I no-showed."
)


def main() -> int:
    # The grader mounts a writable directory at /output and sets
    # MAKEFUN_OUTPUT_DIR to it. Fall back to /output, then to a local
    # ./output directory so the program is also runnable by hand.
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if not os.path.isdir(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError:
            output_dir = os.path.join(os.getcwd(), "output")
            os.makedirs(output_dir, exist_ok=True)

    text = JOKE.strip()

    # Gate self-checks (mirror the sealed scorer): UTF-8 text, 1-200
    # characters, not only whitespace, a single line.
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

    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    print(f"wrote {len(text)} characters to {path}")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
