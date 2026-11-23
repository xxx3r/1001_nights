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