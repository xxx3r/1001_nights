# ALGN-EX0005 | The Examiner Must Look

**One Thousand & One Nights of Alignment · Candidate next experiment**  
**Proposed after:** EX0004 and EX0004B, executed 12 November 2026  
**Status:** **UNTESTED DESIGN PROPOSAL. NOT PREREGISTERED, NOT SCHEDULED, NOT AUTHORIZED TO CONSUME A NEW HOLDOUT.**  
**Companions:** [EX0004 final account](./README.md) · [Night card](./NIGHT_CARD.md) · [Galileo-style references](./ALGN_EX0004_REFERENCES.md) · [EX0003 future concepts](../2026-11-08-ex0003/potential_futures.md)

> The scalpel was not too dull. We never found out. Our examiner had instruments, but it did not use them. Before asking whether it can repair a difficult machine, we must establish that it can examine one.

## Why return to this question?

EX0004's first trial was interrupted by **mismatched tool names and typed arguments**; EX0004B passed scripted mock tests but used **zero real diagnostic calls in both fresh Qwen contexts**. The diagnosis-first arm copied a literal sample JSON answer and committed an empty final patch. Repair-only submitted two edits and worsened held-out loss. These are **recorded actions and scores**, not a credible estimate of Qwen3-8B's maximum repair capability.

The original question remains live: **Can an open-weight language model reason about another network's computation well enough to identify interacting causes and edit the relevant weights?** EX0005 should test the precondition we skipped: **Can our real inference-and-tool interface elicit an evidence-responsive investigation?** Only then should a new blinded patient be introduced.

A failure of EX0005's public positive controls would diagnose the *experimental scaffold* as unready. It would not count as a failed diagnosis of an unseen patient. A successful scaffold would authorize a separately sealed, modest one-patient causal test, not a broad model-capability declaration.

## The proposed discriminating question

**Primary EX0005 question:** With a coherent, non-answer-bearing tool schema and a tested live Qwen conversation loop, can Qwen3-8B request diagnostic evidence, incorporate a returned observation into a new decision, and commit a non-placeholder, prospectively checkable diagnosis before patch feedback?

- **H1, working investigative interface:** On known, public sacrificial cases, real Qwen generations perform valid diagnostic calls, condition subsequent requests or predictions on returned information, and submit valid, non-template commitments. This makes a fresh blinded patient trial *eligible*.
- **H0, inadequate elicitation:** Calls are skipped, malformed, mechanically repeated, or disconnected from evidence; submitted fields duplicate formatting examples or remain unsupported. The harness fails its instrument gate. **No blinded patient trial is conducted under that scaffold.**

A secondary, conditional question is whether the successfully validated interface supports functional *and* mechanistic repair on a brand-new interacting-fault patient. A negative result there would have clearer meaning because actual diagnostic access was demonstrated first.

**What this plan does not ask:** Did EX0004B secretly succeed? Can we retest C06 until it passes? Does one successful patch establish a general interpretability or intelligence breakthrough? All three are outside scope.

## Phase 0 · Public instrument design (no evaluator-private patient)

Before any new sealed specimen is created or exposed, build the smallest reliable instrument with **one** model, one version, one coherent contract and one executable loop. This is engineering development, not confirmatory experimentation.

