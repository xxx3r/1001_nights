# EX0005C family | late-session private-receipt audit | 2026-11-22

**Scope:** Offline consistency audit of the user-uploaded receipts. ZIP files are not copied to the public repository because they contain Apple GSM-Symbolic questions, model outputs or private reasoning traces. Hashes below identify the exact private artifacts. Original EX0005C G0 is separately archived in [G0_RECEIPT_AUDIT.md](../G0_RECEIPT_AUDIT.md).

| Source file | SHA-256 (entire ZIP) | ZIP CRC | Evidence verified |
|---|---|---|---|
| `EX0005Cc_AET_calibration_receipts.zip` | `a06b1b87dab764e7e821c83a39b3908003c56b4a416631d8f1ff4f76ab4c0537` | PASS | 32 unique pilot results; 13 correct, 22 complete; historical NO_QUALIFIED_DISTRIBUTION |
| `EX0005Cc_exploratory_validation_A_receipts.zip` | `05cba3e17aedf49909cdcc50c4efd101462832139898fcb1b4ec23c47b42bf96` | PASS | 24 unique validation results, **zero overlapping IDs with the 32 pilot records**; 8 correct, 15 complete |
| `EX0005Cd_FULLPROBE_03_receipts.zip` | `9cad8c9588c97cf8e616b20a9e8dcef487b37c4b60c76802459dd3ab7381f028` | PASS | 12 API responses; 6 scalar repair probes; Luna's final ABSTAINED decision |
| `EX0005Ce_WSP02_receipts_PRIVATE.zip` | `30a165e80504beb1292743876329c929975cf67d473e6d89de694fc8c6bba5bc` | PASS | 16 complete API responses/actions, 4 forward passes, 20 traced generations, 1 paired four-question run; ABSTAIN |

## EX0005Cc exploratory A: actual baseline versus earlier projection

The 24-question exploratory follow-up was selected post-pilot but before its own results. Unlike the earlier weighted **pilot projection** (9.5 correct, 16 complete), the **actual** observed outcome was **8/24 correct (33.33%)**, **15/24 parser-valid completed (62.5%)**, 6 `truncated_or_unterminated`, 3 `invalid_number`, and 7 completed-but-incorrect.

Observed stratum breakdown: main **2/4 correct, 3/4 complete**; P1 **3/8, 4/8**; P2 **1/8, 4/8**; synthetic **2/4, 4/4**. This demonstrates a non-ceiling difficulty range, **not a weight-edit effect**. It does not overwrite the original AET v1 gate failure.

## EX0005Cd: six-probe surrogate observations

The FULLPROBE-03 file records the following loss probes. Lower is better, but these are **teacher-forced suffix proxies**, not mathematical correctness or preservation testing:

| Multipliers (column 194, column 390) | Math proxy loss | Preservation proxy loss |
|---|---:|---:|
| (1.00, 1.00) | 2.544798 | 6.654499 |
| (0.95, 1.00) | 2.546257 | 6.668599 |
| (1.05, 1.00) | 2.547285 | 6.649252 |
| (1.00, 0.95) | **2.542756** | **6.652827** |
| (1.00, 1.05) | 2.558433 | 6.640719 |
| (0.95, 0.95) | 2.545699 | 6.645067 |

The slight improvement for (1.00,0.95) on **both measured proxies** was insufficient to demonstrate a meaningful behavioral effect. Luna abstained. The previous authenticated `AUTHFIX-02` decision (7 responses; no real edit probe) and initial 401 authentication error are supported by user-pasted logs, **not separate uploaded receipt ZIPs**.

## EX0005Ce: apparatus errors versus executed paired test

**WSP-01:** User-pasted traceback shows repeated `list_practice` errors and an incomplete Luna API response, with **0** forward passes and **0** generated samples. A WSP-01 receipt ZIP was not provided for independent audit; label as a user-reported interrupted attempt.

**WSP-02:** The uploaded action journal contains a legal sequence of 16 responses/tools and one final abstention. Exactly three of five `python` tool actions failed with documented errors: `disallowed function: type`, `unsupported Python syntax: Import`, and `disallowed attribute: dot`. Real operations included catalog discovery, original generations, trace reading, weight listings, activation sampling, CPU edit staging, paired generation, notes and finalize.

The first eight original-model traces show **3/8 correct** (1,024-token limit). Four selected failures were subsequently paired at a 2,048-token limit, producing eight more traces. The final paired run shows for both original and edited: **0/4 correct, 0/4 valid completed, 3/4 truncated, 1/4 invalid number**; all four model output strings differ between conditions. This is a behavioral perturbation without observed accuracy or completion gain; no general statistical conclusion.

The final JSON reports a staged edit in `model.layers.12.mlp.down_proj.weight`, shape 1024×3072, changed float32 elements **3,144,367 / 3,145,728** (about 99.96%), relative norm **0.0014919**. These are staged CPU float32 statistics and **not a separately audited count of BF16 GPU elements changed**. The `abstain` decision means no candidate was selected for final evaluation. The freeze record identifies the WSP-02 controller SHA-256 `b08f5cd36ea165fdc30f04e5a0f73cc41c91f9271953bada98a271f85015f903`, which matches the corresponding local controller file; it fixes development IDs/hashes and says the final heldout was sealed.

**Source availability:** WSP-01/WSP-02 controller and evaluator source files and mocked tests were created and supplied locally in the chat. Their archived ZIP receipts and private traces are **not** public GitHub files. This closeout does not assert independent CUDA replay, model-checkpoint verification, complete answer-key regrading, a passed preservation gate or an optimizer comparison.

**Publication boundary:** no raw Apple questions/answers, generated reasoning, API secrets, private Colab metadata, or potentially sensitive traces are mirrored here. The public report contains only aggregate observations, study metadata and cryptographic hashes.
