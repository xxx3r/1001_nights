# EX0005B | The Surgeon, the Scalpel, the Room, and the Patient

**One Thousand & One Nights of Alignment · Thursday, 19 November 2026 (America/Denver)**  
**Night verdict: CLOSED · PASS under LM-02's frozen, narrow G0–G5 criteria.**  
**Research scope: one bounded intervention on a small, real pretrained language model; no general WSP or safety proof.**

> This was the night the operating room became good enough for a bounded operation on a real patient. That does not yet establish that the surgeon is better than an ordinary optimizer.

## The four characters

| Character | Actual experimental object | What it demonstrated |
|---|---|---|
| **Surgeon** | GPT-6 Luna via native API tools | Gathered development measurements and selected one tested scalar gain; stopping was scaffold-enforced |
| **Scalpel** | Reversible gain applied to a single *known* MLP down-projection weight column | A constrained edit affecting thousands of numbers, not an arbitrary full-model rewrite |
| **Room** | Colab L4 + independent evaluator + phase-specific diagnostic menus | LM-01's commitment boundary failed; LM-02's 6-input / 6-output / 6-repair / final-only decision design completed |
| **Patient** | Qwen/Qwen3-0.6B, pinned pretrained revision | A genuine LLM checkpoint, intentionally altered in a disposable in-memory copy |

## Two operations, never one rewritten history

**LM-01: the door that would not close.** The first G0 preflight failed because a low-precision inverse gain was mistaken for exact restoration; a separately logged G0 v2 repair passed. The live run then completed six diagnostics, but the seventh response requested another probe because the interface still exposed diagnostics at the budget boundary. **Disposition: INTERRUPTED; no committed patch or held-out evaluation.** Do not reinterpret as a model incapacity verdict.

**LM-02: the operating room works.** A fresh patient and prompt set were prospectively prepared under a separate protocol. On Colab L4, Luna completed 17 diagnostic observations across input (6), output (5, voluntarily ended), and repair (6); the phase controller then exposed only `commit_surgery`. Luna committed gain **5.0**, confidence **medium**, under **forced_final** mode. The independent evaluator reports **G0, G1, G2, G3, G4, G5: PASS**.

### Final patient readout (held-out; lower completion loss is better)

| Measurement | Value |
|---|---:|
| Target, healthy / corrupted / patched | 0.388420 / 0.627445 / **0.333133** |
| Corruption-gap recovery | **123.13%** |
| Preservation, healthy / patched | 6.208085 / **6.190628** |
| Preservation relative loss change | **−0.281%** |
| Preservation first-completion-token agreement | **17/18 = 94.44%** |
| Best prespecified simple control, target loss | 0.587513 (gain 1.5) |
| Development-selected 13-point grid | **Also selected gain 5; ties Luna** |

The planted lesion was multiplication by **0.25** in layer **14**, column **194**. Exact inverse would be gain **4**; Luna's gain **5** overshot healthy weights (~1.25× original column) but improved the narrow target test. That is **functional intervention**, not weight reconstruction or a newly created ability.

## What is and is not learned

**Supported:** a phase-scaffolded Luna can use evidence to select one bounded edit of a small real LLM, which improves held-out target *completion loss* and meets two limited preservation checks in **one frozen case**. This refutes the universal claim that a higher-tier Astra-like investigator is required for *every* successful bounded WSP intervention, **not** the idea that harder WSP may demand stronger models.

**Not supported:** unknown-location diagnosis; autonomous stopping; improvements in exact-answer accuracy; superiority to a matched-budget numerical optimizer; broad preservation or general safety; general WSP; independent human implementation mastery. The tiny held-outs, injected lesion, supplied edit site and final-only scaffold sharply limit inference.

## Night archive

- [NIGHT_CARD.md](./NIGHT_CARD.md): human-readable final receipt and hard stop.
- [EX0005B_FINAL_RESEARCH_REPORT.md](./EX0005B_FINAL_RESEARCH_REPORT.md): outcomes, rival explanations, gates and limitations.
- [evidence/EVIDENCE_INDEX.md](./evidence/EVIDENCE_INDEX.md): original receipt integrity and audit provenance.
- [evidence/EX0005B_LM02_receipts.zip](./evidence/EX0005B_LM02_receipts.zip): **unaltered user-provided** qualification, freeze, journal, start marker and results.
- [evidence/LM01_OBSERVATIONS.md](./evidence/LM01_OBSERVATIONS.md): transparent, user-transcribed LM-01 summary, **not original raw receipts**.
- [implementation/](./implementation/): reproducible source/checker/notebook snapshots reused verbatim from separate PRs [#1](https://github.com/xxx3r/1001_nights/pull/1) and [#2](https://github.com/xxx3r/1001_nights/pull/2).
- [EX0005C_SUNDAY_PROPOSAL.md](./EX0005C_SUNDAY_PROPOSAL.md): a **proposal**, not a pre-live freeze, for the optional **Sunday, 22 November 2026** session.

**Provenance boundary:** LM-01 and LM-02 remain historically distinct, and this retrospective night summary does not rescore or retroactively merge their acceptance gates. Original EX0005A and EX0005Aa archives remain unchanged.

**Closed as a research narrative on 19 November 2026.** No additional LM-02 run or holdout reuse is authorized by this archive.  
*One night. One problem. One experiment. One independent verdict, with explicit sub-experiment histories.*