# EX0005Cc · post-pilot exploratory amendment (not a retroactive freeze)

**Authority:** On 22 November 2026, after reviewing all 32 AET pilot outcomes, the user explicitly instructed us to **ignore the earlier arbitrary stopping rule**. This amendment documents a *new exploratory follow-up*, not a rewrite of the original AET protocol or its `NO_QUALIFIED_DISTRIBUTION` historical result.

## Scientific decision

The healthy Qwen3-0.6B was **13/32 correct (40.625%)** and **22/32 parser-valid completed (68.75%)** across four equally sampled difficulty strata. This is more informative for detecting correctness and completion changes than EX0005C's 23/24 correct, 24/24 completed initial development baseline. The original 75%-completion mixture requirement is an optional design preference, not an intrinsic validity constraint.

**Choose original candidate A, exploratory:** 4 Apple main + 8 P1 + 8 P2 + 4 independently generated synthetic = 24. This mixture was explicitly listed **before** the AET pilot and uses the already sealed pool; its **selection despite the originally disqualifying completion rate occurs after pilot results**, and must not be called precommitted or confirmatory.

Original pilot-stratum weighted expectation: **9.5/24 correct (39.58%)** and **16/24 completed (66.67%)**. These are *pilot projections*, not measured validation rates or guaranteed outcomes. No cutoffs are assigned for declaring this distribution a practical success. Report observed accuracy, completion, and per-stratum errors regardless of sign. The completion rate is valuable information for distinguishing H1 mathematical gain from H2 completion repair, rather than a reason to erase a usable sample.

Why A: among the six original alternatives A–F, it is closest to the earlier 55% *accuracy target*, retains all four task strata, and leaves visible room for both improved correctness among finished responses and repaired completions. The 55% target is a design preference; there is no post-hoc "PASS" threshold.

## Validation hygiene and scope

- Sealed source is the original manifest with pilot content hash `d6946bbf897c0e72d5e965c2eaf563aba07bcc2d5573f0469a90748d628a3a04` and validation pool hash `65daa7c616ae806632e01df49c233a3d6467e01d4672a9f4b0ec480751f43552`.
- The exact 24 validation IDs are archived in [EXPLORATORY_SELECTION_A.json](EXPLORATORY_SELECTION_A.json) **before** any follow-up validation; no problem is selected based on its own answer or model output.
- [EX0005Cc_EXPLORATORY_VALIDATION_A_Colab.ipynb](EX0005Cc_EXPLORATORY_VALIDATION_A_Colab.ipynb) is a separate, explicitly opt-in, one-shot healthy-model baseline check that reconstructs the sealed pool and fails closed if IDs or hashes differ. Not yet executed when published.
- Thinking ON, BF16 healthy pinned Qwen, token cap 3,072, sampling temperature 0.6, top-p 0.95, top-k 20 and the **same AET per-item seed namespace** remain unchanged. Run no Luna interventions or numerical optimizer in this qualification notebook.
- Keep original EX0005C G0 = FAIL, original EX0005Cc v1 selection = NO_QUALIFIED_DISTRIBUTION. New validation will be **exploratory**, not an untouched prospective test of the original 75%-completion decision.
- Completion is scored by the same deterministic parser. Report valid completions, token-limit truncations, invalid numbers, correct/wrong and raw per-question transitions when a later edit is ever authorized; don't rescore based on semantic speculation.
- Original AET and new validation evidence must remain distinct. No automatic reruns if result is disappointing. No source/model/data-pool replacement after measurement.

**Interpretation:** We have evidence of a non-ceiling healthy baseline on the AET pilot, not that the baseline distribution will transfer to the reserved pool or that Luna can improve it.
