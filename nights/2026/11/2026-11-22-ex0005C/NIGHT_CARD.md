# EX0005C | NIGHT CARD | 2026-11-22

**Status:** G0 FAIL / SURGEON NOT RUN / HELD-OUT INTERVENTION NOT RUN.  
**Local window:** Sunday atelier, 16:00–20:00 MST; user reported G0 outcome at approximately 19:01 MST. The reported full development run took 674 seconds; this elapsed time is not independently present in the ZIP.

**Question.** Can a bounded Luna-selected weight edit improve healthy Qwen3-0.6B on verified mathematical answers beyond ordinary search, without sacrificing preservation?

**Rivals and prediction.** H1: real correctness and structural-transfer gains persist when both models complete. H2 (human-preferred): any gains arise mainly from repairing incomplete responses; negative changes are also plausible. The human also anticipated scorer/benchmark exploitation as a rival explanation. No edit was attempted, so neither behavioral hypothesis was tested.

**Human-owned exercise.** The six-pair decomposition was independently computed by the user: net +2 = both-complete +1 + completion-changed +1, then checked with assistance. The user's predicted direction favored H2; this was a prediction, not an observed mechanism.

**Method and prior freeze.** Thinking enabled, sampling temperature 0.6 / top-p 0.95 / top-k 20, math limit 3,072 tokens, item-derived seeds. G0 required 2–20 of 24 development math items correct and at least four completed responses before a surgeon call. The original generator argument caused a preflight API error; a seed-scoped generation correction allowed smoke and development-only scoring. No prospective gate was changed.

**Observed.** In the provided ZIP, two smoke items match the first two full development rows and are correct/complete. The 24 unique development rows show **23/24 scorer-correct** and **24/24 scorer-complete**. No row hit the 3,072-token limit; longest 2,394 tokens. One wrong result, `gsm8k_train:4635`, answered 51 red pencils by counting red, yellow and green pencils as red; independent arithmetic on its reproduced problem gives 15 + 3×2 = 21. Archive CRC integrity passed. This is an audit of supplied receipts, not independent GPU rerun or full answer-key regrading.

**Verdict.** **G0 FAIL, STOP** because 23 exceeds the frozen maximum of 20. No selected edit, numerical comparator, held-out scoring, H1/H2 discrimination, or capability claim. An easy development sample, not the hypothesized skill intervention, is the validated limitation.

**Acquired skill / remaining deficit.** Distinguishing a working model from a qualifying model and preserving a preregistered stop; next independent night may prospectively select a more discriminating difficulty distribution, not retrofit this night's gate. **STOP: no continuation debt.**

**Assistance:** human-authored H2 preference and decomposition; AI-assisted protocol, code, repair and independent ZIP consistency audit. Original ZIP SHA-256: `6d07111bcaf81af2a123f12ea12887b3d222e162347b111d7ef2d92b0a80ce01`.