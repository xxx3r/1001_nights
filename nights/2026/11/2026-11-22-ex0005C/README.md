# EX0005C · The First New Skill (22 November 2026)

**Closed scientific result:** **G0 FAIL / STOP**. The healthy Qwen3-0.6B baseline scored **23/24 correct and 24/24 completed** on development math. The prospectively specified G0 eligibility range was **2–20 correct / 24** with at least four valid completions. **No Luna surgery, optimizer, preservation holdout, or math holdout was executed.** This is a baseline-identifiability stop, not evidence for or against a weight-edit capability.

**EX0005Cc (AET) is a separate, newly authorized difficulty-distribution calibration.** As of this archive snapshot, it is prepared, not independently observed on L4. Its pilot or later qualification must never revise EX0005C's G0 or expose EX0005C heldouts. Keep the two experiment labels distinct.

## Evidence and human learning

- [NIGHT_CARD.md](NIGHT_CARD.md): closed 200–400-word one-night report; human-first work, limits, and stopping decision.
- [G0_RECEIPT_AUDIT.md](G0_RECEIPT_AUDIT.md): independent **offline consistency audit of supplied receipts**, not GPU re-execution or a regrade of every answer.
- [evidence/EVIDENCE_INDEX.md](evidence/EVIDENCE_INDEX.md): original receipt ZIP hash, contents and verification boundary. The original user-uploaded ZIP remains unmodified and is **not mirrored into this public repository**.
- [evidence/DEVELOPMENT_SUMMARY.json](evidence/DEVELOPMENT_SUMMARY.json): fixed denominator, failure reason and discrepancy ID; **aggregate derived summary**, not raw model outputs.

Human-owned: the six-pair accuracy decomposition **+2 total = +1 both-complete +1 completion-changed**; expectation that **completion repair (H2)** is more likely than transfer of mathematical correctness (H1); scorer/shortcut exploit as another rival. The user did not derive the implementation independently. AI assisted protocol, source, debugging and receipt analysis.

## Prospectively proposed EX0005C instrument

- [EX0005C_PROTOCOL_v0.3.md](EX0005C_PROTOCOL_v0.3.md): preflight choices, data, two-column editing gates and hard stop, written **before** G0 outcome. Do not rewrite it as a post-hoc result.
- [notebooks/EX0005C_v03_Preflight_Colab.ipynb](notebooks/EX0005C_v03_Preflight_Colab.ipynb): original notebook snapshot, including the failed `generator=` API call.
- [notebooks/EX0005C_v03_1_Preflight_Colab.ipynb](notebooks/EX0005C_v03_1_Preflight_Colab.ipynb): narrow API-compatibility correction; **not a new scientific trial**.
- [API_COMPATIBILITY_ERRATUM.md](API_COMPATIBILITY_ERRATUM.md): what changed and why scientific thresholds were preserved.
- [implementation/](implementation/): scorer, deterministic split builder, and local tests extracted from the source-hashed v0.3.1 notebook. They do not implement the Luna surgery stage.

The clean model was `Qwen/Qwen3-0.6B`, revision `c1899de289a04d12100db370d81485cdf75e47ca` as declared in the supplied manifest (live revision not independently revalidated in this audit). Thinking was enabled; math token cap **3,072**, temperature **0.6**, top-p **0.95**, top-k **20** and item-derived seeds. Development tasks were GSM8K train examples. The historical holdout identity/hash records were sealed at preparation; their examples were not evaluated.

The two smoke outputs were correct and completed. During the later full development G0, **24/24 completed** and **23/24 were scorer-correct**. The one observed error, `gsm8k_train:4635`, counted 51 rather than the independently computed 21 red pencils. Max output length was **2,394 tokens**. The live 674-second development duration was user-reported, not recorded in the ZIP.

## Newly authorized, separate EX0005Cc AET calibration

- [ex0005Cc/README.md](ex0005Cc/README.md): Colab pilot instructions and redistribution boundary.
- [ex0005Cc/PROTOCOL_v1.md](ex0005Cc/PROTOCOL_v1.md): 8 examples each from GSM-Symbolic main/P1/P2 plus synthetic, six prespecified candidate mixtures; pilot selection is **provisional**.
- [ex0005Cc/EX0005Cc_AET_Calibration_Colab.ipynb](ex0005Cc/EX0005Cc_AET_Calibration_Colab.ipynb): self-contained, sealed-source L4 pilot; run deliberately with `RUN_PILOT=True`.
- [ex0005Cc/implementation/](ex0005Cc/implementation/): prospective calibration source and tests.
- [ex0005Cc/LOCAL_AUDIT.md](ex0005Cc/LOCAL_AUDIT.md): local 18/18 checks, with actual pilot result explicitly unknown.

The Apple dataset `apple/GSM-Symbolic` has redistribution restrictions; **do not publish downloaded Apple prompts, answers or model traces automatically**. The source notebook and code contain no executed Apple item responses.

## Historical upstream reconciliation

The two November 19 implementation PRs were independently archived and are now merged:
- [PR #1](https://github.com/xxx3r/1001_nights/pull/1): LM-01, whose later run was interrupted without heldout success.
- [PR #2](https://github.com/xxx3r/1001_nights/pull/2): LM-02, G0–G5 PASS on a planted fault, but a development-selected **13-point numerical grid ties Luna's choice**.
- [EX0005B final report](../2026-11-19-ex0005B/EX0005B_FINAL_RESEARCH_REPORT.md): controlling post-run interpretation, distinct from as-prepared protocol snapshots.

**Scope:** Only an archive of a healthy-model baseline failure and a separate prospective calibration. No new skill, generalized self-improvement, WSP theorem or solver-over-optimizer advantage was established. Original EX0005B and EX0005C observations remain unchanged.

## AET empirical follow-up after this archive snapshot

The independently labelled **EX0005Cc** pilot subsequently ran on the healthy model: **13/32 correct**, **22/32 valid completed**; original frozen v1 mixture-selection decision **NO_QUALIFIED_DISTRIBUTION**. The human operator then explicitly overrode the arbitrary 75%-completion cutoff for a **new, post-pilot exploratory continuation**, selecting original candidate A and sealing 24 reserved item IDs. This is not an amendment to the closed EX0005C G0=FAIL and not an assertion of held-out success. See [pilot audit](ex0005Cc/AET_PILOT_RECEIPT_AUDIT_2026-11-22.md), [dated amendment](ex0005Cc/EXPLORATORY_AMENDMENT_AFTER_PILOT.md), and [optional follow-up notebook](ex0005Cc/EX0005Cc_EXPLORATORY_VALIDATION_A_Colab.ipynb). Raw Apple outputs remain in a private user-uploaded receipt ZIP, not publicly mirrored.