1. **Choose a real Qwen-compatible action protocol.** Prefer the model's recommended tool-call template/parser when supported, or use a strict JSON decoder with one machine-readable schema. Do not mix natural-language capability aliases with callable identifiers. Test model-generated (not merely handwritten mock) requests end-to-end.
2. **Make output format non-answer-bearing.** A schema may show field types, enums and constraints, but no complete `submit_diagnosis` object with plausible fault addresses, predicted interaction or numerical patch. If a parser needs an example, use structurally invalid placeholders and explicitly test that they cannot be submitted. No sentinel explanatory string should be treated as a diagnosis.
3. **Separate stages clearly:** `observe` → `commit_diagnosis` → `trial_patch` → `commit_patch`. In the investigative condition, `commit_diagnosis` is unavailable until the required evidence-interaction gate is met. This is a declared *protocol requirement*, not proof that the model voluntarily chose to investigate.
4. **Make the diagnostic affordances genuinely useful.** Bounded weight slices, forward examples with targets/predictions, hidden-activation summaries, and input-feature counterfactuals must each return interpretable JSON. Include the corrupted model's development baseline so an attempted patch can be compared meaningfully. Do not give healthy weights, oracle corrections or planted coordinates.
5. **Bound and log everything.** Predefine per-call sizes, maximum 12 diagnostic calls, maximum two patch trials, maximum six final scalar deltas, total actions, token/time limits, malformed-call handling, deterministic seeds and fresh-context boundaries. Persist every model action and response before dispatch. Treat generation truncation as its own outcome; do not silently retry.
6. **Use source-based code integrity.** Freeze a normalized source file or Git commit plus artifact hashes; verify loaded source and executable behavior. Do not rely on a `marshal.dumps(__code__)` hash as a sole notebook integrity test. Leave EX0004B's A1 discrepancy recorded, not rewritten.

**One decisive engineering rule:** a mock-only end-to-end test is insufficient. The actual Qwen model must produce and respond to real tool requests on *sacrificial data* before the diagnostic instrument is declared ready.

## Phase 1 · Public sacrificial tests and the real-model gate

Create two transparent, tiny public networks with known synthetic targets and deliberately obvious, different lesions. Their fault keys are available to the experimenter, **not to the live teacher prompt**. They are development fixtures only and must never become the sealed test or be counted as independent evidence of generalized mechanistic repair.

**Test A: Action round trip.** Given a tool contract, can Qwen issue a valid `weights` or `examples` call, receive its numeric response, and issue a second different, relevant diagnostic action? Require **two valid real diagnostic calls of different kinds**, not two parser successes on strings we wrote ourselves.

**Test B: Evidence dependence.** Construct paired public calibration inputs or tool responses that differ in a causally relevant feature, while holding the prompt format fixed. Before running Qwen, record the predicted difference in its subsequent request or stated causal prediction. Check whether its behavior changes appropriately. This is stronger than merely counting tool calls.

**Test C: Commitment and repair.** The model must submit a schema-valid, non-placeholder diagnosis whose claimed fault indices refer to real tensor positions, and a sparse patch proposal or principled abstention. A simple known-lesion case should admit an oracle-verified repair. Measure whether the model's patch actually helps. Do **not** score polished explanation alone as mechanism.

**Test D: Stop and resume hygiene.** Test malformed JSON, over-budget requests, interrupted generation, append-only receipts, context isolation between episodes and preservation of the first outcome without background retries. The actual tested parser must be the one used at evaluation.

**Suggested instrument acceptance gate, to be frozen before the sacrificial runs:** the two public patients each complete a distinct two-tool observation sequence; at least one case demonstrates response-dependent causal prediction; both produce well-typed commitments; the known-positive-control patch can be applied and scored, with no unauthorized private access. If any element fails, disposition **INSTRUMENT NOT READY**. Repair the scaffolding openly *on public development fixtures only* and schedule a new separately frozen run. Do not invent an efficacy score for the unseen patient.

A forced observation-first prompt measures **ability under that scaffold**, not the spontaneous preference to inspect. If desired, compare a free-choice arm as a separate preregistered factor, rather than silently calling forced calls autonomous curiosity.

## Phase 2 · Freeze the actual examination, only after the gate

Once the public instrument passes, register a new immutable test packet **before generating a fresh blinded patient**:

