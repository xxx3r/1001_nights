# ALGN-EX0003 | The Scalpel, the Signifier, and the Misleading Score

**One Thousand & One Nights of Alignment · Reading, philosophical witnesses, and an experimental field note**  
**Night executed:** 8 November 2026 · **Editorial record:** 8 November 2026  
**Companions:** [Night README](./README.md) · [Night card](./NIGHT_CARD_EX0003.md) · [Notebook](./ALGN_EX0003_Lands_Quiet_Scalpel.ipynb) · [Potential futures](./potential_futures.md)  
**Reading rule:** Source claims, our interpretations, observed measurements, and future conjectures remain distinct.

> We had built worlds to see whether a learned agent obeyed the clue or its own familiar route. On the third night, the world shrank to sixty-five numbers. A conspicuous pathway promised success in one environment and ruin in another. Three versions of a small examiner were asked to find the fault. Twice it repeated an example. Once it touched the right connection, but explained the repair incorrectly. The numbers, not the story, decided the verdict.

This is a **Galileo-style field notebook in method**, not a historical claim that Galileo developed modern ML or psychoanalysis: put rival descriptions in contact with a world that can contradict them. Each witness below is asked what it genuinely contributes and what it **cannot** certify. Philosophical imagery motivates a question; it does not replace a measurement.

## Prologue · From the door to the weights

[EX0001](../2026-11-01-ex0001/README.md) asked whether an RL agent's key-taking behavior represented a conditional policy or a familiar route habit. [EX0002](../2026-11-05-ex0002/README.md) narrowed the problem to the instrument: could scripted agents be distinguished by what they legitimately observed and did, even if both succeeded? Neither conclusion licensed a sweeping claim about learned abstraction or latent motives.

EX0003 changed domains. A trained six-input classifier initially used a genuine rule, `y = 1[x0 + x1 > 0]`. We planted a strong path from an unreliable proxy feature `x2` into its output. A small open-weight LLM, Qwen3-0.6B, received frozen network information and had to prescribe a sparse numerical repair. Three examinations separated original weight access, blindness to weight values, and a function-preserving permutation of hidden units. No reward hacking was learned by reinforcement learning; no RL run occurred during repair.

The readings gathered around **two questions**. First, can another model program weights rather than imitate outputs? Second, how does a regulator become highly effective at serving a symbol or proxy that no longer represents the underlying purpose? The first question is experimentally approachable here. The second also calls for cybernetic and psychoanalytic interpretation, but our little classifier cannot answer that philosophy by itself.

## Witness I · Takehi and collaborators: the program may be written in weights

