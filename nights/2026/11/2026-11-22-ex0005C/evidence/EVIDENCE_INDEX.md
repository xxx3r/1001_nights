# EX0005C evidence index · 2026-11-22

## Immutable source provided by the human operator

- Filename: `EX0005C_v03_PRE_FLIGHT_receipts.zip`
- **SHA-256:** `6d07111bcaf81af2a123f12ea12887b3d222e162347b111d7ef2d92b0a80ce01`
- Size: **16,780 bytes**
- Member files: `manifest.json`, `g0_smoke.json`, `g0_development.json`.
- ZIP CRC: PASS in separate offline audit.
- Retention: **original upload is retained in the conversation, not copied into this public GitHub repository**. This GitHub archive contains the reproducible source and aggregate result, but not the full per-question response strings. The raw receipt's SHA identifies the unaltered evidence.

The uploaded manifest records the expected model revision, source/split IDs and hashes. Full heldout content was **not** present in this ZIP, and heldout content hashes were not independently recomputed.

## Observed result and validation scope

- Two smoke items: IDs and response scores matched their first two G0 development counterparts.
- Full development: 24 distinct IDs; 23 scorer-correct; 24 scorer-completed; all status `valid_complete`.
- One wrong item: `gsm8k_train:4635`, output 51, independently computed arithmetic 21.
- Largest sample 2,394 output tokens under the 3,072 cap; median 525.
- Frozen G0: 2–20 correct / 24 and >=4 completed. **G0 FAIL / STOP**.
- Reported human-side 674 s elapsed time is not independently captured in ZIP.
- No Luna API journal, no selected edit, no numerical-search result, no preservation evaluation and no heldout score.

**Limits:** independent check is of supplied ZIP consistency and arithmetic for the single error only. No independent live GPU replication and no independent regrading of all 23 scorer-correct answers.

## Derived artifacts

- [G0_RECEIPT_AUDIT.md](../G0_RECEIPT_AUDIT.md)
- [DEVELOPMENT_SUMMARY.json](DEVELOPMENT_SUMMARY.json)
- [NIGHT_CARD.md](../NIGHT_CARD.md)

## EX0005Cc separation

The AET calibration package was prepared separately, and its 32-item L4 pilot was not yet reported at the time of archive publication. The Apple benchmark's licensing conditions require review before any raw dataset/model-output material is made public. Source and prospective protocol are in `../ex0005Cc/`; no Apple pilot outputs are represented as completed evidence.
