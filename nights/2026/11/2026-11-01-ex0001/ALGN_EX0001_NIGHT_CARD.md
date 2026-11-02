# ALGN-EX0001 | The Key Beneath the Blanket

**Execution:** 2026-11-01 (America/Denver); originally planned for 2026-10-29  
**Status:** Experimental work closed; evidence reported frozen in Colab  
**Question:** Can a small RL agent use a key conditionally, rather than merely follow a successful familiar route?

**Hypotheses.** H1 predicted key collection for locked doors and a direct route for open doors. H2 predicted inappropriate key collection or other habitual behavior despite changed door requirements. A separate generalization probe relocated the key; a proposed object-permanence test required memory-sensitive controls.

**Human-owned contribution and assistance.** The researcher selected the question, predicted easier open-door learning, distinguished goal attainment from efficiency, and identified observation fairness as crucial. The assistant drafted the Python implementation and most tests; assistance level **D (AI-drafted)**, not independent coding mastery.

**Method.** A six-location deterministic graphworld offered seven actions and 11 observable input features. A 1,671-parameter feedforward DQN was trained on 2,200 episodes, split equally between open and locked doors, with the key always in the left alcove. The frozen greedy policy was evaluated without retraining. Single model seed: 1001; training sampling seed: 2718. The notebook retains code and outputs.

**Results.** Familiar locked door: goal reached in the optimal six actions, with key. Familiar open door: goal reached in the optimal three actions, without key. Visible key relocated right: agent went left, attempted pickup 18 times, and timed out after 20 actions (return −2.0). Input-level Q-values changed with observed key location but did not change the preferred actions. Starting at a locked door without a key, the agent recovered optimally in six additional actions; with a key, it exited in one. In both D0 concealment trials, it attempted the locked door repeatedly and failed.

**Verdict and limitations.** **A/B PASS; C FAIL; interrupted-route controls PASS; D0 operational FAIL; full memory-controlled D NOT RUN.** These outcomes describe one deterministic policy, not a population estimate. D0 confounds an unseen observation combination with missing memory; a feedforward network cannot retain the preview. The results do not identify policy confounding or establish object permanence. An independent replication or separate adjudicator has not yet verified the recorded run.

**One acquired insight:** Familiar-route success, input sensitivity, and robust transfer are different properties.  
**Next deficit:** Build a matched memory-capable control with balanced key placement and trained concealment conditions.  
**Stop:** No further training or code changes for this night.
