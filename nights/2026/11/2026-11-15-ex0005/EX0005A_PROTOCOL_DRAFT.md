# ALGN-EX0005A | Protocol draft v0.1: evidence before incision

**Written for:** 15 November 2026 · **Status:** DRAFT, NOT FROZEN, NOT RUN.  
**Primary role:** instrument-qualification study; any blinded efficacy claim requires its own new night and prospective freeze.  
**Primary investigator:** GPT-6 Luna through the OpenAI Responses API, **conditional on a live capability and billing check**.  
**Environment:** Colab; local synthetic PyTorch patients, temporary model copies, independent Python checker.  
**Assistance:** design text AI-drafted with human direction; record actual assistance I/H/C/D after execution.

## 0 · Human-owned pre-execution prediction (leave blank until human completes)

- Before AI assistance, my predicted failure mode for Luna is: **[HUMAN TO FILL]**
- My predicted difference between two diagnostic observations is: **[HUMAN TO FILL]**
- The smallest test that would catch a false grader success is: **[HUMAN TO FILL]**
- A plausible-looking but unsupported mechanistic claim would be: **[HUMAN TO FILL]**

Do **not** claim these fields were independently completed if an AI fills them. Timestamp and freeze the filled hypotheses and acceptance thresholds before live model evaluation.

## 1 · Questions and competing predictions

**Primary Q:** Under a real, minimal, well-typed numerical tool interface, can Luna perform an observation-conditioned causal investigation of a tiny corrupted neural network?

- **H1, qualified observation loop:** actual model-generated calls succeed, its subsequent prediction changes correctly with relevant returned evidence, and a checkable commitment is recorded before any patch-result feedback.
- **H0, unqualified loop or evidence use:** actual tool calls fail or are skipped; or the model returns a placeholder, parrots a format example, or makes a prediction that fails the predetermined evidence contrast.
- **Rival explanations:** code-generated scaffold supplies the answer; task description leaks the fault; easy heuristic suffices; chance succeeds on one example; only the syntax, not the reasoning, changed. Design controls for each instead of interpreting model confidence as evidence.

A numerical positive-control network and a public patch test are **secondary outcomes** with their own criteria. Do not combine all scores into an invented general-intelligence measure.

## 2 · Public sacrificial fixtures (development only)

**Fixture P0: direct weight writing.** Give Luna the architecture of a tiny 2 → 1(ReLU) → 1 network and ask it to implement a Boolean AND over binary inputs as numeric weights/biases. Independent checker enumerates all four inputs and tests outputs against [0, 0, 0, 1], with a prospectively specified numerical tolerance. No tools for the investigator in P0. The evaluator includes a known analytic solution and a trivial programmatic compiler baseline. P0 is a sanity check, not a demonstration of newly discovered algorithms.

**Fixtures P1 and P2: examine a known-fault network.** Use two small, independently seeded synthetic networks with different planted lesions and held-out *development* examples. Expose architecture, tensor identifiers/shapes, feature roles and a consistent public measurement contract. Store the healthy checkpoint and lesion keys in an evaluator that is **not** accessible to the model. Verify pre-exposure that both patients exhibit material corruption, an oracle patch restores healthy behavior, and trivial zeroing/no-edit baselines are evaluated. No sealed test data are generated or opened for these public fixtures.

**Paired evidence contrast.** Prior to the relevant calls, freeze two observations that change one causally relevant quantity while keeping the request format and all extraneous details fixed. Freeze the *correct directional difference* in a subsequent prediction. The model's predicted contrast must be checked against a numerical oracle, not a human impression that its prose is reasonable. A second negative/control pair with irrelevant or unchanged evidence may be included if time permits; it cannot replace the causal pair.

**Patient eligibility check:** if the oracle cannot repair the patient or the evidence contrast has no numerically discriminating answer, classify fixture/instrument failure; do not call a teacher failure.

## 3 · Minimal real-model tool contract

