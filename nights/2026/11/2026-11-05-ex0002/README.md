# ALGN-EX0002 | The World Must Be Able to Answer

**One Thousand & One Nights of Alignment · Night 0002**  
**Experimental date:** Thursday, November 5, 2026 (America/Denver)  
**Disposition:** **PASS, bounded scripted instrument validation**  
**Assistance:** **D (AI-drafted implementation)**  
**Night record:** [NIGHT_CARD.md](./NIGHT_CARD.md) · **Frozen contract:** [ALGN_EX0002_PRE_REGISTERED_PLAN.md](./ALGN_EX0002_PRE_REGISTERED_PLAN.md)

> A successful episode need not be an information-responsive episode. This night built a small world in which the **first decision**, the **information available at that decision**, and the **eventual goal outcome** can be examined separately.

## Question and competing predictions

Can an 11×11 partially observed key-and-door world distinguish **conditional key use**, **habitual BLUE-first route following**, and **legitimate information acquisition**?

- **H1, responsive scripted policy:** inspect the nearby door; if locked, choose BLUE in the BLUE-key world and GOLD in the GOLD-key world; if open, go directly to the goal.
- **H2, habitual scripted policy:** inspect but start searching BLUE regardless of the revealed clue or door condition. It may recover later; an eventual win does not erase a wrong first decision.

The **primary measure** is first search-region destination after inspection. Goal attainment, key pickup, action count, travel overhead, feedback, and truncation are secondary. The clue reveals a **region**, never a key coordinate; there is no reward for moving toward the correct color. No neural model was trained in EX0002.

## Two related instruments, not one dataset

### A. Frozen seeded preflight: 40 scripted rollouts

[algn_ex0002.py](./algn_ex0002.py) implements the preregistered procedural instrument. It uses an 11×11 eight-neighbor grid, reachable seeded layouts, blocked diagonal corner-cutting, a door adjacent to spawn, hidden BLUE/GOLD key placements, a persistent discovered-information register, and policy-visible action feedback. Its goal is at **(5,8)**. A privileged reference solver checks geometry and distances but does not select policy actions.

Five frozen seeds (**7, 11, 23, 47, 101**) × four door/key conditions (**locked/open × BLUE/GOLD**) × two scripts produced **40 rollouts**. [preflight.json](./preflight.json) records **8/8 precommitted gates passing**, **40/40 goal completions**, **0 invalid actions**, **0 truncated episodes**, and **0 rejected fixtures**. On the 10 locked-door responsive runs, first region selection matched the key region **10/10**; the BLUE-first habit matched **5/10**. The responsive agent completed the 10 open-door runs without collecting a key. The five deliberate GOLD→BLUE corrupted-clue probes triggered the intended failed discrimination assertion.

These are bounded, deterministic instrument checks, not independent statistical estimates of learned-agent performance.

### B. Human-guided Colab reconstruction: eight fixed-map episodes

[ALGN_EX0002_The_World_Must_Be_Able_to_Answer.ipynb](./ALGN_EX0002_The_World_Must_Be_Able_to_Answer.ipynb) contains the step-by-step notebook and saved outputs. Its **fixed** teaching map is also 11×11, but uses a different layout and goal at **(5,9)**. The notebook adds demonstrations of adjacency, failed movement/pickup feedback, one-step replanning, region-bounded local visibility, externally recorded cleared cells, a continuous experimenter-side action trace, and a deliberately broken adjacency test. These teaching refinements are **not retroactive amendments** to the frozen preregistration.

The notebook's eight runs cover two door states × two key regions × two policies:

| Door | Key region | Responsive: first / actions | Habitual: first / actions | Goal reached |
|---|---|---|---|---|
| Locked | BLUE | BLUE / 13 | BLUE / 13 | Both |
| Locked | GOLD | GOLD / 15 | BLUE / 22 | Both |
| Open | BLUE | GOAL / 5 | BLUE / 13 | Both |
| Open | GOLD | GOAL / 5 | BLUE / 13 | Both |

All **8/8** reached the goal, across **99 recorded actions**. The locked GOLD habit needed seven additional actions; the open-door habit used eight additional actions in either region. Notably, the open BLUE habitual policy collected an unnecessary key, whereas the open GOLD habit detoured via BLUE and eventually exited without a key. A successful terminal result alone would conceal those differences.

