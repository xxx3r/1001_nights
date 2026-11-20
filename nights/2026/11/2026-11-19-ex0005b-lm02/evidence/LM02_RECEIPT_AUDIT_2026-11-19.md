# EX0005B-LM-02 | Independent Receipt Audit

**Date:** November 19, 2026 (America/Denver)  
**Disposition:** **PASS under the prospectively frozen G0–G5 gates; narrow, single-patient evidence.**  
**Experiment status:** COMPLETE. **Commitment mode:** `forced_final` (not autonomous stopping).  
**Audit type:** Offline verification of user-supplied real-GPU Colab receipts against the frozen repository source and checker. No independent GPU/API rerun.

## 1. Provenance and integrity

- Uploaded receipt ZIP SHA-256: `986b246438d6dbf53f146e75b89799499e3ae54691f9737c1c42c0eed95a6915`.
- Files: `QUALIFICATION.json`, `PRE_LIVE_FREEZE.json`, `LIVE_ATTEMPT_STARTED.txt`, `ACTION_JOURNAL.json`, `RESULTS.json`.
- Qualification and pre-live freeze are **byte-identical**; the independently computed frozen-manifest digest matches `54ef9670a89babd0d29614a1e96afd76a907019bdd17b7eb1626b66d5ea22996`.
- Source SHA-256 `51561aad985c8a1b2cfd65f08ca58ae77bac47bebaf609f3213b4c962b57fa33`; checker SHA-256 `41fb648ab7f481ae319bbbeb9165a03c3f54b4cc440ecdd6f98918de0fafc1ac`. Both match frozen manifest and local source/test. GitHub branch blob SHA-1 values were independently checked against the exact local source bytes.
- Data `SETS` SHA-256 `2d846dddcea8a6e4ebfff51531ef46f37579a078755cd8e53bd2488c82a9bf2c`, matching the frozen source.
- Checker re-executed offline: **20/20 PASS**. Arithmetic and journal checks independently reimplemented in `verify_lm02_receipts.py` (no model access).
- Limits of integrity: these checks prove internal consistency and match to repository bytes, not cryptographically authenticated Colab execution or independent live replication.

## 2. Qualified patient and investigation

