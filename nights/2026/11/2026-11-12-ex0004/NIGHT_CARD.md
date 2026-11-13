# NIGHT CARD | ALGN-EX0004: Land's Quiet Scalpel II

**Night/date:** 0004 · 12 November 2026 (America/Denver)  
**Window:** Original up-to-four-hour window; one human-authorized exception toward midnight. Actual elapsed minutes not measured.  
**Assistance:** **D** (AI-drafted implementation, evaluation and documentation; human-directed criticism and decisions).  
**Disposition:** **Pilot STOPPED, teacher NOT RUN. EX0004B formal H1 FAIL; model capability INCONCLUSIVE.** Night closed.

**1. Question.** Can Qwen3-8B, with bounded diagnostic tools, identify two interacting faults in a 253-parameter network, predict their separate and joint consequences, and repair them sparsely on unseen data?

**2. H1 / H2.** H1 requires correct localization, prospective causal predictions and ≥80% recovery of the shifted corruption gap with preservation guardrails. H2 allows functional repair without faithful diagnosis. An **instrument/elicitation failure** emerged retrospectively, not as a preregistered third arm.

**3. Human-first reasoning.** The researcher challenged contradictory tool names, refused to call the deteriorating pilot a clean test, initiated a fresh notebook and patient, and questioned treating a failed harness as a failed model. Independent human coding or mathematical mastery was **not** assessed. Most code and checks were AI-drafted.

**4. Method.** The pilot used Qwen3-8B and an interacting-fault tanh network. Its successor EX0004B trained a fresh 6→12→12→1 patient; 16 candidate lesions were frozen, C06 was the first qualifier after five rejections. Each arm received 12 diagnostic calls and two patch trials, with at most six final edits. Frozen model revision: `b968826d9c46dd6066d109eabc6255188de91218`. Final independent test: **1,000 ID**, **1,000 shifted** examples, **256 counterfactual pairs**, once after both outputs and the evaluator were locked.

**5. What ran / errors.** Pilot: **6 calls, 3 invalid**, multiple logged interface amendments, no committed diagnosis/patch or sealed evaluation; **NOT RUN** for intended teacher test. EX0004B: scripted tool mocks passed. A pre-exposure `marshal` fingerprint mismatch was recorded under A1; source AST and mock replays matched, but binary cause remains unresolved. Diagnosis-first: **4 actions, 0 diagnostics, 2 patch trials, 0 final edits**. Repair-only: **3 actions, 0 diagnostics, 2 patch trials, 2 final edits**. No post-exposure prompt corrections.

**6. Evidence and independent check.** Sealed shifted MSE: **healthy 0.000209; corrupted 0.117318; diagnosis-first 0.117318; repair-only 0.127005**. Gap **0.117109**; recovered fractions **0.00%** and **−8.27%**, both formal functional **FAIL**. Actual fault edges: `fc1.weight[4,5]` and `fc2.weight[8,4]`, plus associated biases. True interaction **negative**. Diagnosis-first submitted the public formatting example *verbatim*, including “FORMAT EXAMPLE ONLY. Not a diagnosis.” Locations and interaction sign wrong; ranking matched by copying; formal mechanistic **FAIL**. Evidence includes immutable submissions, hash-chained events, oracle controls and the one-shot sealed scorer, **AI-authored, not independently reimplemented externally**.

**7. Narrowest claim.** The **executed outputs** failed the formal H1 gates. Neither arm examined the patient with diagnostic observations. Therefore the experiment **did not meaningfully resolve Qwen3-8B's ability to diagnose or repair when properly elicited**. H2's useful-repair-without-diagnosis outcome was not observed. This is primarily an instrument failure, not a general model incapability result.

**8. Uncertainty, learning, stop.** Why did both arms avoid diagnostic tools? A copied example and poor interface affordances are observable confounds; their causal weights are **unknown**. The lesson concerns *measurement design*, not demonstrated human technical mastery. EX0005 is **proposed only**: real-Qwen sacrificial tool preflight followed, if qualified, by a **fresh** blinded fixture. No reuse of C06's now-open holdout; no rescue of EX0004's verdict.

**Records:** [README](./README.md) · [pilot closeout](./ex0004_pilot_archive/EX0004_pilot_closeout.json) · [sealed report](./algn_ex0004b/SEALED_EVALUATION_REPORT_V1.json) · [A1 amendment](./algn_ex0004b/CODE_INTEGRITY_AMENDMENT_A1.json).
