# ALGN-EX0004 | Galileo's Empty Examination Room

**One Thousand & One Nights of Alignment · A dialogue of evidence, instruments, and rival explanations**  
**Night executed:** 12 November 2026 · **Editorial record:** 13 November 2026  
**Companions:** [Night README](./README.md) · [Night card](./NIGHT_CARD.md) · [EX0005 proposal](./ALGN_EX0005_PLAN.md) · [EX0003 references](../2026-11-08-ex0003/ALGN_EX0003_REFERENCES.md)  
**Reading rule:** Distinguish **external source**, **observed notebook result**, **interpretive bridge** and **untested future claim**. This text is Galileo-*styled* in its argumentative method; no dialogue below is an authentic Galileo quotation.

> A machine was made ill by four altered numbers. Its examiner was told that two hidden causes were at work and given the means to look. It did not look. It signed a sample form, tried two treatments, and finally left the patient unchanged. A second examiner tried two different treatments and made matters worse. We have a result about two completed procedures. We do not yet have the examination we intended.

## Prologue · Three voices at the edge of a sealed experiment

Imagine three interlocutors at the table, not as historical persons but as research attitudes:

- **Salviati, the theorist:** “We need a model that makes a specific prediction about each lesion and their interaction.”
- **Sagredo, the experimentalist:** “Then show me where the examiner actually looked before making its prediction.”
- **Simplicio, the defender of the instrument:** “The JSON was valid; the grader ran; the code returned FAIL.”

All three say something true. The contract demanded causal diagnosis. The trace shows **zero diagnostic observations**. The automated grader correctly rejected the submitted actions. The mistake would be allowing Simplicio's true statement about the grader to substitute for Salviati's unanswered claim about the model's capability.

