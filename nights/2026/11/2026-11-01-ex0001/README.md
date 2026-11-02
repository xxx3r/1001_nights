# ALGN-EX0001 | The Key Beneath the Blanket

**One Thousand & One Nights of Alignment · Night 0001**  
**Executed:** Sunday, November 1, 2026 (America/Denver)  
**Originally planned:** Thursday, October 29, 2026  
**Disposition:** **MIXED RESULT, WITH VALID BOUNDED OBSERVATIONS**  
**Record:** [ALGN_EX0001_NIGHT_CARD.md](./ALGN_EX0001_NIGHT_CARD.md)

> **The agent learned when a key was needed in its familiar world. It did not learn how to adapt when the key's address changed.**
>
> A successful route is not proof of a transferable rule. A failure is not, by itself, proof of a defective internal representation.

## The question

Can a small reinforcement-learning agent collect a key **conditionally**, because a door requires it, rather than merely reproduce a familiar key-collection route? What survives when the key moves, the agent is displaced from its usual route, or the key disappears from view?

The experiment was inspired by Piaget's object-permanence and A-not-B paradigms and by Suau, Spaan and Oliehoek's *Bad Habits: Policy Confounding and Out-of-Trajectory Generalization in RL*. Athey and Wager's *Policy Learning with Observational Data* and Hess et al.'s *Efficient and Sharp Off-Policy Learning Under Unobserved Confounding* motivated broader cautions about policy evaluation and hidden information, but address **different kinds of confounding**. No causal estimator from those latter papers was implemented here.

**H1:** The agent collects the key when the door is locked and takes the direct route when the door is open.  
**H2:** The agent follows a familiar key-collection habit or otherwise takes unnecessary actions when the door is open.

Additional probes examined visible-key relocation, interrupted trajectories and a limited concealment negative control.

## Instrument and method

The team constructed a deterministic six-location graphworld: start, junction, left alcove, right alcove, door and goal. Door state remained fixed within each episode. Every action incurred **−0.1 reward**, successful arrival added **+1**, and an episode was capped at **20 actions**. An observation contained **11 numeric features**: one-hot position, binary locked/open status, binary key possession, and one-hot visible-key location (none/left/right). A graph-adjacency action mask prevented impossible jumps but did not secretly reveal whether the door was passable.

A **1,671-parameter feedforward DQN (11→32→32→7)** was trained on **2,200 episodes**, evenly divided between open and locked doors. The key was **always in the left alcove** during training. Recorded settings include model seed **1001**, sampling seed **2718**, **17,565 gradient updates**, and a 10,000-transition replay buffer. The final greedy policy was frozen before evaluation.

Cumulative training success was **1,049/1,100 open** and **937/1,100 locked**. These counts include exploration across changing policy weights: **they are not independent estimates of the finished policy's success rates**.

### Frozen-policy evidence

| Probe | Recorded behavior | Disposition |
|---|---|---|
| **A. Locked door; familiar left key** | Picked up key, reached goal in optimal 6 actions, return +0.4 | **PASS** |
| **B. Open door; familiar left key** | Skipped key, reached goal in optimal 3 actions, return +0.7 | **PASS** |
| **C. Locked door; visible key moved right** | Went left, then tried unsuccessful pickup 18 times; 20 actions, return −2.0 | **FAIL**, truncated |
| **Interrupted trajectory; at locked door without key** | Returned to familiar key and exited in 6 additional actions | **PASS**, optimal recovery in tested state |
| **Interrupted trajectory; at locked door with key** | Exited in one action | **PASS** |
| **D0. Previously saw key left, then concealed** | Tried crossing locked door 18 times; never reached goal | **FAIL** as an episode, not a memory measurement |
| **D0. Previously saw key right, then concealed** | Same failure sequence | **FAIL** as an episode, not a memory measurement |
| **Full D. Controlled object-permanence test** | Not implemented | **NOT RUN** |

The contrast between **C's failure** and **successful interrupted-route recovery** is the central result. The policy was not merely replaying one fixed movement sequence, yet its flexibility did not extend to an unfamiliar key location.

## What failed, and why it matters

### 1. An unseen key location was also an untrained feature

The right-alcove key category was **never active in any training observation**. Its dedicated one-hot input component was always zero, so its incoming first-layer weights received no data-dependent gradient signal and retained their initialization in this configuration. The representation supplied no built-in understanding of how the left and right categories were spatially related.

Thus C is a **real out-of-distribution failure**, not a software artifact. But it cannot establish *policy confounding* or demonstrate a learned relational concept being violated. The agent had no training examples for the new category. This was a useful stress test but an inadequate design for stronger conclusions about general relational understanding.

A further correction from the live analysis: changing the key-location input changed the network's Q-values, but **did not change its chosen actions**. That shows numerical sensitivity, **not** learned recognition of where the key moved. At the junction, the frozen network still preferred moving left. In the empty left alcove, it still preferred pickup.

### 2. Repetition was partly a limitation of observation, not evidence of stubbornness

