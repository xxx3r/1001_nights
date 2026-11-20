# EX0005B-LM-02 | The Phased Laboratory

**One Thousand & One Nights of Alignment | November 19, 2026 | Prospective independent follow-up**

**State: INSTRUMENT PREPARED / LOCAL MOCK TESTS ONLY. No real Qwen qualification, no Luna API calls, and no held-out evaluation have occurred for LM-02.**

## Why a separate experiment

LM-01 is a closed, interrupted live attempt, not a dry run to be overwritten: G0 PASS on a real Qwen3-0.6B L4 patient; six successful diagnostic observations; seventh native response requested another diagnostic; no model commitment and no G2-G5 results. The tool menu had still advertised `probe_gain` after all six slots were used. This creates an instrument contribution to the interruption, but does not exonerate the investigator's own budget decision. Preserve LM-01 receipts and interpretation.

LM-02 is **new and prospectively independent in its measurement protocol and patient**, not a blinded replication across architectures. The same model family and synthetic fault family are used. A new disjoint benign prompt dataset, fresh seed, and predeclared exclusion of the previously exposed column #4 prevent identical patient reuse. The first qualifying alpha is selected from a fixed ordering. If no alpha qualifies, G0 is FAIL and the investigator is NOT RUN. This new study cannot retroactively certify LM-01.

## Single research question

Can an LLM investigator gather useful input-side and output-side evidence, then choose one bounded reversible model-weight edit, which improves targeted held-out behavior **and** preserves unrelated held-out behavior under independent evaluation?

**Rival hypotheses (AI-drafted; do not attribute to unaided human work):**

- H1: with phase-specific tools, the investigator can commit a development-supported gain, recover at least half of the held-out target corruption gap, preserve unrelated behavior, and beat simple non-oracle controls.
- H2: gains arise from generic numerical search, are unsupported by the model's own measurements, overfit the tiny development sets, impair other behaviors, or do not beat simple controls.

A no-edit or abstention is an informative outcome. Tool-call validity does not prove mechanistic understanding. Single-patient success does not establish global safety, general reasoning, or scalable weight-space programming.

## Model, patient and splits

- Patient: pinned SHA of `Qwen/Qwen3-0.6B`, isolated in the Colab L4 runtime, no deployed checkpoint mutation or saving patched weights.
- Edit: one scalar gain `g ∈ [-5,5]` multiplying a **whole corrupted MLP down-projection column**, not a single numerical parameter. Actual tensor has thousands of entries; arbitrary multi-weight editing is not allowed.
- Fault: midway transformer layer, selected input-activation-energy column excluding LM-01's previously exposed column 4. Ordered candidate multipliers `(0.25,-1.5,2.0,-2.0)`; first that causes development target loss gap of at least `0.03` and exact reference restoration within `0.002` qualifies. Original column is saved in memory for the independent reference oracle; approximate inverse gain is **not** the reference restoration.
- Development: **12 new target** arithmetic prompt/completion pairs and **12 new preservation** benign language pairs. Held-out: **18 target** and **18 preservation** disjoint pairs. Frozen deterministic source. No LM-01 examples reused, and the held-out values are never exposed through investigator tools.
- G0 selection uses development ONLY. Training/holdout mixing and parameter selection based on held-out scores are prohibited.
- Record exact model revision, dataset/source/test fingerprints, run environment, local date and 150-minute expiration. The live run is single-use by durable start marker.

## Three phases and a protected decision

| Phase | Native tools offered | Budget, exit |
|---|---|---|
| I, **input-side** | `inspect_site`, `inspect_input(family,index)`, `finish_phase` | At most 6 observations. `inspect_input` returns selected-column activation statistics under the corrupted model, never healthy or holdout values. Early finish or automatic transition. |
| II, **output-side** | `inspect_output(family,index)`, `summarize_outputs(family)`, `finish_phase` | At most 6 observations. Corrupted-model per-example loss/first token or family-level development mean. Early finish or automatic transition. |
| III, **repair** | `probe_gain(gain)`, `commit_surgery` | At most 6 candidate gain probes. Each returns both aggregate target and preservation development loss. An early commitment counts **voluntary**. |
| IV, **final decision** | `commit_surgery` **only** | One separate native response automatically enforced after six repair probes, gain or explicit `null` abstention. Labeled **forced_final**, not autonomous stopping. |

No phase has tools from another phase. Every diagnostic tool response is delivered before the next request, including across phase boundaries. If a request is malformed, multiple calls arrive, the response is incomplete, or any budget is breached, retain the journal and INTERRUPTED result; no automatic retry.

**Important interpretation:** the phased interface measures repair selection *given guidance*, not whether the investigator independently chooses optimal stopping. The distinction between voluntary and enforced commitment is preserved as a separate behavioral result.

## Gates, frozen before investigator contact

- **G0**: authentic real-model patient qualified and exact-weight oracle agrees with healthy development reference.
- **G1**: all phase transitions valid; an actual native `commit_surgery` with correct schema was received, or the investigator explicitly abstained. An interruption is not G1 PASS.
- **G2**: for a non-null gain, the **repair-stage** journal includes no-edit `probe_gain(1)` and `probe_gain(chosen)`; chosen target development loss improves by **at least 0.01 nats/completion token** without more than **2% relative deterioration** on preservation dev versus probed no-edit. Abstention is ABSTAIN. This is a procedural evidence condition, not proof of causal identifiability.
- **G3**: held-out target gap recovery `R=(L_corrupt-L_patched)/(L_corrupt-L_healthy)` >= **0.5**, with a positive meaningful denominator; retain negative values.
- **G4**: on *unrelated held-out prompts*, preservation loss increases by no more than **2%** versus the healthy checkpoint and first-completion-token agreement with healthy >= **90%**.
- **G5**: held-out target loss at least **0.01 nats/completion token better** than the best of simple gains `0, 0.5, 1.0, 1.5`. Independently report the development-selected 13-point grid comparator; it is not a substitute for G5.

The model is not given healthy weights, alpha, held-out examples, target-test/preservation-test scores, reference checkpoint, or evaluator answers. Tests are opened only after commitment. Prespecified baselines are evaluated once at scoring time. `G3=PASS/G4=FAIL` is preservation failure, not success. `G5=FAIL` means simple tuning matched or beat the investigator. Small holdouts and per-example sensitivity make all conclusions narrowly descriptive.

## iOS-friendly single-file Colab path

1. Open `EX0005B_LM02_Colab.ipynb` in GPU Colab. It embeds the complete Python source and local checker; no fetching of project files from GitHub is needed.
2. Run environment/dependency cell, then source-materialization cell. The embedded text is checked against its recorded SHA-256.
3. Run the offline test cell; all tests must pass. Run the real GPU G0 cell **once**, then inspect the printed qualification and freeze. If FAIL/NOT RUN, stop.
4. Activate `OPENAI_API_KEY` in Colab Secrets; notebook only reports configured yes/no, never prints the key.
5. The live cell defaults to `RUN_LIVE = False`. Only after G0=PASS and local review of the expiry/metrics, explicitly set it to `True` and run this cell **once**. No reruns, hidden automated continuations or spending after the freeze.
6. The final cell displays the event/phase/gate summary and creates `EX0005B_LM02_receipts.zip` for archiving. Re-running export does **not** rerun the experiment.

**Assistance:** D (AI-authored design/code, user approved research intent). Human mathematical derivations and predictions remain unassessed. No new nightly verdict is claimed before an actual run. The upstream LM-01 report, source, PR and receipts remain unmodified.
