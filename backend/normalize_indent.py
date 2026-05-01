#!/usr/bin/env python3
import re, sys, pathlib

p = pathlib.Path("app.py")
src = p.read_text(encoding="utf-8").replace("\t", "    ").replace("\r\n", "\n")

lines = src.split("\n")
out = []
depth = 0
# crude but effective: track (), [], {} balance outside of strings
openers = "([{"
closers = ")]}"

def strip_strings(s):
    # remove string literals to avoid counting brackets inside them
    # simple heuristic for triple/single quotes
    s2 = re.sub(r"'''(?:.|\n)*?'''", "", s)
    s2 = re.sub(r'"""(?:.|\n)*?"""', "", s2)
    s2 = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", "", s2)
    s2 = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', "", s2)
    return s2

for i, raw in enumerate(lines, 1):
    line = raw

    # Left strip only spaces (tabs already replaced)
    lstripped = line.lstrip(" ")
    leading = line[: len(line) - len(lstripped)]

    # Compute depth BEFORE this line for closing-only lines
    scan_prev = strip_strings("".join(out[-1:])) if out else ""
    # quick depth recompute based on everything so far
    # (small file, okay; accurate balancing matters)
    all_so_far = strip_strings("\n".join(out))
    d = 0
    for ch in all_so_far:
        if ch in openers:
            d += 1
        elif ch in closers and d > 0:
            d -= 1

    # Detect pure closing token lines like ")", "],", "},", ")],", etc.
    if re.match(r"^\s*[\]\)\}]+,?\s*$", line):
        # Set indent to max(d-1,0)*4 so the closing aligns with its opener
        new_indent = " " * (max(d - 1, 0) * 4)
        line = new_indent + lstripped

    out.append(line)

fixed = "\n".join(out)

# One more pass: strip trailing spaces
fixed = "\n".join([ln.rstrip() for ln in fixed.split("\n")])

p.write_text(fixed, encoding="utf-8")
print("Normalized indentation for app.py")


__all__ = ['strip_strings']
