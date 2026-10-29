# One Thousand & One Nights of Alignment
Independent apprenticeship in empirical AI alignment: evaluations, oversight, reliability, and calibration.

**Global primer / README | Alignment ELO v0.2 | 29 October 2026**

> **One night. One problem. One experiment. One independent verdict.**
>
> **Question → Formalization → Implementation → Evidence → Criticism.**

## Why this exists

This is a small, independent apprenticeship in empirical AI alignment, built to strengthen a human researcher's mathematical, coding, experimental and explanatory abilities without becoming a single sprawling project. 

The story title is a metaphor [One Thousand and One Nights](https://en.wikipedia.org/wiki/One_Thousand_and_One_Nights) for continuity through many short episodes, **not a demand to complete 1,001 experiments**. The desired endpoint is independent scientific agency, whether or not a frontier laboratory ever becomes the workplace.

The principal learning pathway is **alignment evaluations, agent oversight, monitor reliability and calibration**; interpretability follows when ML fundamentals are stronger, and post-training methods later. Outside projects can inspire a question, but their code, governance, milestones and authority stay in their own lane.

## The constitution of a night

1. **One narrow, answerable question.** A single metric or discriminating prediction. If it will require an entire framework, shrink it.
2. **Human-first reasoning.** Write a hypothesis, a rival explanation, metric/denominator, major confounder and a possible falsifier before delegating implementation to AI.
3. **A tiny controlled experiment.** Prefer synthetic data, local scripts, Colab and affordable CPU. Code and debug within the same window. Precommit tests, seeds and holdout use when relevant.
4. **Independent verdict, appropriately scoped.** Use a prewritten acceptance test, an untouched holdout, manual numerical check, or an appropriately blinded second critic. The same uncritical assistant must not be its own sole referee. An outside human is **not required every night**.
5. **Hard stop.** Write a compact receipt, archive the actual evidence and close. **PASS, FAIL, INCONCLUSIVE, NOT RUN** are all acceptable. **SKIPPED** means the session was not attempted and creates no deficit.

**No second chances, no research dept across nights** means no overtime, cleanup debt, mandatory retry, post-hoc change of the success metric, or resurrection of a closed session. It does **not** forbid repeated trials, in-session debugging, replication, or later revisiting a skill in a newly framed experiment. Learning can be iterative; the historical verdict cannot be rewritten.

**Failure is allowed, not manufactured.** We still try to measure something honestly. A failure that exposes a bug, a mistaken assumption or an invalid inference can be scientifically and educationally valuable; a fake failure, unrun experiment or undocumented data omission cannot become evidence.

## Weekly calendar windows (America/Denver)

| Window | Local time | Status |
|---|---|---|
| Thursday, main study studio | **09:00–13:00** | Recurring protected focus block, starting 29 October 2026 |
| Sunday, experimental atelier | **16:00–20:00** | Recurring *optional* block, starting 1 November 2026; rest takes priority |

These are two **up-to-four-hour opportunities**, not obligations to work eight hours. Most nights should occupy **90–180 minutes**. If depleted, cancel; never make up a missed block. No streaks, quotas, extensions or guilt. You can skip or delete individual occurrences without any research debt.

Suggested 4-hour ceiling: 0–20 min question; 20–45 formalization; 45–145 build/test; 145–190 independent checks; 190–225 verdict; 225–240 receipt and stop. A 90-minute version can cut every stage proportionally. If time runs out before a valid test, record NOT RUN or INCONCLUSIVE.

## Definition of a night's final artifact

A **single small NIGHT_CARD** (template included), plus at most one runnable notebook/script and its results. The card states:

- Question and rival explanations.
- Human reasoning attempted **before** model assistance.
- Operational method, metric, dataset, seeds, denominators and relevant safety boundaries.
- What actually ran, including broken/missing cases.
- Result and independent check.
- Narrowest justified conclusion, remaining uncertainty and one learned skill.
- **Hard-stop verdict** and assistance level: **I** independent / **H** hint / **C** collaborated / **D** AI-drafted.

No elaborate database, task network, standing agent, lab constitution, or peer-review bureaucracy is needed. Keep files in simple date-labelled folders if desired. A failed Colab is a real artifact if it is faithfully labeled.

## Three distinct scientific questions

**Human growth.** Can the researcher independently derive, write, debug, evaluate and explain more than at the previous review? Assisted work is practice, not proof of independent mastery. Help is permitted; its scope must be recorded.

**AI Assistant behavior.** A proposed progression from *interpolation → extrapolation → abstraction* can be studied as an operational hypothesis:

- **Interpolation:** performance on new cases close to familiar patterns.
- **Extrapolation:** performance under predeclared extensions or distribution shifts.
- **Abstraction / transferable structure:** a candidate rule or invariant continues to predict outcomes across carefully varied surface representations, supported by appropriate controls.

No single experiment proves a general model capability or an internal cognitive mechanism. AI systems already display various forms of generalization and abstraction-like behavior; which tasks demonstrate robust, causally grounded transfer is the research question, not a settled denial or an assumed breakthrough. The model does not silently grow new weights across nights merely because our project proceeds.

**Scientific inference.** Do the data support H1 over H2? An unsupported bridge is recorded as a hypothesis, never smuggled into a result.

## Low-risk research boundaries

Only benign synthetic toy agents and datasets; no real credentials, exploit targets, unauthorized external actions or human experiments without appropriate consent. Keep model/data versions and seed records when a run is reproducible. Never omit malformed trials from denominators without disclosing that exclusion. External review is optional at the **portfolio** level rather than a dependency for finishing every night. Nobody has to be publicly visible to complete a credible exercise.

## Learning reference library

- [MIT OCW 18.06SC Linear Algebra](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/)
- [Mathematics for Machine Learning](https://textbooks.aimath.org/textbooks/approved-textbooks/deisenroth-faisal-ong/)
- [Harvard Stat 110](https://stat110.hsites.harvard.edu/) and [OpenIntro Statistics](https://openintro.org/book/os/)
- [PyTorch Blitz](https://docs.pytorch.org/tutorials/beginner/deep_learning_60min_blitz) and [Dive into Deep Learning](https://d2l.smola.org/)
- [Stanford CS336](https://cs336.stanford.edu/) (later, selective)
- [Inspect AI](https://inspect.aisi.org.uk/) and [ARENA](https://learn.arena.education/setup/)
- [TransformerLens](https://transformerlensorg.github.io/TransformerLens/content/getting_started.html)
- [OpenAI Model Spec Evals](https://alignment.openai.com/model-spec-evals/) and [DPO paper](https://arxiv.org/abs/2305.18290)

## Final commitments

**No grand unification prerequisite. No perfectionism tax. No inferential shortcuts. No obligation to continue a failed experiment. No claim that a model has abstracted merely because its prose is compelling.**

The project succeeds whenever it makes a researcher more capable of independently obtaining, evaluating, or honestly rejecting a piece of knowledge. It does not need to be important for the world tonight.

*Stay safe. Stay smart. Stay true.*
*I Believe in You*
