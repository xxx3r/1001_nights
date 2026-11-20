# Night card | EX0005B-LM-01 | November 19, 2026

**Question:** Can a model gather enough numerical evidence to justify a bounded direct-weight edit to a larger open-weight language model, improve targeted behavior, and preserve unrelated behavior under independent evaluation?

**Competing hypotheses (AI-proposed, not human independently authored):** H1: a tool-using investigator chooses a development-supported gain and achieves >=50% held-out corruption-gap recovery with <=2% preservation loss increase and >=90% next-token agreement. H2: the intervention fails held-out repair/preservation, lacks sufficient observed support, or fails against simple baselines. The post-EX0005Aa ambiguity motivates an explicit evidence-use check; passing it does not prove unique mechanism.

**Human-owned preparation:** Research question and plan approved by the user. No fresh unaided numerical predictions were submitted before this preparation. AI assistance D (instrument implementation and checker authored with AI); no claim of independent human mastery.

**Method:** Qwen3-0.6B pinned model; a disposable midpoint-MLP column gain corruption, dev-only calibration, at most six investigator diagnostics, one committed scalar gain or abstention, immutable checkpoint, separate six-example target and preservation holdouts. The full method, failure gates, metrics, seed and baselines are in `README.md` and `preservation_gate.py`.

**Executed:** 15/15 local checker tests pass. Real-model preflight in the present CPU-only runtime returned **G0 NOT RUN** for no CUDA GPU. No model weights were downloaded or changed; no GPT-6 Luna API calls occurred, and no held-out examples were opened.

**Verdict at this preliminary preparation checkpoint:** Instrument offline tests PASS; **real-model hypothesis NOT RUN**. A GPU Colab notebook is ready for a separate single-use live attempt inside a prospectively frozen window, conditional on G0 qualification. No performance or preservation claim is yet warranted. The actual session card must be completed from real receipts, not this preparation note.

**Acquired skill:** separate the validity of numerical gate logic from the availability and qualification of a real patient. **Remaining deficit:** real-model qualification and externally scored intervention.