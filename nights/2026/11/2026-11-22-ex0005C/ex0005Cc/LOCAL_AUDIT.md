# EX0005Cc v1 local design audit

Date: 2026-11-22 (no remote GPU run)

## Evidence preserved
- User-provided immutable historical ZIP: `/mnt/data/EX0005C_v03_PRE_FLIGHT_receipts.zip` SHA-256 `6d07111bcaf81af2a123f12ea12887b3d222e162347b111d7ef2d92b0a80ce01`.
- Historical reported G0: 23/24 correctness, 24/24 completed; disqualified by predeclared ceiling. No Luna surgery or holdout scoring.
- Historical ZIP was READ, not modified. Its manifest IDs were used for source-family exclusions only; its hidden heldout text remains outside the new calibration notebook.

## New AET work completed locally
- Source-verified Apple GSM-Symbolic `main`, `p1`, `p2`, model card and pinned historic sources.
- Defined four strata (including original independently formula-checked synthetic arithmetic stories), 8 pilot items each, and six prospective fixed mixtures.
- Implemented selection based only on stratum-level average correctness/completion; target 55% and eligibility 30-75% correct, >=75% complete.
- Exclusion of historical EX0005C selected Apple template IDs and GSM8K ordinary heldout IDs. Apple original-ID families are unique across pilot and reserved future validation samples.
- Explicit max 90-minute pilot, one run, fail closed on model/schema/test problems; no surgeon tools, no output-weight edits, no holdout evaluator.
- Preserved v0.3 scorer source exactly (SHA-256 `ce0fe0b4633e9c3175889b763fe91fa25e231f5e0889d061e24ee28bd23649ed`).
- Offline tests: 18/18 PASS. Notebook JSON format and Python code-cell syntax parse PASS. Embedded source blobs verify against file SHA-256.

## NOT established
- Live Qwen baseline accuracy/completion on any of the new tasks: NOT RUN.
- P1 or P2 accuracy on *this checkpoint and this prompt*: UNKNOWN, despite benchmark-level difficulty ordering.
- Actual valid Apple dataset download/schema or pinned runtime revision compatibility in Colab: NOT RUN here.
- Provisional difficulty-mixture selection: NOT RUN; no pilot outputs yet.
- Independent 24-item validation, objective correctness on fresh items, model editing, investigator advantage, and preservation: NOT RUN.
- Exact population generalization from only 8 examples per difficulty stratum will remain uncertain even after the pilot.

**Local verdict:** AET instrumentation PREPARED; valid actual calibration depends on human-run Colab L4 pilot. No claim of EX0005Cc PASS.