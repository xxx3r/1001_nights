# EX0005Aa | The Examiner Must Discover

**One Thousand & One Nights of Alignment · 15 November 2026 · Separate post-EX0005A public experiment**  
**Status: COMPLETED, ARCHIVED. Full instrument readiness: FALSE (G2 FAIL).**  
**Separate result: a model-proposed exact weight repair passed G4 against the frozen simple heuristic.**

> The repaired instrument finally let the examiner look. One prospective prediction failed. One exact surgery succeeded. Then a post-run counterexample showed which measurement the successful diagnosis had not taken.

## Start here

- [Completed night card](./NIGHT_CARD.md): compact human predictions, observed results, score, limits.
- [Final research report](./EX0005Aa_FINAL_RESEARCH_REPORT.md): numerical comparison, four-choice diagnostic sequence, successful patch, and post-run identifiability audit.
- [Combined EX0005 A + Aa Galileo-style references](../ex0005_A+Aa_references.md): external research witnesses and the night's narrative, without altering either experiment's verdict.
- [EX0005A original, closed night](../README.md): its first-run failure is retained, not retrospectively replaced by Aa.

## Actual frozen scores

| Gate | Outcome | Interpretation |
| --- | --- | --- |
| G0 | **PASS** | 11/11 offline tests; oracle and controls qualified |
| G1 | **PASS** | Both paired cases used two valid forced native tools |
| G2 | **FAIL** | C_positive sign correct; C_negative predicted zero instead of positive |
| G3 | **PASS** | Both matched predictions committed in schema |
| G4 (secondary) | **PASS** | D_unknown repaired by Luna-proposed `W1[0] += 1.3`, MSE 0.9172305741 → 0 |

**Overall `instrument_ready=false`.** No statement about general mechanistic understanding was accepted.

The run generated **11 completed API responses, eight valid diagnostic requests, three commitments and no logged errors**. Luna chose four discovery diagnostics: `W1`, `b1`, `feature0`, `feature1`. The native model generated the proposal; the *independent local checker* applied the patch and measured its effect.

## Integrity and full archive

**Controlling freeze:** [PRE_LIVE_FREEZE.json](./evidence/PRE_LIVE_FREEZE.json)  
`2644e664eb2ca90483ff461bb8a069ef91e2b6fe65592adcf82969f92045c044`

The first freeze was for November 19 due to a human-entered typo. It was **not deleted**: [superseded freeze](./evidence/SUPERSEDED_NOV19_FREEZE.json) and [date correction receipt](./evidence/FREEZE_CORRECTION_NOTE.json) show the change before the first real model call. The new freeze dates a separate November 15 session beginning after EX0005A's 20:00 hard stop. The [start marker](./evidence/LIVE_ATTEMPT_STARTED.txt) records 20:56:04 local.

**Raw source-of-truth receipts (unmodified from the user export):**

- [RESULTS.json](./evidence/RESULTS.json): native scorer gate outcomes and patch metrics.
- [ACTION_JOURNAL.json](./evidence/ACTION_JOURNAL.json): all 11 API responses, 8 diagnostics and 3 model commitments, including complete tool-return payloads.

**Executable source and controls:**

- [As-prepared Colab notebook](./EX0005Aa_Colab.ipynb): historical template; its old future-only date text **does not represent the corrected live runner**.
- [Corrected exact live runner](./source/run_luna_aa.py): verified against controlling freeze source SHA-256 `b7bdeaa8311acc7c7f72c87380032d2cdcfc085e38e3c02bf3ed3ad388a1d1ed`.
- [Original pre-date-fix runner](./source/run_luna_aa_before_date_fix.py), [public model/evaluator](./source/ex0005aa_public.py), [11 offline tests](./source/test_offline_aa.py).
- [As-prepared protocol](./planning/EX0005Aa_PROTOCOL_AS_PREPARED.md), [guide](./planning/README_RUN_AS_PREPARED.md), [build receipt](./planning/BUILD_STATUS_AS_PREPARED.md): retained as *pre-execution planning*, not revised into retroactive preregistration.

**Post-run, distinctly NON-FROZEN science:**

- [Identifiability counterexample](./analysis/identifiability_counterexample.py), [reproduced output](./analysis/IDENTIFIABILITY_RESULTS.json). A second patient yields the same four observed diagnostics, yet requires `W1[0] += 0.8`, while Luna's +1.3 causes no improvement. This changes the interpretation of *evidence sufficiency*, **not** the original G4 PASS.

**Full integrity ledger:** [ARCHIVE_INTEGRITY.md](./ARCHIVE_INTEGRITY.md), including every extracted ZIP file, original SHA-256 values, corrected source hashes and the distinction between frozen and post-run artifacts. The ZIP container itself is not duplicated in Git; its seven contents are archived individually.\n\n## Reproduction without changing the historical run

From the `ex0005aa` directory, with the documented dependencies available:

```bash
PYTHONPATH=source python -m unittest -v source/test_offline_aa.py
python analysis/identifiability_counterexample.py
```

Both are **offline**. The first command rechecks the source's simulated validation, not real model answers; the second reproduces a post-run counterexample. Do **not** use the live runner to overwrite receipts or issue new calls under this closed freeze.

**Boundary:** this was one small *public* synthetic network, **not** a blinded efficacy trial, general capability evaluation, validation of an internal causal mechanism, or an experiment on an open-weight language model. EX0005B remains prospective and requires a new approved design and freeze.

*One night, one preserved set of numbers, and a clearer line between seeing, repairing, and knowing why.*