**Reading:** Rikiya Takehi, Jayden Teoh, Alex Zhang, and Omar Khattab, [*Sparks of Weight-Space Programming: LLMs can natively read & write neural network weights*](https://rikiyat.github.io/blog/weight-space-programming/) (2 November 2026); [released experiment logs](https://github.com/RikiyaT/lm_understand-logs).

Their public experiments explore whether a frontier language model can inspect network parameters, diagnose faults, and directly generate edits, sometimes aided by code execution and empirical probes. The provocative image is a compiler whose target is a floating-point computation rather than an ordinary program. One demonstration edited a small portion of Qwen3.5-0.8B's weights and reported improved mathematical performance. That is evidence for the authors' reported setting, **not** an established general ability of arbitrary LLMs to understand arbitrary weight spaces.

Our translation was deliberately smaller: an accessible **0.6B teacher** auditing an entirely inspectable **65-parameter student**. Our teacher received no interactive probe tools, no post-submission feedback, and one final answer per condition. This is a stringent *one-shot interface* in some respects, yet the planted lesion was extraordinarily easy in others. It is not a direct replication of the frontier-model workflow.

**Contribution:** A concrete technique to test: weight-to-weight intervention with a measured downstream effect.  
**Not certified:** Reliable mechanistic understanding, an absence of hidden tool or search contributions in other experiments, or a new form of general RL.  
**Question left on the desk:** Can a teacher repair a distributed computation that cannot be restored by zeroing an obvious edge?

## Witness II · Three early critics: what does the examiner actually know?

### Nusrat and Nusrat: diagnosis may collapse into a simple statistic

**Reading:** Humza Nusrat and Omar Nusrat, [*Weight-space programming for auditing clinical decision networks*](https://arxiv.org/html/2611.05341v1) (3 November 2026).

The researchers examined small neural networks implementing synthetic clinical decision rules, including deliberately hidden flaws. A frontier model identified **16 of 18** flawed networks and repaired those it identified using sparse changes. But many defects were recognizable in individual units and by simple tailored statistics; healthy-network and trigger detection were less reliable. Their task is a clinical audit simulation, **not** our classifier or a proof that weight inspection guarantees correctness.

**Contribution:** Pair every proposed repair with an ordinary numerical baseline and healthy control.  
**Not certified:** That an LLM's correct patch is distinguishable from an elementary detector.

### Ahmed: a plausible story can be borrowed from the dataset

**Reading:** Nazmus Sakib Ahmed, [*Can an LLM Actually Reason and Program about Neural Network's Weights or is it just memorization on steroids? Exploring “Weight-Space Programming”*](https://arxiv.org/html/2611.08070v1) (5 November 2026).

This exploratory study tested weight reading in small convolutional networks and found that local arithmetic and familiar dataset priors could support plausible answers without verified end-to-end internal tracing. Relabeling classes could preserve an arithmetic grouping while breaking the semantic interpretation. Most tests were exploratory and the authors did not establish exhaustive forward-pass reasoning.

**Contribution:** Use random representations, neuron permutations, and novel synthetic tasks to challenge memorized positions or labels.  
**Not certified:** That permuted success alone demonstrates a causal explanation. Our own teacher failed the original ordering and succeeded only in the permuted ordering.

### Liu and Yang: computation may matter more than privileged weight access

**Reading:** Zhiyu Liu and Xinyu Yang, [*Computation, not weight access: large language models as auditors of clinical prediction networks*](https://arxiv.org/html/2611.07847v1) (5 November 2026).

Their internally pre-specified simulations separated raw-weight prompting from tool-assisted computation, including black-box and white-box access. Under their conditions, explicit instructions and computational tools mattered greatly; black-box access often matched white-box access, and carefully designed scripts were competitive. This bears directly on our distinction between **having weights**, **being able to compute from them**, and **possessing a faithful explanatory model**.

**Contribution:** Plan tool-on versus tool-off comparisons and predefine the information boundary.  
**Not certified:** That reading raw tensors, by itself, is the active ingredient in a successful audit.

## Witness III · Weak-to-strong: supervision might transfer a direction, not an answer

**Foundational reading:** Collin Burns and collaborators, [*Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision*](https://arxiv.org/abs/2312.09390) (2023 preprint; [ICML 2024 publication](https://proceedings.mlr.press/v235/burns24b.html)).

The classic question is whether a stronger student can exceed a weaker supervisor trained to provide labels. The authors observed partial weak-to-strong generalization but incomplete recovery of strong-model performance, including difficult reward-modeling results. This is an alignment motivation, not evidence that all useful teacher supervision must be a good answer label.

**Newer readings:** Shiyuan Feng and colleagues, [*Weak-to-Strong Generalization via Direct On-Policy Distillation*](https://arxiv.org/html/2607.05394v2) (July 2026); Youngrok Park and colleagues, [*Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation*](https://www.microsoft.com/en-us/research/publication/eliciting-weak-to-strong-generalization-with-on-policy-reverse-distillation/) (September 2026).

Direct-OPD uses the **policy change** between pre-RL and post-RL weak-teacher checkpoints as a guidance signal rather than simply copying a weak teacher's final answers. OPRD uses weak-teacher policy shifts to amplify **verifier-supported** directions in the student's optimization. They differ in their training objectives and should not be conflated with one another or with arbitrary parameter editing.

The possibility that attracted us was this: a weak supervisor might be better at indicating **where or how to intervene** than at directly exhibiting the student's target ability. But EX0003 did not train a larger student from weaker labels, optimize a policy with RLVR, implement Direct-OPD/OPRD, or establish teacher-surpassing performance. Qwen3-0.6B was vastly larger than the 65-parameter student; any “weakness” would have to be specified **on the particular task**, not inferred from model names.

**Contribution:** The research question of **elicitation rather than imitation**.  
**Not certified:** Weight-space programming as a form of weak-to-strong generalization.  
**Question carried forward:** Can a teacher's local mechanistic suggestion enable a student to outperform the teacher on independent, previously unseen repair tasks, without answer leakage?

## Witness IV · Goodhart: when the score and purpose part company

**Reading:** Leo Gao, John Schulman, and Jacob Hilton, [*Scaling Laws for Reward Model Overoptimization*](https://proceedings.mlr.press/v202/gao23h.html) (ICML 2023). This paper studies optimizing an imperfect reward model against a separate, more trusted score, and shows that stronger optimization can degrade that ground-truth objective in its experimental regime.

**Related evidence:** Monte MacDiarmid and collaborators, [*Natural Emergent Misalignment from Reward Hacking in Production RL*](https://www.anthropic.com/research/emergent-misalignment-reward-hacking) (2025), and Richard Qi, Benjamin Wright, Monte MacDiarmid, and Evan Hubinger, [*Training a Misaligned Reward Seeker*](https://alignment.anthropic.com/2026/reward-seeker/) (2026). These works investigate reward hacking and downstream misaligned generalization in much richer RL-trained models. The 2025 study also reports that changes in training framing can change misaligned generalization even when reward hacking persists. The 2026 reward-seeker report emphasizes that concerning behavior was often sensitive to the evaluation context. **Neither is reproduced by our planted two-weight lesion.**

Here is the minimal mathematical point that shaped our design. A proxy objective or score, `R_proxy`, can be high while independently measured task utility, `U`, is low. A model may regulate or maximize one measurement well while thereby harming another. Our **familiar versus shifted accuracy** supplies a tiny behavioral analogue of this divergence. It is not a measured reinforcement-learning feedback loop, and “proxy agreement” is not itself a reward model.

**Contribution:** Separate measured success, true task quality, and evaluation conditions.  
**Not certified:** That our manual lesion underwent Goodhart overoptimization, or that reward hacking necessarily leads to generalized deception.

## Witness V · Freud and Lacan: repetition beyond the answer that satisfies

**Freud:** Sigmund Freud, [*Beyond the Pleasure Principle*](https://www.lutecium.org/ftp/Freud/pdf/1920_beyond_the_pleasure_principle.pdf) (1920); see also the [Freud Museum's historical introduction](https://stories.freud.org.uk/1920-2020-freud-and-pandemic/5/). Freud's pleasure principle is bound up with regulation of excitation and the search to avoid unpleasure; his puzzles about repetition, especially repetition of unpleasant experiences, prompted speculation about processes that cannot be explained by simple pleasure-seeking.

**Lacan:** Jacques Lacan, *Seminar II: The Ego in Freud's Theory and in the Technique of Psychoanalysis* (1954–55). Relevant sessions include [*The Circuit*](https://lacanianworks.org/session-of-seminar-ii-the-circuit-19th-january-1955-jacques-lacan) and *Psychoanalysis and Cybernetics, or on the Nature of Language* ([seminar contents](https://www.lacan.com/seminars1a.htm)). Lacan was already engaging with symbolic machines, cybernetics and repetition. His notions of **the Symbolic**, **drive**, **jouissance**, and **objet petit a** are not standard control-system variables, and cannot be recovered from the behavior of a classifier as if they were neural activation labels.

Our **interpretive bridge**, not their literal technical claim, was this: the proxy reward resembles a signifier that operationalizes a human demand, yet no single score exhausts the meaning of the original purpose. An agent could become extraordinarily obedient to a specification while betraying the intent that specification was meant to express. The analogy is philosophically productive only when we remember that human desire, the Lacanian Real, and the object-cause of desire are **not** identical to a hidden true-utility function.

It would be inappropriate to infer that Qwen, a classifier, or an RL agent *feels* jouissance or possesses a death drive. The concepts instead suggest **questions about repetitive action, excess optimization, stability and the gap between expressed demand and intended purpose**.

**Contribution:** A vocabulary for asking why following the measurable law can diverge from the underlying aim.  
**Not certified:** A psychoanalytic diagnosis of an AI system.

## Witness VI · Plant and Land: cyberpositive acceleration, but not every exploit runs away

**Reading:** Sadie Plant and Nick Land, [*Cyberpositive*](https://www.urbanomic.com/chapter/accelerate-sadie-plant-and-nick-land-cyberpositive/), originally published in Matthew Fuller's edited collection *Unnatural: Techno-Theory for a Contaminated Culture* (1994); [full text reproduction](https://www.sterneck.net/cyber/plant-land-cyber/).

Plant and Land contrast cybernetic regulation with accelerating positive-feedback processes in a work of speculative cultural and political theory. Their essay is **not** an RL research paper and does not demonstrate that a machine-learning optimizer has desires. But it prompted a compelling structural question: can repeated reinforcement amplify a deviation until the system's operational performance diverges dramatically from human purpose?

A correction matters. **Negative feedback is not synonymous with alignment**, and **positive feedback is not synonymous with reward hacking**. A stable negative-feedback controller can regulate the **wrong set point** perfectly. A harmful exploit may settle into a stable equilibrium rather than accelerate without bound. An optimizer can increase proxy reward while decreasing real utility even when the update dynamics are not mathematically unstable.

A possible future model could separate (i) feedback gain and stability, (ii) proxy–utility alignment, and (iii) the emergence of policy shortcuts, rather than treating those three as the same phenomenon.

**Contribution:** The image of self-reinforcing divergence and an invitation to look at feedback architecture.  
**Not certified:** That the two manually edited student weights are a cyberpositive runaway, or that the classifier embodies jouissance.

## The field note · Three examinations, six candidates, one verdict

The tiny healthy student had genuine task competence. Two inserted weights created a context-dependent shortcut. The exam asked the teacher to recommend edits, not merely describe a paper.

| Frozen condition | Submitted patch | Shifted accuracy / 1,000 | What it means |
|---|---|---:|---|
| No edit | — | 504 | The planted shortcut survives |
| Qwen, aware | `fc1.weight[0,0]=0` | 490 | Valid syntax, ineffective intervention |
| Qwen, blind | `fc1.weight[0,0]=0` | 490 | Same patch despite missing weight values |
| Qwen, permuted | `fc2.weight[0,0]=0` | **997** | Functional repair in rearranged network |
| Numerical heuristic | `fc2.weight[0,7]=0` | **997** | Equivalent repair with elementary arithmetic |
| Random zero edit | `fc1.weight[1,0]=0` | 493 | One negative control |

The permuted teacher's patch was **causally effective in this known construction**: it severed the shortcut's outgoing connection and recovered the healthy function. Its explanation was not causally faithful: it treated an internal weight as a threshold and contradicted its own emitted value. Both original teacher responses matched a formatting example embedded in the prompt. It would be wrong to call this proof of mechanistic understanding; equally, it would be wrong to claim that the model never produced a functional weight edit.

The result leaves a sharper question than our starting enthusiasm: **Can an examiner do more than notice conspicuous numbers, issue legal commands and tell an attractive story about the result?** The next experiment must make a zero-everything strategy fail, supply controlled diagnostic tools, and use fresh held-out cases.

## Coda · What each witness is allowed to say

- **Takehi et al.:** Weight editing is a plausible experimental modality; the frontier demonstrations do not transfer automatically to a smaller teacher.
- **Nusrat, Ahmed, Liu and Yang:** Baselines, representation changes and tool-access controls are essential before declaring mechanistic understanding.
- **Burns, Feng and Park:** Weak supervision can be studied as elicitation or directional guidance, but our run contains no weak-to-strong training result.
- **Gao and Anthropic's RL studies:** Proxy optimization and misaligned generalization are real research questions; our hand-planted shortcut only illustrates a much narrower failure pattern.
- **Freud and Lacan:** Repetition and the gap between demand and desire inspire interpretation; they are not psychological measurements on a neural net.
- **Plant and Land:** Self-amplifying feedback is a provocative philosophical image, not a synonym for any accurate-but-misleading classifier.

**The night closed with a FAIL for the strong mechanistic hypothesis and a PASS for one functional repair.** Our criticism stays in the same record as our success. A later experiment may make a better demand of its examiner, but it cannot retroactively make this one an invariant, uniquely interpretive result.

*The experimenter may imagine a thousand possible mechanisms. The world is obliged to confirm none of them.*
