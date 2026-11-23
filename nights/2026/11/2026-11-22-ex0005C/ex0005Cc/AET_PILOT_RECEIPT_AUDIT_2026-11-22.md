# EX0005Cc AET · independent offline pilot receipt audit

**Local research date:** 2026-11-22 (America/Denver)  
**Original frozen protocol outcome:** `NO_QUALIFIED_DISTRIBUTION`, because none of the original six candidate mixtures met its predeclared >=75% predicted-completion eligibility criterion. **That historical outcome is not revised here.**  
**Separate user-directed decision:** set aside that arbitrary criterion for a new exploratory validation; see [EXPLORATORY_AMENDMENT_AFTER_PILOT.md](EXPLORATORY_AMENDMENT_AFTER_PILOT.md).

## Provenance
- Source: user-uploaded `EX0005Cc_AET_calibration_receipts.zip`, SHA-256 **`a06b1b87dab764e7e821c83a39b3908003c56b4a416631d8f1ff4f76ab4c0537`**, 42,312 bytes.
- Members: `manifest.json`, `PILOT_STARTED.marker`, `pilot_results.json`, `calibration_decision.json`.
- ZIP CRC check: PASS. 32/32 unique result IDs match the manifest's ordered pilot IDs. All original stratum/mixture calculations reproduced from 32 result flags. Thirty-six reserved pool IDs are distinct from the pilot IDs (the reserved pool includes alternatives across strata, not all of which will be scored).
- The uploaded manifest records model revision `c1899de289a04d12100db370d81485cdf75e47ca`, Apple revision `93b5b3758d9d9841ffe81d6cd2ae2b030685b078`, `pilot_content_hash=d6946bbf897c0e72d5e965c2eaf563aba07bcc2d5573f0469a90748d628a3a04`, `validation_pool_hash=65daa7c616ae806632e01df49c233a3d6467e01d4672a9f4b0ec480751f43552`. **Pool content hashes are manifest claims, not independent rereads of datasets in this offline audit.**

## Counts exactly as submitted

| Pilot stratum | Correct | Parser-valid completed | N | Correct percentage | Completion percentage |
|---|---:|---:|---:|---:|---:|
| Apple main | 4 | 5 | 8 | 50.0% | 62.5% |
| Apple P1 | 4 | 6 | 8 | 50.0% | 75.0% |
| Apple P2 | 2 | 4 | 8 | 25.0% | 50.0% |
| Synthetic | 3 | 7 | 8 | 37.5% | 87.5% |
| **Total** | **13** | **22** | **32** | **40.625%** | **68.75%** |

Status detail: **22 `valid_complete`**, **7 `truncated_or_unterminated`** (all hit the 3,072-token limit), **3 `invalid_number`** (generation ended but the exact numeric-answer parser rejected it). Thus "incomplete" is not synonymous with token-limit truncation. The ten non-valid completions were counted incorrect, as originally specified. There were **9 completed-but-incorrect** answers.

The 32 per-item durations total **2,080.79 seconds (~34m41s)**; this is summed from user-uploaded result metadata rather than independently measured GPU time.

**All 6 originally eligible-mixture flags are false** under the historical >=75% completion rule. Original `choice=null` and `NO_QUALIFIED_DISTRIBUTION` are consistent with the frozen code. The investigator never edited model weights or evaluated the reserved pool in the supplied receipt.

## Limits and privacy

This checks internal receipt consistency, not independent L4 replay or fresh human regrading of all 32 mathematical solutions. Apple generated questions and raw model outputs remain in the private uploaded ZIP; do **not** mirror them publicly without reviewing licensing. A tiny eight-example sample per stratum carries wide uncertainty. No evidence of new reasoning capability, Luna advantage or improvement of model weights is claimed.
