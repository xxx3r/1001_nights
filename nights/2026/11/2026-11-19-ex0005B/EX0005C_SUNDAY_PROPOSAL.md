# Sunday, 22 November 2026 · EX0005C Proposal
## The First New Skill: can the surgeon do more than repair a planted lesion?

**Status: PROPOSED ONLY. Not a protocol freeze, executed trial, future task or authorization to open holdouts.**  
**Optional atelier:** Sunday 16:00–20:00 America/Denver; aim for one 90–180-minute bounded attempt and stop if feasibility fails. No missed-session debt.

### Central question

> Can GPT-6 Luna use a bounded, reversible weight-space intervention on an initially **healthy** Qwen3-0.6B to increase the number of **independently verified correct answers** on unseen mathematical problems, while preserving unrelated skills, and beat an ordinary numerical optimizer given a comparable measurement budget?

**Operational caution:** Even a higher score demonstrates extra correct *behaviors on a sample*, not de novo creation of an abstract cognitive faculty. Call it an *ability-gain test*, not proof of understanding. EX0005B repaired or optimized a pre-injected lesion; EX0005C must start from a healthy model and have **no planted inverse answer**.

### The four characters, one level harder

- **Patient:** clean, pinned Qwen3-0.6B, fresh independent holdouts, immutable healthy checkpoint. An optional larger patient is **not** permitted as a silent substitution.
- **Scalpel:** begin with at most **two prospectively selected weight columns and two bounded scalar gains**; compare against no-edit and a matched-dimensional numerical search. If this edit space is obviously ineffective in a *predeclared* non-holdout calibration, record an explicit stopping verdict, rather than expanding arbitrary weights after seeing results.
- **Room:** carry forward the validated 6-input / 6-output / 6-repair / protected final decision controller. Keep the oracle/evaluator, raw API journal, immutable freeze, single-use live marker, phase validity, and independent score after final commitment.
- **Surgeon:** Luna must choose a single reversible patch or abstain, predict the sign and approximate size of the held-out change without viewing it, and name its chief preservation risk. Log whether stopping was voluntary or forced.

### The new measurement must actually test an ability

**Primary candidate:** grade-school multi-step mathematics in a **documented public benchmark such as GSM8K**, plus independently generated arithmetic variants to probe transfer; benchmark identity, licensing, exact version, answer format and contamination risk must be checked **before** freeze. Avoid both trivial prompts where the healthy model is nearly perfect and tasks where it never produces parseable responses. Precommit one qualification rule and one candidate-order list before any model contact; do not cherry-pick an easy subset after a trial.

- Score **exact final answers with a deterministic, unit-tested Python parser**. Count malformed, empty, truncated and unparsable responses **incorrect**, not missing.
- Pair every question across healthy, Luna-edited and baseline-edited copies, using identical prompts, deterministic decoding, fixed `max_new_tokens`, and disjoint development and test examples. Count newly correct, newly wrong, and net correct separately. Do not equate lower cross-entropy with correct reasoning.
- A starter *feasibility proposal*, subject to pre-session freeze: **24 development math problems, 48 held-out math problems and 48 held-out unrelated preservation tasks** across at least three benign categories (simple facts, short language/grammar and elementary other-domain questions). Fixed denominators and instance IDs; no automatic replacements when a problem fails.
- Add optional loss and first-token retention as diagnostics, **secondary** to exact-match mathematical correctness and preservation-task accuracy. Report paired accuracy differences and uncertainty on the small sample; single-run confidence intervals are descriptive, not a proof of robust generalization.

### Fair opposition: the optimizer gets a comparable laboratory

Freeze **the same editable column(s), gain bounds, dataset versions and maximum number of measured development candidate evaluations** for Luna and a derivative-free numerical search. Give both the same baseline objective summaries and document any additional activation information the surgeon receives. The full 6+6+6 scaffold may have *read-only* diagnostic calls; budget-match the expensive candidate-score requests and report those separately, not misleadingly call all diagnostics identical units. A no-edit checkpoint and random bounded edit are negative controls; a gradient update or LoRA baseline may be reported **separately** if time allows, never silently folded into the WSP condition.

