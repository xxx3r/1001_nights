# EX0005B-LM-01 | Failed G0 v1 and corrected instrument v2

**November 19, 2026, 18:25 Mountain (user-reported Colab L4 trial).**

G0 v1: **FAIL**. No Luna investigator call, patch commitment or held-out evaluation was made. Original `QUALIFICATION.json` must remain in the existing `ex0005b_lm01_receipts/` directory.

| alpha | corrupt target dev loss | inverse-gain *oracle* target dev loss |
|---:|---:|---:|
| 0.25 | 0.15091786161065102 | 0.1515267180899779 |
| -1.5 | 0.20766328647732735 | 0.14843973517417908 |
| 2.0 | 0.15203354135155678 | 0.1515267180899779 |

Investigation: original `Patient.metrics(1/alpha, ...)` is not a mathematically exact oracle on a low-precision parameter tensor. A BF16 multiply followed by inverse multiplication can select a different rounded value. The -1.5 case cleared the original dev corruption gap given the stable reference reading (~0.151526718), but failed the required 0.002 oracle-restoration tolerance.

G0 v2 changes ONLY the oracle/reference pathway: re-evaluate by copying the original column values directly, then restore the corrupted column in a `finally` block. It separately reports the inverse-gain candidate loss; candidate patches still pay the actual quantization error. It DOES NOT change the alpha sequence, dev gap 0.03, oracle tolerance 0.002, preservation thresholds, model ID, splits, or investigator tools. This repaired preflight is **not** a blinded independent replication and must not retroactively convert G0 v1 to PASS.

All prospective v2 receipts go into the separate `ex0005b_lm01_v2_receipts/` directory. The original receipt directory stays untouched.

No model-inference claim is made here. A model-independent BF16 tensor roundtrip counterexample is in the expanded offline tests.