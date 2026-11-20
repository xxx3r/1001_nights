# EX0005B · Evidence Ledger and Reproduction Boundary

**This is a retrospective archive index, not a new experiment or amended freeze.**  
**Canonical night:** `nights/2026/11/2026-11-19-ex0005B`.

## Unmodified source receipts

The user's uploaded `EX0005B_LM02_receipts.zip` is preserved at `evidence/EX0005B_LM02_receipts.zip`. Original archive size **6016 bytes**, SHA-256:

`986b246438d6dbf53f146e75b89799499e3ae54691f9737c1c42c0eed95a6915`

| Original ZIP entry | SHA-256 |
|---|---|
| `ACTION_JOURNAL.json` | `86096c886bb0da8c0d135f3df8907d6040e88eb38dc0486e4d870a3855ab5876` |
| `LIVE_ATTEMPT_STARTED.txt` | `364119798ee793ace0a1cade9e1c4e0e9616bc8156302dc0d5d71ac1d66fe1f3` |
| `PRE_LIVE_FREEZE.json` | `2bf55a5369575cfa8ead9aa7f24f3fadb06b7e85810313082a409675c51953c2` |
| `QUALIFICATION.json` | `2bf55a5369575cfa8ead9aa7f24f3fadb06b7e85810313082a409675c51953c2` |
| `RESULTS.json` | `2bd8f372c49d983e47272c9648be7f76b4b40472a3cd278310fdc76be1e9a0bf` |

The qualification and pre-live freeze are byte-identical. Frozen manifest SHA-256 `54ef9670a89babd0d29614a1e96afd76a907019bdd17b7eb1626b66d5ea22996`. Frozen source SHA-256 `51561aad985c8a1b2cfd65f08ca58ae77bac47bebaf609f3213b4c962b57fa33`; test source SHA-256 `41fb648ab7f481ae319bbbeb9165a03c3f54b4cc440ecdd6f98918de0fafc1ac`; dataset fixture SHA-256 `2d846dddcea8a6e4ebfff51531ef46f37579a078755cd8e53bd2488c82a9bf2c`.

## Exact code and review history

LM-01's final G0-v2 notebook, Python instrument, checker and numeric-restoration note are copied as Git blobs under `implementation/lm01/`; original historical PR [#1](https://github.com/xxx3r/1001_nights/pull/1). LM-01 user-quoted observations are in [LM01_OBSERVATIONS.md](./LM01_OBSERVATIONS.md), **not** original raw journal files. No LM-01 raw ZIP was supplied here.

LM-02 source, checker and notebook are **identical Git blobs** to [draft PR #2](https://github.com/xxx3r/1001_nights/pull/2), copied under `implementation/lm02/`. Original independent offline audit is [LM02_RECEIPT_AUDIT_2026-11-19.md](./LM02_RECEIPT_AUDIT_2026-11-19.md). The offline checker ran **20/20 tests** in preparation. The attached raw receipt integrity and arithmetic were additionally verified offline without contacting the L4 or OpenAI; it is **not a replication of the live API/GPU run**.

## Verify locally, do not rerun the night

With the repository checked out:

```bash
sha256sum evidence/EX0005B_LM02_receipts.zip
unzip -l evidence/EX0005B_LM02_receipts.zip
(cd implementation/lm02 && python -m unittest -v test_preservation_gate_lm02.py)
```

The unittest command is an **offline checker**, not a new Luna investigation. For numerical gate derivations, see the audit report and the frozen `RESULTS.json` in the ZIP. The original notebook's live command is single-use and should **not** be replayed against these same holds as a confirmatory trial.

## Limits of the archive

The immutable ZIP is a user-provided Colab artifact; neither source logs nor hash matching authenticate the human runtime or grant independence from user control. The public prompts and heldout samples are tiny and no answer-accuracy improvement was scored. The exact gain 5 ties a development-selected numerical grid. The surgeon was handed the edit site. Live commitment was forced by the final-only menu. The research conclusions explicitly retain all these qualifications.

**Historical artifacts are immutable evidence; narrative closure does not revise them.**