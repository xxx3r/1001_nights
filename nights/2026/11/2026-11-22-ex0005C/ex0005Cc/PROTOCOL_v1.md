# EX0005Cc · AET difficulty-frontier calibration · v1

**Authority:** User explicitly authorized a separate AET ex0005Cc after EX0005C stopped at G0. This is **not** a retrospective amendment or a surgeon trial. This document is a prospective source/specification, not evidence that a successful difficulty distribution has been found.

## Historical boundary
- Preserve EX0005C November 22 baseline 23/24 correct, 24/24 completed; G0 FAIL, no surgery, no holdouts opened.
- The original user's receipt archive remains unmodified, SHA-256 `6d07111bcaf81af2a123f12ea12887b3d222e162347b111d7ef2d92b0a80ce01`.
- Do not access the historical holdout prompts/answers or treat original holdout IDs as newly available training data. The new calibration excludes the historical heldout Apple template IDs and GSM8K test IDs by identifier only.

## Question
Can a fixed mixture of four *predefined* numerical word-problem strata give the unedited healthy Qwen3-0.6B an estimated baseline accuracy **30–75%**, preferably near **55%**, while retaining at least **75% valid completions**?

This is a distribution-calibration question, not evidence of new model learning, and a pilot estimate is not an independently validated baseline.

## Model, inference, and cost
- Original Qwen `Qwen/Qwen3-0.6B`, revision `c1899de289a04d12100db370d81485cdf75e47ca`, healthy BF16, L4. No weights changed.
- Thinking `enable_thinking=True`, the same explicit math prompt/parser from EX0005C, temperature 0.6, top-p 0.95, top-k 20, min-p 0.0, one sample per item, `max_new_tokens=3072`, per-item SHA-256 seeds. The **seed namespace changes**, which is recorded. No greedy decoding and no shortening context to force failure.
- One calibration pilot with **32 items**, 8 per stratum. No more than 90 minutes after start, with no silent continuation or model substitution. Stop if source/schema/model fails or if a pilot fails partway. No API/Luna tools and no heldout evaluation.

## Candidate strata
- `main`: Apple GSM-Symbolic default, benchmark `main`.
- `p1`: same source with one extra clause.
- `p2`: same source with two extra clauses.
- `synthetic`: original reproducible numeric word problems in 4 template types, 2 parameterizations each. Answer keys computed with two algebraically equivalent formulas. The synthetic stratum is a different task distribution, not proof of an ordered P3 difficulty level.
- Apple revision `93b5b3758d9d9841ffe81d6cd2ae2b030685b078`, `test` split; Apple license CC BY-NC-ND 4.0. Retrieve the dataset at runtime, do not rehost or publish the dataset prompts or model traces without checking licensing. Any Apple gold-label discrepancy must be disclosed, not silently rewritten.

## Source-family selection
- Deterministic SHA-256 keyed ordering from `EX0005Cc-AET-2026-11-22-v1`.
- Apple sample families `original_id` are unique *across* the three strata and across pilot/qualification pools. Selected historical EX0005C template IDs and ordinary GSM8K test IDs are excluded from Apple sampling. One `instance` per Apple family.
- Synthetic pilot/qualification instances use different generated seeds but reuse four generator templates: **item-disjoint, not template-family-disjoint**.
- Seal 32 pilot ID/hash pairs and a separate 24-maximum validation candidate pool before any Qwen scoring. The validation candidate pool remains unevaluated in this AET. Never pick individual questions on the basis of error or model confidence.

## Fixed candidate mixtures for a later 24-item validation (main, P1, P2, synthetic)
| Candidate | Main | P1 | P2 | Synthetic |
|---|---:|---:|---:|---:|
| A | 4 | 8 | 8 | 4 |
| B | 4 | 4 | 12 | 4 |
| C | 0 | 8 | 8 | 8 |
| D | 0 | 4 | 12 | 8 |
| E | 0 | 4 | 8 | 12 |
| F | 0 | 0 | 12 | 12 |

For each stratum, compute `correct/8` and `complete/8`, counting malformed/truncated as incorrect. Weight these four pilot proportions by each mixture's **fixed integer counts**, with denominator 24. Eligible mixtures satisfy predicted accuracy ∈[0.30,0.75] and predicted completion ≥0.75. Choose the eligible mixture whose predicted accuracy is closest to 0.55; ties take earlier alphabetic candidate. If **none** qualify, record `NO_QUALIFIED_DISTRIBUTION`, do not expand the mixture grid.

## What would actually validate a selected distribution?
Not in this trial. In a separately authorized prospective qualification, run the **presealed 24-item validation set once** with the same healthy model and generation settings. A qualifying *observed* baseline should have 2–20 correct and at least 18 valid completions. If it falls outside, stop; do not adjust the mixture after observing validation. This is a follow-up validation rule and **not permission to run the old EX0005C surgeon or old heldouts**.

## Reporting
- Raw item-level accuracy, completed, truncated/malformed, answer format, token count, timing and wall-clock/cost.
- Stratum counts, candidate mixture table, recommendation or explicit nonselection, plus observed calibration uncertainty (8 per stratum is weak).
- Benchmark labels and generated oracle are not equivalent to independently hand-verified full reasoning; manually inspect a sample of discrepancies.
- There are no EX0005Cc model improvements, Luna comparisons, preservation gates, or H1/H2 results in this calibration.

**Stopping verdict:** PREPARED until executed on L4. Pilot may yield `PROVISIONAL_DISTRIBUTION_SELECTED`, `NO_QUALIFIED_DISTRIBUTION`, `INTERRUPTED`, or `NOT RUN`. Even a selected mixture is not a validated G0.