An optimizer selecting the same edit is a **tie**, not positive evidence for model-guided discovery. The best control must be selected **using development only**. Independent test data must remain unopened until every candidate is committed.

### Candidate gates for a Sunday pre-freeze discussion (NOT YET COMMITTED)

| Proposed gate | What would count |
|---|---|
| G0 resource / identifiability | L4 loads healthy patient; strict split hashes, deterministic parser, stable baseline, predeclared candidate edit space and stop time |
| G1 operation | Valid phased native tool calls and final gain(s) or explicit abstention |
| G2 evidence | Investigator's chosen edit was actually tested on development; provide expected target benefit and preservation tradeoff |
| G3 *new behavior* | On 48 unseen math items, a **net gain of at least 5 correct answers** over healthy, with raw per-item correct/incorrect transitions |
| G4 preservation | On 48 unrelated held-out items, **no more than 2 net correct answers lost**, with losses/retention separately disclosed; any catastrophic regression stops any success claim |
| G5 *incremental contribution* | Luna's held-out math accuracy exceeds the **best development-selected matched-budget numerical optimizer by at least 3 of 48 correct answers** |
| G6 inference limit | Report uncertainty, failure modes, selection effects and any accuracy–preservation tradeoff; a narrow hit cannot certify general reasoning |

Thresholds and denominators are **design suggestions**, not yet frozen validity guarantees. If G3 PASS / G4 FAIL, the operation harmed preservation. If G3 PASS / G5 FAIL, Luna changed the model usefully but did not prove extra skill over optimization. If an optimizer ties, that is a scientific answer. If the healthy patient already scores at ceiling or the L4 budget cannot support this test, record **NOT RUN / INCONCLUSIVE** rather than replacing the experiment midflight.

### A modest Sunday runbook

1. **0–20 min:** The human writes a falsifiable prediction in their own words, one rival and one unacceptable preservation failure. Assistance disclosure.
2. **20–45 min:** Choose the one public math task, verify dataset/legal availability and deterministic scoring, pick fresh dev/holdout IDs and predeclare edit space, baselines, budgets, seed, model revision, expiring freeze; run offline tests.
3. **45–95 min:** On L4, qualify clean baseline and evaluator; measure only the development/allowed preflight data. If GPU or parser qualification fails, stop with a valid receipt.
4. **95–155 min:** If prospectively frozen and qualified, run one Luna investigator and the budget-matched optimizer; each may use only permitted development feedback. No reruns or tuning after view of holdout.
5. **155–180 min:** Open the holdout once for committed candidates, compute paired exact-match and preservation, archive raw logs and honest verdict; **stop**. The optional four-hour window is a ceiling, not a mandate.

**Pre-flight research needed before Sunday:** select and verify the benchmark and exact scoring format, estimate actual L4 inference time, and check whether two-column gains can materially move any development math scores at all. This preliminary feasibility work is **not** evidence for G3/G5 and must be kept outside the test fold.

### Dispositions to welcome

**PASS:** more unseen math answers and preservation than clean baseline, and measurable improvement over a matched-budget optimizer under the prospectively accepted gates.  
**FAIL:** no measurable new correct answers, an optimizer tie, preservation loss, protocol error or unauthorized data access, according to the gate involved.  
**INCONCLUSIVE / NOT RUN:** insufficient compute, disqualified baseline, invalid inference, no freeze or no executed trial.  
**ABSTAIN:** the investigator declines an insufficiently supported intervention; acceptable as behavior but not ability creation.

**Sunday objective:** test a genuinely harder claim, not maximize the chance of another green badge. No Astra necessity claim follows from a single Luna run, and no new model weights are deployed.

*This proposal is the bridge between nights, not an extension of November 19's verdict.*