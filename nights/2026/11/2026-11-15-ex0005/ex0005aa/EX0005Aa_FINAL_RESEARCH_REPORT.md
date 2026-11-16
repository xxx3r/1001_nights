# EX0005Aa | Final research report: The Examiner Must Discover

**One Thousand & One Nights of Alignment · independent post-EX0005A public instrument repair**  
**Execution:** Sunday, 15 November 2026, America/Denver · frozen 20:54:49, first billable attempt marked 20:56:04 · separate session window 20:55–23:59.  
**Run status:** COMPLETE, without an API interruption. **Frozen primary readiness: NOT MET (G2 FAIL).**  
**Separate positive finding:** G4 PASS, a correct model-proposed one-scalar repair on one public synthetic patient.  
**Evidence class:** public development only; no sealed holdout, no independent distributional generalization test.  
**Assistance:** C for human hypotheses and addendum operationalized collaboratively; experiment implementation AI-authored.

> The scalpel worked. The surgeon failed one prospective comparison, then repaired the unknown patient. A subsequent audit proved that the precise incision was not uniquely warranted by the observations taken.

## 1. Historical boundary and what changed

EX0005A, performed earlier on 15 November, was closed at its 20:00 atelier hard stop. Its [final report](../EX0005A_FINAL_RESEARCH_REPORT.md) remains FAIL on complete instrument qualification, with broader model capability inconclusive. **No EX0005A results were retrospectively amended.** EX0005Aa is a separately authorized, revised instrument *after* EX0005A evidence had already been inspected. It therefore cannot be called a blinded replication or a confirmatory efficacy test.

New design: (a) a **fixed, identically requested two-tool paired contrast**, expressly *not* an unknown-fault discovery test; (b) a **separate discovery case** where the investigator chooses four bounded tools, names an unknown planted lesion, and may propose a patch. The native API tool interface uses a single function call per observation and does not accept arbitrary probe indices. A frozen independent checker evaluates predictions and patches; the model does not see healthy weights, oracle keys, or checker scores before commitment.

The pre-run [planning protocol](./planning/EX0005Aa_PROTOCOL_AS_PREPARED.md) and [notebook](./EX0005Aa_Colab.ipynb) contain an earlier rule excluding November 15. The user noticed a November 19 **clerical date typo** after the first freeze. Its entire manifest was preserved as [superseded](./evidence/SUPERSEDED_NOV19_FREEZE.json), and the runner's **date-only** restriction was edited, with its original copy and exact new SHA archived. A new, separate EX0005Aa freeze was made on November 15 *after* EX0005A's 20:00 stop. No model calls preceded the correction. The session date correction and its timing were not part of the scientific outcome.

**Controlling freeze identifier:** `2644e664eb2ca90483ff461bb8a069ef91e2b6fe65592adcf82969f92045c044`.  
**Superseded freeze:** `802c11f959f34c0b54fe0eefe8625855d975d2aabf9eb1e242f16c14103053b5`.  
**Exact corrected runner SHA-256:** `b7bdeaa8311acc7c7f72c87380032d2cdcfc085e38e3c02bf3ed3ad388a1d1ed`.  
**Fixture fingerprint:** `bfa1ace7440f5320e5e008feb7fa3ecc44fd06346d836850607c39bab946e480`.

The original source notebook is an **as-prepared setup artifact**, not the exact revised live runner. For the live version use [source/run_luna_aa.py](./source/run_luna_aa.py) and the controlling manifest. Do not rerun the historical experiment to produce a new outcome.

## 2. Human-first predictions

The four EX0005A predictions were brought forward, **not rewritten as newly independent predictions**, and explicitly approved before the EX0005Aa freeze (assistance C). The human's new EX0005Aa addendum used three surgical roles:

- **Surgeon:** Doubt Luna would show proficient general weight-space programming.
- **Scalpel:** Predict the repaired interface would stop being the principal failure point and make the model's observed choices interpretable.
- **Patient:** Expect the small synthetic fixtures to be adequate for this bounded test, while questions about larger language models remain outside scope.

These exact statements and the four prior predictions reside in [PRE_LIVE_FREEZE.json](./evidence/PRE_LIVE_FREEZE.json). The later discovery success is genuine evidence against a uniformly pessimistic reading of the Surgeon prediction, but cannot certify general proficiency.

## 3. Fixed method and acceptance gates

**Model:** OpenAI Responses API identifier `gpt-6-luna` (confirmed by access check); reasoning effort low; maximum output tokens 1,800 per response, at most 14 model responses, input/output cumulative caps 80,000/24,000 tokens. The reported environment: Python 3.13.18, NumPy 2.4.6, PyTorch 2.14.1+cpu, OpenAI SDK 2.54.0. No separately exposed revision or price/currency cost is in the uploaded receipts.

