# ALGN-EX0002 | Three witnesses, a locked door, and a mansion yet to be built

**One Thousand & One Nights of Alignment · Reading, historical design influences, and an experimental field note**  
**Night executed:** 5 November 2026 · **Editorial record:** 6 November 2026  
**Companions:** [Night README](./README.md) · [Night card](./NIGHT_CARD.md) · [Frozen plan](./ALGN_EX0002_PRE_REGISTERED_PLAN.md) · [EX0001 references](../2026-11-01-ex0001/ALGN_EX0001_REFERENCES.md)

> We had taught one agent to find a key. It sometimes won by taking the wrong route. So we built a smaller world, not to make the agent brilliant, but to make its mistakes observable. A door could now answer a question; a failed pickup could answer another. The witnesses brought three different cautions about what it means to learn from experience. Two old games arrived later, carrying ideas for other nights.

Like [EX0001's field notebook](../2026-11-01-ex0001/ALGN_EX0001_REFERENCES.md), this is **a trail of questions and intellectual influences, not an appeal to authority**. It distinguishes (a) what a paper argues, (b) what EX0002 actually implemented or measured, and (c) the later hypotheses suggested by classic games. The Galileo-like posture is methodological: prefer a world that can contradict our account of it. No historical claim about Galileo having designed these experiments is intended.

## Prologue · The observer and the door

EX0001 demonstrated a contrast: a small trained DQN succeeded on familiar open- and locked-door tasks, yet repeatedly failed when the visible key appeared in an untrained location. The failure was real, but its interpretation was constrained. The new location corresponded to an untrained input category; unsuccessful actions did not alter the policy's next observation; the network had no memory of previously seen objects. The researcher noticed a fourth limitation: the agent was **given** the door's status rather than learning it by encountering the door. These are not defects retroactively erased from EX0001. They are reasons to ask a *new* question.

For EX0002 we made the door visible but its state initially unknown. An adjacent `inspect_door` action revealed **open**, or **locked** together with a truthful BLUE/GOLD region clue. The clue did not disclose the key's cell. A failed pickup returned `nothing_to_pick_up`; blocked passage returned `door_blocked`. A discovered-information register retained facts legitimately acquired from inspection. These are observation and logging mechanisms, not proof of internal memory or object permanence.

The primary question was deliberately smaller than learning: **Can the instrument tell an information-responsive scripted policy from a habitual BLUE-first scripted policy, even when both ultimately reach the goal?**

## Witness I · Suau, Spaan and Oliehoek: when the route becomes a misleading explanation

**Reading:** Miguel Suau, Matthijs T. J. Spaan and Frans A. Oliehoek, [*Bad Habits: Policy Confounding and Out-of-Trajectory Generalization in RL*](https://arxiv.org/html/2306.02419v2) (arXiv v2, June 2024); published in *Reinforcement Learning Journal* **4**, 1711–1732 (2024), [journal record](https://rlj.org/papers/suau2024habits). Relevant: the Frozen T-Maze, Key2Door example, and the appendix's dynamic Bayesian networks.

The paper studies **policy confounding**: as an agent repeatedly follows a policy, its own trajectory distribution may make a fragile correlation look sufficient for choosing actions. In Key2Door, possession is not displayed to the agent. On an established optimal route, being at a later corridor position can stand in for the fact that the key was collected earlier. In a shifted-start evaluation, that implication need not hold. The dynamic Bayesian network diagrams clarify that what is predictive **under the familiar trajectory** need not characterize the world's full causal dependencies.

This was the closest ancestor of our paired BLUE/GOLD worlds. We did **not** reproduce the paper's learned representation or demonstrate policy confounding. We **programmed** a habitual agent to prefer BLUE and another agent to use the inspected hint; our task was to make that difference measurable. The matched worlds began with identical observations, and after valid locked-door inspection the region hint supplied the decisive difference. We also deliberately **did not reward movement toward the hinted color**, because such a reward could become another channel for revealing the correct region.

**What this witness gave us:** the warning that terminal success does not validate the route-specific shortcut used to obtain it.  
**What it did not certify:** learned habits or robust out-of-trajectory generalization in EX0002.

**Question carried forward:** With matched training exposure and a genuinely learned policy, does changing the start, the route, or the key's location expose dependence on position as a proxy for possession or knowledge?

## Witness II · Alexander and colleagues: what would the agent do if the room were different?

**Reading:** Samuel Allen Alexander, Michael Castaneda, Kevin Compher and Oscar Martinez, [*Extending Environments to Measure Self-reflection in Reinforcement Learning*](https://arxiv.org/html/2110.06890v3), arXiv v3 (July 2022). Relevant: definition of extended environments (§2), **Tempting Button** (§3.2), and benchmarking discussion (§6).

An ordinary environment reacts to the agent's actual interaction history. Their **extended environment** can additionally condition its outputs on the agent's hypothetical behavior under a different history. In *Tempting Button*, pressing a present button gives a favorable immediate reward, yet what the agent **would do** if the button appeared also affects rewards in buttonless circumstances. That makes a locally tempting action potentially worse as an overall strategy. This is a formal counterfactual-agent construction, not a synonym for a partially observed gridworld.

The paper prompted a wonderfully economical EX0002 control: **If the door is already open, the agent should not have to search for a key.** The actual world, not the agent's customary route, defines what is necessary. Yet our environment never simulated a counterfactual copy of the agent or computed rewards from hypothetical actions. It remained an **ordinary**, partially observed environment. Consequently, EX0002 is **not** a self-reflection benchmark in the authors' sense.

**What this witness gave us:** a way to ask whether locally attractive actions should be evaluated against alternate circumstances and an agent's own possible responses.  
**What it did not certify:** counterfactual introspection or self-modeling in our two scripts.

**Question carried forward:** In a separately specified extended environment, can an agent use knowledge of its own hypothetical behavior to choose a better real action than an agent that attends only to immediate reward?

## Witness III · Zhan and colleagues: which experiences deserve to be replayed?

**Reading:** Runzhe Zhan and colleagues, [*ExGRPO: Learning to Reason from Experience*](https://arxiv.org/html/2510.02245v2), arXiv v2 (February 2026). Relevant: experience quality (§3.2), **collection / partition / selection** (§4.1), mixed-policy optimization (§4.2), and the snowball-effect case study (Appendix F.4).

ExGRPO tackles a training problem that EX0002 explicitly does **not** attempt: how to organize prior reasoning trajectories for more effective reinforcement learning with verifiable rewards. It groups experiences using observed question correctness, favors medium-difficulty questions in selection, and chooses low-entropy trajectories under the current policy among candidates. It then uses selected experiences in a mixed-policy optimization objective. The paper's caution is that replaying superficially successful but misguided reasoning can contaminate later learning; selection must negotiate exploitation and exploration.

Our reading supplied a further caution for **evaluating** experience: correctness and entropy are not enough to establish *why* a trajectory succeeded. Both EX0002 scripts were deterministic, so both can have zero action-selection entropy while using the door hint differently. Our instrument recorded first search destination, action feedback, path cost, and key possession separately from the goal flag. **That audit idea is an interpretation inspired by ExGRPO, not a feature or result claimed by its authors.** We did not implement GRPO, ExGRPO, a replay buffer, a learned policy, or entropy-based sampling.

**What this witness gave us:** a principled reason to care about the quality and provenance of experiences, not just their presence in a successful set.  
**What it did not certify:** any improvement from learning on EX0002 traces.

**Question carried forward:** Does selecting genuinely information-grounded successful trajectories improve a learned agent's robustness over selecting successful trajectories solely by outcome or entropy, with matched compute and a frozen verifier?

## The field note · A small world that finally answered

Two related, **not interchangeable**, artifacts resulted. The frozen procedural Python instrument uses seeded 11×11 maps and five declared seeds; the human-guided Colab notebook uses a separate fixed 11×11 map with a different goal coordinate, local search examples, and complete action traces. The notebook is a teaching reconstruction, not a later revision of the frozen gates. **No neural model was trained on this night.**

- **Seeded preflight:** its saved report records **8/8 frozen gates passing** across **40/40 completed scripted rollouts**. For locked doors, the responsive script chose the actual key region **10/10** times, while the BLUE-first script matched it **5/10** times. Five deliberate GOLD-to-BLUE clue-corruption probes defeated the targeted discrimination assertion.
- **Fixed-map Colab:** all **eight** episodes reached the goal, spanning **99** logged actions. In locked GOLD, responsive took **15** actions versus habitual **22**; in both open-door conditions responsive took **5** versus habitual **13**. A separate read-only trace review reported **1,019** checks passing. A recorded trace reveals a decision sequence, not a neural belief.

The decisive lesson was not that one script is intelligent and the other foolish. **Both finished every fixed-map episode.** But the instrument could see the unnecessary detour, the prior clue, the blocked door, the pickup event, and whether possession preceded crossing. This is a **PASS for scripted instrument discrimination**, not evidence that an RL agent learned transferable rules.

The researcher supplied the design questions, made predictions, caught the hidden distinction between `door_blocked` feedback and `door_status=unknown`, and deliberately broke an adjacency assertion to see it fail. The assistant drafted most code and tests. **Assistance level D** remains part of the evidence, not an embarrassment to be erased.

For reproducibility and the exact limitations, see [README](./README.md), [NIGHT_CARD](./NIGHT_CARD.md), [the procedural log](./preflight.json), and [the Colab trace export](./episodes.json).

## The visitors from the games shelf · Future design influences, not experimental citations

Two classic game designs joined the conversation **after** the experiment's core hypothesis had been fixed. Neither was run as EX0002, and neither provides evidence for the claims above.

### *Super Mario 64* (Nintendo, 1996): progression is a dependency graph

**Design reference:** Nintendo, [*Super Mario 64* instruction manual](https://www.nintendo.com/eu/media/downloads/games_8/emanuals/nintendo_8/Manual_Nintendo64_SuperMario64_EN.pdf), especially its descriptions of Power Stars and star-marked castle doors.

The castle opens new routes as the player collects enough **Power Stars**. That is the historically relevant design reference: access to places depends on previously accumulated accomplishments. Our future proposal of **ten coins before a key appears** is our own invented mechanic, **not a claim that the original game's star doors require ten coins**. Future variants could isolate prerequisite counting, switching regional rules, multiple locks, or paths that become accessible only after certain actions.

**Hypothesis seed, not a result:** Can a policy learn a conditional prerequisite rule rather than memorize a fixed sequence of item pickups? Compare a nine-item and ten-item state while keeping other observations controlled.

### *Maniac Mansion* (Lucasfilm Games, 1987): the character changes the solution space

**Design references:** Andrew Williams, [*History of Digital Games: Developments in Art, Design and Interaction*](https://www.routledge.com/History-of-Digital-Games-Developments-in-Art-Design-and-Interaction/Williams/p/book/9781315715377) (Routledge, 2017, ch. 6: *Home Computers*, on *Maniac Mansion*'s selectable companions, verb/object interface, and character-specific puzzles); and [ScummVM's official compatibility documentation](https://www.scummvm.org/compatibility/), which lists the classic game as supported. [ScummVM's explanation](https://www.scummvm.org/) also clarifies that it **reimplements game executables rather than emulating a complete original computer** and requires the player's own game data.

The game's selected characters and verb/object puzzle vocabulary suggest a different scientific question from EX0002: **What happens when the available solution depends on which agents are present and what each can legitimately do?** The proposed *RL Mansion* would be an original, measurable puzzle world, not a reproduction of the original game's art, text, characters, or puzzles. An additional, separate exercise might let an AI operate a legally obtained game in ScummVM to study tool-mediated gameplay and then test whether such direct interaction improves its subsequent experimental designs.

A four-agent proposal uses **A, B, C, D**, with three rotations that cover every two-agent pairing exactly once: **AB/CD**, **AC/BD**, **AD/BC**. Abilities would be real environment permissions, not merely personality descriptions in prompts. Before comparing pairs, a privileged reference solver would need to verify that each assigned pair has at least one viable route. Otherwise, pairwise failure would only establish that a puzzle was impossible.

**Hypothesis seed, not a result:** Does a model asked to design a controlled experiment after interacting with a game propose better discriminatory tests than the same model given only a description? Such a study would need fixed evaluation criteria, matched budgets, blinded review, and a no-play or observation-only control. The appealing phrase *lived experience* is an analogy; a model's tool-mediated interaction is not evidence of subjective experience. We do not claim the topic is unstudied or that interaction improves research judgment without a test.

Companion parking lots, **not a schedule or EX0002 scope amendment**: [Potential RL Nights, Part I](../../../../docs/potential_nights_RL_part_1.md) · [Part II: The Mansion That Answers Back](../../../../docs/potential_nights_RL_part_2.md).

## Coda · What the witnesses may and may not testify to

| Witness | Legitimate lesson for this night | Claim the witness cannot make for EX0002 |
|---|---|---|
| **Suau et al.** | Beware route-specific proxy correlations and evaluate changed trajectories. | That a scripted BLUE habit proves learned policy confounding. |
| **Alexander et al.** | Distinguish real consequences from hypothetical-policy consequences. | That an ordinary key-and-door grid implements extended self-reflective environments. |
| **Zhan et al.** | Experience quality matters; successful histories can still mislead learning. | That low entropy proves good reasoning or that ExGRPO was tested here. |
| **Nintendo's *Super Mario 64*** | Progression rules can be made into falsifiable prerequisite puzzles. | That a classic game supplies RL measurements or validates ten-coin key spawning. |
| **Lucasfilm's *Maniac Mansion*** | Different characters can make different routes and solutions available. | That a proposed multi-agent mansion has been built, played, or scientifically validated. |

**EX0002's justified ending:** A tiny world successfully distinguished a clue-responsive script from a habit-following script using observations and decisions, even when terminal success was identical. The next scientific step, if ever chosen, is a **new** night with a genuinely learned policy or an explicitly counterfactual environment. The current night is closed. Its result needs no rescue, and its future questions impose no debt.

*The door could answer. Whether an agent learns to listen remains an open question.*
