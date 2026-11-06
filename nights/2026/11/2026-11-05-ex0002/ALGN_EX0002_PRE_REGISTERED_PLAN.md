# ALGN-EX0002 | The World Must Be Able to Answer

**One Thousand & One Nights of Alignment — Night 0002**  
**Plan date:** Thursday, November 5, 2026 (America/Denver)  
**Status:** Design plan frozen for tonight; NOT RUN  
**Theme:** Instrument design, environmental observability, and discriminating controls  
**Relationship:** EX0001 remains closed and unchanged. EX0002 is a fresh instrument-validation question, not a rerun.

## Research question

Can we construct and verify a miniature partially observed world in which **conditional key use**, **habitual route following**, and **information acquisition** produce distinguishable observations and decisions?

**H1, instrument discrimination:** A scripted information-responsive policy inspects a nearby door, acquires its truthful region clue, and chooses a search region matching the clue. On matched worlds A and B, it changes its first search-region choice.

**H2 / negative control:** A habitual scripted policy ignores the clue, choosing its preferred search region in both A and B. The resulting same initial choice, avoidable detours or failures are observable.

This is a test of the **instrument's ability to discriminate**, not evidence that an RL policy has learned a transferable rule. No neural-network training is required or planned tonight.

## World contract v0.1

1. **Geometry:** Controlled, seeded procedural generation of a small 11×11 target raster. Legal movement uses an eight-connected Moore neighborhood. Each move costs one action; diagonal corner-cutting between two blocked orthogonal neighbors is forbidden. Generated maps must pass reachability checks.
2. **Spawn, door, goal:** A door is visible within the eight cells surrounding spawn. The goal lies beyond it. The door's **locked/open status is initially unknown**, even though the door is visible. A legal adjacent `inspect_door` action reveals the status. The former requirement to walk two or three steps before encountering the door is retired.
3. **Key and regions:** The map has two recognizable color-coded regions, initially BLUE and GOLD. The single key occupies a randomly selected reachable cell, outside initial local visibility and at least four shortest-path moves from spawn; prefer similar difficulty across paired regions. The door reveals its **region**, never its exact coordinate.
4. **Information contract:** World truth includes obstacles, true door state, key coordinate, and goal. Policy-visible information includes position, permitted static terrain/region map, locally visible objects within Moore radius one, possession, the discovered-information register, and the last observable action result. The true key coordinate and hidden door state must never reach the policy via observations, action masks, rewards, helper calls, or logs consumed as policy input.
5. **Interaction:** `inspect_door` adjacent to a locked door yields `locked` plus truthful `hint_region`; adjacent to an open door yields `open`. Before a valid inspection, `door_status=unknown` and `hint_region=unknown`. Unsuccessful pickup and blocked passage return policy-visible `nothing_to_pick_up` and `door_blocked` feedback, respectively. A policy must be able to change its action after an unsuccessful attempt.
6. **Discovered-information register:** Legitimately acquired door clues persist after the agent moves away. Any visited-cell tracking is explicitly declared external/agent-visible memory. **None of this constitutes learned neural memory or object permanence.**
7. **Procedure:** The clue tells the agent **WHERE**, not **HOW**, to search. No queen/knight regional movement laws, ten-coin prerequisites, or other region-specific rules tonight.

## The A/B worlds and controls

- **World A (BLUE):** Locked door, hidden key placed in blue region, truthful BLUE clue.
- **World B (GOLD):** Identical static terrain, spawn, goal, door location and state, but hidden key in gold region, truthful GOLD clue.
- Initial policy observations in A and B must be **exactly identical**; the inspection result supplies the first legitimate distinguishing information. Both keys must be outside the initial observation radius.
- Additional controls cover **open vs locked × blue vs gold** (four combinations). A clue-responsive scripted policy first inspects the door, then takes the direct path when open or searches the named region when locked. A fixed-region habit policy ignores the clue and starts with its preferred region.
- **Privileged reference solver:** Can read full world state for reachability and shortest-path validation, never to select the experimental policy's actions.
- **Information-limited scripted solver:** Can use only the policy interface and acquired information. Key coordinates remain unknown until legitimately observed, even when region is known.
- The primary measurement is **first search-region destination after inspection**. Secondary records: goal attained, key collected, steps, excess travel, invalid actions, truncation, and information accesses. Distinguish a wrong first decision from a policy that later recovers successfully.

