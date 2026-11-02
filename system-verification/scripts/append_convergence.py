#!/usr/bin/env python3
"""Append a convergence phase to a task list without altering existing bytes.

Input:
  TASKS     the project's existing task file (markdown checklist with T### ids)
  FINDINGS  a JSON file holding a list of findings (or {"findings": [...]}):
            {
              "id": "F1",                     stable finding id (unique)
              "source_ref": "FR-003",         FR-###, SC-###, US1/AC2, "plan: <decision>", "Constitution II"
              "gap_type": "missing",          missing | partial | contradicts | unrequested
              "severity": "HIGH",             CRITICAL | HIGH | MEDIUM | LOW
              "description": "Add ...",       imperative remaining work, one line
              "evidence": "path/to/file.py"   optional; shown in the summary only
            }

Behavior:
  - Validates every finding; any invalid finding aborts with exit 2 and no write.
  - Prints the severity-graded findings summary before writing.
  - Empty findings: the converged outcome. The task file is not touched
    (byte-for-byte unchanged, no empty phase header); exit 0.
  - Otherwise computes M = highest existing task id and N = highest existing
    phase number + 1, then appends "## Phase N: Convergence" with one item per
    finding, ordered CRITICAL, HIGH, MEDIUM, LOW (constitution findings first
    inside each severity), ids T{M+1:03d}, T{M+2:03d}, ...
        - [ ] T042 <description> per <source_ref> (<gap_type>)
    CRITICAL items are written as "CRITICAL: <description>".
  - Locks the file and checks its bytes again before appending. Concurrent
    changes abort the append. Post-write verification never restores a stale
    snapshot or truncates somebody else's edits; conflicts return exit 1.
  - --dry-run prints the section that would be appended and writes nothing.

Exit codes: 0 converged or appended, 1 verification failure, 2 invalid input.

Usage:
  append_convergence.py TASKS FINDINGS [--dry-run] [--with-finding-ids] [--json]
"""
import argparse
import fcntl
import json
import os
import pathlib
import re
import sys

GAP_TYPES = ("missing", "partial", "contradicts", "unrequested")
SEVERITIES = ("CRITICAL", "HIGH", "MEDIUM", "LOW")
TASK_ID_RE = re.compile(r"^\s*- \[[ xX]\]\s+T(\d+)\b")
PHASE_RE = re.compile(r"^#{2,3}\s+Phase\s+(\d+)\b", re.I)


def load_findings(path):
    try:
        data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise ValueError(f"cannot read findings JSON: {e}")
    if isinstance(data, dict):
        data = data.get("findings")
    if not isinstance(data, list):
        raise ValueError("findings must be a JSON list or an object with a 'findings' list")
    seen = set()
    problems = []
    for i, f in enumerate(data):
        where = f"finding[{i}]"
        if not isinstance(f, dict):
            problems.append(f"{where}: not an object")
            continue
        for key in ("id", "source_ref", "gap_type", "severity", "description"):
            v = f.get(key)
            if not isinstance(v, str) or not v.strip():
                problems.append(f"{where}: missing or empty '{key}'")
            elif "\n" in v or "\r" in v:
                problems.append(f"{where}: '{key}' must be a single line")
        if f.get("gap_type") not in GAP_TYPES:
            problems.append(f"{where}: gap_type must be one of {', '.join(GAP_TYPES)}")
        if f.get("severity") not in SEVERITIES:
            problems.append(f"{where}: severity must be one of {', '.join(SEVERITIES)}")
        fid = f.get("id")
        if isinstance(fid, str):
            if fid in seen:
                problems.append(f"{where}: duplicate id {fid!r}")
            seen.add(fid)
    if problems:
        raise ValueError("; ".join(problems))
    return data


def scan_tasks(text):
    max_id = 0
    max_phase = 0
    fence = None
    for line in text.splitlines():
        if fence:
            if re.match(r"^ {0,3}" + re.escape(fence[0]) + "{" + str(fence[1]) + r",}\s*$", line):
                fence = None
            continue
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if opening and not (opening[1][0] == "`" and "`" in opening[2]):
            fence = (opening[1][0], len(opening[1]))
            continue
        m = TASK_ID_RE.match(line)
        if m:
            max_id = max(max_id, int(m.group(1)))
        p = PHASE_RE.match(line)
        if p:
            max_phase = max(max_phase, int(p.group(1)))
    return max_id, max_phase


