# NIGHT CARD | ALGN-EX0005A: The Examiner Must Look

**Night:** Sunday, 15 November 2026 (America/Denver). **Window:** 16:00–20:00; precise live-run start/stop not preserved in uploaded files (first preflight freeze reported 19:19).  
**Status:** CLOSED. **Night verdict:** **FAIL — full instrument qualification not met**. **General model-capability verdict:** **INCONCLUSIVE**.  
**Assistance:** C for human predictions translated collaboratively; D for AI-drafted harness. No post-freeze live rerun.

**1. Question.** Can GPT-6 Luna use bounded real numerical observations to make a prospectively checkable, evidence-responsive causal prediction and optionally a verifiable direct-weight intervention?

**2. Rival predictions and freeze.** Human predicted likely heuristic improvement without robust explanation, doubted correct P1+/P1− contrast, and warned that prompts/checkers could supply the answer. Original preflight freeze SHA 5019d1a9fc3baff6a5e4f21b5b1b2ae0de9b70b1a6cabad031e93bab8ff476c1; live-run freeze SHA **4fad7aa72bd20393d04b09212da1adccd288f1b838fcfdf2c9c7eaec406e4112**. Full live freeze manifest not uploaded.

**3. Human-first logic.** A successful patch is not a mechanistic explanation; a wrong-sign prediction must fail independent checking. These ideas were expressed by the human and operationalized collaboratively.

**4. Method.** gpt-6-luna Responses API; synthetic P0 AND and P1+/P1−/P2 public fixtures; read-only inspect_weights and probe_examples; independent NumPy/PyTorch checks. Fixture fingerprint **39e3064ac2c4391b1013e9a37299bc527f5a7e6cd67549e1b075b06c85706fc6**. No sealed holdout.

**5. Executed evidence.** Local tests **7/7 PASS**. Luna P0 **4/4 exact**. **11 API responses** (10 completed, 1 incomplete); **19 diagnostic requests** (9 valid, 10 invalid/over budget). P1+ had two valid distinct tools and one commitment: predicted delta MSE **−0.05**, actual **−0.272198**, correct sign, inaccurate magnitude, high uncertainty, **no patch**. P1− had three valid weight inspections but no valid probe or commitment. P2 had four valid weight inspections, no valid probe, and stopped on **max_messages**.

**6. Independent check.** Oracle/no-edit/heuristic baselines behaved as recorded; the heuristic perfectly repaired both P1 fixtures. The paired requests differed, so causal evidence dependence was **not established**. No model patch was scored.

**7. Disposition.** Original runner G1–G4 statuses remain **NOT RUN** because interruption skipped scoring; instrument_ready=false. Manual review shows primary readiness requirements **not met**, without implying general Luna incapability. Functional intervention NOT RUN; mechanistic understanding unproven.

**8. Learning and stop.** Separate tool compliance, numerical direction, localization, patch efficacy and explanation. Remaining deficit: an unknown-fault, matched-observation test without answer leakage. **EX0005A closed at its 20:00 hard boundary; archival documentation only afterward.**

**Evidence:** [final report](./EX0005A_FINAL_RESEARCH_REPORT.md) · [RESULTS](./evidence/RESULTS.json) · [journal](./evidence/ACTION_JOURNAL.json) · [notebook](./EX0005A_Colab.ipynb) · [original protocol draft](./EX0005A_PROTOCOL_DRAFT.md).

*One night. One problem. One independent verdict. No retroactive pass.*
