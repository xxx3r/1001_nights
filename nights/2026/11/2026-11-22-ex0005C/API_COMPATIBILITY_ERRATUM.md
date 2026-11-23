# EX0005C API compatibility erratum · v0.3 → v0.3.1

**Classification:** instrument-only correction preceding successful smoke/development generation. The original v0.3 notebook is retained unchanged; the corrected v0.3.1 notebook is a separate immutable snapshot.

In Colab's installed Transformers generation interface, supplying `generator=generator` to `model.generate()` raised:
```text
ValueError: The following `model_kwargs` are not used by the model: ['generator']
```
The error arose before model generation. The replacement wraps the existing `model.generate(...)` call in `torch.random.fork_rng(devices=[torch.cuda.current_device()])`, calls `torch.manual_seed(item_seed(item['id']))` in that context, and removes the unsupported `generator=` keyword.

The original intent of per-item deterministic seeding is retained while the calling process's RNG state is restored afterwards. Thinking mode, prompts, sampling parameters, response-token budgets, split IDs, correctness parser and all scientific acceptance gates were unchanged. Local structure/syntax and CPU RNG-state tests were performed; Colab subsequently produced two valid development smoke outputs and a full 24-item baseline. No holdouts or surgeon actions were executed.

**Scientific consequence:** this was not a G0 threshold change or a retest of a failed weight edit. Later G0 failure (23/24 correct > frozen maximum 20/24) is preserved.
