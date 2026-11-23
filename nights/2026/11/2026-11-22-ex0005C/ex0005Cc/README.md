# EX0005Cc AET | difficulty-frontier calibration

A new calibration experiment. It cannot change EX0005C (2026-11-22 G0 FAIL, 23/24, 24/24). This package does not access EX0005C's heldout vault and contains no surgeon/optimizer.

1. Open `EX0005Cc_AET_Calibration_Colab.ipynb` in **Colab L4**. It embeds SHA-verified sources.
2. Run setup and local unit tests, then the dataset-family seal and model-load cells.
3. Only when ready, set `RUN_PILOT=True` for the 32-item development-calibration pilot. This is the sole permitted live model scoring. The marker prevents reruns.
4. Run the mixture-selection cell, then export private receipts. Share the status and stratum counts, or upload the ZIP for a separate audit.
5. Do **not** score the selected qualification pool or original EX0005C holdouts in this notebook.

If the chosen distribution is close to 55% on pilot, that is provisional. A separate, single-use 24-item qualification is required to verify that the healthy baseline is actually non-ceiling. No mathematical improvement or model surgery is claimed.

The dataset source `apple/GSM-Symbolic` is CC BY-NC-ND 4.0. Keep downloaded question/answer content and model traces private until its usage and redistribution conditions are reviewed.

The original parser snapshot SHA-256 is `ce0fe0b4633e9c3175889b763fe91fa25e231f5e0889d061e24ee28bd23649ed`.
## Post-pilot update: exploratory candidate A

The real 32-item pilot finished **13/32 correct, 22/32 valid completions**, and the frozen v1 decision returned **NO_QUALIFIED_DISTRIBUTION** because its original 75% mixture-completion rule was not met. The human operator subsequently overrode that arbitrary design preference for a **new exploratory continuation**, not a reinterpretation of the original v1 verdict.

See [pilot receipt audit](AET_PILOT_RECEIPT_AUDIT_2026-11-22.md), [exploratory amendment](EXPLORATORY_AMENDMENT_AFTER_PILOT.md), [sealed selection A IDs](EXPLORATORY_SELECTION_A.json), and the [one-shot optional exploratory validation notebook](EX0005Cc_EXPLORATORY_VALIDATION_A_Colab.ipynb). Candidate A (4 main/8 P1/8 P2/4 synthetic) is from the **original** candidate grid and has projected accuracy 9.5/24 and projected completion 16/24; neither is a held-out result. Original EX0005C remains G0 FAIL, untouched.
