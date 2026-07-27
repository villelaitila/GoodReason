# Submarine safety — placed into the SuperGoodReason form

A **placement study**: every substantive thesis in a nuclear-submarine reliability corpus (SUBSAFE, Naval Reactors / Rickover, UK MOD Safety Case, PRA, SPAR-H / CREAM) assigned to its most defensible `(sector, level)` location in the 8 × 7 form, so that *unoccupied* locations become visible as candidate blind spots.

This is not yet a full model or an application instance — it is the step before both. It answers one question: **where does an existing body of engineering knowledge fail to reach the form?**

## Files

```
placement.json   the data — 65 source theses + 20 proposed completions, tensions, triads
template.html    the page, with a /*__DATA__*/ token where the data is injected
index.html       built artifact (template + data), self-contained, no external requests
```

## Build

```bash
python3 -c "
import json; d=json.load(open('placement.json')); t=open('template.html').read()
open('index.html','w').write(t.replace('/*__DATA__*/null', json.dumps(d,ensure_ascii=False,separators=(',',':'))))"
```

`placement.json` is the single source of truth. Argue with the placement there; the page follows.

## Placement rule

An item is placed where the model's own level semantics fit its **function**, not where its vocabulary superficially matches. One location may hold many items. Three states distinguish what is actually there:

| State | Meaning |
|---|---|
| `evidence` | A working mechanism with a means of verification. |
| `asserted` | Stated as principle; the corpus supplies no instrument that would implement or measure it. |
| `thin` | A single acknowledgement, a limitation, or a historical instance — not a standing capability. |

A location counts as **empty** only when no thesis performs that function at all. That is a falsifiable claim: produce a thesis that belongs there and the gap closes.

## Result

**41 of 56 locations occupied. 15 empty — and 13 of those sit at level 5 or above.**

The pattern is not a weak sector. It is a **ceiling**: the architecture is close to complete at levels 1–4 (component, system, coordination, control) and thins to nothing at 5–7 (development strategy, mission, worldview). The missing VSM System 4 at β5 is one instance of a gap that runs across the whole form.

Three empties are load-bearing, and they form a triangle:

- **τ4** — exosystem / interfaces. No owner for propagation routes crossing a certification boundary. The Thresher cascade crossed the post-1963 boundaries four times.
- **β5** — VSM System 4. No environment-scanning or future-adaptation function, while β4 (System 3) holds six items.
- **Ω6** — metacybernetics. Every audit checks conformance to a standard that nothing ever re-examines.

Structure draws the boundary, implementation crosses it, feedback never observes the crossing.

The **circle profile** confirms it on the second axis: 47 of 65 theses sit at circles 1–2 (rules known, environment slow, feedback reinforcing the current way of operating). The only circle-6 items are the Thresher chain and the 1963 founding of SUBSAFE — the system knows disruption as history, not as a state it could currently be in.

## The page

`index.html` renders the 56-cell register and steps proposed completions into the empty locations one press at a time, in load-bearing order. Each proposal carries a provenance mark — **AI-derived** where the gap is structural and derivable from the form, **human authority** where it needs mandate or domain judgement, **co-produced** where AI structures the gap and humans supply the evidence — and a `why` naming the reason that location is empty, often citing the model's own `failure_note`.

The intended use is the realistic entry route for this method in a regulated engineering domain: **a design-review and safety-case challenge aid**, not a governance layer. The page does not claim to know more about submarines than the certifying authority. It claims to know which questions were never asked, and it offers each one in a form an engineer can refute in a sentence.

## Limits

Placement is interpretation, and some assignments are genuinely arguable — CDF/LSR sit at χ2 (metasystemic view) rather than Ω because they are predictions rather than observations; the UK regulatory framework sits at φ7. Those are the right things to argue about, because the argument *is* the review the instrument exists to provoke.

The study rests on one open-source secondary synthesis. Some empty locations may be documentation gaps rather than architectural ones; run against primary programme material, several red cells would likely fill. That does not weaken the method — it is the method's first useful output.
