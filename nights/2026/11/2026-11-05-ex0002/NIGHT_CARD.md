# NIGHT CARD | ALGN-EX0002: The World Must Be Able to Answer

**Night / date:** 0002 · November 5, 2026 (America/Denver)  
**Duration:** Not recorded; no estimate substituted · **Assistance:** D (AI-drafted)  
**Verdict:** **PASS, scripted instrument discrimination** · **Status:** Closed; preregistration preserved

**Question.** Can a partially observed world distinguish clue-responsive search, habitual BLUE-first search, and conditional key use?

**H1 / H2.** A responsive script inspects the adjacent door, chooses the hinted BLUE/GOLD key region when locked, and heads directly to the goal when open. A habitual script searches BLUE first regardless of the clue. Matched locked BLUE/GOLD worlds must have identical initial observations; a corrupted GOLD clue must defeat the discrimination check.

**Human-owned reasoning.** The researcher connected *Bad Habits* to the door-hint proposal, rejected a potentially leaky direction reward, predicted GOLD versus BLUE choices, identified the difference between `door_blocked` feedback and an undiscovered `door_status`, tested a broken adjacency rule, and interpreted cleared-cell memory. Python and most assertions were AI-drafted, not proof of coding mastery.

**Method.** Frozen procedural 11×11 instrument: seeds **7, 11, 23, 47, 101**; four locked/open × BLUE/GOLD worlds per seed; two scripts; **40 rollouts**; eight preregistered gates; no neural training. A separate, fixed-map, human-guided Colab reconstruction used eight matched episodes with action/observation traces. Do not pool their counts.

**Results.** Procedural evidence reports **8/8 gates PASS**, **40/40 goal completions**, zero rejected fixtures, invalid actions or truncations. Responsive locked-door first choices **10/10** correct; BLUE-first habit **5/10**. All ten responsive open-door trials reached the goal without a key; five clue-corruption probes broke the intended assertion. Colab: **8/8** goals reached across **99 actions**; locked GOLD took **15 responsive vs 22 habitual actions**, and open-door runs took **5 vs 13**. The JSON digest matches the audit; read-only review reported **1,019 passing trace checks**.

**Limit and independent check.** Notebook, source, logs and verifier are archived. The fixed-map verifier validates recorded behavior but currently expects a separately staged ZIP; it is not a turn-key repo replay. No learned RL policy, object permanence or generalization was established. Deterministic fixtures are not statistical replications.

**Learned:** Success can hide a wrong initial decision. **Remaining deficit:** Portable verifier and future learned-policy controls. **Stop:** No retroactive gate changes or experiment reruns in documentation AET.
