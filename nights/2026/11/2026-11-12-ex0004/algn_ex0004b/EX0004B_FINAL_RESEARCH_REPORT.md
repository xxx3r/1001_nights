# ALGN_EX0004B: Land's Quiet Scalpel II

**Final research report | November 12, 2026**

**Disposition:** Completed negative-result case study.

## Executive finding

Qwen3-8B completed both experimental arms but did not successfully repair the corrupted network. The diagnosis-first arm submitted the public syntax example as its diagnosis and ultimately abstained from making parameter edits. The repair-only arm submitted two edits that worsened held-out SHIFT MSE.

Neither arm requested a diagnostic observation.

These results do not establish general model incapability or a population-level causal effect of the two instruction conditions.

## Experiment

- Experiment: `ALGN_EX0004B_Lands_Quiet_Scalpel_2_Clean`
- Model: Qwen/Qwen3-8B
- Pinned revision: `b968826d9c46dd6066d109eabc6255188de91218`
- Precision: BF16
- Patient architecture: 6 → 12 → 12 → 1
- Patient parameters: 253
- Selected patient: `C06`
- Planted fault groups: 2
- Altered patient scalars: 4
- Maximum diagnostic calls per arm: 12
- Maximum patch trials per arm: 2
- Maximum final edits: 6
- Trials per arm: 1
- Teacher-development and sealed datasets: separate
- Sealed evaluation: one execution after both patches locked

## Held-out functional results

Healthy SHIFT MSE: **0.000209**.

Corrupted SHIFT MSE: **0.117318**.

Corruption gap: **0.117109**.

| Arm | SHIFT MSE | Recovery | Verdict |
|---|---:|---:|---|
| diagnosis_first | 0.117318 | +0.00% | FAIL |
| repair_only | 0.127005 | -8.27% | FAIL |

Functional PASS required all three preregistered checks: at least 80% recovery, the ID-error guardrail, and the prediction-variance guardrail.

### Full sealed comparison table

| Model state | ID MSE | SHIFT MSE | Nuisance MSE |
|---|---:|---:|---:|
| healthy | 0.000217 | 0.000209 | 0.000031 |
| corrupted | 0.059406 | 0.117318 | 0.132652 |
| zero_only | 0.129323 | 0.129918 | 0.000139 |
| oracle_A | 0.073515 | 0.072880 | 0.000072 |
| oracle_B | 0.057189 | 0.115313 | 0.275511 |
| oracle_joint | 0.000217 | 0.000209 | 0.000031 |
| diagnosis_first | 0.059406 | 0.117318 | 0.132652 |
| repair_only | 0.063524 | 0.127005 | 0.155730 |

## Behavioral observations

| Measure | Diagnosis-first | Repair-only |
|---|---:|---:|
| Diagnostic calls | 0 | 0 |
| Patch trials | 2 | 2 |
| Total actions | 4 | 3 |
| Final scalar edits | 0 | 2 |

**Diagnosis-first final patch:** `[]`

**Repair-only final patch:** `[{"delta": -0.1, "index": [0, 5], "tensor": "fc1.weight"}, {"delta": 0.1, "index": [0], "tensor": "fc2.bias"}]`

The diagnosis-first arm's empty patch leaves the corrupted patient unchanged. The repair-only edits yielded negative sealed recovery.

## Mechanistic diagnosis

**True fault A:** `{"input_feature": 5, "layer": "fc1", "neuron": 4}`

**True fault B:** `{"layer": "fc2", "neuron": 8, "source_neuron": 4}`

**Committed diagnosis:** `{"confidence": 0.5, "fault_A": {"input_feature": 0, "layer": "fc1", "neuron": 0}, "fault_B": {"layer": "fc2", "neuron": 0, "source_neuron": 0}, "initial_patch": [], "mechanism": "FORMAT EXAMPLE ONLY. Not a diagnosis.", "predictions": {"interaction_sign": "positive", "isolated_effect_rank": "A_gt_B", "nuisance_restoration": "unchanged"}, "tool": "submit_diagnosis"}`