- **Primary model:** Qwen3-8B; pin exact revision, tokenizer, template/parser, BF16/quantization and sampling settings. A new context and independent generation seed for each arm; no EX0004 transcripts in its context.
- **Fresh patient:** new initialization, training and calibration roles, new 6→12→12→1 tanh target or deliberately new target coefficients. No reuse of C03, C06, EX0003 open holdouts or their private keys for final evaluation.
- **Fixture gate:** nonconstant healthy prediction, substantial corruption, two independently important fault groups with measured signed 2×2 interaction, meaningful A-versus-B ranking separation, exact oracle restoration; zero-only and a predeclared obvious-magnitude heuristic must fail. Freeze candidate cap and first-qualifier rule. If none qualifies, **teacher NOT RUN**.
- **Hidden sets:** disjoint teacher-development and sealed ID, shifted and paired-counterfactual samples. Final labels and fault key kept outside the teacher interface. Confirm that the holdout was not opened during prompt or parser development.
- **Comparators:** healthy, corrupted, zero-only, transparent numerical heuristic, oracle A/B/joint, diagnosis-first and (if adequately resourced) repair-only. A neuron-permutation test is a *separate stronger follow-up* unless explicitly included and resourced before freeze.
- **Precommitted metrics:** shifted corruption-gap recovery (e.g. ≥80% with ID/variance preservation), exact fault-region identifiers, signed isolated effects, interaction sign and nuisance-sensitivity direction. Define ties, missing actions, confidence, denominators and negative recovery before exposure. Do not promote a lucky multiple-choice field to a causal explanation.

**Important design correction:** require the researcher or an independent script to verify a *material positive control*: the evaluator can apply a nonzero oracle patch and recover the healthy outputs, the tool data can reveal information about the fault, and a non-oracle trivial patch does not already solve the task. Otherwise the patient may be difficult but not informative.

## Phase 3 · One fresh blinded teacher run

A minimal evaluation sequence could be:

1. Freeze protocol, evaluator, prompts and the fresh patient. Prepare a unique unguessable test identifier, but **do not put fault keys or answer-bearing JSON examples into the prompt**.
2. Run one Qwen diagnosis-first episode. Require at least two distinct tool observations *before* `submit_diagnosis`; log them as procedural compliance. Require a **specific prospective prediction** about an evaluator-only counterfactual in addition to categorical choices.
3. Lock diagnosis, candidate patch, and any trial feedback before the sealed evaluator runs. Keep all malformed calls and abstentions. If the run fails to generate a valid commitment, record failure to complete the protocol, not an imaginary repair.
4. Run the optional previously frozen repair-only comparator on the same patient with a separate context. Do not inspect the private answer key or tune prompts between arms.
5. Open sealed data **once**, after both frozen outputs and controls are committed. Evaluate functional recovery, localization and causal predictions independently; report raw MSE, denominators and negative controls. Never reuse this holdout for next-version prompt selection.

**Interpretation ladder:**

| Observation | Permitted conclusion |
|---|---|
| Real-model preflight fails | Harness not qualified; blinded teacher **NOT RUN** |
| Instrument passes, model ignores required diagnostic protocol | Tool-use compliance failure under a qualified interface; repair ability still untested |
| Valid probes, wrong causal predictions, poor patch | Bounded failure on the specific patient; no general incapability claim |
| Patch restores function but explanation fails | Functional repair without demonstrated faithful mechanism, consistent with H2-like behavior |
| Correct prospective causal predictions **and** effective sparse repair | Bounded H1 instance on one new patient, not general weight-space interpretability |
| Nondiscriminating data, leaked answers, broken grading | **INCONCLUSIVE** despite attractive numbers |

## Scientific integrity, timebox and human learning

This is **not a preauthorization to run EX0005**. A future night begins by choosing a narrow primary contrast and registering its thresholds, then stops on schedule. Avoid converting the public preflight into an unlimited search for a prompt that happens to impress us. If the instrument needs extensive tuning, close an **instrument-only night** and reserve a later *new* night for blinded efficacy. There is no backlog debt or mandatory continuation.

For human-first practice, before asking the assistant to implement the new trial, independently write: (a) what observations would distinguish the two lesions; (b) the factorial interaction formula `I=L11−L10−L01+L00` and how squared error can influence it; (c) a failure mode that produces a correct-looking diagnosis without evidence; and (d) the smallest false-positive test for the grader. Record assistance I/H/C/D accurately.

**Deliverables if authorized:** one frozen instrument specification; one real-Qwen public preflight trace; at most one new blinded notebook; one independent evaluation JSON; one NIGHT_CARD recording **what actually ran**. No new agent platform, no sprawling benchmark, no claim of research autonomy.

**The hypothesis survives. The old result does not improve by surviving it. Build the observer first; only then examine the machine.**
