# EX0005Aa | The Examiner Must Discover

**New protocol, written after inspecting EX0005A evidence. Separate future session required. DRAFT until user approves and executes notebook freeze; zero model calls in this package.**

## Research question
Can a repaired, bounded native tool loop produce (a) correctly differing numerical counterfactual predictions under *matched observations*, and (b) independent localization and repair of a deliberately corrupted *new public developmental network*, against a simple heuristic?

These are separate arms. The matched counterfactual arm does not establish independent fault discovery because its proposed intervention names a coordinate. The discovery arm does not use a named-fault hint.

## New cases and precomputed numerical oracle
- `C_positive` vs `C_negative`: share healthy target, probe input definitions, evaluation set and every healthy parameter, and differ only in sign-flipped `W2[1]` lesion. Both face **identical** prompts and exactly two **forced native read-only tool calls**: `inspect_output_weights({})`, `probe_feature1({})`. Neither case label nor lesion key is passed to Luna. Prediction: a counterfactual `W2[1] -= 0.25` decreases MSE in C_positive and increases MSE in C_negative. The forced calls show interface compliance only, not autonomous investigative preferences.
- `D_unknown`: separate novel planted lesion in a hidden-layer parameter. A new Luna context receives only architecture and four *model-chosen* read-only observations, exactly one native call per response (`parallel_tool_calls=False`). Available tools: `inspect_weights(tensor)` and `probe_examples(pack)` with fixed enumerated packs and no index bounds to guess. Luna then commits its fault hypothesis and optional edit. Evaluation scores function against no-edit, simple output-layer heuristic, zeroing baseline, and exact oracle; *fault localization and functional repair are separate outcomes*. One public case cannot establish generality or a mechanism.
- No sealed holdout, no reuse of P1/P2 lesion keys, no claims of novel blinded efficacy. Fresh public developmental seeds: paired 150619, discovery 150631. A separate new sealed experiment would require a prospectively accepted protocol.

## Controls and changes motivated by EX0005A
1. Every generated API response can contain **at most one** function call (`parallel_tool_calls=False`), and multiple or malformed tool calls are rejected and logged.
2. Pair uses fixed and exactly matched tool signatures. Discovery allows choice but caps it at four observations, even if Luna repeats an ineffective call.
3. No `indices` argument; every probe pack is a valid tool enum. Model prompt states the defined input packs. There is no ambiguous range hidden from the model.
4. Exception handling is per case, with incremental atomic journal writes. Incomplete/failed response is a real error, not a valid observation, and gets no automatic retry. Subsequent independent cases may continue if within the frozen call/time budget; earlier partial evidence is retained.
5. Separate new `PRE_LIVE_FREEZE.json`, single-use marker, `ACTION_JOURNAL.json`, and `RESULTS.json` folder; historical receipts are not overwritten. Source hashes, fixture fingerprint, previous receipt hashes, settings, user-carried prior hypothesis and hard session boundaries are included.
6. Live run cannot occur on or before the closed November 15 session. The human selects a future date and a <=4-hour window **before freezing**. The runner refuses calls outside it.
7. API key comes from Colab Secrets into **subprocess environment only**, without printing the secret. No credentials are stored with artifacts.

## Proposed acceptance gates (fixed in code before first AA model contact)
- **G0:** Independent analytical oracle works; no-edit and heuristic are scored; numpy and torch agree; malformed inputs rejected. This is a local instrument control.
- **G1:** Both paired cases produce exactly two completed, native, valid read-only function calls with matching specified kinds.
- **G2:** Both paired commitments have opposite, correct signs for `MSE_after - MSE_before` and identical call signatures. Numerical magnitude error remains a separate reported value; model reasoning versus a simple heuristic is not established by sign alone.
- **G3:** Both paired cases return schema-valid, non-placeholder commitments. Unsuccessful commitments and abstentions are not silently scored as correct.
- **G4 secondary:** In D_unknown, optional model patch improves development MSE by >=50% and beats the trivial output-layer heuristic by >=0.05 absolute MSE, with no-edit and oracle retained. No patch = NOT RUN; malformed/ineffective committed patch = FAIL. These fixed thresholds describe only this *public developmental fixture*.
- **Mechanistic explanation:** Only a bounded hypothesis; correct localization and patch score do **not** prove causal-mechanistic understanding. The discovery fault label is checked only after commitment.

Outcomes and denominator (response attempts, successful tool calls, errors, case completions, valid commitments, abstentions and patches) are reported separately. No combined AI intelligence score. No automatic retry, no overtime, no batch future experiments.

**Budget:** model `gpt-6-luna`; low reasoning; <=14 total Responses generations, <=80,000 input tokens, <=24,000 output tokens (with 1,800 maximum per call), two 2-call + 1-commit paired cases and one four-call + 1-commit discovery case. Recorded token caps bound usage, not guaranteed dollar price. Unsupported settings or model access failure are recorded as infrastructure failure.

**Human approval:** EX0005A human-first predictions may be carried forward only when explicitly marked **prior hypotheses**, with assistance disclosure C. They must never be represented as newly independent EX0005Aa predictions. A separate new human pre-run decision may be recorded in notebook without rewriting the old words.