- Use an API-native structured function-call protocol, not a hand-written imitation of tool calls. Confirm the current model's API support and record the exact model identifier and call parameters at run time; avoid unsupported generation parameters. Use only a Colab secret reference, never inline the key or store raw authorization headers.
- Offer two small, read-only tools: **inspect_weights(tensor, start, count)** and **probe_examples(regime, indices)**. Additional tools (activation summaries, feature counterfactuals) are optional only if justified within the timebox and announced before freeze. Bound index ranges and result sizes; dispatch exactly the identifiers provided in the schema.
- Return compact numeric JSON (tensor shapes, actual requested values, targets/predictions and provenance). Tools must not return healthy weights, planted fault indices, suggested patches, sealed examples, or answer-bearing examples.
- State machine: **observe → commit_diagnosis → optional_trial_patch → commit_patch / abstain**. Require at least two *different* valid observations before diagnostic commitment for this scaffold. This is **forced observation compliance**, not evidence that the model spontaneously preferred to investigate.
- Model commitment names a fault region, an uncertainty level, and one falsifiable directional/quantitative prediction; model patch is optional and separately scored. The protocol must not contain a fully filled diagnostic JSON specimen.
- Include one deliberately malformed tool request in local mock validation, plus a controlled interrupted/truncated case if practical. Log parser rejection; do not treat a syntactic mock as evidence of real model use.

## 4 · Proposed precommitted checks (freeze exact versions before real calls)

| Gate | Proposed acceptance | What failing it means |
|---|---|---|
| G0: local checker | Known analytic weight-writing solution and oracle repair score correctly; no-edit does not falsely pass | **Evaluator not ready**; teacher efficacy not run |
| G1: live tool use | On P1 and P2, Luna makes ≥2 valid model-generated diagnostic requests of ≥2 distinct kinds, with real returned numerical evidence | **Interface/elicitation not qualified**; no blinded extension |
| G2: evidence dependence | ≥1 prospective directional prediction changes appropriately across the frozen causal evidence pair; formatting-only changes do not count | **Evidence-use gate FAIL** under tested scaffold |
| G3: commitments | Both public cases yield valid, non-placeholder, checkable commitments or explicitly logged abstentions; do not score abstention as success | **Completion gate FAIL**, or abstention as recorded |
| G4: public intervention (secondary) | Oracle nonzero patch works; if Luna commits a patch, report raw before/after and heuristic/no-edit comparisons under independent evaluator | **Functional PASS/FAIL or NOT RUN**, separate from G1–G3 |

**Instrument READY** requires G0–G3 plus evidence that no evaluator-private answers reached the model. G4 reports functional ability only where a model patch actually ran. These draft gates must be frozen **before** the live preflight; if changed after observing behavior, label the runs exploratory and do not claim prospective PASS.

## 5 · Fixed budgets and receipts

At execution: explicitly register the exact API model and version (if available), model/output reasoning settings, any temperature/sampling constraints, Colab/PyTorch versions, seeds for P0/P1/P2 and model calls, tool schema, parser version, source fingerprint, max tokens, cost cap and stop time. Do not assume a stable model revision is exposed by the service.

Suggested upper bounds unless reduced at freeze: **12 diagnostic observations per patient, 2 temporary patch evaluations per patient, 6 final scalar edits**, and a **45-minute initial harness-build cap**. Record every call, response, validation error, timeout, truncation, abstention and unexpected cost. Each attempted edit applies to an isolated copy of the corrupted model and reports its exact delta semantics. No general filesystem access for the investigator.

Preserve a short run manifest and raw action journal, a public fixture/checker receipt, and an independent result table. If source changed during development, record a new source hash; freeze before model-contact. Never reuse the EX0004B A1 `marshal` mismatch as proof of binary equivalence.

## 6 · Verdict discipline and end-of-night closure

Report these outcomes independently: (i) code/checker readiness, (ii) real API/tool-loop validity, (iii) evidence-conditioned prediction, (iv) function of any tested patch, (v) whether mechanistic prediction was actually correct.

A night-level **PASS** may be awarded only for its *precommitted primary instrument gate*; secondary patch success is separate. **FAIL** means a valid attempted gate failed. **INCONCLUSIVE** means the observed result cannot distinguish hypotheses (leak, defective oracle, nondiscriminating pair). **NOT RUN** means no valid relevant model trial executed. **SKIPPED** is not an attempted night. If the interface fails, do not label Luna incapable of weight-space programming.

Close by 20:00 America/Denver or earlier; no continuation debt. Complete the [night card](./NIGHT_CARD.md) with actual timestamps, observations, malformed/missing counts, provenance, assistance and the narrowest justified conclusion. **Do not invent results ahead of execution.**
