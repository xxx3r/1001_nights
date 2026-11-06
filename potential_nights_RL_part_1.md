# Potential RL Nights: Worlds That Can Answer Back

**One Thousand & One Nights of Alignment | Idea bank | 2026-11-05**  
**Status:** UNTESTED FUTURE SEEDS, NOT PREREGISTERED EXPERIMENTS  
**Suggested future repo path:** `notes/potential_nights_RL.md` (or another location chosen during documentation AET)

> This file is a parking place for questions, **not a backlog, schedule, roadmap, or amendment to EX0002**. A future night must choose just one narrow hypothesis, construct its own frozen controls and acceptance checks, and finish at its own hard stop. EX0001 and EX0002 retain their original verdicts and evidence.

## The organizing idea

A useful world should distinguish **what happened**, **what information the agent legitimately received**, **what decision it made**, and **whether success was causal or accidental**. A complete observer-side action trace can support behavioral interpretation, but it does not prove an agent's hidden beliefs or thought process. The policy interface must not inherit the experimenter's ground truth or audit log.

The ideas below originated in the November 5 notebook conversation: rooms with walls and open entrances; genuine and false keys; ten coins before a key appears; region-specific rules; multiple locks; helpful and deceptive agents; cooperation; and agents competing to prevent another agent from finding keys. The additional controls and metrics are candidate operationalizations, not results.

## Small candidate nights (select individually, never bundle by default)

| Seed | Narrow question | Minimal distinguishing control / measurement |
|---|---|---|
| **RL-01 · The Window Is Not a Wall** | Does local perception respect physical line of sight rather than arbitrary color-region membership? | Same key and distance, but alternate a clear sight line with an opaque wall. Measure premature key visibility and successful discovery after opening an entrance. |
| **RL-02 · The Decoy Key** | Can an agent respond appropriately to an object that looks collectible but does not open the door? | Single real key vs real-plus-decoy worlds. Ensure a decoy cannot be detected via a privileged observation field. Record what was picked up, failed door feedback, and whether search resumes. |
| **RL-03 · The Tenth Coin** | Can an agent distinguish a conditional appearance rule from the habit of searching a familiar key location? | Key spawns only after ten *distinct* coins are collected. Compare nine versus ten coins at the same position; log counter state as legitimately earned evidence, not hidden truth. |
| **RL-04 · Two Regions, Two Laws** | Does a policy condition its search on a stated rule rather than transfer a familiar procedure blindly? | Give BLUE and GOLD different *explicit, testable* mechanics (e.g., collect coins vs activate a switch). Swap which region contains the key while keeping the clue truthful. Measure invalid assumptions and first rule-relevant action. |
| **RL-05 · Several Locks, Several Keys** | Can an agent plan around prerequisites rather than merely collect objects opportunistically? | Two locks with a simple directed dependency graph versus an order-swapped graph. Verify necessity and sufficiency of the right key set; measure successful ordering and excess actions. |
| **RL-06 · The Unreliable Guide** | Can an agent use evidence to distinguish reliable from misleading hints? | A helpful NPC and an NPC who deliberately gives false clues in an isolated toy world. Balance names, positions, and clue content; add a way to verify claims. Measure reliance before and after contradictory evidence. |
| **RL-07 · Two Searchers, One Map** | Does communication reduce duplicated search rather than just duplicate agents' actions? | Two agents with disjoint initial observations. Compare no communication, truthful messages, and messages delivered too late. Score information coverage, duplicate visits, and completion time. |
| **RL-08 · The Rival Search Party** | Can cooperative opponents hinder a searcher in a bounded competitive game, and can the searcher detect the interference? | Toy-world adversaries can hide *public game items* or block routes under fixed legal moves. Compare an adversary policy to nonadversarial random movement; measure discovery and recovery. No real-world cyber actions or adversarial exploitation. |
| **RL-09 · The Counterfactual Open Door** | Does an agent choose differently when the *actual* door is open versus when it is locked, even if it habitually searches for keys? | Matched maps with open/locked states, controlled information access, and no intrinsic key reward. Measure needless key collection and steps to goal. A true extended-environment simulation is **not** implied. |
| **RL-10 · The Start-Position Trap** | Does an apparently successful key-carrying policy fail when the start position changes? | Train/evaluate a scripted or later learned policy across matched conventional versus shifted starts. Measure whether position substitutes incorrectly for possession; keep true inventory out of hidden channels. |
| **RL-11 · Successful for the Wrong Reason** | Do trajectory filters distinguish information-grounded success from lucky or habitual success? | Store identical terminal rewards alongside action/observation traces. Compare clue-use labels, first search region, and path costs. Do not treat low entropy as proof of correct reasoning. |
| **RL-12 · What Would I Do If…?** | Can hypothetical policy behavior influence decisions in an *explicitly implemented extended environment*? | First reproduce a tiny, fully specified counterfactual-action payoff table; compare agents that do and do not condition on a defined simulated copy. This is a later theory-heavy night and **not** a property of the current key world. |