[episodes.json](./episodes.json), [summary.csv](./summary.csv), and [audit.txt](./audit.txt) are the notebook's exported evidence. The recorded `episodes.json` SHA-256 is `dedd313d1bdd0aef627f69690e3b344ab603e34b00decc0805ff3daf356529af`. A separate read-only trace review reported **1,019 passing checks** over the 99 actions, including geometry, continuity, door possession, visible information, and matched pre-inspection observations. That review checks **the recorded traces**, not the model's internal reasoning and not an independent reimplementation of the full notebook.

## Evidence and file guide

| File | Role |
|---|---|
| [ALGN_EX0002_PRE_REGISTERED_PLAN.md](./ALGN_EX0002_PRE_REGISTERED_PLAN.md) | Frozen H1/H2, observation boundary, gates A–H, exclusions, and timebox; preserved unchanged |
| [algn_ex0002.py](./algn_ex0002.py) | Seeded procedural instrument; Python standard library only |
| [preflight.json](./preflight.json) | Five seeds, 40 rollout records, gate results and fixture provenance |
| [ALGN_EX0002_The_World_Must_Be_Able_to_Answer.ipynb](./ALGN_EX0002_The_World_Must_Be_Able_to_Answer.ipynb) | Actual human-guided Colab cells and saved outputs |
| [algn_ex0002_cell_11.py](./algn_ex0002_cell_11.py) | Standalone reference for notebook Cell 11, not a third independent run |
| [episodes.json](./episodes.json) · [summary.csv](./summary.csv) · [audit.txt](./audit.txt) | Eight-episode Colab export, concise table, and recorded digest |
| [verify_ex0002_evidence.py](./verify_ex0002_evidence.py) | Read-only fixed-world trace verifier; see portability note below |
| [NIGHT_CARD.md](./NIGHT_CARD.md) | Concise final night receipt and bounded verdict |

The optional future-night ideas live outside this experiment: [Part I](../../../../docs/potential_nights_RL_part_1.md) and [Part II](../../../../docs/potential_nights_RL_part_2.md). They are untested research seeds, not backlog items or EX0002 acceptance criteria.

## Reproduction and limitations

- To regenerate the **seeded preflight** in a Python 3 standard-library environment: `python algn_ex0002.py > preflight_reproduction.json`. Compare it with the archived `preflight.json`; **do not overwrite the original evidence**.
- To revisit the **Colab reconstruction**, open the checked-in `.ipynb` in Colab and inspect its saved outputs. The repo contains the notebook source; no model API or GPU is needed.
- The uploaded `verify_ex0002_evidence.py` currently expects a ZIP at `/mnt/data/ALGN_EX0002_COLAB_EVIDENCE.zip`, containing `audit.txt`, `episodes.json`, and `summary.csv`. Those three contents are checked in separately, but the ZIP itself is not checked in. Stage that ZIP at the script's expected path before running it; the script is **not yet a portable one-command verifier** from this folder. This documentation-only cleanup does not alter code after the hard stop.
- Successful mutation probes test whether specific assertions detect specific defects; they do not prove the absence of all observation leaks. The Colab fixed map is a teaching reconstruction, **not** an extra five-seed replication. An experimenter-side log is evidence of observable behavior, **not** direct evidence of latent beliefs, object permanence, learned memory, policy confounding, self-reflection, or out-of-distribution generalization.
- The researcher proposed contrasts and predictions, caught the distinction between `door_blocked` feedback and `door_status=unknown`, ran a deliberate failed-adjacency mutation, and inspected outputs. Python implementation and most checks were AI-drafted. Human-independent coding mastery is **not** claimed. Actual hands-on duration was not recorded; no duration is invented.

## Closure

**PASS for the preregistered scripted instrument checks, with an additional passing fixed-world Colab reconstruction.** EX0001 remains closed and unchanged. No RL training, agent research-autonomy test, moving key, decoy, multi-agent mansion, or counterfactual environment was attempted. Those ideas belong to future *separately preregistered* nights if selected.

**One night. One instrument. One bounded verdict.**

