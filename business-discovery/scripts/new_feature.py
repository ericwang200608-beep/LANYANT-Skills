#!/usr/bin/env python3
"""Create a new feature directory and spec file.

Usage: new_feature.py [options] <feature_description>

Creates <root>/<specs-dir>/<prefix>-<short-name>/spec.md from the project's
composed spec-template stack, with the skill's assets as the final fallback. The prefix is the next sequential 3-digit number
(timestamp directories are skipped when numbering) or, with --timestamp, a
YYYYMMDD-HHMMSS timestamp. Never creates or switches git branches.

A feature pointer file (.lanyant/feature.json) is written only when the
project opts in: pass --write-pointer, or set "write_feature_pointer": true in
<root>/.lanyant/config.json. The same config file may set
"feature_numbering": "timestamp" | "sequential".

Python 3.10+ standard library for JSON template manifests; other YAML manifests
require PyYAML or a configured compatible interpreter.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path
from typing import Optional

_STOP_WORDS = frozenset(
    """
    i a an the to for of in on at by with from is are was were be been being
    have has had do does did will would should could can may might must shall
    this that these those my your our their want need add get set
    """.split()
)

_MAX_NAME_LENGTH = 244
_MAX_FEATURE_NUMBER = 2**63 - 1
_ASCII_LOWER = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"
)
_DEFAULT_TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "spec-template.md"
_POINTER_RELATIVE = Path(".lanyant") / "feature.json"
_CONFIG_RELATIVE = Path(".lanyant") / "config.json"


def _err(message: str) -> None:
    print(message, file=sys.stderr)


def _json_line(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"


def _int64_from_digits(value: str) -> Optional[int]:
    normalized = value.lstrip("0") or "0"
    maximum = str(_MAX_FEATURE_NUMBER)
    if len(normalized) > len(maximum) or (
        len(normalized) == len(maximum) and normalized > maximum
    ):
        return None
    return int(normalized, 10)


def _unicode_words(name: str, separator: str) -> str:
    return "".join(
        char if char.isalpha() or char.isdecimal() else separator
        for char in name.translate(_ASCII_LOWER)
    )


def clean_name(name: str) -> str:
    cleaned = _unicode_words(name, "-")
    cleaned = re.sub(r"-+", "-", cleaned)
    return cleaned.strip("-")


def generate_short_name(description: str) -> str:
    clean = _unicode_words(description, " ")
    meaningful = []
    for word in clean.split():
        if word in _STOP_WORDS:
            continue
        if len(word) >= 3 or not word.isascii():
            meaningful.append(word)
        # Keep short words that appear as an uppercase acronym in the original.
        elif re.search(
            rf"(?<![0-9A-Za-z_]){re.escape(word.upper())}(?![0-9A-Za-z_])",
            description,
        ):
            meaningful.append(word)

    if meaningful:
        max_words = 4 if len(meaningful) == 4 else 3
        return "-".join(meaningful[:max_words])

    cleaned = clean_name(description)
    return "-".join([part for part in cleaned.split("-") if part][:3])


def highest_sequential_number(specs_dir: Path) -> int:
    highest = 0
    if not specs_dir.is_dir():
        return highest
    for entry in specs_dir.iterdir():
        if not entry.is_dir():
            continue
        name = entry.name
        # Match sequential prefixes (>=3 digits), but skip timestamp dirs.
        if re.match(r"^[0-9]{3,}-", name) and not re.match(
            r"^[0-9]{8}-[0-9]{6}-", name
        ):
            number = _int64_from_digits(re.match(r"^[0-9]+", name).group())
            if number is not None:
                highest = max(highest, number)
    return highest


def fit_name(feature_num: str, suffix: str) -> str:
    """Fit prefix and suffix within the 244-byte name limit."""
    name = f"{feature_num}-{suffix}"
    if len(name.encode("utf-8")) <= _MAX_NAME_LENGTH:
        return name
    max_suffix_length = _MAX_NAME_LENGTH - (len(feature_num) + 1)
    truncated = suffix.encode("utf-8")[:max_suffix_length].decode(
        "utf-8", errors="ignore"
    ).rstrip("-")
    return f"{feature_num}-{truncated}"


def _prefix_exists(specs_dir: Path, feature_num: str) -> bool:
    try:
        return any(
            entry.is_dir() and entry.name.startswith(f"{feature_num}-")
            for entry in specs_dir.iterdir()
        )
    except OSError:
        return False


def _read_config(root: Path) -> dict:
    path = root / _CONFIG_RELATIVE
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _err(f"[new-feature] Warning: cannot read {path} ({exc}); using defaults")
        return {}
    return data if isinstance(data, dict) else {}


def _read_pointer(root: Path) -> str:
    path = root / _POINTER_RELATIVE
    if not path.is_file():
        return ""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ""
    value = data.get("feature_directory") if isinstance(data, dict) else None
    return value if isinstance(value, str) else ""


def write_pointer(root: Path, feature_dir_value: str) -> bool:
    """Write .lanyant/feature.json; return True when the file changed."""
    if _read_pointer(root) == feature_dir_value:
        return False
    path = root / _POINTER_RELATIVE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_json_line({"feature_directory": feature_dir_value}).encode("utf-8"))
    return True


def _relative_inside(root: Path, value: str, label: str) -> Path:
    if value.startswith("/") or re.match(r"^[A-Za-z]:", value) or "\\" in value:
        raise ValueError(f"{label} must be a project-relative path with '/' separators; got '{value}'")
    if ".." in value.split("/"):
        raise ValueError(f"{label} must not contain '..' segments; got '{value}'")
    target = (root / value).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        raise ValueError(f"{label} resolves outside the project root; got '{value}'")
    return root / value


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="new_feature.py",
        description="Create a numbered feature directory with a spec file from the spec template. Never creates git branches.",
    )
    p.add_argument("description", nargs="*", help="feature description")
    p.add_argument("--json", action="store_true", help="output JSON {FEATURE_DIR, SPEC_FILE, FEATURE_NUM}")
    p.add_argument("--dry-run", action="store_true", help="compute names and paths without creating anything")
    p.add_argument("--allow-existing", action="store_true", help="reuse an existing feature directory; never overwrite an existing spec.md")
    p.add_argument("--short-name", default="", help="custom short name (2-4 words)")
    p.add_argument("--number", default="", help="preferred feature number (auto-corrected if its prefix exists)")
    p.add_argument("--timestamp", action="store_true", help="use a YYYYMMDD-HHMMSS prefix instead of sequential numbering")
    p.add_argument("--root", default=".", help="project root (default: current directory)")
    p.add_argument("--specs-dir", default="specs", help="project-relative specs directory (default: specs)")
    p.add_argument("--template", default=None, help="explicit spec template path (default: composed project template stack)")
    p.add_argument("--write-pointer", action="store_true", help="write .lanyant/feature.json (project opt-in)")
    return p


def main(argv: Optional[list] = None) -> int:
    args = _parser().parse_args(argv)
    description = " ".join(args.description).strip()
    if not description:
        _err("Error: Feature description cannot be empty or contain only whitespace")
        return 1

    root = Path(args.root).resolve()
    if not root.is_dir():
        _err(f"Error: project root '{root}' is not a directory")
        return 1
    try:
        specs_dir = _relative_inside(root, args.specs_dir, "--specs-dir")
    except ValueError as exc:
        _err(f"Error: {exc}")
        return 1

    config = _read_config(root)
    use_timestamp = args.timestamp or config.get("feature_numbering") == "timestamp"
    pointer_opt_in = args.write_pointer or config.get("write_feature_pointer") is True

    suffix = clean_name(args.short_name) if args.short_name else generate_short_name(description)
    if not suffix:
        _err(
            "[new-feature] Warning: Feature name is empty after removing unsupported characters. "
            "Use --short-name with letters or digits (for example, user-auth)."
        )

    requested = args.number
    if use_timestamp and requested:
        _err("[new-feature] Warning: --number is ignored when timestamp numbering is used")
        requested = ""

    if use_timestamp:
        feature_num = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    else:
        if requested:
            if not re.fullmatch(r"[0-9]+", requested):
                _err(f"Error: --number must be an unsigned integer, got '{requested}'")
                return 1
            number = _int64_from_digits(requested)
            if number is None:
                _err(f"Error: --number must be between 0 and {_MAX_FEATURE_NUMBER}, got '{requested}'")
                return 1
        else:
            number = highest_sequential_number(specs_dir) + 1
        if number > _MAX_FEATURE_NUMBER:
            _err(f"Error: feature number must be between 0 and {_MAX_FEATURE_NUMBER}, got '{number}'")
            return 1
        feature_num = f"{number:03d}"

        # An explicit number is a preference; move past it when its prefix is taken.
        if requested:
            requested_dir = specs_dir / fit_name(feature_num, suffix)
            reuse = args.allow_existing and requested_dir.is_dir()
            if not reuse and _prefix_exists(specs_dir, feature_num):
                requested_num = feature_num
                number = highest_sequential_number(specs_dir)
                while True:
                    number += 1
                    if number > _MAX_FEATURE_NUMBER:
                        _err(f"Error: feature number must be between 0 and {_MAX_FEATURE_NUMBER}, got '{number}'")
                        return 1
                    feature_num = f"{number:03d}"
                    if not _prefix_exists(specs_dir, feature_num):
                        break
                _err(
                    f"[new-feature] Warning: --number {requested_num} conflicts with "
                    f"an existing spec directory; using {feature_num} instead"
                )

    if _MAX_NAME_LENGTH - (len(feature_num) + 1) <= 0:
        _err("Error: feature number is too long for a feature name")
        return 1

    original = f"{feature_num}-{suffix}"
    name = fit_name(feature_num, suffix)
    if name != original:
        _err("[new-feature] Warning: Feature name exceeded the 244-byte limit")
        _err(f"[new-feature] Original: {original} ({len(original.encode('utf-8'))} bytes)")
        _err(f"[new-feature] Truncated to: {name} ({len(name.encode('utf-8'))} bytes)")

    feature_dir = specs_dir / name
    spec_file = feature_dir / "spec.md"
    feature_rel = feature_dir.relative_to(root).as_posix()
    # Check final resolved destinations before any directory/file mutation.
    try:
        for destination in (feature_dir, spec_file):
            destination.resolve().relative_to(root)
        if pointer_opt_in:
            (root / _POINTER_RELATIVE).resolve().relative_to(root)
    except (OSError, ValueError):
        _err("Error: feature, spec, or pointer path resolves outside the project root")
        return 1
    pointer_written = False

    if not args.dry_run:
        if feature_dir.is_dir() and not args.allow_existing:
            hint = (
                "Rerun to get a new timestamp or use a different --short-name."
                if use_timestamp
                else "Use a different feature name or specify a different number with --number."
            )
            _err(f"Error: Feature directory '{feature_dir}' already exists. {hint}")
            return 1

        template_content = None
        needs_spec = not spec_file.is_file()
        if needs_spec:
            if args.template is not None:
                template_path = Path(args.template)
                if template_path.is_file():
                    template_content = template_path.read_text(encoding="utf-8")
                else:
                    _err(f"Warning: Spec template not found at {template_path}; created empty spec file")
            else:
                sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "project-environment" / "scripts"))
                from common import TemplateResolutionError, resolve_template_content
                try:
                    template_content = resolve_template_content("spec-template", root)
                except (TemplateResolutionError, OSError, UnicodeError) as exc:
                    _err(f"Error: cannot resolve spec-template: {exc}")
                    return 1
                if template_content is None:
                    _err("Error: required spec-template was not found; no feature created")
                    return 1

        feature_dir.mkdir(parents=True, exist_ok=True)
        if needs_spec:
            if template_content is not None:
                spec_file.write_bytes(template_content.encode("utf-8"))
            else:
                spec_file.touch()

        if pointer_opt_in:
            pointer_written = write_pointer(root, feature_rel)

    if args.json:
        payload = {
            "FEATURE_DIR": str(feature_dir),
            "SPEC_FILE": str(spec_file),
            "FEATURE_NUM": feature_num,
        }
        if args.dry_run:
            payload["DRY_RUN"] = True
        if pointer_written:
            payload["POINTER_FILE"] = str(root / _POINTER_RELATIVE)
        sys.stdout.write(_json_line(payload))
    else:
        print(f"FEATURE_DIR: {feature_dir}")
        print(f"SPEC_FILE: {spec_file}")
        print(f"FEATURE_NUM: {feature_num}")
        if pointer_written:
            print(f"POINTER_FILE: {root / _POINTER_RELATIVE}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:  # pragma: no cover
        pass
    raise SystemExit(main())