## Optional combinations for a future larger environment

**Puzzle-world mode:** Enclosed BLUE/GOLD rooms with open entrances, region-specific rules, decoys, ten-coin thresholds, and multiple locks can form a Mario 64 / Resident Evil-style navigation puzzle. Build only after the relevant isolated mechanics have independent tests. Otherwise success or failure will have too many explanations.

**Social-world mode:** Helpful guides, deliberately deceptive guides, multiple cooperators, and opposing teams can be added to a toy multi-agent environment. Separate false-information susceptibility, cooperation, competition, and policy adaptation before combining them.

**Experience-management mode:** Keep a researcher-only complete trace of observations, proposed actions, actual action outcomes, and chosen destinations. Compare outcome-based labels with information-grounded decisions. An audit trace is not the model's inner reasoning and must never be exposed as policy input.

## Minimal protocol for selecting any future seed

1. State **one** falsifiable contrast in ordinary language and define the observable decision that should differ.
2. Freeze paired worlds and a negative/mutation control **before** coding or inspecting outcomes.
3. Separate world truth, local observation, agent-visible memory, and researcher-only logs; count invalid actions, missing trials, and exclusions.
4. Prefer one CPU-scale scripted reference before considering any training. Keep a privileged reachability solver out of experimental policy decisions.
5. Report PASS / FAIL / INCONCLUSIVE / NOT RUN under that night's own preregistration and record I/H/C/D assistance. No retroactive repairs to closed nights.

## Reading connections (ideas, not experimental evidence)

- **Bad Habits: Policy Confounding and Out-of-Trajectory Generalization in RL**: position and history may look interchangeable only along a habitual trajectory. https://arxiv.org/html/2306.02419v2
- **ExGRPO: Learning to Reason from Experience**: motivates comparing experience quality and selection with crude outcome-only replay; does not establish that low entropy ensures valid reasoning. https://arxiv.org/html/2510.02245v2
- **Extending Environments to Measure Self-reflection in Reinforcement Learning**: proposes environments whose outputs depend on hypothetical policy behavior; distinct from an ordinary partially observed gridworld. https://arxiv.org/html/2110.06890v3

**Provenance:** User supplied the future-world concepts during the EX0002 Colab session; ChatGPT organized them into possible one-night falsifiable tests. No proposal in this file has been executed, validated, scheduled, or added to the frozen EX0002 criteria.

## New seed from Cell 9: RL-13 · The Conveyor Key

**Idea (2026-11-05):** A key advances one cell along a fixed row or column inside its region every time the searching agent takes an action, like a conveyor belt or airport moving walkway. This is **not** part of EX0002.

**Narrow question:** When a previously visible key changes position, does a closed-loop policy re-observe and intercept it, whereas an open-loop policy continues toward its stale coordinate?

**Paired control:** Same region, spawn, walls and initial key position. In condition STATIC, the key stays fixed; in MOVING, the key advances deterministically after each agent action, reversing at endpoints. Expose the key only by the same local perception rule, with no key-coordinate leakage via rewards or legal-action masks. Define whether motion occurs before or after observation in advance, as this affects interceptability.

**Primary measurement:** Number of attempted moves toward stale locations after a newer key observation; separately count interception success, action cost, unrecoverable misses, and timeouts. Compare an observation-responsive re-planner with an open-loop route follower. Avoid claims about neural learning when both are scripted. A changing-target policy is also a good mutation test: deliberately suppress the refreshed observation and verify that interception behavior changes.

**Additional control:** Place the key on a reachable path and verify that its motion never makes collection impossible under the chosen action order. Consider a key that pauses on collectible cells, or moves after every *movement action* but not after pickup; specify this before running.

**Status:** Future optional seed only. Not a task, experiment result, or retroactive change to EX0002.
