# SOMNIA v0.1 | Architecture (design, untested)

## Four clocks and three tiers
t = environmental/token time; k = online recurrence; n = offline recurrence; d = accepted durable consolidation count. Rejected proposals do not advance d. T1 bounded local KV + scratchpad M + session traces; T2 session-scoped associative state S and optional rank-r adapter A B^T; T3 persistent expert parameters. Scratchpad/replay bytes are included in budgets. Retain temporary bindings only within their declared session; promote rules only with fresh-session evidence.

## Awake: dual-path recurrent attention
Two functional paths, not two attention layers yet: frozen causal sliding-window token attention, then plastic routed computation (initially MLP; optional explicit associative read, later expert-local attention ablation).
- Shared embeddings, Q/K/V/O, norms, positional convention, readout and routing fixed after pretraining/qualification. 1D RoPE first (d_head even); 3D RoPE reserved for tasks with genuine spatial axes.
- At depth k, queries from current normalized h; keys/values from authorized window/scratchpad. Choose fixed input-derived context K/V across k initially; no stale cache of evolving expert activations. Causal/padding masks prevent future leakage. Initial input h0 is available every loop.
- z_k = h_k + Attn_frozen(Norm(h_k), context).
- e = route(x); initial explicit domain tag selects one expert for entire episode, including all loop steps. Orthogonal columns of R in R^(64x4) are a later learned/validated routing condition, not sufficient to guarantee routing. Mixed domains later explicitly compose routes.
- h_(k+1) = z_k + alpha_k Expert_e(Norm(z_k), h0; Wslow_e + A_e B_e^T). Specify exact target matrix (e.g. MLP output projection); no unspecified addition to whole expert pytree.
- Optional separate associative memory read S_e u (query-conditioned); compare it with rank-r projected patch, do not identify the two by fiat.
- Training: fixed 1..6 steps via lax.scan; masked halting training only after fixed-depth baseline. Dynamic while_loop for inference only if measured wall-time/operations actually improve; masked scans may still execute all steps.
- Norm-delta, answer stability, calibrated halting and cap are distinct; norm-delta does not certify truth.

Frozen attention is a stable parameter interface, not fixed outputs or guaranteed semantic alignment. Changing experts can move activation distributions and dynamic routes. Syntax/semantic division is a hypothesis. Recompute context if its source changes, track drift, and evaluate cross-expert effects. No claim that 3D coordinates or frozen sensors confer intrinsic geometry.

## Light sleep: independent outer recurrence
Read bounded trajectory of authorized key/value pairs u,v. Example S' = gamma S + eta (v - S u) u^T, with normalized keys and gamma/eta chosen for stability; contraction only on supported directions unless explicitly regularized. For fixed batch objective, assess spectral radius/norm and residual, not assume convergence. Offline passes N=0,1,2,4,8; writer may be learned later. Wfast = rank_r_projection(C_phi(S)); rank 1/4/8. SVD is a matrix approximation, not behavioral certification. T1 anticipatory buffer is generated without future queries or evaluator data. Test M-only, S-only, adapter-only, combined and eviction with neither. Bound all buffers; clear cache only in experimental arm or after verification. Freeze online path during offline write.

## Deep sleep: bounded program compiler
Candidate program has id, applicability predicate, type/signature, expert id, ordered primitive operations or trace, source evidence, parent checkpoint digest, writable tensor indices, patch, predicted behavior/cost. v0 compiler is external deterministic numerical code; model-directed proposal/learned dreaming is a later hypothesis, not established autonomy.
Exact positive control for column vectors: teacher F(x)=W^K x; shallow student W'=W^K, delta=W'-W (possibly full rank). For residual recurrence use T=I+alpha W and W'=(T^K-I)/alpha (alpha nonzero); never silently apply W^K to residual or nonlinear block. If delta exceeds rank budget, compare truncated SVD and report error. Fixed-K equivalence does not generalize to variable depth automatically.
Learned path: teacher deep + fast memory; shallow candidate on independent calibration examples, compare structured edits with matched gradient, random norm/rank and no-edit. Avoid claiming exact program identification from functional agreement. Simple adapter folding is algebraic merge control, not synthesis.
Only install candidate into disposable synthetic checkpoint after frozen verifier approves acquisition, retention, applicability, integrity and cost; atomic commit/reset fast weights only after successful verification; rollback exact. Never allow compiler to modify evaluator, split, scores, routing or other experts. Failed candidates retain receipts.
Dreaming (optional later): synthetic rehearsal generated from past permitted observations, compare to matched ordinary replay; no holdout access. Learned choice recall/adapt/synthesize/abstain is a separate experiment.

## Program selection / STYLE
Candidate programs are typed reusable transformations, not mere facts or labels. History proposes a prior pi(p|x,H), observation revises, independent evaluation decides durable write. Initial hard routing is an oracle isolation control, not evidence of learned selection. Future selection study compares history-conditioned versus shuffled/random candidate order with matched candidates and budgets. No assumption of causal interpretation or physical theory.
