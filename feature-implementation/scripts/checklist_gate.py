#!/usr/bin/env python3
"""Read-only requirements-quality checklist gate.

Scans every checklists/*.md file under a feature directory (or a checklists
directory given directly), counts checkbox items, and prints a status table.

  Total     lines matching "- [ ]", "- [x]" or "- [X]"
  Checked   lines matching "- [x]" or "- [X]"
  Unchecked lines matching "- [ ]"

A checklist passes when it has zero unchecked items. The overall gate passes
only when every checklist passes. The script never edits any file.

Exit codes:
  0  PASS, or not applicable (no checklists directory / no checklist files)
  1  FAIL (one or more checklists have unchecked items)
  2  usage error (path does not exist or is not a directory)

Usage:
  checklist_gate.py FEATURE_DIR_OR_CHECKLISTS_DIR [--json]
"""
import argparse
import json
import pathlib
import re
import sys

ITEM_RE = re.compile(r"^\s*- \[( |x|X)\]")


def count_items(path):
    total = checked = unchecked = 0
    fence_char = None
    fence_length = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence_char is not None:
            closing = re.match(r"^ {0,3}(" + re.escape(fence_char) + r"{" + str(fence_length) + r",})[ \t]*$", line)
            if closing:
                fence_char = None
                fence_length = 0
            continue
        if opening and not (opening[1][0] == "`" and "`" in opening[2]):
            fence_char = opening[1][0]
            fence_length = len(opening[1])
            continue
        m = ITEM_RE.match(line)
        if not m:
            continue
        total += 1
        if m.group(1) == " ":
            unchecked += 1
        else:
            checked += 1
    return total, checked, unchecked


def resolve_dir(arg):
    p = pathlib.Path(arg)
    if not p.exists():
        return None, f"path does not exist: {arg}"
    if not p.is_dir():
        return None, f"not a directory: {arg}"
    if p.name == "checklists":
        return p, None
    sub = p / "checklists"
    if sub.is_dir():
        return sub, None
    return False, None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Read-only checklist gate.")
    ap.add_argument("path", help="feature directory containing checklists/, or the checklists directory")
    ap.add_argument("--json", action="store_true", help="print machine-readable result")
    args = ap.parse_args(argv)

    cdir, err = resolve_dir(args.path)
    if err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    files = sorted(cdir.glob("*.md")) if cdir else []
    if not files:
        result = {"status": "NOT_APPLICABLE", "checklists": [],
                  "reason": "no checklists directory" if cdir is False else "no checklist files"}
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Checklist gate: NOT APPLICABLE ({result['reason']})")
        return 0

    rows = []
    for f in files:
        total, checked, unchecked = count_items(f)
        rows.append({"checklist": f.name, "total": total, "checked": checked,
                     "unchecked": unchecked, "status": "PASS" if unchecked == 0 else "FAIL"})
    overall = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"

    if args.json:
        print(json.dumps({"status": overall, "checklists": rows}, indent=2))
    else:
        w = max(len("Checklist"), *(len(r["checklist"]) for r in rows))
        print(f"| {'Checklist'.ljust(w)} | Total | Checked | Unchecked | Status |")
        print(f"|{'-' * (w + 2)}|-------|---------|-----------|--------|")
        for r in rows:
            print(f"| {r['checklist'].ljust(w)} | {r['total']:>5} | {r['checked']:>7} | "
                  f"{r['unchecked']:>9} | {r['status']:<6} |")
        print()
        print(f"Overall: {overall}")
        if overall == "FAIL":
            print("Some checklists have unchecked items. Checklist markers are reviewer-owned; "
                  "do not edit them to pass this gate.")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