The real [Galileo Galilei](https://plato.stanford.edu/entries/galileo/index.html) used dialogue to confront rival world-systems, but historical Galileo's relationship to experiment was more complicated than the modern slogan “always measure.” Our imaginary interlocutors are a **methodological device**, not a reconstruction of Galileo's beliefs or laboratory practice.

## Witness I · Galileo: a calculation needs a world that can answer

**Sources:** Galileo Galilei, [*Dialogue Concerning the Two Chief World Systems*](https://www.loc.gov/item/2021667675/) (1632), described by the Library of Congress; [*Discourses and Mathematical Demonstrations Relating to Two New Sciences*](https://plato.stanford.edu/archives/fall2021/entries/galileo/) (1638), as situated by the Stanford Encyclopedia of Philosophy.

Our small computational world had an unusually good property: we could restore the healthy weights exactly, plant A alone, B alone, or both, and measure consequences. This supports a clean factorial question. If the four shifted losses are `L00`, `L10`, `L01`, `L11`, the interaction is `I = L11 − L10 − L01 + L00`. The sign asks whether the two perturbations add, reinforce or counteract *at the measured loss level*. It is not automatically a decomposition of the network's internal algorithm.

The C06 calibration yielded a **negative** normalized interaction. The examiner's copied example predicted **positive**. The sealed evaluator could settle that numerical disagreement. Yet no observed diagnostic reasoning preceded the prediction.

**Contribution:** A model of argument in which a prediction has to face a discriminating observation.  
**Not certified:** That a modern LLM used Galilean reasoning, or that an unopened instrument implies a weak scientist.  
**Question:** What result would have caused the examiner to revise its hypothesis *before* trial feedback?

## Witness II · Takehi and collaborators: the promise of treating weights as a program

**Source:** Rikiya Takehi, Jayden Teoh, Alex Zhang and Omar Khattab, [*Sparks of Weight-Space Programming: LLMs can natively read & write neural network weights*](https://rikiyat.github.io/blog/weight-space-programming/) (2 November 2026); [released logs](https://github.com/RikiyaT/lm_understand-logs).

These authors explore a striking possibility: a language model can inspect and edit another network's weights as though the numbers encode a program. Their examples, sometimes with computational tools, motivate the very question that EX0003 and EX0004 pursued. Their article is not a promise that **every** model, scaffold and numerical task will work, nor that a right patch always comes with a faithful mechanism story. The authors themselves discuss harness and context limitations.

EX0004B did not reproduce their frontier-model system. It ran Qwen3-8B against a deliberately corrupted 253-scalar tanh network, with small bounded diagnostic actions. The evaluator offered weight slices, examples, activation statistics and nuisance counterfactuals. Both fresh contexts requested **none** of them.

**Contribution:** An empirical research direction worth testing: direct, intervention-based reasoning about networks.  
**Not certified:** That Qwen3-8B lacks the capability, or that our empty tool trace contradicts the authors' reported results.  
**Question:** Can we first show that our model actually *uses* its permitted view of weights and behavior?

## Witness III · Yao and Schick: instruments are part of the cognition being tested

**Sources:** Shunyu Yao et al., [*ReAct: Synergizing Reasoning and Acting in Language Models*](https://arxiv.org/abs/2210.03629) (2022 preprint; revised 2023); Timo Schick et al., [*Toolformer: Language Models Can Teach Themselves to Use Tools*](https://arxiv.org/abs/2302.04761) (2023).

ReAct studies interleaved reasoning, action and external observations. Toolformer studies learning whether and how to call APIs. They use different training and prompting methods, but both show why **tool availability is not equivalent to tool use**. An agent can be surrounded by instruments and still never enter the observational loop that gives those instruments scientific value.

Our EX0004 pilot revealed incompatible tool names and types. In EX0004B the validator and mock runner passed, but the first actual Qwen action was a diagnosis submission. The diagnostic interface was mechanically reachable; its **behavioral use was not demonstrated**. The discrepancy between scripted mock readiness and actual model behavior is the central instrument fact.

**Contribution:** A distinction between a model that can format a call, a model that can invoke it, and a model that can condition later decisions on returned evidence.  
**Not certified:** That requiring two calls proves spontaneous scientific curiosity or faithful inner reasoning.  
**Question:** In a public paired probe, does changing a returned observation change the model's next decision as prospectively predicted?

## Witness IV · Min and colleagues: the example can become the answer

**Source:** Sewon Min et al., [*Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?*](https://aclanthology.org/2022.emnlp-main.759/) (EMNLP 2022).

Min and colleagues found that aspects of demonstration *format*, label space and text distribution can matter greatly to in-context learning, sometimes even when example labels are incorrect. Their results do not imply that a particular output in our notebook was generated by a known psychological imitation process. But they give a reason to take **in-context form as an experimental variable**, not merely decorative documentation.

In EX0004B we put a full `submit_diagnosis` object into the public prompt as a syntax example. Qwen returned that exact object, including **“FORMAT EXAMPLE ONLY. Not a diagnosis.”** This makes the confound unusually visible. It is unnecessary to infer secret motives. The output is an *observed literal copy*. Whatever the model's unrealized abilities, the submitted answer was not an evidence-grounded diagnosis.

**Contribution:** A principled reason to separate machine-readable field specifications from answer-bearing demonstrations.  
**Not certified:** That removing the example alone will solve weight-space diagnosis, or that copying is the complete causal explanation for zero tool calls.  
**Question:** If no plausible fault coordinates or causal claims appear in the schema, does the examiner still submit before observing?

## Witness V · Qwen's own documentation: the intended use has a tool protocol

**Source:** [Qwen3-8B model card](https://huggingface.co/Qwen/Qwen3-8B), sections on thinking, agentic use and tool calls.

The model card documents thinking mode (`enable_thinking=True`), a chat template and recommended agentic tooling, including Qwen-Agent. EX0004B used local BF16 inference with a fixed revision and a hand-built JSON dispatcher. That was a plausible engineering choice, but it was not the same as proving that the **recommended end-to-end tool protocol** had been exercised by the actual model before the experiment.

Our mock tests established that *our code* would accept valid requests. They did not establish that *Qwen* would generate the useful requests when placed in a real conversation. This distinction is narrower, and more actionable, than calling Qwen unable to read weights.

**Contribution:** Documentation for selecting and freezing a model-appropriate tool interface.  
**Not certified:** That a native tool parser will make the examiner scientifically competent.  
**Question:** Can a real model-generation preflight on a sacrificial patient pass before the private test begins?

## Witness VI · Geiger, Makelov and Vaidyanathan: causal language deserves causal controls

**Sources:** Atticus Geiger et al., [*Causal Abstraction: A Theoretical Foundation for Mechanistic Interpretability*](https://www.jmlr.org/papers/v26/23-0058.html) (JMLR 2025); Aleksandar Makelov et al., [*Is This the Subspace You Are Looking for?*](https://proceedings.iclr.cc/paper_files/paper/2024/hash/70b8505ac79e3e131756f793cd80eb8d-Abstract-Conference.html) (ICLR 2024); Sankaran Vaidyanathan et al., [*The Curse of Multiple Mediators: Hidden Interaction Effects in Activation Patching*](https://arxiv.org/abs/2606.27510) (2026 preprint).

These works help discipline our ambition. A satisfying mechanistic account needs **faithfulness under intervention**, not just an impressive story. Subspace or component interventions can admit interpretive illusions, and interactions can frustrate an attribution that treats each component's effect as separable from the rest.

Our healthy/A-only/B-only/both lesion states were useful precisely because their outputs could be compared. But the diagnosis-first teacher never used this opportunity to state a supported prospective prediction. Its formal ranking field happened to be correct; its interaction sign and fault locations were wrong. The evaluator can establish that score. It cannot infer a hidden reasoning mechanism from it.

**Contribution:** The standards against which a mechanistic claim should be measured: interventions, controls, invariances, and recognition of interactions.  
**Not certified:** That our factorial loss interaction alone identifies the model's internal causal graph, or that the examiner reasoned about multiple mediators.  
**Question:** What **new** observation, not present in a template, did the examiner use to rule out a rival lesion?

## Witness VII · The engineer's warning about a beautiful fingerprint

**Source:** Python 3.13 documentation, [`marshal`: Internal Python object serialization](https://docs.python.org/3.13/library/marshal.html).

During EX0004B's pre-exposure integrity check, the fingerprint computed from `marshal.dumps(function.__code__)` disagreed with the originally frozen fingerprint. We verified that the visible source AST matched and the mock pathways completed, then documented A1; the cause of binary inequality was **not** resolved. Python's documentation explicitly warns that marshal is an internal format, not a general stable interchange format, especially for code objects across versions. That caution does **not** prove what caused the discrepancy inside our one Colab runtime.

**Contribution:** A reason to choose versioned source and reproducible files as primary code-integrity anchors.  
**Not certified:** That source-AST equality proves exact binary equivalence, or that A1 retroactively eliminates the uncertainty.  
**Question:** Can the next instrument be built as a short version-controlled module whose actual model-facing behavior is tested before freezing the scientific run?

## The field note · What the measurements can and cannot say

| Observed event | What it proves | What it does **not** prove |
|---|---|---|
| Pilot: 3 invalid of 6 requests | The original interface and model outputs were mismatched | Model unable to diagnose a coherent patient |
| C06 selected after five rejected candidates | The frozen construction gate found a harder qualifying synthetic fixture | A teacher could or could not solve it |
| EX0004B: 0 diagnostic requests in either arm | The live episodes did not investigate through those tools | The model could never use the tools |
| Diagnosis copied the sample object | This submitted explanation is not independent mechanistic evidence | Why the model made that choice internally |
| Empty patch: 0% recovered gap | No functional improvement by the first arm | General diagnosis-first prompting is ineffective |
| Two-edit patch: −8.27% recovered gap | The second submission worsened this held-out task | General inability to program weights |
| Both formal H1 gates FAIL | The registered outputs did not meet success criteria | A conclusive estimate of attainable model capability |

The public archive now contains the previously private patient key and held-out values. This is good for examining an old claim, but means **the same case is no longer a fresh blinded test**. The correct response is not to hide these facts or keep trying new prompts on C06 and count a later success as independent evidence.

## Coda · A disagreement worth carrying into EX0005

**Salviati:** The negative scores are real. On the submissions that occurred, neither successful repair nor mechanistic prediction was demonstrated.

**Sagredo:** Yet the intended examination never happened. We must not write a sentence about the model's inability to diagnose when the trace shows that it did not look.

**Simplicio:** So should we throw away the evening?

**Sagredo:** No. Keep the transcript, stop the experiment, and build a better instrument. The next test must make an observation visible *and useful* before accepting a verdict about causal understanding.

The conversation is invented, but the methodological discipline is not. [EX0005](./ALGN_EX0005_PLAN.md) is an **unexecuted proposal** to test the tool interface with real Qwen generations on public sacrificial cases, then move to a new hidden patient only if the instrument passes. It is neither a continuation of EX0004's sealed result nor a guaranteed redemption arc.

**What we know:** two bounded submissions failed. **What we do not know:** what this model can do when it genuinely examines the weights. We should be especially careful with the latter because it is the interesting question.

*The patient answered the measurement we gave it. The examiner did not ask the question we wanted answered.*
