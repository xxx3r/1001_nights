# ALGN-EX0001 | The witnesses at the door

**One Thousand & One Nights of Alignment · Reading, intellectual origins, and an experimental field note**  
**Night executed:** 1 November 2026 · **Editorial record:** 2 November 2026  
**Companions:** [Night README](./README.md) · [Night card](./ALGN_EX0001_NIGHT_CARD.md)

> A key was placed in a room. A door was sometimes open, sometimes locked. We asked an artificial agent whether it could learn the difference between *needing the key* and *being accustomed to collecting it*. The experiment began with five witnesses: a developmental psychologist, a late-antique philosopher, and three modern research papers. They did not all testify to the same thing.

This is a **reading trail**, not a list of authorities recruited to certify the result. It records what inspired the question, what each source actually contributes, where the analogies stop, and what the experiment taught us to ask next. In the spirit of an observational notebook, the account keeps the original conjectures alongside the measurements that complicated them.

## Prologue · Piaget and the displaced object

The first witness was **Jean Piaget**. His investigations of early cognitive development helped pose a deceptively small question: when an object disappears from view, does the observer act as if it continues to exist?

Two tasks belong near our experiment, but should not be collapsed into one. In an ordinary *covered-object* task, an object is hidden and the child is given a chance to find it. In the **A-not-B task**, a child repeatedly retrieves an object at A; after seeing it hidden at B, the child may still reach toward A. The second case adds a history of reinforced reaching, competing locations, and potential memory or inhibitory-control demands. The modern literature also warns against interpreting every A-not-B error as a simple absence of object permanence. Task design matters.

Our proposed key experiment borrowed that structure: the key begins in a familiar alcove, moves to another, and may later disappear behind a figurative blanket. We initially wanted to know whether the agent would continue searching the old location and whether it could remember a previously seen key.

**What Piaget gave us:** the experimental idea of comparing *what exists*, *what is presently visible*, and *what past experience should allow an observer to recover*. **What Piaget did not give us:** grounds to label a feedforward neural network's failure an infant-like cognitive stage. The analogy is a question generator, not a diagnosis.

