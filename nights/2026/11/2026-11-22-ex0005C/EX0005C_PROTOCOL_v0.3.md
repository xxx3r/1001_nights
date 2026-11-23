# EX0005C · The First New Skill
## Prospective protocol v0.3 · November 22, 2026 · NOT EXECUTED

**Status:** PREPARED FOR COLAB PREFLIGHT, not a validated/sealed live trial. No holdout evaluation, investigator intervention, or healthy-model qualification has occurred. This document does not amend the historical EX0005B report. It defines a fixed candidate rule-set; a valid final freeze requires successful source checks, identified split hashes, runtime qualification, and a time-limited start record before any surgeon contact.

### Human-authored inputs
- **Preferred rival:** H2 completion repair more likely than H1 capability improvement in the 0.6B patient. Negative outcome also plausible.
- **Falsifier to inspect:** both-complete correctness improvement + structural-shift improvement, not merely output completion. Benchmark/scorer shortcuts must be checked separately.
- **Human arithmetic:** toy six-case decomposition correctly derived as net total +2 = both complete +1 + completion changed +1. This is human-first, assisted verification afterward.

### Freeze candidates (all conditions; not yet GPU qualified)
| Field | v0.3 fixed choice | Reason or limitation |
|---|---|---|
| Patient | `Qwen/Qwen3-0.6B` SHA `c1899de289a04d12100db370d81485cdf75e47ca` | EX0005B source-continuity; healthy unmodified reference. |
| Model arithmetic | L4 GPU, BF16, no quantization, no LoRA/gradient | Same dtype and checkpoint for all variants; fail if incompatible. |
| Qwen thinking | `enable_thinking=True` | Explicit human choice. |
| Decoding | sampling on; temperature 0.6; top-p 0.95; top-k 20; min-p 0; one sample per item | Qwen's recommended thinking-mode sampling avoids the known greedy repetition confound. One draw is noisy, so report that limitation. |
| Token budgets | math `max_new_tokens=3072`; unrelated preservation `max_new_tokens=512` | Generous yet bounded; thinking tokens count against cap. Same limit across variants **for each item**. No post-result cap changes. |
| Prompt | single user turn; no worked examples; require last line `Final answer: <number>` for math or `Final answer: <short text>` for preservation | Output formatting identical for all treatments. Do not inject gold answers or Apple `canary` metadata. |
| Seeds | seed derived from `EX0005C-2026-11-22-v0.3-family-seal` plus item identifier using SHA256; same per item across variants | Pairing controls intended randomness, but paths can diverge under sampling; not bitwise-paired outcomes. |
| Edit sites | model layer 14, `mlp.down_proj.weight` columns 194 and 390 | No site search. Column 194 is previously exposed in EX0005B and explicitly declared as prior knowledge; column 390 is a prespecified comparison site. Confirm dimensions on loading. |
| Edit parameters | two independent column multipliers `(g_194,g_390)` in `[0.75,1.25]` inclusive; identity `(1,1)` | Reversible in-place edits, original columns restored bit-exactly after evaluation. These are whole matrix columns, not two individual weights. |
| Development | 24 `openai/gsm8k` main/train, plus 12 unrelated preservation (4 per category) | Visible to Luna and numerical search, not heldout. |
| Ordinary heldout | 24 `openai/gsm8k` main/test | One opening after all commitments. |
| Structural heldout | 24 `apple/GSM-Symbolic` main, **one instance per distinct template family** | Exclude every selected family's `original_id` GSM8K test index from ordinary heldout. Verify `original_question` matches GSM8K test source; stop on mismatch. Source answer keys are not independent theorem proofs. |
| Preservation heldout | 48 fixed tasks: 16 language/grammar, 16 facts, 16 toy logic | Predefined independent of model performance; preservation dev/heldout are disjoint. |
| Dataset revisions | GSM8K `740312add88f781978c0658806c59bc2815b9866`; GSM-Symbolic `93b5b3758d9d9841ffe81d6cd2ae2b030685b078` | Explicit pinned revisions; Apple license CC BY-NC-ND 4.0: respect use and redistribution limitations. |
| Split selection | deterministic SHA-256 keyed ordering of original dataset IDs/template families and instance IDs | Not row cherry-picking. Split IDs and content hashes must be generated in Colab before live run and sealed. |
| Completion definition | EOS / chat-end reached before token cap AND exactly one parseable final answer after a closed thinking block | Completion is operational, not a claim of coherent reasoning. |
| Correctness | exact normalized numeric GSM answer; malformed/empty/unparseable/truncated score incorrect | Fixed denominator. Numeric equivalence through exact `Decimal`; model final line must contain scalar number only. |
| Surgeon | GPT-6 Luna, 6 input observations, 6 output observations, 6 scored repair probes, protected final-only commitment | Any extra read-only diagnostics and early/forced stopping logged separately. |
| Numerical comparator | **six** measured development candidate evaluations in same 2D edit space | Fixed grid `(1,1)`, `(.75,1)`, `(1.25,1)`, `(1,.75)`, `(1,1.25)`, `(1.25,1.25)`, choose development winner by correct, then preservation, then closeness to no edit. This is a bounded grid, **not** an exhaustive optimal search. |
| Negative controls | healthy identity; one SHA-seeded random bounded edit | Random edit gets one dev measurement; it is not allowed to select from holdout. |
| Development decision | maximize 24-item math exact correct subject to dev preservation net loss no worse than -1/12; tie-break fewer malformed, then smaller squared edit magnitude, then lexicographic gains | The 12 dev preservation tasks are visible to all selecting conditions. |
| Candidate data exposure | identity, Luna, optimizer and random selected using development only; no heldout text/answer/results in tool menus | Development-only choice must precede the sealed one-shot heldout open. |
| Deadline | stop by the original 20:00 America/Denver Sunday atelier window (absolute four-hour cap from chosen session start); no recovery overtime | If incomplete, save accurate NOT RUN, FAIL or INCONCLUSIVE receipt. |

