# After the Scalpel: Two Possible Nights

**One Thousand & One Nights of Alignment · Idea bank arising from ALGN-EX0003**  
**Written:** November 8, 2026  
**Status:** **UNTESTED PROPOSALS; NOT PREREGISTERED; NOT SCHEDULED**  
**Source night:** [Land's Quiet Scalpel](./README.md) · [Night card](./NIGHT_CARD_EX0003.md) · [References](./ALGN_EX0003_REFERENCES.md)

> The first examiner could touch the weights. Once it severed the right connection, the little network recovered. But a simple statistic could do the same, and the examiner could not reliably tell us why. The next world should have more than one dial, and turning every dial to zero should destroy something valuable. Only after the examiner learns to repair a difficult little machine should we ask whether the examiner itself can be repaired.

This file stores **two independent research seeds**, not a multi-night roadmap. Each prospective night must state a new falsifiable contrast, prepare new locked evaluation examples, record assistance level, and close by its own hard stop. EX0003's opened held-out datasets must **never** be reused for teacher or prompt selection. The original EX0003 verdict stays FAIL for distinctive mechanistic understanding, with one bounded functional-repair PASS.

## Land's Quiet Scalpel II: The Dials Must Interact

**Candidate:** EX0004 · Thursday, November 12, 2026

**Status:** Strong candidate for the Thursday research window, **not yet authorized as a frozen experiment**.  
**Question:** Can a tool-assisted language-model examiner infer and repair an **interacting, distributed fault** that cannot be corrected by simply zeroing an unusually large parameter?

### Why this is a different experiment

EX0003 gave its teacher a healthy 6→8→1 network plus one conspicuous pathway. A single zeroing edit restored the original function, and a simple path-magnitude heuristic passed the same evaluation as the successful teacher. The original prompt also contained a complete example patch copied by two responses. These facts make the first experiment an interface demonstration and an effective caution about causal explanation, not a robust measure of mechanistic interpretation.

The next experiment should hold the architecture small but change the **kind of problem**. We want a known-good computational mechanism with **multiple coupled coefficients**, a planted defect that distorts it, and an oracle correction that must contain **nonzero numerical values**. Disconnecting the entire mechanism, zeroing the conspicuous connection, or predicting from the task description alone must fail preflight controls.

### Proposed specimen (to be tested before preregistration)

Construct one synthetic classifier with a context-dependent, two-path computation, for example a small ReLU network with a genuinely necessary feature pathway and a second pathway that sometimes opposes it. Inject a **coupled scaling-and-bias fault**: both the strength and threshold of an existing subcircuit are wrong. The correct repair should adjust at least **two interacting parameters** to specific nonzero values while preserving the useful circuit.

The desired properties are a **design specification, not yet an achieved fixture**:

- Healthy reference solves clean and shifted task regimes.
- Corrupted student degrades substantially under a predeclared context shift.
- A fixed, known oracle patch restores the task without destroying necessary behavior.
- **Any simple zeroing of the implicated pathway fails** the preservation gate; a largest-weight removal heuristic also fails.
- The student's behavior is sensitive to the **joint** intervention, not adequately repaired by changing either parameter alone.
- A hidden-neuron permutation preserves the function and moves the relevant numerical addresses.

Before contacting a teacher, the researcher should **prove or test those properties** and freeze the entire fixture. If such a controlled specimen cannot be constructed within the night, record **NOT RUN** or **INCONCLUSIVE** for teacher evaluation rather than improvising a new test until one passes.

### Teacher as researcher, not just JSON emitter

Candidate teacher: **Qwen3-8B** on Colab (subject to actual memory availability; quantization may be needed) **or** a GPT-6 Luna API call (subject to confirmed model access and cost). **Choose one primary teacher before freezing the study**, rather than changing model, scaffold and prompt simultaneously. Qwen3-0.6B can be retained as a fixed smaller-model comparator if the timebox permits. A richer teacher is no guarantee of better weight understanding.

Instead of a single unexamined guess, provide a tiny **read-only diagnostic tool surface**. The teacher may request, for example:

1. Selected parameter blocks and their names/shapes, without original healthy weights or planted-fault coordinates.
2. A small, capped number of development-only forward predictions and hidden-activation traces on examiner-selected synthetic inputs.
3. A similarly capped number of ablation or counterfactual-forward probes that operate only on temporary model copies.
4. One final structured patch with exact tensor addresses, finite **nonzero** replacements where relevant, and a causal prediction that an independent evaluator can check.

Possible initial budget: **four forward probes, two temporary ablations, one final patch, at most four edited scalars**. These are **candidates**, not frozen thresholds. All tool calls and outputs should be archived; no access to final labels, oracle patch, hidden fault construction, general-purpose filesystem writes, or repeat sampling after final submission. Tool access must be equally specified for each comparator.

### The discriminating comparison

| Condition | What it isolates |
|---|---|
| Teacher with actual weights and bounded probes | Does computational interaction with the student add value? |
| Same teacher with descriptions/shapes but no weights | How much comes from the task specification alone? |
| Same teacher with weights but no probes | How much do tools, rather than raw weight access, contribute? |
| Simple analytic/coordinate heuristic with comparable budget | Is the intervention beyond trivial path/magnitude rules? |
| Hidden-neuron permutation | Does the examiner identify the **same mechanism** at relocated coordinates? |
| Healthy-network negative control | Does it abstain rather than invent defects? |
| Oracle patch, scored only by independent checker | Does this fixture admit a genuine bounded solution at all? |

**Primary measure:** independently held-out task accuracy improvement **and** preservation on unaffected cases, both defined before running the teacher. **Secondary measures:** patch validity, edit magnitude, performance relative to zeroing/heuristic, ablation-prediction correctness, permutation agreement, and all model/tool errors. Do not let the evaluator use a pretty explanation as proof of faithful internal reasoning.

A meaningful **PASS** would require an effective, nontrivial patch exceeding predetermined baselines under the locked protocol; a separate stronger claim about mechanistic inference would require correct causal predictions and invariance controls. If the oracle succeeds but all teachers fail, that is a valid **FAIL** for teacher performance. If the oracle itself cannot satisfy the constraints, the teacher question is **NOT RUN** or **INCONCLUSIVE**, not a hidden failed teacher trial.

### The smallest Nov 12 execution

Within **one protected Thursday window (up to four hours, ideally 90–180 minutes)**, prioritize one synthetic fixture, one independently frozen oracle and negative control, one teacher interface, one or two controlled comparisons, and one sealed evaluation. Keep the notebook cell-by-cell, with no elaborate service, agent hierarchy or reusable framework. A tool-using Qwen3-8B and a Luna API comparison **in the same night** would likely confound model capability, tools and time. Select only one primary contrast.

**Stop after the verdict.** Do not turn an Ex0004 negative result into an overnight hyperparameter search. EX0003's successful shortcut is an inspiration for a harder *new task*, not a benchmark to tune on again.

## The Surgeon Becomes the Student

**Timing:** Later independent project  
**Status:** More ambitious research seed; **not** recommended as the initial Nov 12 experiment.  
**Question:** Can a stronger, tool-assisted teacher such as **GPT-6 Luna** propose a bounded modification to **Qwen3-0.6B itself** that improves Qwen's ability to diagnose and repair previously unseen tiny neural networks?

### The reversal

In EX0003, Qwen was the examiner and a 65-parameter MLP was the patient. In this possible future study, Qwen becomes the **patient**. The teacher proposes changes to Qwen's internal computation, after which Qwen must operate **alone** on novel repair tasks.

The chain is:

**Luna (teacher) → bounded intervention on Qwen3-0.6B (student) → modified Qwen → fresh, unseen networks.**

A model with hundreds of millions of parameters cannot be responsibly represented as one giant editable weight list in a prompt. The experiment must first identify a **small, causally justified intervention surface**. Possible choices include one carefully selected attention/MLP tensor slice, a few controllable gates, or a low-rank adapter. These are different mechanisms and must be labeled honestly. Training a LoRA adapter by gradients is **not** equivalent to Luna directly writing numerical weights; the first experiment should choose one method and report exactly which parameters were changed.

### Proposed staged design, each stage optional

**Stage 0: Establish a real baseline.** Freeze a collection of fresh small-network repair problems with planted faults, harmless synthetic inputs, known oracles, and independent held-out variants. Run unmodified Qwen3-0.6B under a fixed inference scaffold. Score *functional repairs* and *correct causal predictions* separately. Include examples on which the unmodified model fails. The original EX0003 test cases and their opened holdouts must not serve as the final benchmark.

**Stage 1: Localize the candidate mechanism.** Use development-only model activations, controlled ablations and parameter inspection to identify a small intervention surface potentially related to the target skill. Do not presume a single ‘mechanistic interpretability neuron’ stores the ability to reason about weights. Keep the investigation distinguishable from dataset memorization, output prompt engineering, and unrestricted parameter search.

**Stage 2: Teacher-proposed intervention.** Give Luna bounded diagnostic access and require a machine-readable patch or compact adapter proposal. Enforce edit-count/norm budgets, immutable checkpoint snapshots, and a no-gradient condition **if the claim is direct weight-space programming**. A budget-limited tool may apply the edit to a **copy** and run development-only checks. No uncontrolled mutation of the original checkpoint or evaluation data.

**Stage 3: Transfer test.** Run original and modified Qwen on **unseen network families, novel hidden-unit orderings and fresh task rules** using identical prompts, decode settings and tool allowances, with Luna absent at inference time. Add matched random, null, and ordinary fine-tuning/adapter baselines where feasible. Report both accuracy and regressions on unrelated benign capabilities. A locally successful edit that merely installs one answer does not demonstrate an acquired general skill.

**Stage 4: Teacher-surpassing test, if justified.** Measure Luna's own zero-shot or tool-assisted performance on the same repair distribution under a comparable evaluation protocol. Only then ask whether modified Qwen exceeds its teacher **on that specific task**. A gain over Qwen's own baseline is not automatically weak-to-strong generalization or a result about superalignment.

### Scientific and resource boundaries

- Verify API availability, model identity, price and any promotional credits **before** a run; do not assume free Luna tokens or a particular private tier.
- A GPU that comfortably runs Qwen inference may not support arbitrary teacher-guided full-model editing; prefer an inspected small adapter or local tensor slice.
- Keep training updates, direct patches, activation steering and reward-guided search **separate experimental treatments**. They cannot all be called weight-space RL.
- Use synthetic non-sensitive tasks and no real-world actions. Preserve the original checkpoint, hashes, tool transcripts, ablation receipts and independent grader.
- Pre-register a meaningful null and a positive control. An apparent gain can be caused by prompt leakage, model selection, repeated searching, or grading defects.
- Declare model/task capabilities only at the granularity supported by matched held-out evidence. No single successful patch establishes superalignment.

This future project would draw its motivation from [weak-to-strong generalization](https://arxiv.org/abs/2312.09390), [Direct-OPD](https://arxiv.org/html/2607.05394v2), [OPRD](https://www.microsoft.com/en-us/research/publication/eliciting-weak-to-strong-generalization-with-on-policy-reverse-distillation/), and the [original weight-space experiments](https://rikiyat.github.io/blog/weight-space-programming/). It would **not** be a direct reproduction of any of them without matching their methodology.

## A common rule for either future

The philosophical interest remains: a system may become excellent at satisfying a measured rule while failing the unmeasured purpose. But neither **cyberpositive acceleration** nor **Lacanian jouissance** is a measured variable in these studies. The scientific task is to ask whether a weight edit improves real, independently scored behavior, and whether the claimed explanation survives **causal** controls. In a later RL study, proxy reward and independently measured utility could be separated explicitly, with stability and feedback measured rather than assumed.

**Provenance:** Both project concepts were proposed during the November 8 EX0003 conversation. The human researcher emphasized interacting nonzero repairs, tool use and the speculative Luna→Qwen reversal; ChatGPT converted them into candidate controlled protocols. **No new model, fixture, teacher run, acceptance threshold or schedule has been executed or frozen by this document.**

*One future night may sharpen the scalpel. Another may try to teach the surgeon. Neither is an obligation owed to the past.*
