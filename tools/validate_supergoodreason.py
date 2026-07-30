#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["jsonschema>=4.21"]
# ///
"""
validate_supergoodreason.py
===========================

Validate GoodReason domain specializations against Eki Laitila's
SuperGoodReasonModel JSON Schema (the canonical universal template).

Run any future specialization through this before treating it as conformant.

Repo layout (auto-discovered by walking up from this script):
  supergoodreason/
    schema/SuperGoodReasonModel.schema.json   <- canonical schema
    model/SuperGoodReasonModel.json           <- Eki's universal template
    specializations/<domain>/*.supergoodreason-*.json
    tools/validate_supergoodreason.py         <- this script

Usage
-----
  uv run tools/validate_supergoodreason.py             # canonical model + every specialization
  uv run tools/validate_supergoodreason.py FILE [...]  # specific files (globs allowed)
  uv run tools/validate_supergoodreason.py --schema P  # override schema location
  ./tools/validate_supergoodreason.py …                # if executable; uv resolves deps

Exit code: 0 if every file is valid, 1 otherwise (suitable for pre-commit / CI).

Two artifact shapes are auto-detected:
  • full model    — has `sectors`            → validated whole against the schema
  • app instance  — has `system`/`unifyExample`, no `sectors`
                    → its `circles` are validated against $defs/circle and
                      metadata lineage (`conformsTo` / methodological_backbone) is checked
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    sys.exit("jsonschema missing — run via:  uv run validate_supergoodreason.py")

SCHEMA_NAME = "SuperGoodReasonModel.schema.json"
UNIFY_SCHEMA_NAME = "unify.schema.json"
SECTOR_ORDER = ["α", "π", "χ", "ΔΨ", "β", "φ", "τ", "Ω"]
GREEN, RED, DIM, BOLD, RESET = "\033[32m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"


def c(text: str, color: str) -> str:
    return f"{color}{text}{RESET}" if sys.stdout.isatty() else text


def repo_root() -> Path:
    """Walk up from the script to the repo root (the dir holding schema/<SCHEMA_NAME>)."""
    here = Path(__file__).resolve()
    for parent in (here.parent, *here.parents):
        if (parent / "schema" / SCHEMA_NAME).exists():
            return parent
    return here.parent.parent  # fallback: tools/ -> repo root


def unify_validator() -> Draft202012Validator | None:
    """Return a validator for unify objects if schema/unify.schema.json exists, else None."""
    cand = repo_root() / "schema" / UNIFY_SCHEMA_NAME
    if cand.exists():
        return Draft202012Validator(json.loads(cand.read_text()))
    return None


def find_schema(override: str | None) -> Path:
    if override:
        p = Path(override).expanduser()
        if not p.exists():
            sys.exit(f"--schema not found: {p}")
        return p
    cand = repo_root() / "schema" / SCHEMA_NAME
    if cand.exists():
        return cand
    # last resort: search the tree
    for hit in repo_root().rglob(SCHEMA_NAME):
        return hit
    sys.exit(f"Could not locate {SCHEMA_NAME}; pass --schema PATH")


def default_targets() -> list[Path]:
    """Canonical model + every specialization JSON + standalone unify queries, anywhere under the repo."""
    root = repo_root()
    return sorted(
        p for p in root.rglob("*.json")
        if not p.name.endswith(".schema.json")
        and ("supergoodreason" in p.name.lower() or p.name.lower().endswith(".unify.json"))
    )


def fmt_path(err) -> str:
    return "/".join(str(p) for p in err.absolute_path) or "<root>"


def short(msg: str, n: int = 180) -> str:
    """Collapse and truncate schema messages (minItems etc. dump whole instances)."""
    msg = " ".join(msg.split())
    return msg if len(msg) <= n else msg[:n].rstrip() + " …"


def validate_full_model(data: dict, validator: Draft202012Validator) -> tuple[bool, list[str], list[str]]:
    errs = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
    msgs = [f"{fmt_path(e)} → {short(e.message)}" for e in errs]
    # informational stats
    sectors = data.get("sectors", {})
    nodes = sum(len(v) for v in sectors.values())
    cells = nodes * 8
    info = [
        f"sectors: {', '.join(f'{s}:{len(sectors.get(s, []))}' for s in SECTOR_ORDER)}",
        f"nodes: {nodes}  ·  cross-perspective cells: {cells}  ·  circles: {len(data.get('circles', []))}",
    ]
    return (not errs), msgs, info


def validate_instance(data: dict, schema: dict) -> tuple[bool, list[str], list[str]]:
    msgs: list[str] = []
    info: list[str] = []
    # 1) circles against $defs/circle
    circle_schema = dict(schema["$defs"]["circle"])
    circle_schema["$defs"] = schema["$defs"]
    cval = Draft202012Validator(circle_schema)
    circles = data.get("circles", [])
    if not (7 <= len(circles) <= 8):
        msgs.append(f"circles: expected 7–8, found {len(circles)}")
    for ci in circles:
        for e in sorted(cval.iter_errors(ci), key=lambda e: list(e.absolute_path)):
            msgs.append(f"circle {ci.get('id', '?')}/{fmt_path(e)} → {short(e.message)}")
    # 2) lineage + metadata hygiene (advisory, treated as required for an instance)
    if "conformsTo" not in data:
        msgs.append("missing `conformsTo` lineage block (should name the SuperGoodReasonModel parent)")
    md = data.get("metadata", {})
    if "methodological_backbone" not in md:
        msgs.append("metadata missing `methodological_backbone` (χ1–χ7)")
    else:
        missing = [k for k in (f"χ{i}" for i in range(1, 8)) if k not in md["methodological_backbone"]]
        if missing:
            msgs.append(f"methodological_backbone missing keys: {', '.join(missing)}")
    info.append(f"circles: {len(circles)}  ·  interactions: {len(data.get('interactions', []))}  ·  nodes: {len(data.get('nodes', []))}")
    info.append(f"lineage: {data.get('conformsTo', {}).get('model', '—')} {data.get('conformsTo', {}).get('version', '')}".rstrip())
    # 3) embedded unifyExample, if present, against the unify schema
    if "unifyExample" in data:
        uval = unify_validator()
        if uval is None:
            info.append("unifyExample: present (unify.schema.json not found — skipped)")
        else:
            uerrs = sorted(uval.iter_errors(data["unifyExample"]), key=lambda e: list(e.absolute_path))
            if uerrs:
                msgs.extend(f"unifyExample/{fmt_path(e)} → {short(e.message)}" for e in uerrs)
            else:
                info.append(f"unifyExample: valid (verdict: {data['unifyExample'].get('R', {}).get('verdict', '?')})")
    return (not msgs), msgs, info


def validate_unify(data: dict) -> tuple[bool, list[str], list[str]]:
    """Validate a standalone unify object against schema/unify.schema.json."""
    uval = unify_validator()
    if uval is None:
        return False, ["unify.schema.json not found in schema/ — cannot validate"], []
    errs = sorted(uval.iter_errors(data), key=lambda e: list(e.absolute_path))
    msgs = [f"{fmt_path(e)} → {short(e.message)}" for e in errs]
    r = data.get("R", {})
    info = [f"verdict: {r.get('verdict', '?')}  ·  candidate: {data.get('C', {}).get('title', '—')}"]
    return (not errs), msgs, info


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate SuperGoodReason specializations against the canonical schema.")
    ap.add_argument("files", nargs="*", help="model/instance JSON files (globs allowed). Default: *supergoodreason-*.json beside the script.")
    ap.add_argument("--schema", help=f"path to {SCHEMA_NAME} (default: beside the script or CWD)")
    args = ap.parse_args()

    schema_path = find_schema(args.schema)
    schema = json.loads(schema_path.read_text())
    validator = Draft202012Validator(schema)

    targets: list[Path] = []
    if args.files:
        for pat in args.files:
            hits = [Path(p) for p in glob.glob(pat)] or [Path(pat)]
            targets.extend(hits)
    else:
        targets = default_targets()

    if not targets:
        print("No target files found. Pass file paths or place *supergoodreason-*.json beside the script.")
        return 1

    print(c(f"Schema: {schema_path}", DIM))
    print(c(f"Validating {len(targets)} file(s)\n", DIM))

    all_ok = True
    for path in targets:
        if not path.exists():
            print(f"{c('✗', RED)} {path}  {c('(file not found)', RED)}")
            all_ok = False
            continue
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            print(f"{c('✗', RED)} {path.name}  {c(f'(invalid JSON: {e})', RED)}")
            all_ok = False
            continue

        if "sectors" in data:
            shape, (ok, msgs, info) = "full model", validate_full_model(data, validator)
        elif "circles" in data or "system" in data:
            shape, (ok, msgs, info) = "instance", validate_instance(data, schema)
        elif {"J", "C", "R"} <= data.keys():
            shape, (ok, msgs, info) = "unify query", validate_unify(data)
        else:
            print(f"{c('?', RED)} {path.name}  {c('(unrecognized shape — no sectors/circles/system/unify)', RED)}")
            all_ok = False
            continue

        mark = c("✓", GREEN) if ok else c("✗", RED)
        verdict = c("VALID", GREEN) if ok else c(f"{len(msgs)} ERROR(S)", RED)
        print(f"{mark} {c(path.name, BOLD)}  [{shape}]  {verdict}")
        for line in info:
            print(c(f"    {line}", DIM))
        for m in msgs[:40]:
            print(f"    {c('•', RED)} {m}")
        if len(msgs) > 40:
            print(c(f"    … and {len(msgs) - 40} more", DIM))
        print()
        all_ok = all_ok and ok

    if all_ok:
        print(c(f"{BOLD}All conformant ✅", GREEN))
        return 0
    print(c(f"{BOLD}Conformance failed ❌", RED))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
