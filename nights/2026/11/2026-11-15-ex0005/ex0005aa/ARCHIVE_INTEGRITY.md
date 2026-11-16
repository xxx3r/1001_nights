# EX0005Aa | Archive integrity and provenance ledger

**Purpose:** Document which user-uploaded bytes were preserved, which files were reconstructed from a frozen notebook or the documented date-only edit, and which files were newly generated in the post-run audit. This ledger is not an experimental measurement and does not change any scored gate.

**Original user-uploaded ZIP:** `EX0005Aa_receipts.zip` (16,225 bytes), SHA-256 `cb1890de47ecf787766fe62eef821dbe4987efa17dd07305616175fadb732af1`. Its **seven constituent files** were extracted and committed as ordinary inspectable repository files; the redundant binary ZIP container itself was not added to GitHub. The Git blob hashes of all seven stored files were compared with hashes computed directly from the ZIP's contents and matched.

| Original ZIP entry | Repository path | SHA-256 of original bytes |
| --- | --- | --- |
| `RESULTS.json` | [evidence/RESULTS.json](./evidence/RESULTS.json) | `65963efb3aaf1dd44b118da887a9c44236148a541646920c6d29efaebfd64411` |
| `ACTION_JOURNAL.json` | [evidence/ACTION_JOURNAL.json](./evidence/ACTION_JOURNAL.json) | `6310856df3858518a39f9be5fd74a077943c2ccd27ceaf533256b1b23bebe8ea` |
| `PRE_LIVE_FREEZE.json` | [evidence/PRE_LIVE_FREEZE.json](./evidence/PRE_LIVE_FREEZE.json) | `3ac835843e169fa907c93b22f881be7043de94dac9d157b91861bf239ea40287` |
| `SUPERSEDED_NOV19_FREEZE.json` | [evidence/SUPERSEDED_NOV19_FREEZE.json](./evidence/SUPERSEDED_NOV19_FREEZE.json) | `adc3e79068ab1c33b8ff8431f11031ca0c142dc7a299f46216915c16fbf0ce4a` |
| `FREEZE_CORRECTION_NOTE.json` | [evidence/FREEZE_CORRECTION_NOTE.json](./evidence/FREEZE_CORRECTION_NOTE.json) | `41627a2af805591640535415066f81ea863e6da69820b4365004ec09dc0aaefc` |
| `LIVE_ATTEMPT_STARTED.txt` | [evidence/LIVE_ATTEMPT_STARTED.txt](./evidence/LIVE_ATTEMPT_STARTED.txt) | `c4b89a1b318a95dcde13524fd285524d3ea51d24df733affa0af3b170086e6ab` |
| `ORIGINAL_RUNNER_BEFORE_DATE_FIX.py` | [source/run_luna_aa_before_date_fix.py](./source/run_luna_aa_before_date_fix.py) | `fd4dedbab706c42736164bb63917a8257fb92c6a0b7a2292c94e3ab7e9f2618a` |

The separately uploaded `RESULTS (1).json` and `ACTION_JOURNAL (1).json` matched the corresponding ZIP entry **byte for byte**. The archive uses the canonical names without ` (1)`; they are not separate model runs.

**Live-source reconstruction and identity:** The public fixture `ex0005aa_public.py` and offline test module were extracted from the as-prepared notebook; the original runner inside the ZIP matched the notebook's generated runner. The documented date-only amendment was independently reconstructed from the original runner. The corrected runner's SHA-256 **exactly equals** the controlling live freeze's source hash, `b7bdeaa8311acc7c7f72c87380032d2cdcfc085e38e3c02bf3ed3ad388a1d1ed`. The public fixture source SHA-256 likewise matches the freeze: `d410ecc5752018e35bbf7d4e9b74089a44bc41643bf7992f0d98a457fc622426`.

**Controlling freeze self-hash:** Recomputing SHA-256 over the canonical sorted JSON payload excluding `freeze_sha256` matched `2644e664eb2ca90483ff461bb8a069ef91e2b6fe65592adcf82969f92045c044`.

**Notebook and historical planning:** [EX0005Aa_Colab.ipynb](./EX0005Aa_Colab.ipynb), [protocol](./planning/EX0005Aa_PROTOCOL_AS_PREPARED.md), [run guide](./planning/README_RUN_AS_PREPARED.md), and [build status](./planning/BUILD_STATUS_AS_PREPARED.md) were preserved separately as **as-prepared artifacts**. They predate the user's corrected same-day freeze. Do not mistake their old date restriction for the active, hash-matched live source.

**Post-run analytical addition, NOT model evidence:** [analysis/identifiability_counterexample.py](./analysis/identifiability_counterexample.py) and [analysis/IDENTIFIABILITY_RESULTS.json](./analysis/IDENTIFIABILITY_RESULTS.json) were generated only after the original model commitment and scoring. No API calls were made for this check. Its role is a mathematical counterexample to *unique intervention identifiability*, not a new hidden test case or a rescore.

**Local reproduction:** Python offline unit tests were run against the *amended* runner and finished **11/11 PASS**. The post-run audit script was independently executed against the same public fixture source, reproducing identical feature0 and feature1 observations and the alternate-patient MSE. No training or billable inference was needed.

**Scope limit:** The exact exported Colab *runtime state*, cloud notebook session metadata, full provider-side model revision and billed currency cost were not included in the uploaded ZIP. The journal and manifest provide the available API/tool and execution provenance. None of those unavailable fields is invented here.
