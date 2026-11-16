# ALGN-EX0005A | The Examiner Must Look

**One Thousand & One Nights of Alignment · Night 0005A**  
**Planned date:** Sunday, 15 November 2026 (America/Denver)  
**Status:** **CLOSED — 15 November 2026 run attempted; primary instrument qualification FAIL (manual evidence audit); general Luna capability INCONCLUSIVE.**  
**Scope:** GPT-6 Luna API + Colab; public instrument qualification, **not** a new blinded repair-efficacy trial.  
**Question:** Can bounded numerical observations support an externally verifiable causal prediction and intervention, rather than merely an unsupported, plausible diagnosis?

> First qualify the instruments. On a distinct night, compare surgeons and operating rooms.

## Final disposition (archived from the executed night)

**Local checker G0:** PASS (7/7 tests). **Luna P0:** Boolean AND exact (4/4). **Live record:** 11 API responses (10 completed, 1 incomplete); 19 diagnostic attempts (9 valid, 10 rejected or over budget). P1_plus produced one valid, correct-sign but inaccurate prediction and abstained from patching. P1_minus produced no commitment; P2 ended incomplete at max_messages. The P1 pair lacked matched diagnostic requests.

**Full instrument-ready criterion:** NOT MET. The original runner's G1/G2/G3/G4 entries remain NOT RUN because a runtime interruption skipped formal gate scoring. The post-run manual audit therefore records a **night-level instrument qualification FAIL**, while the narrower question of model evidence dependence and general mechanistic understanding remains **INCONCLUSIVE**. No model-authored patch was evaluated and no sealed test was opened.

The original fixture already directed attention to W2[0], and a simple heuristic perfectly repairs both P1 variants. Correctly naming that weight is not independent fault discovery. This limitation is central to the research conclusion.

**Read first:** [Final research report](./EX0005A_FINAL_RESEARCH_REPORT.md) · [Completed night card](./NIGHT_CARD.md) · [Raw RESULTS](./evidence/RESULTS.json) · [Raw action journal](./evidence/ACTION_JOURNAL.json) · [Archived notebook](./EX0005A_Colab.ipynb).

**Historical boundaries:** EX0005A is closed. EX0005Aa, authorized afterward to repair the instrument, is a separately labeled new investigation and cannot rescore this night.

## Companion on the same date: EX0005Aa, a separately frozen post-run experiment

The original **EX0005A remains closed**, with its historical instrument-qualification **FAIL** and broader model-capability **INCONCLUSIVE** verdict. It is not merged with or rescored by its successor.

After the original result was examined, the human explicitly authorized **EX0005Aa** to repair the public instrument. A new freeze was made after 20:00 local and the model contacted only after that freeze. The revised interface produced all valid native observations and a complete run. EX0005Aa's paired causal contrast **G2 FAIL** remains a real failure; its separate unknown-fault repair **G4 PASS** is a real success: Luna proposed `W1[0] += 1.3` and the independent checker measured MSE 0.9172305741 → 0 against a non-improving simple heuristic.

A later **post-run identifiability counterexample** proved that the four observed diagnostics did not uniquely establish the exact edit magnitude. It does not alter G4 or count as a fresh Luna attempt.

**Companions:** [EX0005Aa archive and completed report](./ex0005aa/README.md) · [EX0005Aa night card](./ex0005aa/NIGHT_CARD.md) · [combined Galileo-style references, EX0005 A + Aa](./ex0005_A+Aa_references.md).

## Why EX0005A exists

[EX0003](../2026-11-08-ex0003/README.md) recorded one functional repair by Qwen3-0.6B; a simple numerical heuristic made the same repair, and the model's mechanistic explanation was wrong. [EX0004](../2026-11-12-ex0004/README.md) stopped its initial pilot after tool-interface problems. The fresh EX0004B run formally failed its repair criteria, but both Qwen3-8B arms used **zero real diagnostic calls**. The capability question remained inconclusive. Neither historical verdict is changed.

The earlier [EX0005 proposal](../2026-11-12-ex0004/ALGN_EX0005_PLAN.md) is **revised for tonight's scope only**: use the budget-feasible GPT-6 Luna investigator, a minimal real API tool loop, and sacrificial public specimens. Any future blinded efficacy study is separate.

## Research hypothesis (not established)

Weight-space programming competence may depend on the interaction of (i) the investigator's learned capabilities, (ii) the target network's representational structure, and (iii) available numerical information and computational tools. EX0005A **does not estimate that interaction**. It tests whether the instrument can support an actual evidence-responsive investigation.

