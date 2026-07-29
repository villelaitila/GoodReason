# GoodReason — SuperGoodReasonModel & tooling

> **Part of the GoodReason project.** GoodReason is documented across two repositories:
>
> - **[goodreason-systemic-method](https://github.com/EkiLaitila/goodreason-systemic-method)** — the method and the reasoning behind this model. **New to GoodReason? Start there.**
> - **GoodReason / SuperGoodReason** — *you are here* — the runnable model, schema, validator, and domain specializations.

A home for the **SuperGoodReasonModel** — a universal α–Ω systemic configurator — together with the tooling and domain **specializations** built on it.

The model expresses GoodReason as a machine- and human-readable systemic ontology: **8 sectors × 7 levels = 56 nodes**, each node cross-described through all 8 symbols, plus a 7-circle depth coordinate. It carries failure realism, a Viable-System-Model mapping (β), an ecological scale ladder (τ), reflexive researcher/object modes (α and Ω), an emancipatory lens (Δψ), and a χ methodological backbone. From this universal template, specialized models are generated for any System of Interest while the α–Ω form is preserved.

## Layout

```
schema/          SuperGoodReasonModel.schema.json   — canonical JSON Schema (the conformance contract)
model/           SuperGoodReasonModel.json          — the universal template
                 CANONICAL-MODEL-README.md          — notes on the model
specializations/ <domain>/                          — domain models generated from the template
                 iran-war/                          — the 2026 Iran war (first specialization)
tools/           validate_supergoodreason.py        — schema validator (uv, self-contained)
docs/            unify.md                           — the unify(S, J, C) → R query operation
```

## Validate

The validator runs via [uv](https://docs.astral.sh/uv/) with inline dependencies — no virtualenv setup needed:

```bash
uv run tools/validate_supergoodreason.py            # validate the canonical model + every specialization
uv run tools/validate_supergoodreason.py path/to/new.supergoodreason-model.json
```

Exit code is 0 if everything conforms, 1 otherwise — suitable for pre-commit or CI. It auto-detects two artifact shapes: **full models** (`metadata` + `sectors` + `circles`, validated whole against the schema) and **application instances** (which add `system`/`unifyExample`; their `circles` and lineage are checked).

## Two artifact kinds

- **Full model** (`*.supergoodreason-model.json`) — a complete schema-conformant clone of the template, specialized to a domain. All 56 nodes × 8 perspectives populated.
- **Application instance** (`*.supergoodreason-instance.json`) — an application built *on* a model: adds the System/Meaning of Interest, pairwise interactions, and the executable `unify(S, J, C) → R` operation.

### The `unify` query operation

Where a model *describes* a system, **`unify(S, J, C) → R`** *queries* it — judging a candidate object **C** against a condition **J** through the model **S**, returning a structured per-symbol verdict **R** (not a keyword match). Standalone queries use `*.unify.json`; an embedded worked example lives under `unifyExample` in an instance. Full spec: **[`docs/unify.md`](docs/unify.md)**, validated against `schema/unify.schema.json`.

## Adding a specialization

1. Create `specializations/<domain>/`.
2. Generate `<domain>.supergoodreason-model.json` following the schema (8 sectors × 7 levels, each node cross-described through all 8 symbols, with the required per-sector notes).
3. Run the validator until it reports 0 errors.
4. Optionally add an application instance and a short `README.md`.