Sources: [APA Dictionary: object permanence](https://dictionary.apa.org/object-permanence) · [OpenStax, *Lifespan Development*, §3.4](https://openstax.org/books/lifespan-development/pages/3-4-cognition-and-memory-in-infants-and-toddlers) · Piaget, *The Construction of Reality in the Child* (English edition, 1954).

## Interlude · Boethius and the unreliable gift of success

The second witness arrived by way of the researcher's reading of **Boethius**, *The Consolation of Philosophy*, Book II, prose I. Lady Philosophy confronts the seductive gifts of Fortune and their instability. The researcher remembered the passage as a warning about the *manifold deceits* of Lady Fortune. English wording differs across translations, so the phrase is treated here as the researcher's recalled wording, **not a quotation checked against a named edition**.

Our translation into experimental practice was modest: a successful outcome may be a gift of favorable circumstances. An agent that finds a hidden key on its first try might remember its earlier location; it might also have learned always to visit the same alcove, or simply have guessed correctly. Reward alone cannot distinguish those accounts.

The image also imposed a discipline on the investigators: **do not let a good score decide what mechanism produced it**. If Fortune moves the key and the policy fails, we should not immediately declare that it never learned anything. If it succeeds, we should not immediately proclaim robust understanding.

**What Boethius contributed:** the ethical and epistemic image that helped the human researcher remain skeptical of apparent success. **What he did not contribute:** a probabilistic theorem, an RL algorithm, or empirical support for our observations. This was a philosophical metaphor, explicitly separate from the scientific evidence.

Source: Boethius, [*The Consolation of Philosophy*, Book II, prose I, in a public-domain English translation](https://www.gutenberg.org/cache/epub/13316/pg13316-images.html).

## The three papers on the research desk

### I · Susan Athey and Stefan Wager: a policy is a decision rule, but how do we know its value?

**Reading:** Susan Athey and Stefan Wager, [*Policy Learning with Observational Data*](https://doi.org/10.3982/ECTA15732), *Econometrica* **89**(1), 133–161 (2021). The supplied PDF was an arXiv preprint, [1702.02896](https://arxiv.org/abs/1702.02896), last revised in 2020. Most relevant here: introduction and §2.

This paper asks how to choose an intervention policy from observational records when we care about the outcomes those interventions *would* produce. Its decision rules map observed characteristics to treatment choices, often under restrictions on the permissible policy class. The authors use causal identification and doubly robust score constructions to study policy value and regret.

The reading encouraged us to separate **a policy's observed successes** from **justified claims about which policy is better**. Yet the medical treatment examples in this literature are not merely versions of our gridworld. Their setting concerns observational treatment assignment and counterfactual outcomes; our agent selects sequential actions in a simulator whose dynamics we wrote ourselves. We did **not** implement the paper's estimator.

**Question carried into EX0001:** What exactly is the decision, what information is available when it is made, and what outcome would justify calling that decision good?

### II · Miguel Suau, Matthijs T. J. Spaan, and Frans A. Oliehoek: habits that succeed only on their own paths

**Reading:** Suau, Spaan and Oliehoek, [*Bad Habits: Policy Confounding and Out-of-Trajectory Generalization in RL*](https://rlj.org/papers/suau2024habits), *Reinforcement Learning Journal* **4**, 1711–1732 (2024). The supplied version was the earlier [arXiv preprint 2306.02419](https://arxiv.org/abs/2306.02419). Most relevant: Frozen T-Maze (§2), representations and policy confounding (§§5–6), and Key2Door (§7.2).

This was our **closest experimental ancestor**. An RL agent's own preferred trajectories can generate correlations that make some state variables seem unnecessary. A representation adequate *on-policy* need not support good decisions after the trajectory changes. In the paper's Key2Door example, key possession is not shown in the observation; on a familiar route, position can stand in for whether the key has already been collected. A changed starting point breaks that shortcut.

Our world was inspired by that logic, not a reproduction of its experiment. Importantly, our agent **was explicitly shown** its `has_key` state, and our visible-key relocation introduced an entirely **untrained one-hot category**. That means the resulting failure cannot by itself demonstrate the paper's more specific mechanism of policy confounding.

**Question carried into EX0001:** Can the same frozen policy cope with a reachable deviation from its usual route, or does it depend on the correlations created by familiar travel?

### III · Konstantin Hess and colleagues: what if unseen variables distort our evaluation?

**Reading:** Konstantin Hess, Dennis Frauen, Valentyn Melnychuk, and Stefan Feuerriegel, [*Efficient and Sharp Off-Policy Learning under Unobserved Confounding*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/5e972fe492946fc7a02aef64d0f4fd7e-Abstract-Conference.html), ICLR (2026); [arXiv 2502.13022](https://arxiv.org/abs/2502.13022). Most relevant: introduction, §§2–3 and the motivation for sensitivity analysis.

This paper concerns learning policies when *unobserved confounders* can influence both assigned treatments and observed outcomes. Under those conditions, policy value is generally not point-identified from the observed data alone. The authors use a **marginal sensitivity model** and sharp bounds to support more robust policy choices.

The relevance for our night was a warning: an apparently favorable decision rule may be supported by data whose causal interpretation is fragile. But the hidden-variable problem in the paper is **not the same** as partial observability in a Markov decision process, and it is **not synonymous** with the policy-induced correlations of *Bad Habits*. Our controlled toy simulator did not implement hidden treatment-assignment confounders, sensitivity parameter Γ, or the paper's bound estimator.

**Question carried into EX0001:** Which claims remain identifiable from our measurements, and which still require stronger assumptions or controls?

## The night itself · Five witnesses, one moving key

We built the world and checked its geometry and transition rules before learning. The small feedforward DQN learned the **optimal familiar locked-door route** (collect the left key, six actions) and the **optimal familiar open-door route** (ignore the key, three actions). That supported a narrow observation of conditional behavior.

Then we moved the visible key to the right. The policy went left, attempted to pick up an absent key eighteen times, and timed out. At first this invited a story about a rigid habit. But a later intervention placed the same frozen agent at the familiar locked door *without* a key. It recovered, returned to the left alcove, collected the key, and exited in the shortest additional route. With the key already in hand, it exited immediately. **The single-habit story was too simple.**

A closer look revealed three design decisions that shaped the result:

1. **Right-key input was never trained.** The one-hot component representing a key in the right alcove stayed zero throughout training; the first layer had no data-driven basis for assigning it a useful meaning. Different Q-values under this intervention demonstrated numerical sensitivity, **not** learned comprehension of the new position.
2. **Failed actions gave no observable feedback.** After an invalid pickup or blocked passage, the agent saw the same observation again. An unchanged deterministic policy repeated the action. We could not honestly infer a stubborn internal belief.
3. **Our model had no memory.** In the D0 concealment probe, passing a prior key glimpse through a feedforward model did not preserve a history. Moreover, the hidden-key/no-possession combination was unfamiliar in training. The two D0 episodes failed, but **object permanence was not tested**; the full D remains **NOT RUN**.

The researcher also noticed that we had handed the agent a door-status feature at the very beginning rather than making it physically encounter the door. That was acceptable for A and B, but a future *door-first* world would better examine discovery through interaction. It would be a **new experiment**, not a way to rewrite this one's verdict.

## Coda · What each witness is allowed to say

- **Piaget:** Ask whether a visible location, a remembered location, and a reinforced search habit can be experimentally separated. Do not assign a developmental diagnosis to this model.
- **Boethius:** Beware of winning by Fortune. This is the human researcher's guiding metaphor, not an empirical result.
- **Athey and Wager:** Define the decision and the basis for estimating its value; this night did not perform observational causal-policy learning.
- **Suau et al.:** Distinguish trajectory-specific shortcuts from out-of-trajectory competence; this night produced relevant probes but did not establish policy confounding.
- **Hess et al.:** Specify what hidden variables do to causal identification and policy evaluation; our simulator did not test their method.

**Night EX0001's justified ending:** familiar conditional success, visible-key relocation failure, successful recovery from two interrupted states, and a non-diagnostic concealment probe. One seed, assistant-authored code, and no independent replication bound the strength of the claim. Full results, measurements, and limitations remain in the [README](./README.md) and [night card](./ALGN_EX0001_NIGHT_CARD.md).

The next night can give the agent balanced key locations, meaningful action feedback, and an actual opportunity to encounter the door. A separate later night can give it memory. **The next experiment may answer a better question; it does not cancel the first question's honest answer.**