### Gates (all must retain raw row-level receipts)
- **G0 qualified:** exact revision/model; source and schema checks; frozen split/hashes; offline scorer unit tests pass; GPU/phase controller works; 24 math-development baseline has >=2 and <=20 correct plus >=4 valid completions. If infeasible, STOP; thresholds were prechosen, not retrospectively adjusted.
- **G1 lawful intervention:** Luna valid phased native call sequence, commit one in-bound two-gain edit or explicitly abstain.
- **G2 precommit evidence:** Luna's final candidate and `(1,1)` actually measured among <=6 repair probes on 24 math dev + 12 preservation dev; record predicted improvement, completion change, preservation risk and extra diagnostic information.
- **G3 functional gain:** relative to no edit, +5 or more net correct of 48 heldout math (24 ordinary + 24 structural).
- **G4 distinguish capability:** at least +3 net correct among **both-complete** math items and >=+2 net correct on 24 structural math. For transparency, report completion-changed contribution, not merely improvement percentage on a postselected subset.
- **G5 preservation:** no more than 2 net correct lost out of 48 heldout unrelated tasks; also report individual newly wrong transitions.
- **G6 investigator incremental contribution:** >=3 additional correct out of 48 math beyond best **development-selected** six-evaluation grid comparator.

A G3 pass/G4 fail suggests completion-related gains but does **not** by itself prove H2's mechanism. G3 pass/G6 fail is a weight-edit result without evidence of investigator superiority. Even all passes would be a single-sample, selected, noisy result, not acquisition of a general reasoning faculty.

### Reporting and integrity
- The identity baseline and all committed edits are evaluated on the same 96 heldout item IDs once. Responses are generated with the same sampling policy and per-item seeds. Report total right, completion rates, both-complete net gain, completion-changed net gain, wrong→right, right→wrong, ordinary and shift separately, as well as 48 preservation counts.
- Estimate paired bootstrap uncertainty over fixed items; no significance guarantee from n=48. Keep individual outputs for independent manual audit; explicitly inspect several symbolic derivations and suspected shortcut/format exploits.
- Separate score based on provided benchmark numerical answer keys from a human's independent recomputation. Do **not** claim an independent mathematical proof of all 24 Apple answers.
- Archive `manifest.json`, non-secret source hashes, environment versions, GPU details, full prompts, seed derivation, investigator API journal, selected model gains, raw responses, scorer statuses, independent recomputation notes, timing and hard-stop reasons.
- Preserve EX0005B as historical; EX0005C must not alter Aurora production governance, model production weights or old night verdicts.

### Source links
- Historic repository source: https://github.com/xxx3r/1001_nights/blob/main/nights/2026/11/2026-11-19-ex0005B/EX0005C_SUNDAY_PROPOSAL.md
- Qwen3 mode and sampling: https://huggingface.co/Qwen/Qwen3-0.6B
- GSM8K: https://huggingface.co/datasets/openai/gsm8k
- Apple generated-data schema: https://huggingface.co/datasets/apple/GSM-Symbolic

**Current disposition:** PREPARED; no claim of Colab readiness until the downloaded dataset schema, tokenizer, BF16 model and prompt behavior are verified by the human-operated L4 preflight.