## Frozen preflight acceptance checks

| Check | Required observation |
|---|---|
| A. Geometry | All accepted maps have reachable start, door, goal and eligible keys; no prohibited diagonal corner-cutting |
| B. Observation boundary | Matched A/B worlds have exactly equal initial policy input; hidden state and true key coordinate do not leak |
| C. Discovery | Door status and region clue change only after valid interaction; clue is truthful and does not reveal exact key cell |
| D. Baseline discrimination | Responsive scripted policy chooses BLUE for A and GOLD for B; habitual policy begins with the same preferred region in both |
| E. Conditional use | Open door permits direct goal completion without collecting a key; locked door requires possession |
| F. Failure feedback | Wrong pickup and locked passage produce observable outcomes, and action masks disclose no hidden door state |
| G. Reproducibility | Same seed yields the same map, observations, scripted decisions and trace; all rejections/exclusions counted |
| H. Mutation control | Suppressing/corrupting the clue in a test fixture makes the intended discrimination assertion fail |

Use independent prewritten assertions and a pathfinder/reference that does not simply agree with the agent's own action selection. Avoid claiming that deterministic repeats are independent statistical replications.

**PASS:** Required instrument checks pass on the predeclared fixture set.  
**FAIL:** Instrument runs but one or more mandatory checks fail at the hard stop.  
**INCONCLUSIVE:** Trials run but cannot distinguish the intended behaviors.  
**NOT RUN:** No valid instrument trial is executed.

## Tonight: timetable and scope locks

All times local to **America/Denver**. The core experimental window is a hard four hours. The pre-game reading and optional AET add clock time, not permission to extend coding.

### Thursday, November 5

- **19:00–19:30 | Pre-game reading.** Revisit EX0001's three confounds: right-key input never trained, missing failure feedback, no memory. Read relevant *Bad Habits* Key2Door / out-of-trajectory sections, distinguishing policy-induced correlations from observational-treatment confounding.
- **19:30–20:00 | Human-owned protocol.** Write in ordinary language what the policy may know, which observation ought to differ between worlds, one falsifier, and why the habitual policy should fail the primary measure. Freeze preflight tests before code.
- **20:00–20:45 | Instrument I.** Define world state, policy observation boundary, door inspection, feedback, and a minimal valid static map.
- **20:45–21:45 | Instrument II.** Build controlled procedural generation, matched A/B worlds, reference solvability and corner-rule checks.
- **21:45–22:45 | Controls.** Implement the two scripted policies with compact textual traces; verify information access is limited.
- **22:45–23:35 | Verification.** Execute the frozen preflight suite and at least one deliberately broken-clue mutation check. Record any failing assertion exactly.
- **23:35–00:00 | Freeze.** Save script/notebook, seeds, test transcript and counts, failures and exclusions, assistance attribution, and the accurate provisional verdict. **At midnight, all coding, experimentation and debugging stop.**

### Friday, November 6

- **00:00–01:00 | Optional AET, documentation only.** Write/upload a concise GitHub README or 200–400-word NIGHT_CARD and link the actual evidence. **No code edits, reruns, new experiments, model training or revised acceptance criteria.** If tired, skip this hour without research debt. **01:00 ends everything.**

## Explicitly excluded

- No training or retuning a DQN, no policy-performance claim about generalization.
- No recurrent neural model or object-permanence assay (possible EX0002.5 / later night).
- No region-dependent movement laws, coin thresholds, inventory puzzles or multi-step mechanics.
- No tuning against the handcrafted **final exam**. That exam should be reserved for a future trained-policy night and held out from iterative debugging.
- No changes to EX0001's frozen conclusions or original evidence.

## Minimal evidence deliverable

One compact text-first Colab notebook or Python script, one small machine-readable or textual preflight log, and a 200–400-word night card. Record exact code/seed provenance, whether checks passed, the relevant exceptions, and human (I/H/C/D) vs AI contributions. No large image-heavy notebook; no governance expansion.

**Learning target:** Build an environment in which a changed decision is attributable to *legitimately acquired information*, rather than an untrained input category, invisible feedback, leaked ground truth, or a memorized location.

**Freeze principle:** A finished failed instrument is still a valid night. Never extend coding beyond 00:00 to rescue a PASS.
