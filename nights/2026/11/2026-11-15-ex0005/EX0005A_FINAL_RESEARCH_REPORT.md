# ALGN-EX0005A | Final research report: The Examiner Must Look

**Session:** 15 November 2026 (America/Denver), Sunday atelier, hard stop 20:00.  
**Archival closure:** retrospective documentation after the session; **no post-freeze Luna calls or edits** are included in these results.  
**Investigator:** GPT-6 Luna, OpenAI Responses API.  
**Night disposition:** **FAIL — full instrument-qualification criterion not met**.  
**Capability disposition:** **INCONCLUSIVE — no general finding about Luna's causal or mechanistic understanding**.  
**Assistance:** C (human predictions collaboratively expressed with AI); original instrument implementation AI-drafted.  
**Test surface:** public synthetic networks only; no new sealed patients or blinded efficacy claim.

## Research question

Can model-generated, bounded numerical observations yield an externally verified, evidence-responsive causal prediction and an optional independently scored direct-weight intervention?

The original design separated numerical calibration (P0), native API diagnostics (G1), a matched causal evidence contrast (G2), checkable commitments (G3), and optional public patch efficacy (G4). These do not collapse into one measure of intelligence or mechanistic understanding.

## What was frozen and what survived

- Original protocol: [EX0005A_PROTOCOL_DRAFT.md](./EX0005A_PROTOCOL_DRAFT.md), retained **unchanged** as the pre-run design document. Its DRAFT/NOT RUN header describes that historical snapshot, not the final result.
- Human predictions: recorded collaboratively, including skepticism about explaining why a repair works, concern about a heuristic shortcut, an incorrect-sign checker test, and caution against inferring mechanism from patch success. Disclosure was **C**, not independent I.
- User-shared original preflight freeze: 2026-11-15T19:19:00.431419-07:00, SHA-256 5019d1a9fc3baff6a5e4f21b5b1b2ae0de9b70b1a6cabad031e93bab8ff476c1. The child-process credential issue was fixed by passing the notebook secret through a temporary environment variable; the model/patient source code and hypotheses were not changed.
- **Actual live-run freeze identifier:** 4fad7aa72bd20393d04b09212da1adccd288f1b838fcfdf2c9c7eaec406e4112, as independently recorded in the uploaded RESULTS.json. The full second freeze-manifest JSON was not uploaded, so its exact creation timestamp and full bytes are **not archived here**. Do not mistake the 19:19 timestamp for the actual live freeze.
- Source SHA-256 as recorded in the preflight: ex0005a_public.py = 2bb71522adfa5a4334b0dd374d92b360544b378d86ec8e52e9e8a95152b1bf9e; run_luna.py = 2c8716c889824a58fd59ed70194a5396a41068654bcf3be3f5158879f05fb3ff. The archived source files match these hashes. The notebook is an executable *setup template*; the human-first cell in the Colab run was filled later.
- Public fixture fingerprint: 39e3064ac2c4391b1013e9a37299bc527f5a7e6cd67549e1b075b06c85706fc6. User-recorded frozen settings: reasoning effort low, 1,800 maximum output tokens per response, 16 response-call cap, 4 valid diagnostics per case, model identifier gpt-6-luna, no model sampling seed.

## Independent numerical controls

Colab Cell 2 reported **7/7 local tests passing** and independent checker status G0_LOCAL_PASS_ONLY. The known Boolean AND oracle produced [0,0,0,1] exactly; a deliberately bad candidate produced [0,0,0,0] and failed. Known oracle repair recovered all three public cases; no-edit had nonzero error, and zeroing was not accepted as an oracle substitute.

| Public case | Corrupted MSE | Oracle MSE | Heuristic MSE | Delta MSE for a −0.25 edit to W2[0] |
| --- | ---: | ---: | ---: | ---: |
| P1_plus | 0.489956 | 0 | 0 | −0.272198 |
| P1_minus | 0.489956 | 0 | 0 | +0.381077 |
| P2 | 0.322914 | 0 | 0.116249 | +0.116608 |

P1_plus/P1_minus use a sign-flipped relevant coefficient; under the planned intervention the correct directions are opposite. The exact heuristic repairs both P1 variants, limiting any claim of model advantage even if patching had been attempted.

## What the investigator actually did

**Response denominator:** 11 native API responses, 10 completed and 1 incomplete. **Diagnostic denominator:** 19 model-generated diagnostic attempts: 9 valid, 10 invalid or over budget. The uploaded journal logs the P2 attempt even though RESULTS.json omits the interrupted case.

| Case | Diagnostic requests (valid / attempted) | Distinct valid tools | Committed prediction | Outcome |
| --- | --- | --- | --- | --- |
| P1_plus | 2 / 3 | inspect_weights, probe_examples | Yes | Correct sign, inaccurate magnitude, patch abstained |
| P1_minus | 3 / 8 | inspect_weights only | No | No matched prediction; 1 invalid probe and 4 over-budget calls |
| P2 | 4 / 8 | inspect_weights only | No | 4 over-budget probes; incomplete final API response |