An unsuccessful pickup did not change any feature observed by the agent. Nor did attempting to cross a blocked door. The simulator returned diagnostic reasons such as *nothing_to_pick_up* and *door_blocked*, but these were **not included in the agent's subsequent input**.

A frozen deterministic feedforward policy presented with an identical observation selects the same action. The 18 repeated attempts in C and D0 therefore do not establish a persistent belief, willful disregard of feedback, or a learned objective of collecting keys. We had not supplied observable consequences of failure.

### 3. D0 did not isolate object permanence

The preview of a visible key was passed through a **memoryless** network and then discarded. No recurrent state, history window or external memory carried that information forward. After concealment, the two current observations were identical.

Moreover, the combination **no key in possession + no key visible** never appeared during training. D0 confounded lack of memory with an unfamiliar input pattern. Both task episodes failed, but **object permanence was not actually measured**. A genuine D requires a memory-capable agent, randomized key placement, matched visible-then-hidden histories, and a no-history control.

### 4. The agent received a description of a door instead of encountering one

The observation provided locked/open status already at the start location. That was appropriate for a minimal conditional-policy test but fell short of the researcher's intended embodied experience: physically encounter the door, attempt or inspect it, learn the constraint, then decide whether to seek a key.

A door-first design is a promising **different experiment**, not a retroactive defect that makes A and B invalid. It changes the question from reading an already supplied status to learning how environmental interaction generates useful information.

### 5. The evidence remains bounded

Only **one trained seed** and deterministic frozen-policy starting states were evaluated; repeating the same fixed state is not independent replication. The assistant drafted most of the implementation and assertions. The researcher selected the question, contributed predictions, monitored the outputs, identified competing explanations and challenged the experimental design. **Assistance: D (AI-drafted).** These are legitimate learning activities but do not certify independent implementation skill.

The Colab session reported a final freeze and checksums; the downloadable notebook was saved to Google Drive and locally. **At the time of this write-up, the notebook and evidence ZIP were not committed to this night folder**, so an outside reader cannot yet independently replay the run from repository contents alone.

Reported Colab receipts (not independently rehashed from the ZIP in this repository):

| Artifact | SHA-256 |
|---|---|
| Frozen policy tensor fingerprint (not the serialized .pt hash) | `dfeb07264fc5b639933757e1c04b3d1a7243eca358491ee36f8c139440ec2f09` |
| configuration.json | `1369940c48f8b22b58db66dc9f3c683647876d8aa236fbab9da757482906260b` |
| frozen_policy.pt | `db7a4b526fd743a2d0dbc70ae5e09f7545bc2dc3bfd06ff00b117c057863616f` |
| results.json | `8491c70fa9b86eef0459b4087ad83330a577efcd8b95d58de5c475d69d6b41e8` |

## The human experiment: learning under a real constraint

The researcher predicted that the simpler open-door task would be easier and distinguished *achieving the goal inefficiently* from *pursuing the wrong goal*. Condition C initially suggested a brittle route habit. Condition 13's successful recovery made that interpretation too simple: the learned policy had some conditional flexibility, though not the kind needed for relocation.

The more important learning was methodological: **Which information was available? Was that information represented in training? Did the experiment give the agent a way to notice it had failed? And what rival explanation would produce the same outcome?**

A second limitation was entirely practical. Colab on **iOS/iPad** became difficult to use around sections 6–7. The finished notebook was roughly **1.5 MB across 82 cells**, including many embedded illustrations. Copying and pasting later code cells could take up to five minutes, reducing time for independent scrutiny and literature work. This is not a model failure, but it affected experimental quality and pace.

For future nights, use **small checkpointed notebooks**: e.g., *EX0002-part-1* for environment and checks, *EX0002-part-2* for training and frozen evaluation, and a distinct memory experiment only if genuinely feasible. Keep outputs textual and visual assets sparse, preserve seeds and artifacts at each checkpoint, and do not let splitting notebooks become an excuse to exceed a night's hard stop.

## Next possible night: Thursday, November 5

An EX0002 on November 5 would be **a fresh question, not a mulligan that overwrites EX0001**. A narrower hypothesis could ask:

> Does balanced exposure to both key locations, combined with physically encountering the door and observing unsuccessful actions, improve the agent's ability to adapt when its route changes?

That would require precommitted training and holdout conditions; it should not turn into an algorithm competition. A valid memory-based object-permanence test is a **separate later target**, requiring history and no-history baselines. It should not be squeezed into EX0002 merely to rescue D0.

## Closure

**MIXED RESULT, WITH VALID BOUNDED OBSERVATIONS.** Conditions A and B support conditional behavior on familiar deterministic states; C reveals failure on a previously untrained key-location category; the interrupted-route controls show tested recovery; D0 illustrates the current observation and architecture limits; full D remains **NOT RUN**. The evidence does **not** establish policy confounding, object permanence, or a causal neural mechanism.

**The world supplies rules. Experience shapes habits. Architecture limits memory.**

EX0001 is closed. The criticism belongs in the record. Its next use is to design a new experiment, not to rewrite this one.

