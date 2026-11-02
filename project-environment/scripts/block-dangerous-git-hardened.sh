#!/bin/bash
# Shell-hook adapter. Python's standard library parses JSON and quoted static
# shell tokens; no shell text is evaluated. Missing Python fails closed.
if ! command -v python3 >/dev/null 2>&1; then
  echo "BLOCKED: python3 is required to parse hook input, so the command was not checked. The user has prevented you from doing this." >&2
  exit 2
fi
script_dir="${BASH_SOURCE[0]%/*}"
exec python3 "$script_dir/block-dangerous-git.py"
