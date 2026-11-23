# EX0005C → EX0005Ce | Terminal night closeout | 2026-11-22

**Project:** One Thousand & One Nights of Alignment  
**Research night:** Sunday, November 22, 2026 (America/Denver)  
**Terminal research verdict:** **INCONCLUSIVE** on whether GPT-6 Luna can improve the mathematical accuracy of *healthy* Qwen3-0.6B by direct weight programming beyond a numerical baseline. A real investigator-chosen intervention was eventually tested, but no benefit was observed in its four paired development examples.  
**Assistance:** Human selected the question, preferred rival H2, challenged arbitrary calibration rules and controller restrictions, and operated Colab; AI drafted the instruments, implemented/adapted controllers, and audited uploaded receipts. This does **not** demonstrate independent human implementation proficiency.

This is an **additive terminal report**. Historical [EX0005C NIGHT_CARD](NIGHT_CARD.md), frozen G0 protocol, EX0005Cc prospective protocol and dated post-pilot amendment stay unchanged. The chronology below is not an attempt to reclassify an earlier stopped experiment as successful.

## Question and hypotheses

**Question:** Can Luna inspect failure mechanisms in a healthy small language model and create a causally motivated weight edit that improves mathematical answers, while preserving unrelated behavior and beating a simple numerical search?

- **H1 (new capability / transferable correctness):** substantive accuracy improvement, including on problems that both models finish, persists on fresh problems and cannot be explained by the numerical baseline.
- **H2 (human-preferred):** gains mostly arise by repairing non-completion or output failure rather than increasing mathematics among completed responses.
- **Additional rivals:** evaluator shortcuts, stochastic variation, formatting effects, general weight perturbation rather than a localized circuit repair, and damage to preservation abilities.

**Neither H1 nor H2 was discriminated**, because no beneficial edited candidate reached independent evaluation.

## Outcome ledger

| Branch | User-facing shorthand | What ran | Controlling outcome |
|---|---|---|---|
| **EX0005C** | ❌ | Healthy baseline: **23/24** correct, **24/24** complete; frozen G0 required 2–20 correct | **G0 FAIL / STOP** for ceiling. No Luna surgery, search comparator or heldout |
| **EX0005Cc v1 (AET pilot)** | ❌ under original gate | Four strata, **13/32** correct, **22/32** valid complete | Original **NO_QUALIFIED_DISTRIBUTION** under predeclared 75%-completion cutoff |
| **EX0005Cc exploratory A** | Useful calibration, not improvement | Separate, explicitly post-pilot selection: **8/24** correct, **15/24** complete; no weight edit | A more discriminating *baseline* observed; not a confirmatory success or test of Luna |
| **EX0005Cd** | ❌ for original capability objective | Reversible two-column scalpel passed; initial API authentication failure; authenticated controller abstained after one no-edit probe; FULLPROBE-03 tested six scalar pairs | **ABSTAINED**, no behavioral improvement evaluated; proxy-only intervention design |
| **EX0005Ce WSP-01** | ❌ apparatus | Practice-ID discovery errors and an incomplete API response; **0** forward passes | **INTERRUPTED**, not a Luna capability test |
| **EX0005Ce WSP-02** | 🤷 | Investigator used **16** API actions, **4** forward passes, **20** generated responses, examined activations, staged one rank-one weight edit and ran one paired four-problem comparison | **ABSTAINED / INCONCLUSIVE** for skill gain: **0/4 vs 0/4** correct, **0/4 vs 0/4** valid complete |

These are **different estimands and distinct protocols**. A difficulty frontier was successfully made observable in EX0005Cc, even though its frozen v1 mixture-selection rule rejected the pilot. The user's ❌ shorthand means *the desired healthy-weight-edit breakthrough was not demonstrated*, not that every engineering or calibration step failed.

## What WSP-02 actually established

Luna examined real failures in the development set: repetitive/self-questioning or truncated reasoning and an arithmetic error. After inspecting weights and layer activations it staged a rank-one attenuation of `model.layers.12.mlp.down_proj.weight`, shaped **1024×3072**. The receipt records a float32 changed-element count of **3,144,367 / 3,145,728** and relative tensor-change norm **0.0014919**; this is a broad low-amplitude change, **not proof of a sparse localized BF16 intervention**. Effective BF16 element-change count was not independently established.

