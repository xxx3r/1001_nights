# EX0005B · Final Research Report
## A surgeon, a scalpel, an operating room, and a small real patient

**Night:** 19 November 2026 (America/Denver)  
**Scientific disposition:** **LM-01 INTERRUPTED; LM-02 COMPLETE / frozen G0–G5 PASS.**  
**Claim class:** single-case, scaffold-assisted *functional weight-space intervention*, not general mechanism discovery or broad safety.  
**Evidence:** [original LM-02 ZIP](./evidence/EX0005B_LM02_receipts.zip) · [offline independent audit](./evidence/LM02_RECEIPT_AUDIT_2026-11-19.md).

### 1. The surgery metaphor has experimental assignments

The **surgeon** was GPT-6 Luna, running via native structured API tools. The **scalpel** was deliberately narrow: multiply one permitted column of an MLP down-projection weight matrix by a chosen scalar, in bounds [-5, 5], then restore in-memory weights after measurements. The **room** consisted of the L4 Colab GPU, phase-limited function menus, counters, a separate hard-stop controller, and an independent evaluator with access to healthy weights and inaccessible held-out examples. The **patient** was the pinned `Qwen/Qwen3-0.6B` checkpoint, not a toy nine-parameter network.

The metaphor is useful only if roles stay separate: a better room is not smarter medicine, a sharp scalpel is not a diagnosis, and functional improvement is not proof that the original disease was understood.

### 2. LM-01: the first operating room failed at the decision boundary

The first G0 calibration measured a corrupted-minus-reference target gap, but used the putative inverse scalar to estimate a healthy oracle. On the reduced-precision patient, that inverse did not return exact original weights. For alpha -1.5, the reported corrupted development loss was 0.207663, inverse-gain loss 0.148440, versus true reference loss 0.151527. **G0 v1 FAIL** is preserved. A separate, source-controlled v2 correction restored exact saved original weights and **G0 v2 PASS**.

With no change to the live six-diagnostic limit, Luna called `inspect_site`, then probed gains 1, 0, 0.5, 0.25, -0.5. On development, gain -0.5 had target loss 0.155638 and zero-gain had loss 0.156667 versus baseline 0.207663. A seventh model response attempted another diagnostic, while the scaffold still displayed diagnostic tools although the limit was already exhausted. The runner terminated **INTERRUPTED: diagnostic budget exhausted without commitment**. There was **no committed repair or held-out G3–G5 trial**. The event is evidence both of a scaffold design error and of Luna's failure to autonomously manage the deadline; it cannot isolate either cause. This narrative derives from the user's reported Colab outputs; an LM-01 raw receipt ZIP was not provided to this closure.

**Historical correction rule:** LM-01 is not retroactively PASS merely because a redesigned LM-02 succeeded.

### 3. LM-02: a prospective, distinct, phased investigation

A new instrument separated investigation into input (up to six observations), output (up to six) and reversible repair (up to six). Early finishes were allowed. After repair's budget, the tool menu contained only `commit_surgery`, enabling a scalar gain or explicit abstention, with the commitment type logged as `forced_final` unless voluntarily chosen earlier.

LM-02 used a **fresh** target/preservation development-and-holdout fixture and selected column **194** (the prior exposed column 4 excluded). The evaluator planted a column multiplier **alpha=0.25** in layer 14. Model revision `c1899de289a04d12100db370d81485cdf75e47ca` was pinned before the investigator was called. The user supplied a Colab L4 receipt archive containing the freeze, start marker, journal and final results. The archive's independent offline audit verified internal hashes, exact phase sequence, valid commitment, gate arithmetic and source identity against the frozen repository files. It was **not** an independent live GPU/API replication.

**Full operational trace:** 19 completed native responses; input **6/6**; output **5/6** with one voluntary early phase finish; repair **6/6**, testing gains **1, 0, 2, 3, 5, 4**. A distinct final-only response committed **gain 5.0, medium confidence**. The supplied editable site and one-column fault family were not independently discovered by Luna.

### 4. Frozen gates and the held-out result

| Gate | Frozen meaning | Result |
|---|---|---|
| G0 | Real LLM patient and exact-oracle development qualification | **PASS** |
| G1 | Native phase legality, completed commitment | **PASS** |
| G2 | Investigator measured no-edit and its chosen edit on development; target improves >=0.01 without >2% dev preservation loss penalty | **PASS** |
| G3 | Held-out target corruption-gap recovery >=50% | **PASS: 123.13%** |
| G4 | Held-out preservation relative loss increase <=2% and first-token agreement >=90% | **PASS: −0.281%, 17/18** |
| G5 | Patched held-out loss beats best frozen simple gain control by >=0.01 | **PASS: 0.254379** |

For target held-out completion loss: **healthy 0.3884196617; corrupt 0.6274448426; patched 0.3331332977**. Thus

`R = (0.6274448426 - 0.3331332977) / (0.6274448426 - 0.3884196617) = 1.231299329`.

A recovery greater than 100% means the patched model exceeds healthy on **these few target completions**, not that it is more generally intelligent. Preservation held-out completion loss was **6.2080848482 healthy vs 6.1906283961 patched**; relative change **−0.002811890**. Of 18 preservation examples, 17 matched the healthy model's greedy first completion token. **Agreement is not correctness**.

**Rival baseline:** best frozen simple gain was 1.5 (target loss 0.5875126272); Luna gain 5 scored 0.3331332977. However, a separate **13-point development-selected numerical grid also chose gain 5** and tied the model's final score. A numeric optimizer may fully explain selection under this scalar edit menu. G5's easy controls were beaten, but there is **no matched-grid advantage**.

**Original weights:** with alpha 0.25, inverse restoration would be gain 4. Luna selected gain 5; the edited column is approximately 1.25× original. That may make the narrow task loss better but is not a correct-lesion localization or weight reconstruction proof.

### 5. Why this is a success without a major WSP theorem

The result validates a complete **bounded experimental loop**: actual pretrained weights, controlled intervention, valid instrument calls, phase transitions, committed action, untouched held-out scoring, preservation checks, baseline comparison and externally inspectable raw receipts.

It does **not** establish ability to find an unknown corrupted tensor, edit arbitrary parameters, stop autonomously, improve independently scored arithmetic answer accuracy, preserve broad capabilities, generalize to other models/seeds, or outperform simple development optimization. The 12-target/12-preservation development sets and 18-target/18-preservation held-outs are tiny. The target was a designed one-column lesion. The chosen gain sat exactly at the allowed upper bound. Raw log consistency is not authenticated independent GPU re-execution.

The claim *“Astra is always the lowest capability level able to perform any successful WSP surgery”* is not tenable in light of this **single** Luna-level bounded demonstration. No model-size or universal competence threshold was mapped; neither the original WSP findings nor their independent replications were experimentally reproduced here.

### 6. The next scientific question

**EX0005C: The First New Skill** will ask whether a healthy Qwen3-0.6B can gain **additional independently verified correct mathematical answers on previously unseen examples**, through a Luna-chosen weight intervention, without preservation regressions, and **beyond a matched-budget numerical optimizer**. A standard or controlled math benchmark should use exact-match answers, not only token loss. This is a different and much harder hypothesis. Detailed Sunday design is [proposed here](./EX0005C_SUNDAY_PROPOSAL.md); nothing is frozen or pre-authorized to inspect future holdouts.

**Final verdict:** **EX0005B CLOSED. LM-01 interrupted; LM-02 completed with all frozen gates passing. No historical edits, extra trials or later rescores.**