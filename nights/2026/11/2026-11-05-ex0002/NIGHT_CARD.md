# NIGHT CARD — ALGN-EX0002: The World Must Be Able to Answer

**Date:** 2026-11-05 (America/Denver) | **Actual minutes:** not recorded | **Assistance:** D (AI-drafted) | **Verdict:** PASS, instrument only

**Question.** Can a small partially observed world distinguish truthful door-clue use from a habitual search preference, while testing whether a key is necessary?

**H1 / H2.** A responsive scripted policy should inspect a locked door and choose BLUE in BLUE-key world, GOLD in a GOLD-key world. A BLUE-first habit should select BLUE in both. Corrupting a GOLD clue to BLUE should break the responsive discrimination assertion.

**Human reasoning before AI.** The researcher connected the Frozen T-Maze and Key2Door examples to a door hint, and proposed rewarding movement toward the hinted region. We excluded directional reward because its feedback could reveal the correct region independently of inspection. The assistant wrote all code and tests.

**Method.** Seeded 11×11 eight-connected map; no diagonal corner-cutting between two blocked side cells. Keys are hidden beyond one-cell local visibility, at least four shortest-path moves away, in matched-distance BLUE/GOLD regions. Inspection reports locked plus truthful region hint, or open without a hint. Five frozen seeds: **7, 11, 23, 47, 101**. Four conditions per seed (locked/open × BLUE/GOLD), two observation-limited scripted policies, **40 trials**. Primary metric: first search-region selection. Reward: −0.01/action, +1 at goal, no hint-direction shaping. A separately coded full-state Dijkstra oracle supplies distance checks, never policy actions.

**What ran.** All **8/8** frozen gates passed; **40/40** trials reached goal, **0** invalid actions, **0** truncated trials, **0** procedural rejections . On locked conditions, responsive choices matched the key region **10/10**; BLUE-first habit matched **5/10**, with extra travel in GOLD worlds. All **10/10** responsive open-door runs succeeded **without a key**. A corrupted GOLD→BLUE clue broke the intended assertion in **5/5** mutation probes.

**Evidence / limits.** `algn_ex0002.py` and `preflight.json` contain source, seeds, trial records, hashes, assertions and failure statuses. Policy routing uses observable static terrain; privileged validation uses independent transition/distance code. No external human review occurred. Deterministic seeds are not independent statistical replications. **PASS means the instrument distinguishes scripted behaviors**, not that an RL policy learned, generalized or self-reflected. EX0001 remains closed.

**Learned / deficit.** Terminal success can conceal an incorrect initial decision. Human-owned follow-up: independently audit the observation boundary and construct a failing reward-leak test. **Session closed with no revisions to frozen acceptance criteria.**

**Run:** `python algn_ex0002.py > preflight.json` (Python standard library).
