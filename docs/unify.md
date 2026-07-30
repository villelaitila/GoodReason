# `unify(S, J, C) → R` — the GoodReason query operation

`unify` is the **Unification Axiom** of the SuperGoodReasonModel (Eki Laitila, *Axiomatic Systems Science – Geometry of Thinking*, §3.4). Where a model **describes** a system, `unify` **queries** it: it judges a candidate object against a condition by passing it through the eight α–Ω roles and returning a structured, reasoned verdict — not a keyword match.

```
unify(S, J, C) → R
```

| Term | Name | What it is |
|---|---|---|
| **S** | model | A SuperGoodReasonModel — the 56-node α–Ω grammar for a domain. The standing lens. |
| **J** | condition | The question, optionally focused by a filter (which symbols, which ring depth). |
| **C** | candidate | The object being judged — a proposal, plan, deal, design, policy, artifact. |
| **R** | result | A per-symbol interpretation of *why* C satisfies / partially satisfies / fails J, plus an overall verdict, ring profile, conclusion and confidence. |

## When to use it

Reach for `unify` once a model **S already exists** for the domain and you want to **evaluate something against it**:

- **Score** a proposal/plan/deal/design against the systemic lens — "does this intervention actually close the loop?"
- **Compare** candidates: run the same J across each C and read the per-role R's side by side.
- **Find the weak role** — the single symbol where a plausible-looking artifact fails (in the Iran case it was Ω: no verification mechanism).
- **Let an AI agent answer new questions** against the model without re-deriving the whole analysis: S is the knowledge base, `unify` is the query.

It is *not* needed to build or visualize a model — it is specifically the **evaluation / retrieval step** that consumes one.

## The contract

### J — condition
```json
{
  "naturalLanguage": "Does the candidate contain a de-escalation off-ramp viable within 6 months?",
  "filter": { "symbols": ["phi", "tau", "omega"], "minRing": 3, "targetRing": 5 }
}
```
- `naturalLanguage` *(required)* — the question in plain words.
- `filter` *(optional)* — focus, not restriction:
  - `symbols` — id-form symbols the question primarily concerns (`alpha pi chi deltapsi beta phi tau omega`). **R must still assess all 8** (the balance rule — no role left unexamined).
  - `minRing`, `targetRing` — the interpretive depth expected (1–7; see the rings/circles in the model).

### C — candidate
```json
{ "type": "content-object", "title": "Draft US–Iran MoU (12 June 2026)", "content": ["…", "…"] }
```
- `title` *(required)*; `type`, `content` (string or list of strings), `source` *(optional)*.

### R — result
```json
{
  "verdict": "partially-satisfies",
  "interpretation": {
    "alpha": { "assessment": "satisfies", "why": "…" },
    "…": { "assessment": "…", "why": "…" }
  },
  "ringProfile": { "phi": 5, "tau": 4, "omega": 3 },
  "conclusion": "…",
  "confidence": "medium-high; degrades with distance from 2026-06-13"
}
```
- `verdict` *(required)* — overall: `satisfies` · `partially-satisfies` · `fails` · `unverifiable`.
- `interpretation` *(required)* — **one entry per symbol, all 8 required**. Each is `{ assessment, why }`, where `assessment` is `satisfies` · `partial` · `at-risk` · `fails`. This is the heart of the operation: the *why* per role.
- `ringProfile` *(optional)* — the ring depth reached on key symbols.
- `conclusion` *(required)* — the synthesis, ideally naming the repairs that would change the verdict.
- `confidence` *(optional)* — and, for time-sensitive domains, its decay.

## Worked example (Iran war)

The only worked instance in this repo lives in `specializations/iran-war/iran-war.supergoodreason-instance.json` under `unifyExample`. In summary:

- **J:** "Does the candidate contain a viable, implementable-within-6-months de-escalation off-ramp?" focused on φ/τ/Ω, rings 3→5.
- **C:** the draft US–Iran memorandum of understanding.
- **R:** **partially-satisfies** — *satisfies* on α (dual-victory framing) and ΔΨ (converts blockade pressure into a signature incentive); *partial* on π/β/τ; **fails on Ω** ("no named verification mechanism — the deal cannot observe its own compliance, stuck at ring 3"). Conclusion: viable as a 6-month off-ramp *conditional on two repairs* — name a verification mechanism (IAEA re-entry as first milestone) and decouple the Lebanon front.

That is the operation's payoff: not just *whether* C works, but *which role it fails on and what to fix*.

## Validation

`unify` objects are validated against `schema/unify.schema.json`. The repo validator checks both forms automatically:

```bash
uv run tools/validate_supergoodreason.py            # validates each instance's embedded unifyExample too
uv run tools/validate_supergoodreason.py path/to/query.unify.json   # a standalone unify object
```

## Authoring a unify query

1. Pick or build the model **S** for the domain.
2. Write **J**: the question + an optional symbol/ring filter.
3. Describe **C**: the candidate object.
4. Produce **R**: assess all 8 symbols (`assessment` + `why`), set the overall `verdict`, add `ringProfile`, write a `conclusion` that names the fixes, and a `confidence`.
5. Validate against `schema/unify.schema.json`.

## Status

- `unify` is **defined in Eki's paper** and **specified here**; it is an *application-layer* operation. It is **not** part of `model/SuperGoodReasonModel.json` (the canonical template describes structure, not queries) and is intentionally separate from `SuperGoodReasonModel.schema.json`.
- Standalone unify queries use the convention `*.unify.json`; embedded examples use the `unifyExample` key inside an application instance.