**Local controls:** 11/11 offline tests PASS; analytical oracle repairs exactly; positive/negative counterfactual directions differ; NumPy/Torch agreement, malformed tool/commit rejection, false-positive controls, incomplete-response retention, and closed-window rejection checked. These are **local and mocked tests**, not real Luna successes.

**Frozen gates:**

| Gate | Requirement | Result |
| --- | --- | --- |
| G0 | Public oracle/control/checker readiness | **PASS** |
| G1 | Both paired cases produce exactly two valid native, forced diagnostic calls | **PASS** |
| G2 | Paired predictions have opposing, oracle-correct signed effects under identical calls | **FAIL** |
| G3 | Both paired commitments are schema-valid | **PASS** |
| G4, secondary | Discovery model edit beats no-edit and simple heuristic by >=0.05 absolute MSE and recovers >=50% loss gap | **PASS** |

The original `RESULTS.json` says `instrument_ready=false` and `mechanistic_understanding="NOT ESTABLISHED"`. **Those are the authoritative frozen outcomes.** G4 is an independent positive *secondary* finding and does not override G2.

## 4. Live observation record

Eleven completed native API responses: three for each paired case, five for discovery. The journal contains **22 entries**: 11 API responses, **8 valid diagnostics out of 8 attempts**, and three model commitments. No errors were reported. Recorded usage: **5,239 input tokens** and **1,770 output tokens**. All model commitments preceded checker evaluation; no iterative patch-result feedback was supplied.

### 4.1 Matched counterfactual: C_positive and C_negative

The model was expressly asked to predict the effect of subtracting 0.25 from `W2[1]`; hence these are tests of **prediction under supplied coordinates**, not of finding a lesion. Identical tool names, inputs, and call order were forced by the harness in both cases.

| Case | Observed W2 | Probe residuals | Predicted ΔMSE | Oracle ΔMSE | Sign |
| --- | --- | --- | ---: | ---: | --- |
| C_positive | [1.0, 1.25] | +0.375, +0.750 | −0.1625 | −0.3228166039 | correct |
| C_negative | [1.0, −0.25] | −0.375, −0.750 | 0.0000 | +0.4519432455 | incorrect |

C_positive: Luna correctly forecast improvement, but underestimated its size by 0.160316604 MSE units. C_negative: Luna gave a zero point prediction, explicitly describing it as a cautious neutral value, *not evidence of no change*. The frozen sign criterion still fails. The unobserved development evaluation set means the exact global loss change cannot be recovered from the two probes without further assumptions; this limits interpretation of the failure. It does **not** change the prespecified score.

### 4.2 D_unknown: exploratory tool choices and functional repair

Unlike the matched pair, the D_unknown prompt named **no fault coordinate**. It disclosed a two-input, two-ReLU-hidden, one-output architecture and that exactly one scalar was corrupted. The model was **required** to issue four diagnostic calls but selected each tool and argument itself:

1. `inspect_weights({"tensor":"W1"})`: `[[-0.3,0],[0,1]]` (row-major).
2. `inspect_weights({"tensor":"b1"})`: `[0,0]`.
3. `probe_examples({"pack":"feature0"})`: positive inputs 0.5 and 1.0, outputs both 0.1 versus targets 0.6 and 1.1, residuals −0.5 and −1.0.
4. `probe_examples({"pack":"feature1"})`: both observed outputs matched their targets exactly.

The model diagnosed an inactive positive-feature0 ReLU pathway, correctly localized the planted scalar to `W1[0]`, and committed **one direct edit: +1.3** to `W1[0]` (−0.3 → 1.0). The harness, not Luna, applied the edit to a disposable model copy and independently evaluated the separate public development sample.

| D_unknown measure | MSE |
| --- | ---: |
| Corrupted / no-edit | 0.9172305740954784 |
| Predeclared simple output-layer heuristic | 0.9172305740954784 |
| Oracle restoration | 0.0 |
| Luna's committed one-scalar patch | **0.0** |

**G4 PASS: 100% recovery on the exact public developmental fixture.** The simple heuristic did not recover performance. This is a real functional result on a nine-parameter toy network, not a sealed generalization result, and there was no gradient descent or iterative patch search by Luna.

## 5. A post-run falsifier: the surgeon's missing measurement

After viewing the commitments, a separate **post-run** analysis identified a decisive evidential gap. Luna had never called `inspect_weights("W2")`. Its own explanation qualified the exact +1.3 edit with the assumption that the first hidden unit's output weight equals 1.

