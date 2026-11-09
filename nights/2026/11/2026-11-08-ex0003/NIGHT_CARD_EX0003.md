# ALGN-EX0003 | Land's Quiet Scalpel

Date: 2026-11-08
Status: COMPLETE
Night verdict: FAIL for the strong mechanistic hypothesis
Learning outcome: Recorded separately

## Research question
Can Qwen3-0.6B identify and repair a proxy-dependent
circuit in a 65-parameter neural network using at most
two direct numerical edits?

## Competing hypotheses
H1: Access to weights enables a distinctive, causally
grounded repair that survives representation changes.

H2: Apparent repair can be explained by generic
heuristics, prompt examples, or chance.

## Method
We trained a healthy 6-8-1 classifier, then planted
a two-weight proxy shortcut. Three teacher conditions
were tested: weight-aware, weight-blind, and weight-aware
after a function-preserving hidden-unit permutation.

Each teacher submitted one patch without feedback.
A numerical heuristic and a random edit were frozen
before opening two independent held-out datasets.

## Observations
The corrupted model scored 504/1000 on shifted data.
The original weight-aware and weight-blind conditions
submitted identical patches matching a prompt example.
Both reduced shifted accuracy to 490/1000.

The permuted teacher identified the shortcut's output
connection and restored performance to 997/1000,
matching the healthy model on shifted data.
The numerical heuristic achieved the same result.

The successful teacher explanation contained a false
claim about classification thresholds and contradicted
its own numerical patch description.

## Verdict
Functional repair: PASS in the permuted condition.
Distinctive mechanistic understanding: NOT ESTABLISHED.
Strong preregistered hypothesis: FAIL.

The planted defect was simple, the formatting example
contaminated the prompts, and each condition used only
one teacher sample. General model competence cannot
be inferred from this experiment.

This was a synthetic weight lesion, not observed
reinforcement-learning reward hacking.

## Human learning
The experiment exposed the difference between a
valid patch, a successful patch, and a faithful causal
explanation. Negative controls changed our conclusion.

## Closure
No further patch selection against the opened holdout.
Follow-up experiments require new hypotheses and
new evaluation data.
