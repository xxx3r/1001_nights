# EX0005C | G0 receipt audit | 2026-11-22

Source: user-uploaded `EX0005C_v03_PRE_FLIGHT_receipts.zip` (unaltered). SHA-256 `6d07111bcaf81af2a123f12ea12887b3d222e162347b111d7ef2d92b0a80ce01`.

Archive members: `manifest.json`, `g0_smoke.json`, `g0_development.json`. ZIP integrity: PASS. No held-out answer or model-output file in the archive. The manifest records IDs and hashes for held-out data but the data themselves are not included; the content hashes have **not** been independently recomputed from dataset files.

| Check | Observation |
|---|---|
| Model revision manifest | `c1899de289a04d12100db370d81485cdf75e47ca` (reported, not independently verified against live model) |
| G0 development distinct IDs | 24 / 24 |
| Development IDs agree with manifest's math subset | Yes |
| First two smoke entries agree with development entries | Yes |
| Correct scorer flags | 23 / 24 |
| Completed scorer flags | 24 / 24 |
| Statuses | 24 `valid_complete` |
| Largest output tokens | 2394 / 3072 |
| Median output tokens | 525.0 |
| Frozen G0 math criterion | At least 2 and at most 20 correct, at least 4 complete |
| Verdict | FAIL because 23 > 20 |

**Manual error inspection:** `gsm8k_train:4635` in the emitted model text describes 15 packs, each containing one red, one yellow and one green pencil, with 3 packs containing 2 extra red pencils each. The model returned 51, incorrectly counting all normal pencils as red. The arithmetic from the reproduced problem is 15 + 3×2 = **21**. This is a reasoning mistake, not an incomplete-output or malformed-parser case. Other 23 correctness flags were not manually recomputed from independent answer keys.

**Evidence limits:** no original Colab environment transcript or model parameters in the ZIP; elapsed 674 s and the live stop message are user-reported separately. No claim of independent L4 replication. No full preservation or held-out evaluation, model surgery or Luna journal. A baseline-only G0 disqualification is not evidence for either H1 or H2.