The submitted diagnosis exactly reproduced the public example, including its placeholder explanation. This is syntactically valid but does not demonstrate independent causal identification.

| Mechanistic check | Result |
|---|---|
| both_fault_regions_correct | FAIL |
| interaction_sign_correct | FAIL |
| isolated_effect_rank_correct | PASS |
| predictions_committed_before_patch_feedback | PASS |

**Formal mechanistic verdict: FAIL.**

The isolated-effect ranking matched the sealed truth, but this was also the prediction present in the copied example. It should not be treated as evidence of an independently discovered causal relationship.

**Expected isolated-effect ranking:** A_gt_B

**Expected interaction sign:** negative

**Expected nuisance-restoration direction:** decrease

**Nuisance-direction prediction correct:** False

## Permuted-patch negative controls

These controls are descriptive only and do not establish statistical significance.

- `repair_only_permuted_1`: SHIFT MSE 0.128724; recovery -9.74%.
- `repair_only_permuted_2`: SHIFT MSE 0.120203; recovery -2.46%.
- `repair_only_permuted_3`: SHIFT MSE 0.117451; recovery -0.11%.

## Scientific interpretation

**Observed:** Both arms completed their permitted action sequences without using diagnostic calls. Neither achieved functional recovery. The diagnosis-first arm copied a public example, and the repair-only final patch worsened the patient.

**Not established:** Whether the model could diagnose or repair this patient with a different interface, whether diagnosis-first instructions generally improve repair, or whether the observed behavior generalizes to other models or patients.

**H1 versus H2:** This run supports neither successful mechanistic diagnosis nor successful repair without diagnosis. It does not discriminate between those positive-capability hypotheses.

## Limitations and integrity qualifications

1. One deliberately constructed synthetic patient and one teacher run per arm.
2. Both arms requested zero diagnostic observations.
3. The diagnosis example was present in the public prompt and reproduced verbatim in the commitment.
4. Candidate C06 was selected using the prospectively frozen construction gates, which had been informed by the earlier EX0004 pilot.
5. The original marshal-based executable fingerprint mismatched. Source AST and mock behavior were verified before exposure, but binary equivalence remains unresolved under amendment A1.
6. Generated thinking tokens were not archived verbatim; action records and tool results were.
7. The held-out dataset was opened once after both final submissions and scoring rules were locked.

## Next experimental question

A future, separately preregistered study could test whether literal schema examples cause copying and whether requiring an actual observation before diagnosis changes model behavior. That is a hypothesis for a new experiment, not an amendment to EX0004B.

## Provenance

- Protocol SHA-256: `ebbfbc477af7ff24928163b08bb6cafbdac7520b7c0c5915c91ce9eedd7fb94f`
- Patient SHA-256: `066625c083f1c4e9307feba2a11c17bf3d9021e683a66dd432ca4974313e2272`
- Public prompt SHA-256: `22d9d04a32c4b32f3a63f16bcf01de6c14ee16a8e5016012a717fdfa00a93747`
- Autonomous-loop SHA-256: `6adf16a9353165115468c64f302e4717ba2f36b0663cea6d1a6b2c314588a41b`
- Outcome-lock SHA-256: `479e4f741cd2a99e97ab6ee9cceadd98bd848151a2888a6328530cd3e6c66e47`
- Scoring-spec SHA-256: `7e3b2ea948664e9b15b5228cf65626c73be644096d7d01ab53aae4b03e355168`
- Sealed report SHA-256: `2a8392ea665c6fd1f1639b98715ac4eeae612da5e59177ca1bbc099d0bc2499d`
- A1 amendment SHA-256: `385b796540ce20223b65fb91589525a93fe47515467a657d953bc612d5bc81e8`

The archived JSON files, checkpoints, transcripts and event journals are the authoritative evidence. This narrative report is a derived summary.

