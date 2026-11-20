# LM-01 · User-reported Observations (not raw receipts)

**Separate live experiment, 19 November 2026. Historical status: INTERRUPTED.**

This note captures the user's verbatim numerical outcomes and typed summary from the conversation, **not original uploaded machine receipts**. Do not treat it as authenticated raw evidence or apply LM-02 scores to this patient.

## G0 v1: FAIL, numerical oracle flaw

On the Qwen3-0.6B L4 patient the original qualification selected no alpha because the inverse-gain “oracle” did not exactly restore rounded weights:

- alpha 0.25: corrupted target dev 0.1509178616; inverse oracle 0.1515267181.
- alpha -1.5: corrupted target dev 0.2076632865; inverse oracle 0.1484397352; true healthy target dev 0.1515267181.
- alpha 2.0: corrupted target dev 0.1520335414; inverse oracle 0.1515267181.

Instrument was corrected under a separate G0 v2 source checksum. Frozen alpha ordering/thresholds were not changed. The corrected qualifier used the **exact original saved column** as the oracle, recorded the approximate inverse separately and **G0 v2 PASS**.

## G0 v2: PASS (user-reported Colab qualification)

- Patient `Qwen/Qwen3-0.6B`; revision `c1899de289a04d12100db370d81485cdf75e47ca`; `cuda:0`.
- Layer **14**, column **4**, planted alpha **-1.5**.
- Healthy dev target loss **0.1515267181**, healthy dev preservation loss **6.5532937447**, corrupt dev preservation loss **6.5577176412**.
- Frozen manifest SHA-256 `2865716979e2147f609f71155ccac4870cd98bc74cea4361b5dd5c0f82d6ecf7`.

## Live attempt: INTERRUPTED

The printed final result was:

```json
{"status":"INTERRUPTED","G0":"PASS","G1":"NOT RUN","G2":"NOT RUN","G3":"NOT RUN","G4":"NOT RUN","G5":"NOT RUN","error_type":"RuntimeError","reason":"diagnostic budget exhausted without commitment"}
```

User's separate journal inspection: **7 API responses** (last requesting another diagnostic), **6 accepted observations**:

| Operation | Candidate gain | Target dev loss | Preservation dev loss |
|---|---:|---:|---:|
| inspect_site | — | — | — |
| probe_gain | 1 | 0.2076632865 | 6.5577176412 |
| probe_gain | 0 | 0.1566669804 | 6.5317819118 |
| probe_gain | 0.5 | 0.1733264637 | 6.5549142361 |
| probe_gain | 0.25 | 0.1658126662 | 6.5385919015 |
| probe_gain | -0.5 | 0.1556384241 | 6.5666445494 |

The original scaffold continued advertising `probe_gain` beyond the six-measurement budget. Luna chose another diagnostic instead of `commit_surgery`; the runner correctly refused it, **but the menu was ill-posed**. Since there was no commitment, **no G3–G5 held-out scores exist**.

**Lesson:** accurate counters are not sufficient; tool availability and phase completion must enforce the declared protocol. No claims about Luna's unseen ability or incapacity are justified by this interruption.

**Sources:** user-supplied notebook/Colab excerpts during 19 November conversation; original source and G0 correction note retained under `implementation/`.