The Alan Turing Institute's 2026 [replication report](https://www.turing.ac.uk/news/publications/replicating-weight-space-programming-writing-and-reading-neural-network-weights) found that direct weight writing often looks like compiling an explicit program; reading input-layer structure is not necessarily understanding the network's mechanism (especially pp. 4–8, 11–15). That study did not establish a general model-size threshold or perform our intended model-by-harness factorial experiment.

## Original four bounded questions

1. **Numerical positive control:** Can Luna emit weights for a tiny rule-based network, with numerical correctness evaluated by an independent script? This is calibration, not evidence of deep interpretability.
2. **Real interface:** Can an actual Luna generation request one read-only diagnostic, use its numeric return, then request a second *different* diagnostic? Mock-only success is insufficient.
3. **Evidence dependence:** On an independently checked pair of sacrificial cases that differs in a causally relevant observation, does Luna make a correctly differing, pre-specified prediction? Attractive prose alone does not pass.
4. **Public intervention (secondary):** Does a bounded patch to a deliberately corrupted public network improve held-out *development* behavior against no-edit and a simple heuristic? Score function separately from diagnosis.

## Original scope, integrity, and stopping boundaries

- One investigator: **GPT-6 Luna** via the OpenAI API. At execution verify the exact available model identifier, model revision if exposed, supported call format, inference settings, usage and cost. The researcher reports a Colab secret connected to the OpenAI API. **Never print, store, commit or echo the secret value.**
- Public synthetic networks only; keep their answer keys in the evaluator, outside model prompts and tool responses. No reuse of EX0003 or EX0004 opened holdouts as selection data and **no new sealed patient tonight**.
- Use the smallest real structured tool interface supported by the API, with exact callable identifiers; no complete answer-bearing diagnosis or patch examples. Freeze predictions before observing the comparison condition.
- Limit initial harness engineering to **45 minutes**. Freeze model/tool budgets before live runs (suggested cap: 12 diagnostic calls, 2 patch trials per case, and at most 6 final scalar edits, if such trials are attempted). Record malformed calls, failures, truncation, and abstentions in denominators; do not silently retry.
- Preserve original weight checkpoints; any intervention is applied only to a disposable copy. No gradient descent within a condition described as *direct weight editing*. The checker must verify known oracle and no-edit controls before considering the model's patch.
- Stop within the ordinary Sunday atelier (16:00–20:00 America/Denver; four hours maximum, ideally 90–180 minutes). No overtime, no penalty for stopping, no resurrection of prior results.
- Keep separate outcomes: **instrument qualification**, **evidence-responsive model behavior**, **functional intervention**, and **mechanistic explanation**. A successful instrument gate does not certify model competence. A failed tool interface cannot certify model incapability.

## Documents

- [EX0005A_FINAL_RESEARCH_REPORT.md](./EX0005A_FINAL_RESEARCH_REPORT.md): completed, source-bound analysis, denominator audit, validity limits and final disposition.
- [NIGHT_CARD.md](./NIGHT_CARD.md): closed one-night receipt with post-run documentation clearly distinguished.
- [evidence/RESULTS.json](./evidence/RESULTS.json) and [evidence/ACTION_JOURNAL.json](./evidence/ACTION_JOURNAL.json): original user-uploaded raw machine receipts, unaltered.
- [evidence/G0_LOCAL_RECEIPT.json](./evidence/G0_LOCAL_RECEIPT.json) and [evidence/TEST_RESULTS.txt](./evidence/TEST_RESULTS.txt): original pre-live local numerical/checker receipts; their live-model NOT RUN status is a historical preflight snapshot.
- [EX0005A_Colab.ipynb](./EX0005A_Colab.ipynb) and [source/](./source/): historical runnable public scaffold, independent fixture/checker and API runner. These are archived source, not permission to rerun a closed night.
- [EX0005A_PROTOCOL_DRAFT.md](./EX0005A_PROTOCOL_DRAFT.md): unchanged **pre-execution draft** retained as provenance; its DRAFT/NOT RUN language describes the earlier planning state.
- [potential_future.md](./potential_future.md): separate speculative EX0005B proposal and research idea bank; not part of the night's verdict.

**Originally authorized on 15 November:** public calibration, real-model instrument validation, bounded synthetic interventions, and one honest receipt. **That window is now closed.** No unseen sealed patient, historical rescore, external project change, or general self-improvement/superalignment claim was authorized.

*One night. One question. One independent verdict.*
