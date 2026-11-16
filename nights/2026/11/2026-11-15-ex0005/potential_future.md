# After the Examination: EX0005B and Distant Bridges

**One Thousand & One Nights of Alignment · Research idea bank arising from EX0005A**  
**Written:** 15 November 2026 (America/Denver)  
**Status:** **SPECULATIVE / UNTESTED. NOT PREREGISTERED, SCHEDULED, OR AUTHORIZED TO CONSUME A HOLDOUT.**  
**Source documents:** [EX0005A](./README.md) · [Protocol draft](./EX0005A_PROTOCOL_DRAFT.md) · [EX0003 futures](../2026-11-08-ex0003/potential_futures.md) · [EX0004B report](../2026-11-12-ex0004/algn_ex0004b/EX0004B_FINAL_RESEARCH_REPORT.md).

> The ambition is not to make the surgeon look clever. It is to find out which part of a successful operation belongs to the surgeon, which to the instruments, and which to the patient.

## 1. EX0005B | The Surgeon and the Operating Room

**Potential future independent night.** A matched comparison of **investigator capability × scaffolding**. This is a new experiment, not a continuation owed to EX0005A, and not a retrospective rescore of EX0003 or EX0004.

### Hypothesis

Weight-space programming competence depends on the interaction of **(a) learned model capabilities, (b) target network representational structure, and (c) numerical evidence/tool access**. EX0005B would investigate part (a) × (c) while holding patient types as closely matched as practicable. A two-model study cannot establish a sharp intelligence threshold or cleanly isolate parameter count from post-training.

### Minimal 2 × 2 design

| Investigator | Static evidence only | Interactive numerical evidence |
|---|---|---|
| Qwen3-8B | A | B |
| GPT-6 Luna | C | D |

Static evidence receives a frozen diagnostic packet and no feedback before commitment. Interactive evidence permits a prespecified observation-and-patch protocol. These conditions differ in **available information and feedback**, not solely interface quality; identify the scaffold effect honestly. Compare equal patient families, frozen target specifications, newly independent seeds, measurable tool/token/compute budgets, and a transparent scoring script.

### Primary and secondary measures

**Primary, if preregistered:** shifted corruption-gap recovery from a sparse patch, with familiar-performance and prediction-variance guardrails. Let loss be held-out MSE and define recovery R = (L_corrupt − L_patch)/(L_corrupt − L_healthy), only when the denominator is materially positive; retain negative values. Compare the scaffold benefit within each investigator and their difference:

- Δ_H(M) = R(M, interactive) − R(M, static)
- I = Δ_H(Luna) − Δ_H(Qwen3-8B)

**Separate secondary outcomes:** schema validity, real observation use, prospective sign/direction predictions for isolated faults and their interaction, localization, nuisance counterfactual prediction, explanation accuracy, tool errors, cost, and time. Do **not** infer true mechanism from the final patch score alone.

### Essential controls and sample discipline

- Completely new patients and independent calibration/development/sealed test splits, with prospective seed namespaces; never re-use EX0003/EX0004 opened holdouts or C06 for selection.
- Simple no-edit, zero-only, magnitude/path heuristic, random edit and exact oracle recovery, checked before any model exposure. A trivially solvable fixture does not establish model advantage.
- For a difficult patient: two independently important interacting fault groups; measurable signed 2×2 interaction; a nontrivial oracle; verified that naive zeroing fails preservation gates. If prospective fixture gate fails, report **teacher NOT RUN**.
- Independently freeze each model's full prompts/configuration, budgets and total trials. If using only one patient per cell, report descriptive observations, not a population-level interaction or threshold.
- Hold diagnosis and patch outputs fixed before opening new sealed evaluation *once*. A different night must be used for a redesigned follow-up.

**Interpretation:** Qwen only improving with tools supports harness value for that tested task; Luna outperforming under identical evidence supports a model effect; different within-model scaffold gains are consistent with interaction. None of these by itself proves emergence at a universal model-size threshold, fidelity of causal explanations, or superalignment.