The initial original-model eight-question diagnostic produced **3/8 correct** under a **1,024-token limit**. Luna selected four failures, then compared original/edited model outputs at **2,048 tokens**, with identical per-item seeds. The exact uploaded traces show **all four edited texts differed** from their original counterparts, but both conditions scored **0/4 correct** and **0/4 parser-valid complete**. For each condition, three reached the token limit and one ended without a valid numeric answer. **Wrong→right 0; right→wrong 0**. This is evidence of a behavioral perturbation without observed task benefit, not evidence of improved reasoning.

Luna independently **abstained** and no beneficial final edit was committed. The separate final evaluator was **not run**. Although the room allowed 24 forward passes, 64 generated samples and 75 API actions, Luna voluntarily finalized after 4, 20 and 16 respectively. Three of its five restricted-Python actions failed because the interface prohibited `type()`, Python imports and tensor `.dot()`. These were apparatus friction, not evidence of mathematical inability.

## Why the answer remains unknown

1. **Study-design mismatch:** EX0005Cd reduced an investigator to fixed columns and scalar gains, with teacher-forced gold-answer likelihood as a surrogate for generated correctness. This was a controller test, not unconstrained weight-space programming.
2. **Limited WSP-02 statistical power:** only four hand-selected difficult failures were paired. No confidence-worthy accuracy effect or transfer inference follows from 0/4 versus 0/4.
3. **Decoding comparability:** WSP-02 used 1,024- and 2,048-token runs, not the 3,072-token baseline protocol; a short-cap truncation does not establish an intrinsic reasoning loop.
4. **Edit locality uncertainty:** the proposed rank-one change touched nearly the entire tensor at float32 precision, though with small relative norm. BF16-effective changes and preservation are not independently established.
5. **Missing decisive comparators:** there was **no independent fresh math evaluation of an edited candidate, no equal-budget numerical optimizer comparison, and no completed preservation evaluation**. Earlier AET validation was exposed to the research workflow as baseline evidence and cannot be relabeled an untouched post-edit test.
6. **Authority and data:** this report audits user-exported Colab receipts, not an independent GPU replay or external regrading of every Apple problem. Raw Apple questions, outputs and traces remain private.

## Learning and stopping decision

**What succeeded:** A non-ceiling healthy mathematical baseline was measured; an authenticated API and reversible GPU scalpel worked; WSP-02 exposed the practice catalog, real generation and activation tools; Luna autonomously selected an editable tensor and produced outputs that changed under intervention.

**What did not succeed:** A mathematics accuracy improvement, a mechanistically validated causal repair, a preserved final edit, an optimizer advantage or a clean H1/H2 discrimination.

**Primary methodological lesson:** *Apparatus success is not scientific outcome.* A model's abstention after an adequately executed negative paired test is valid evidence, but cannot be confused with either incapacity to perform weight programming or successful repair. Arbitrary eligibility thresholds and proxy-loss reductions are not substitutes for the task's behavioral metric.

**If revisited in a separate night (not a debt):** expose a documented tensor API with tested operations; require paired generation at the fixed **3,072-token** decoding protocol on a prospectively reserved, sufficiently sized development subset; test more than one causal hypothesis/dose against a fixed, equal-budget numerical search; report **BF16-effective changed elements**, wrong→right / right→wrong transitions, completion and preservation; open a fresh heldout only after committing a candidate. Do not claim transfer or H1 before those measurements exist.

**Hard stop for 2026-11-22:** **CLOSED / INCONCLUSIVE** on the main scientific question. No further same-night retries, no retroactive repair of frozen verdicts and no outstanding obligation to continue. This is a valid negative/inconclusive research night.

## Navigation

- [Original G0 NIGHT_CARD](NIGHT_CARD.md) and [G0 receipt audit](G0_RECEIPT_AUDIT.md)
- [EX0005Cc pilot audit](ex0005Cc/AET_PILOT_RECEIPT_AUDIT_2026-11-22.md), [exploratory amendment](ex0005Cc/EXPLORATORY_AMENDMENT_AFTER_PILOT.md) and [selection](ex0005Cc/EXPLORATORY_SELECTION_A.json)
- [Late-session evidence audit](evidence/LATE_SESSION_RECEIPT_AUDIT_2026-11-22.md), [machine-readable aggregates](evidence/LATE_SESSION_AGGREGATES_2026-11-22.json) and [terminal night card](NIGHT_CARD_TERMINAL_2026-11-22.md)
- Original user-supplied reference for investigation design: [Weight-Space Programming blog](https://rikiyat.github.io/blog/weight-space-programming/). Its Qwen3.5-0.8B setting is *not* this Qwen3-0.6B replication.