def order(findings):
    def key(item):
        idx, f = item
        constitution = 0 if f["source_ref"].strip().lower().startswith("constitution") else 1
        return (SEVERITIES.index(f["severity"]), constitution, idx)
    return [f for _, f in sorted(enumerate(findings), key=key)]


def build_section(findings, max_id, max_phase, with_ids):
    phase = max_phase + 1
    lines = [f"## Phase {phase}: Convergence", ""]
    assigned = []
    for n, f in enumerate(order(findings), start=1):
        tid = f"T{max_id + n:03d}"
        desc = f["description"].strip()
        if f["severity"] == "CRITICAL":
            desc = f"CRITICAL: {desc}"
        line = f"- [ ] {tid} {desc} per {f['source_ref'].strip()} ({f['gap_type']})"
        if with_ids:
            line += f" [{f['id'].strip()}]"
        lines.append(line)
        assigned.append({"task_id": tid, "finding_id": f["id"]})
    return phase, "\n".join(lines) + "\n", assigned


def summary(findings):
    out = ["## Convergence Findings", "",
           "| ID | Gap Type | Severity | Source | Evidence | Remaining Work |",
           "|----|----------|----------|--------|----------|----------------|"]
    for f in order(findings):
        out.append(f"| {f['id']} | {f['gap_type']} | {f['severity']} | {f['source_ref']} | "
                   f"{f.get('evidence', '') or ''} | {f['description']} |")
    by_gap = {g: sum(1 for f in findings if f["gap_type"] == g) for g in GAP_TYPES}
    by_sev = {s: sum(1 for f in findings if f["severity"] == s) for s in SEVERITIES}
    out += ["", "Findings by gap type: " + ", ".join(f"{k} {v}" for k, v in by_gap.items()),
            "Findings by severity: " + ", ".join(f"{k} {v}" for k, v in by_sev.items())]
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Append a convergence phase to a task list.")
    ap.add_argument("tasks")
    ap.add_argument("findings")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--with-finding-ids", action="store_true",
                    help="append [F#] to each task line for traceability")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    tasks = pathlib.Path(args.tasks)
    if not tasks.is_file():
        print(f"error: tasks file not found: {tasks}", file=sys.stderr)
        return 2
    try:
        findings = load_findings(args.findings)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    original = tasks.read_bytes()
    try:
        text = original.decode("utf-8")
    except UnicodeDecodeError:
        print("error: tasks file is not UTF-8", file=sys.stderr)
        return 2

    if not findings:
        result = {"outcome": "converged", "tasks_file": str(tasks), "appended": []}
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("Converged: no findings. The task file was not modified (no empty phase header).")
        return 0

    max_id, max_phase = scan_tasks(text)
    phase, section, assigned = build_section(findings, max_id, max_phase, args.with_finding_ids)

    if not args.json:
        print(summary(findings))
        print()
    if original and not original.endswith(b"\n"):
        sep = b"\n\n"
    elif original.endswith(b"\n\n") or not original:
        sep = b""
    else:
        sep = b"\n"
    payload = sep + section.encode("utf-8")

    if args.dry_run:
        if args.json:
            print(json.dumps({"outcome": "dry_run", "phase": phase, "appended": assigned,
                              "section": section}, indent=2))
        else:
            print(f"Dry run: would append Phase {phase} with {len(assigned)} task(s):")
            print(section, end="")
        return 0

    # O_APPEND preserves an uncooperative writer's append even between seek and
    # write. The lock serializes cooperating invocations; the byte comparison
    # rejects a stale plan rather than allocating duplicate task identifiers.
    try:
        fd = os.open(tasks, os.O_RDWR | os.O_APPEND)
        with os.fdopen(fd, "a+b") as fh:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
            fh.seek(0)
            if fh.read() != original:
                print("error: tasks changed concurrently; nothing appended; reread and retry", file=sys.stderr)
                return 1
            fh.write(payload)
            fh.flush()
            after = tasks.read_bytes()
            if after != original + payload:
                print("error: concurrent change or verification failure; all current bytes preserved; inspect before retry", file=sys.stderr)
                return 1
    except OSError as error:
        print(f"error: append failed; current bytes preserved: {error}", file=sys.stderr)
        return 1

    result = {"outcome": "tasks_appended", "tasks_file": str(tasks), "phase": phase,
              "appended": assigned, "prefix_verified": True}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Appended Phase {phase}: Convergence with {len(assigned)} task(s) "
              f"({assigned[0]['task_id']}..{assigned[-1]['task_id']}). Original bytes verified unchanged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