### Relationship to EX0005A

A passing EX0005A is a **measurement readiness gate**, not automatic authorization of B. If A fails, preserve its verdict; a future new instrument night can repair public scaffolding, without opening a blinded patient or extending A overtime.

## 2. Future bridge | Can a smaller student learn to repair networks?

**Speculative independent line, not an EX0005B subtask.** A stronger teacher could potentially propose a bounded intervention in a small open-weight language model (for example, a 0.6B–0.8B student). The modified student would then operate **alone** on novel toy weight-repair tasks, compared against its frozen pre-intervention checkpoint and a larger reference model such as an 8B model.

A narrowly trained or edited 0.8B model might beat an 8B model on **a specific task distribution** without being generally more capable. This is plausible specialization, not evidence of automatic recursive self-improvement. Record whether intervention is a direct numerical weight patch, gradient-based adaptation, LoRA/adapter training, activation steering, or simple prompt/tool scaffolding; these are different treatments.

A defensible test requires a small isolated edit surface, immutable original checkpoint, controls for random patch, ordinary fine-tuning and training leakage, held-out *novel* task families, matched inference budgets, and preservation tests for unrelated capabilities. Any test of student surpassing a larger model must evaluate both on identical independent problems and clearly disclose assistance at deployment.

## 3. True recursive self-improvement (RSI) remains speculative

A **single successful self-edit is not RSI**. A stronger operational claim would require a system to repeatedly propose and validate improvements to its *own* future improvement process across multiple cycles, on new tasks, without a hidden external teacher solving the steps or repeated test-set selection. It would need independent evaluations, cumulative-versus-transient gain measurements, resource accounting, preserved reference checkpoints, and failure/regression monitoring.

A model editing an external toy network, a stronger teacher editing a weaker student, and a model modifying its own weights are three different cases. Even verified bounded self-modification would not establish an open-ended intelligence increase, safety, autonomy, or recursive runaway dynamics. Compute costs and selection artifacts could defeat the premise.

## 4. The superalignment question is still open

**Research question:** How could human oversight remain reliable when the systems being trained or deployed outperform human supervisors in relevant domains? This is broader than solving weight editing. Weak-to-strong generalization typically studies weaker supervision of a stronger learner; a strong teacher modifying a weak student, or a weak model inspecting a stronger target, tests related but different mechanisms.

One potential contribution of weight-space methods would be **bounded, externally verifiable oversight**: a system proposes an intervention; independent measurements check whether it improves specified behavior while preserving unrelated functions. This would be useful only with realistic distribution shift, trustworthy metrics, adversarial controls, and the ability to reject unsupported causal narratives. A repaired task score is not evidence that the target is aligned, honest, controllable, or safe to deploy.

The Alan Turing Institute replication itself found that frontier models could sometimes identify suspicious checkpoints and adapters while failing to recover the trigger or underlying malicious behavior. That gap between anomaly detection and causal understanding is directly relevant to oversight. [2026 paper](https://www.turing.ac.uk/news/publications/replicating-weight-space-programming-writing-and-reading-neural-network-weights), pp. 12–15. The authors also warn that frontier-model inference costs may exceed conventional optimization costs for small networks and that recursive self-improvement remains speculative.

## 5. Research hygiene and boundaries

These ideas are **not** a multi-night backlog, prerequisite chain, commitment, authorization for more expensive API usage, or permission to alter live systems. Keep later studies synthetic and bounded; avoid credentials, real-world misuse targets, external deployment, or uncontrolled model mutation. Preserve the user's human-first hypothesis, independent evaluator, evidence receipts, explicit assistance level and hard stop. Treat a null result as a valid result, not a summons to keep working.

**Provenance:** This futures file articulates the user's November 15 distinction between intelligence and harness, the proposed A/B split, a possible 0.8B-versus-8B specialized self-edit, and the still-open superalignment question. All future claims are hypotheses, not observed results of EX0005A or EX0005B.

*First prove that we can observe a change. Only later ask how much change can be sustained, transferred, and governed.*