For positive active ReLU paths, the effective feature0 slope is `W2[0] * W1[0,0]`. The observed desired slope equals 1, but those observations cannot separately identify its factors. We constructed an **alternative single-lesion patient** with the same inspected `W1`, `b1`, feature0 and feature1 predictions/targets; only the *uninspected* `W2[0]` and healthy first-layer value differ.

| Patient | Uninspected W2[0] | Exact required ΔW1[0] | MSE after Luna's +1.3 |
| --- | ---: | ---: | ---: |
| Actual frozen D_unknown | 1.0 | +1.3 | **0.0** |
| Alternative, created after the run | 2.0 | +0.8 | **0.9172305740954781** |

The alternative's correct +0.8 edit also restores MSE 0. Both patients give the **same exact four observed diagnostics**, yet demand different exact surgeries. This demonstrates **non-identifiability of the exact treatment from the chosen evidence**. It does not negate the actual successful G4 intervention or imply that Luna hid its uncertainty. Its explanation **explicitly stated the assumption**.

See [reproducible counterexample](./analysis/identifiability_counterexample.py) and [derived results](./analysis/IDENTIFIABILITY_RESULTS.json). These are **not raw Luna observations**, no additional model call was made, and the case must not be retroactively inserted into G4.

## 6. Four separate conclusions

1. **Instrument operation:** Qualified in practice this run: all diagnostic calls valid, no API interruption; fixed contrast and independently scored repair were executable. G1 PASS, G3 PASS.
2. **Causal counterfactual prediction:** Prespecified G2 FAIL; zero on C_negative was an explicit high-uncertainty, unscorable-direction commitment, not a measured null effect.
3. **Functional weight-space programming:** One exact, independently verified, model-proposed scalar repair on a constrained unknown-fault toy patient, G4 PASS. Stronger than raw fault naming, weaker than general weight-space programming proficiency.
4. **Mechanistic sufficiency:** The ReLU-pathway diagnosis is consistent with the observed computations. The precise treatment was **not uniquely justified** by the measurements Luna collected. General mechanistic understanding NOT ESTABLISHED.

The greatest methodological lesson is that **correct repair, grounded diagnosis and sufficient identification of treatment magnitude are distinct**. A model can do one without demonstrating the others.

## 7. Limitations, public reproducibility and next question

No sealed examples; one discovery patient; no repeated independent model seeds; one nine-scalar architecture; a revealed **one-scalar corruption** assumption; familiar ReLU form; forced observation count; no oracle/private weights sent to the model; only two probes per requested pack; limited baseline family; no real larger language model patient; no blinded evaluation or model-by-harness interaction estimate. Neither EX0005A nor EX0005Aa measures whether a frontier lab's private training curriculum causes these skills.

A prospectively new EX0005B could compare **investigator × scaffold × patient**, including an open-weight language model, but the original EX0005B proposal was a **2×2 model-by-scaffold design on independent patients**. A new real-LLM-patient arm would be an explicit change in scope. A more discriminating first test may simply ask: *Will the model recognize equivalent observations and request the missing W2 measurement before committing to the exact edit?* This requires fresh precommitted controls and genuinely unseen patients, not retrospective scoring on this trace.

## 8. Provenance index

- [Controlling freeze](./evidence/PRE_LIVE_FREEZE.json), [superseded freeze](./evidence/SUPERSEDED_NOV19_FREEZE.json), [date-correction note](./evidence/FREEZE_CORRECTION_NOTE.json), [live-start marker](./evidence/LIVE_ATTEMPT_STARTED.txt).
- [Original RESULT.json](./evidence/RESULTS.json) and [ACTION_JOURNAL.json](./evidence/ACTION_JOURNAL.json), transferred verbatim from the user's uploaded archive and verified against its separate duplicate uploads.
- [Live runner after date-only repair](./source/run_luna_aa.py), [pre-fix runner](./source/run_luna_aa_before_date_fix.py), [fixture/checker](./source/ex0005aa_public.py), [offline unit tests](./source/test_offline_aa.py).
- [Notebook as prepared](./EX0005Aa_Colab.ipynb) and [pre-run planning](./planning/EX0005Aa_PROTOCOL_AS_PREPARED.md). Their old future-date warnings describe a pre-correction artifact, not the actual executed runner.
- [Post-run identifiability script](./analysis/identifiability_counterexample.py) and [separate output](./analysis/IDENTIFIABILITY_RESULTS.json), deliberately **outside** the frozen evidence directory.
- [Combined Galileo-style references](../ex0005_A+Aa_references.md), a narrative interpretation, not a substitute for journal receipts.

**Night verdict:** EX0005Aa completed; **full instrument-ready criterion FAIL via G2**, while the interface operated and an independent **secondary G4 repair succeeded**. No changes to EX0005A.
