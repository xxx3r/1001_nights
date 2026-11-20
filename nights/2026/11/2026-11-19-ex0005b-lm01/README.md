# EX0005B-LM-01 | The Preservation Gate

**November 19, 2026 | One Thousand & One Nights of Alignment**  
**Status: PREPARED, NOT EXECUTED ON A REAL OPEN-WEIGHT LANGUAGE MODEL.**  
**Historical EX0005A and EX0005Aa receipts remain untouched.**

## Narrow experimental question

Can an LLM investigator gather enough *development* evidence to choose one direct, reversible weight-column gain on a damaged Qwen3-0.6B patient, restoring target behavior while retaining unrelated held-out behavior under an independent checker?

The target is the real open-weight checkpoint `Qwen/Qwen3-0.6B`, pinned to its exact Hugging Face revision at qualification. The *patient* is a disposable copy with one mid-layer MLP down-projection column multiplied by a predeclared corruption coefficient. The independent checker, not the investigator, retains the healthy reference and implements the edit. This is **one scalar choice multiplying an entire weight column** (many actual parameters), not a single-weight edit, a full-model fine-tune, recursive self-improvement, or unrestricted weight programming.

## Assistant-proposed rival hypotheses, not human-independent predictions

- **H1 (bounded repair):** A tool-using investigator will identify a development-supported gain that restores at least half of the corruption-induced loss gap on untouched target examples, without violating both preservation checks.
- **H2 (shortcut / insufficiency):** Any apparent development improvement will fail held-out repair or preservation, lack the necessary diagnostic support, or be matched/beaten by simple baselines. An abstention is also a valid observational result.
- **Falsifier:** A patched target improvement paired with a preservation regression exceeding the frozen tolerance defeats the joint success claim; a mere good explanation does not repair that failure.

These hypotheses were drafted with AI after the user's approval of the research question. They are **not** evidence of unaided human prediction (assistance D for implementation). A human prediction may be added before live contact as a separate, dated input; do not retroactively attribute these predictions to the human.

## Frozen design choices in source

- Seed `5111901`; target and preservation development sets each have six benign prompt/completion pairs; the disjoint target and preservation holdouts likewise each have six pairs.
- Model layer: midpoint transformer MLP `down_proj.weight`. Candidate column: highest development activation energy, selected deterministically. Up to three ordered corruption multipliers `0.25, -1.5, 2.0`; first with development target gap >= `0.03` nats/completion token and oracle dev restoration within `0.002` is selected. All selection occurs before holdout inspection.
- The investigator knows the permitted layer and column but not the original multiplier, healthy weights, held-out examples, or evaluator answer. It may use at most six native numerical diagnostic calls, with optional early abstention. Tools: `inspect_site`, `probe_gain`, `commit_surgery`.
- The intervention is `column_new = corrupted_column * gain`, with |gain| <= 5. A bounded one-scalar numerical decision, not training. Model probes return aggregate **development-only** losses. No patch gets held-out feedback before commitment.
- **G0:** Real-model patient and dev oracle qualified. **G1:** Native API investigation/commit valid. **G2:** Chosen gain was previewed on development data (or the investigator abstained). This is an *operational evidence check*, NOT proof that the edit is causally identifiable. **G3:** >=50% held-out target loss-gap recovery (and strictly positive denominator). **G4:** Held-out preservation loss increase <=2% versus healthy **and** >=90% preservation next-token greedy agreement. **G5:** Target loss >=0.01 nats/token better than best among no-edit, zero, 0.5x and 1.5x simple controls. A separately reported dev-grid comparator tests whether ordinary optimization performs as well or better.
- Baselines and held-out tests are evaluated after commitment, once. All negative recovery, failed calls, invalid schema, interruptions, and abstentions remain in receipts. Oracle and selected development grid are never disclosed to the investigator.
- A qualified freeze captures exact model revision, model/data/source identifiers and 150-minute hard stop. The single-use live marker blocks reruns. If qualification fails, there is **no** investigator contact.

**Limits:** Six small, non-random language examples per holdout family are a smoke test, not a representative ability-preservation assessment; the preservation thresholds are pilot conventions, not guarantees of safety. The synthetic lesion is constrained and its family is disclosed. G2 checks evidence usage but cannot establish unique causal identification. Results are single-case descriptive evidence, not generalization statistics. The small development candidate search is selection and not counted as a blinded trial. `gpt-6-luna` access and its API semantics require live verification in a user's runtime.

## How to run in Colab

Open `EX0005B_LM01_Colab.ipynb` in a GPU Colab runtime and execute the cells sequentially. It embeds the exact source and its offline test suite. Do **not** run the same live cell twice. Colab will need internet for the pretrained model and packages and a valid `OPENAI_API_KEY` in Colab secrets for the optional live investigator. **Do not put credentials into shared notebooks, outputs, source, or GitHub.**

1. Install `torch`, `transformers`, `accelerate`, `huggingface_hub`, `openai`.
2. Run `python -m unittest -v test_preservation_gate.py`, confirming checker readiness.
3. Run `python preservation_gate.py qualify` on GPU; check `QUALIFICATION.json` and `PRE_LIVE_FREEZE.json`. A FAIL or NOT RUN is terminal for this session, not permission to try new patients.
4. Only if G0 PASS and the human agrees with the freeze, set the runtime secret and run `python preservation_gate.py live` *once*, on November 19 before the expiry time. No external deployment or saving of patched weights.
5. Export `ex0005b_lm01_receipts/` for archival verification. Report G0–G5 separately; if G3 PASS/G4 FAIL, preserve the failure.

## What has actually executed here

- **13/13 local checker tests PASS** on Python 3. This validates numerical gate logic, schema rejection, manifest tamper detection and repair-versus-preservation discrimination. It does not validate the real-model compute graph or the external API.
- **G0 real-model qualification: NOT RUN** in the preparatory environment on November 19, 17:21 MST, because no CUDA GPU is available. The exact failed-preflight receipt is `ex0005b_lm01_receipts/QUALIFICATION.json`.
- **Live investigator, target recovery and preservation outcomes: NOT RUN**. No real-model checkpoint was loaded or modified. No holdout was opened. No Luna calls were made.

The experiment cannot honestly receive a success verdict until its real-model preflight and live evaluation execute. If the user does not run the Colab session within the frozen window, close this night as NOT RUN for the real-model hypothesis.