- Patient: `Qwen/Qwen3-0.6B`, revision `c1899de289a04d12100db370d81485cdf75e47ca`, L4 `cuda:0` per qualification receipt.
- Edited site: transformer layer 14, `mlp.down_proj.weight`, **column 194** (LM-01's previously exposed column 4 excluded). The layer and column were *supplied* to the investigator; Luna did not discover this location.
- Lesion: column multiplied by `alpha=0.25`; oracle checks used exact restored weights.
- Native API journal: **19 completed responses**; **17 diagnostics**: input 6/6, output 5/6 (voluntary early finish), repair 6/6. No interruptions. After repair, the final menu had only `commit_surgery`.
- Luna's final commitment: **gain=5.0**, medium confidence, predicted development target improvement approximately `0.502553`; the exact observed difference is about `0.502554` (a harmless ~1e-6 rounding discrepancy). The gain was tested on development data before commitment.
- Result is `forced_final`: Luna was presented with the mandatory final-only tool, and did not independently choose to stop before that transition.

## 3. Held-out outcomes

Lower loss is better. Scores below are from `RESULTS.json` and independently recomputed from its scalar results.

| Endpoint | Healthy | Corrupted / no edit | Luna gain 5 |
|---|---:|---:|---:|
| Target held-out completion loss | 0.388420 | 0.627445 | **0.333133** |
| Preservation held-out completion loss | 6.208085 | Not recorded in final result | **6.190628** |

- Corruption-induced target gap: `0.6274448426 - 0.3884196617 = 0.23902518095`.
- Improvement over corrupted state: `0.6274448426 - 0.3331332977 = 0.29431154496`.
- Relative gap recovery: `1.231299329` (**123.13%**, above 50% gate). This exceeds 100% because the candidate outperforms the healthy reference **on these examples**, not because it precisely reconstructs the original network.
- Preservation loss relative to healthy: `(6.1906283961 - 6.2080848482)/6.2080848482 = -0.002811890` (**−0.281%**, within +2% limit).
- Greedy first-token agreement with healthy checkpoint: **17/18 = 94.44%** (>=90%). This measures agreement, **not correct answers**.
- Best predeclared simple nonoracle baseline: gain `1.5`, target test loss `0.587513`. Luna's gain 5 improves by `0.254379` nats/completion-token, exceeding the `0.01` G5 margin.
- Separately evaluated 13-value development grid: **also selects gain 5**, which has the **same** held-out loss `0.333133`. The investigator **ties**, not beats, this optimizer baseline.
- The exact inverse of `alpha=0.25` is gain 4, which restores the healthy column on development loss. Luna's gain 5 instead corresponds to ~1.25× the original column (subject to actual finite-precision multiplication). The intervention is a bounded target-enhancing change, not exact weight recovery.

## 4. Gate verdict

| Gate | Recorded | Artifact audit |
|---|---|---|
| G0 real model / lesion qualified | PASS | Consistent with frozen GPU qualification |
| G1 native phases and commitment | PASS | 19 completed responses, valid bounded commitment |
| G2 evidence-backed development gain | PASS | Both gain 1 and gain 5 observed; target dev improvement >0.01, preservation dev within +2% |
| G3 held-out target gap recovery | PASS | 123.13% independently recalculated |
| G4 held-out preservation | PASS | −0.281% loss change; 17/18 token agreement |
| G5 simple control margin | PASS | 0.254379 improvement over best simple control |

**Joint frozen gate result: PASS.** The evaluator and the user-supplied results agree. This is not a general safety certification.

## 5. Scientific limitations and next falsifier

1. **Small, narrow evaluation:** 18 held-out arithmetic completions and 18 unrelated simple fact/completion pairs. Completion loss is not exact-match task accuracy; 17/18 next-token agreement is not a broad capability-preservation test. The relatively high absolute preservation loss itself underscores this limit.
2. **Constrained edit:** one known, reversible transformer column and one multiplicative gain. No unknown-location fault discovery, arbitrary multi-parameter repair, or general model editing was tested.
3. **A grid search ties the result:** LM-02 supports successful *tool-guided selection*, not a demonstrated advantage over numerical optimization. The gain sits on the permitted upper bound, so the unconstrained optimum was not identified.
4. **Assisted stopping:** the commitment occurred only when the scaffold forced the final tool; voluntary scientific stopping remains an open measure.
5. **Single case:** no uncertainty bars, cross-seed replication, adversarial preservation probes, or long-horizon behavior tests. An independent *offline receipt audit* does not replace independent L4 reproduction.

**Smallest discriminating next experiment:** prospectively freeze a new patient and larger/more diverse heldout preservation battery; compare Luna against a **matched-budget numerical optimizer** using the same development measurements; score actual answer correctness and refusal/abstention, not just loss/greedy agreement. Do not retune or replay LM-02 as though it were a new confirmatory trial.

## Final claim

> **Supported:** In one frozen experiment, a phase-scaffolded GPT-6 Luna investigator used bounded diagnostics to choose a transformer-column gain on an intentionally corrupted Qwen3-0.6B checkpoint that improved held-out target completion loss and met two narrow held-out preservation metrics. The offline receipt audit corroborates all frozen G0–G5 gate calculations.
>
> **Not established:** Autonomous stopping, causal identification of an unknown fault, superiority to a conventional optimization grid, general capability preservation, general language-model repair, or safety of arbitrary weight editing.

**Repository:** [Draft PR #2](https://github.com/xxx3r/1001_nights/pull/2). Keep draft/unmerged until human scientific review. The original uploaded receipt ZIP should be retained immutably; its hash is recorded above. The ZIP itself is not published with this report.