P1_plus: Luna saw W2 = [1.75,0.5] and one feature0 development probe with target 0.6, prediction 0.975 and residual +0.375. It committed a downward effect for the −0.25 W2[0] intervention: **predicted delta MSE −0.05**, independently computed **actual −0.2721980156625408**, absolute error **0.22219801566254083**. The sign and reported fault region were correct. Its uncertainty was high and its patch was empty (explicit abstention); **no model patch was evaluated**.

P1_minus: Luna saw W2 = [0.25,0.5], plus W1 and b1 values. Its probe request failed validation; subsequent calls exceeded the four-diagnostic budget. It made no completed causal prediction. The valid request signatures differ between P1_plus and P1_minus, so the prespecified matched-observation contrast is **not satisfied**.

P2: The journal records four valid weight-inspection requests and four over-budget probe requests. The eleventh API response returned **incomplete**, reason **max_messages**, with no valid final commitment. The runner raised a RuntimeError and skipped its final scoring block.

**Do not silently replace raw machine statuses.** The immutable RESULTS.json reports G1/G2/G3/G4 = NOT RUN and instrument_ready = false. These gate labels were never computed because of the interruption. The manual evidence audit shows the **full instrument-ready criterion was not met**: P2 lacked distinct kinds, the P1 pair lacked two matched commitments, and G3 was incomplete. G2's model evidence-dependence hypothesis is **inconclusive**, not demonstrated false. G4 was not executed.

## Causal interpretation, failure modes and limits

1. **Prompt leakage of the target:** The scaffold already highlighted the W2[0] perturbation. Correctly naming W2[0] does **not** demonstrate independent discovery of an unknown lesion.
2. **One probe does not establish global mechanism:** P1_plus's overprediction made a downward-weight heuristic plausible, but the magnitude prediction was inaccurate; there was no activation-level causal check or matched P1_minus commitment.
3. **Tool interface matters:** Invalid index packs, batched native tool requests exhausting the local budget, and an incomplete response obstructed the planned evidence contrast. These are observed interface/elicitation failures, not a finding that Luna is unable to understand weights.
4. **A complete independent comparator matters:** The simple heuristic achieved MSE zero on both P1 variants. Even a correct model patch would need comparison with it and with no-edit/oracle checks.
5. **No causal claim about model internals:** Correct numerical behavior, successful future repair, or confident narration alone cannot prove an internal mechanistic representation.

There was **no model-authored intervention** and no sealed holdout opened. No population-level statistics or model-size threshold are inferable from these few public cases. Actual billed currency cost and a separately exposed model revision were not available in the uploaded receipts; token use was logged per response.

## Final verdict and learning

- **G0, public numerical/checker readiness:** PASS.
- **P0, Luna Boolean AND positive control:** PASS (4/4).
- **Real interface evidence:** Some native tool use observed; complete required G1 **not met**.
- **G2, evidence-responsive paired causal contrast:** INCONCLUSIVE, no matched completed pair.
- **G3, checkable commitments across required cases:** Not met; P1_plus only.
- **G4, functional direct patch:** NOT RUN (abstention, then interruption).
- **Night-level instrument qualification:** **FAIL**, based on the completed manual audit of the attempt; not a rewrite of the uncomputed runner labels.
- **Broader model capability:** **INCONCLUSIVE**.

**Acquired skill:** separate raw events, evaluator validity, counterfactual predictions, and mechanistic claims; inspect denominators and freeze history rather than inferring success from a zero exit code.  
**Remaining deficit:** a matched, instrument-qualified contrast and fault-localization task that does not point to the answer.

## Evidence and reproduction

- [Raw RESULTS.json](./evidence/RESULTS.json), user-uploaded SHA-256 **16bd3d9dd5c9346a06a2b3ea9d2e432f86d42b70264a6cbe4687cd5d85e6178c**.
- [Raw ACTION_JOURNAL.json](./evidence/ACTION_JOURNAL.json), user-uploaded SHA-256 **48d0f918dfc1c0b42a935a3af8f12d2189ed0318a6b72dfdcedd20b1d44ddb72**.
- [Archived Colab notebook](./EX0005A_Colab.ipynb) and frozen [public fixture/checker](./source/ex0005a_public.py), [API runner](./source/run_luna.py), [offline tests](./source/test_offline.py). These are historical instruments, **not instructions to reopen EX0005A or rerun after its stop time**.
- [Night card](./NIGHT_CARD.md) is the short closure record. [Potential futures](./potential_future.md) is speculative, not an EX0005A result.

**Successor boundary:** EX0005Aa is separately authorized *after* this evidence was observed. Its changed instruments and any future Luna responses must receive new prospective receipts and a distinct verdict; they never change EX0005A's historical outcome.
