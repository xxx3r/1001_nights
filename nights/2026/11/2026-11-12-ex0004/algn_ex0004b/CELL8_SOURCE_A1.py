
# EX0004B — Cell 8: Autonomous-loop preflight
# Mock responses ONLY. No Qwen generation or C06 probes.

import os
import json
import hashlib
import marshal
from copy import deepcopy
from pathlib import Path

print("🌒 EX0004B — AUTONOMOUS LOOP PREFLIGHT")
print("=" * 60)

assert B_MANIFEST["teacher_status"] == "LOADED_NOT_EXPOSED"
assert B_MANIFEST["execution_status"] == "MOCK_PREFLIGHT_PASS"
assert b_file_sha(B_CORRUPT_PATH) == B_CORRUPT_SHA
assert b_file_sha(B_PUBLIC_GUIDE_PATH) == B_PUBLIC_GUIDE_SHA
assert b_file_sha(B_TEACHER_RECEIPT_PATH) == B_RUNTIME_SHA

# 1. Complete neutral JSON example for diagnosis submission.
# These are FORMAT examples, not evidence or recommendations.
B_DIAGNOSIS_EXAMPLE = {
    "tool": "submit_diagnosis",
    "fault_A": {
        "layer": "fc1",
        "neuron": 0,
        "input_feature": 0
    },
    "fault_B": {
        "layer": "fc2",
        "neuron": 0,
        "source_neuron": 0
    },
    "predictions": {
        "isolated_effect_rank": "A_gt_B",
        "interaction_sign": "positive",
        "nuisance_restoration": "unchanged"
    },
    "confidence": 0.5,
    "mechanism": "FORMAT EXAMPLE ONLY. Not a diagnosis.",
    "initial_patch": []
}

B_NEUTRAL_EDIT = {
    "tensor": "readout.bias",
    "index": [0],
    "delta": 0.01
}

assert b_validate_action(
    B_DIAGNOSIS_EXAMPLE, "diagnosis"
) == "submit_diagnosis"

assert b_validate_action({
    "tool": "patch_trial",
    "edits": [B_NEUTRAL_EDIT]
}, "repair") == "patch_trial"

# 2. Arm-specific instructions, frozen BEFORE live exposure.
B_SYSTEM_PROMPTS = {
    "diagnosis_first": (
        "You are a blinded neural-network investigator. "
        "Your task is to diagnose two planted fault regions, "
        "predict their isolated and interacting causal effects, "
        "and then attempt a sparse weight repair. "
        "Use only the permitted JSON actions. "
        "Submit your diagnosis before any patch trial. "
        "After submitting it, use patch_trial or submit_patch. "
        "You may submit a diagnosis before exhausting probes. "
        "When probes are exhausted, submit your diagnosis. "
        "Uncertainty is permitted; do not invent observations. "
        "Output exactly ONE JSON object per turn, without "
        "Markdown fences or additional explanatory text. "
        "Do not request arbitrary Python or filesystem access."
    ),
    "repair_only": (
        "You are a neural-network weight-repair investigator. "
        "Your task is to improve a corrupted network using "
        "bounded diagnostic observations and sparse weight edits. "
        "You do not need to submit a mechanistic diagnosis. "
        "You may use patch_trial or submit_patch immediately. "
        "All patch deltas are relative to the original corrupted "
        "checkpoint, not to a previous trial. "
        "Use only permitted JSON actions. "
        "Output exactly ONE JSON object per turn, without "
        "Markdown fences or additional explanatory text. "
        "Do not request arbitrary Python or filesystem access."
    )
}

def b_public_prompt_for_arm(arm):
    guide = deepcopy(B_PUBLIC_GUIDE)

    if arm == "diagnosis_first":
        guide["diagnosis_submission_example"] = (
            B_DIAGNOSIS_EXAMPLE
        )
        guide["allowed_actions"] = [
            *B_DIAGNOSTIC_TOOLS,
            "submit_diagnosis",
            "patch_trial",
            "submit_patch"
        ]
        guide["phase_rule"] = (
            "patch_trial and submit_patch are unavailable "
            "until submit_diagnosis is accepted."
        )
    else:
        guide.pop("diagnosis_fields", None)
        guide.pop("diagnosis_predictions", None)
        guide["rules"]["diagnosis_before_patch_feedback"] = False
        guide["allowed_actions"] = [
            *B_DIAGNOSTIC_TOOLS,
            "patch_trial",
            "submit_patch"
        ]
        guide["phase_rule"] = (
            "No diagnosis submission is required or allowed."
        )

    guide["patch_trial_example"] = {
        "tool": "patch_trial",
        "edits": [B_NEUTRAL_EDIT]
    }
    guide["final_patch_example"] = {
        "tool": "submit_patch",
        "edits": []
    }
    guide["example_warning"] = (
        "Examples demonstrate syntax only. They are not "
        "observations, diagnoses or recommended repairs."
    )
    return guide


B_INITIAL_MESSAGES = {}

for arm in ("diagnosis_first", "repair_only"):
    B_INITIAL_MESSAGES[arm] = [
        {
            "role": "system",
            "content": B_SYSTEM_PROMPTS[arm]
        },
        {
            "role": "user",
            "content": (
                "FROZEN TOOL AND TASK CONTRACT:\n"
                + json.dumps(
                    b_public_prompt_for_arm(arm),
                    indent=2
                )
                + "\n\nChoose your first permitted JSON action."
            )
        }
    ]

B_PROMPT_RECORD = {
    "version": "EX0004B_PROMPTS_V1",
    "initial_messages": B_INITIAL_MESSAGES,
    "model_revision": B_MODEL_REVISION,
    "generation": B_GENERATION,
}

B_PROMPT_PATH = ROOT / "FROZEN_TEACHER_PROMPTS_V1.json"
B_PROMPT_SHA = b_freeze_record(
    B_PROMPT_PATH, B_PROMPT_RECORD
)

# Tokenizer preflight without model generation.
end_think_id = B_QWEN_TOKENIZER.convert_tokens_to_ids(
    "</think>"
)

assert isinstance(end_think_id, int)
assert end_think_id >= 0

for arm, messages in B_INITIAL_MESSAGES.items():
    rendered = B_QWEN_TOKENIZER.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=True
    )
    assert isinstance(rendered, str)
    assert len(rendered) > 100
    assert "C06" not in rendered
    assert "HEALTHY_PRIVATE.pt" not in rendered

print("Frozen public prompts: 2 arms")
print("Complete diagnosis JSON example: PASS")
print("Canonical tool names: PASS")
print("Qwen chat-template rendering: PASS")

# 3. Deterministic per-turn sampling seeds.
# Do not reuse the identical seed for every turn.
def b_turn_seed(arm, turn_number):
    base = (
        B_SEEDS["diagnosis_generation"]
        if arm == "diagnosis_first"
        else B_SEEDS["repair_only_generation"]
    )
    material = f"{base}|{arm}|turn={turn_number}"
    digest = hashlib.sha256(material.encode()).digest()
    return int.from_bytes(digest[:8], "big") % (2**31 - 1) + 1


# 4. Actual Qwen generation adapter.
# DEFINED HERE; NEVER CALLED IN THIS PREFLIGHT.
def b_live_decision(messages, arm, turn_number):
    prompt = B_QWEN_TOKENIZER.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=True
    )

    prompt_hash = hashlib.sha256(
        prompt.encode()
    ).hexdigest()

    inputs = B_QWEN_TOKENIZER(
        [prompt],
        return_tensors="pt"
    ).to("cuda:0")

    seed = b_turn_seed(arm, turn_number)

    with torch.random.fork_rng(devices=[0]):
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

        with torch.inference_mode():
            output = B_QWEN_MODEL.generate(
                **inputs,
                max_new_tokens=B_GENERATION["max_new_tokens"],
                do_sample=B_GENERATION["do_sample"],
                temperature=B_GENERATION["temperature"],
                top_p=B_GENERATION["top_p"],
                top_k=B_GENERATION["top_k"],
                pad_token_id=B_QWEN_TOKENIZER.eos_token_id
            )

    new_tokens = output[0][
        inputs["input_ids"].shape[1]:
    ].tolist()

    completed = end_think_id in new_tokens

    if completed:
        split = (
            len(new_tokens) - 1
            - new_tokens[::-1].index(end_think_id)
        )
        final_text = B_QWEN_TOKENIZER.decode(
            new_tokens[split + 1:],
            skip_special_tokens=True
        ).strip()
    else:
        final_text = ""

    return {
        "text": final_text,
        "thinking_completed": completed,
        "generated_tokens": len(new_tokens),
        "generation_seed": seed,
        "prompt_sha256": prompt_hash,
        "completion_sha256": hashlib.sha256(
            B_QWEN_TOKENIZER.decode(
                new_tokens,
                skip_special_tokens=False
            ).encode()
        ).hexdigest(),
    }


# 5. Append-only, hash-chained event journal.
def b_append_journal(path, kind, body):
    path = Path(path)

    previous_hash = None
    if path.exists():
        lines = path.read_text().splitlines()
        if lines:
            previous_hash = json.loads(
                lines[-1]
            )["sha256"]

    record = {
        "kind": kind,
        "body": body,
        "previous_hash": previous_hash
    }

    payload = json.dumps(
        record, sort_keys=True, allow_nan=False
    )

    record["sha256"] = hashlib.sha256(
        payload.encode()
    ).hexdigest()

    with path.open("a") as stream:
        stream.write(
            json.dumps(record, sort_keys=True) + "\n"
        )
        stream.flush()
        os.fsync(stream.fileno())


def b_verify_journal(path):
    events = [
        json.loads(line)
        for line in Path(path).read_text().splitlines()
    ]

    previous_hash = None
    for event in events:
        assert event["previous_hash"] == previous_hash
        unsigned = dict(event)
        stored = unsigned.pop("sha256")

        calculated = hashlib.sha256(
            json.dumps(
                unsigned,
                sort_keys=True,
                allow_nan=False
            ).encode()
        ).hexdigest()

        assert stored == calculated
        previous_hash = stored

    return len(events)


# 6. One fixed runner for BOTH teacher arms.
# No human prompt edits between its actions.
def b_run_arm(arm, backend, decide, output_dir):
    output_dir = Path(output_dir)
    assert not output_dir.exists(), (
        "Arm already has records. Never silently restart."
    )
    output_dir.mkdir(parents=True)

    journal = output_dir / "events.jsonl"
    transcript = output_dir / "transcript.json"

    session = BSession(backend, arm)
    messages = deepcopy(B_INITIAL_MESSAGES[arm])

    status = "ACTION_LIMIT_REACHED"

    for turn in range(1, 21):
        # Record intent BEFORE generation.
        b_append_journal(journal, "TURN_START", {
            "turn": turn,
            "arm": arm,
            "phase": session.phase,
            "diagnostic_calls": session.diagnostic_calls,
            "patch_trials": session.patch_trials,
        })

        decision = decide(messages, arm, turn)

        # Persist output BEFORE dispatching any tool.
        b_append_journal(journal, "GENERATION", {
            "turn": turn,
            "decision": decision,
        })

        if not decision["thinking_completed"]:
            status = "INCOMPLETE_GENERATION"
            break

        # One submitted action, one dispatch.
        response = session.dispatch(decision["text"])

        b_append_journal(journal, "TOOL_RESULT", {
            "turn": turn,
            "response": response,
            "phase_after": session.phase,
            "diagnostic_calls": session.diagnostic_calls,
            "patch_trials": session.patch_trials,
            "session_event_hash": session.events[-1]["sha256"],
        })

        messages.append({
            "role": "assistant",
            "content": decision["text"]
        })

        # Fixed feedback template; no adaptive coaching.
        messages.append({
            "role": "user",
            "content": (
                "TOOL RESPONSE:\n"
                + json.dumps(response, sort_keys=True)
                + "\nCURRENT STATE:\n"
                + json.dumps({
                    "phase": session.phase,
                    "diagnostic_calls_remaining":
                        max(0, 12-session.diagnostic_calls),
                    "patch_trials_remaining":
                        max(0, 2-session.patch_trials),
                    "total_actions_remaining":
                        max(0, 20-session.total_actions)
                }, sort_keys=True)
                + "\nChoose one permitted JSON action."
            )
        })

        # Save complete current conversation after each action.
        snapshot = {
            "arm": arm,
            "turn": turn,
            "messages": messages,
            "phase": session.phase,
            "diagnostic_calls": session.diagnostic_calls,
            "patch_trials": session.patch_trials,
            "diagnosis": session.diagnosis,
            "final_patch": session.final_patch,
        }

        temporary = transcript.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(snapshot, indent=2, allow_nan=False)
        )
        temporary.replace(transcript)

        if session.phase == "complete":
            status = "COMPLETED"
            break

    summary = {
        "arm": arm,
        "status": status,
        "diagnostic_calls": session.diagnostic_calls,
        "patch_trials": session.patch_trials,
        "total_actions": session.total_actions,
        "diagnosis_committed": session.diagnosis is not None,
        "final_patch_committed": session.final_patch is not None,
        "diagnosis": session.diagnosis,
        "final_patch": session.final_patch,
        "sealed_evaluation": "UNOPENED",
    }

    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, allow_nan=False)
    )

    b_append_journal(journal, "FINAL_STATUS", summary)
    b_verify_journal(journal)

    return summary


# 7. Mock a complete response-generation sequence.
# No actual Qwen output and no C06 patient observations.
B_MOCK_ACTIONS = {
    "diagnosis_first": [
        {
            "tool": "weights",
            "tensor": "fc1.bias",
            "start": 0,
            "count": 6
        },
        {
            "tool": "activations",
            "regime": "shift"
        },
        B_DIAGNOSIS_EXAMPLE,
        {
            "tool": "patch_trial",
            "edits": [B_NEUTRAL_EDIT]
        },
        {
            "tool": "submit_patch",
            "edits": []
        },
    ],
    "repair_only": [
        {
            "tool": "examples",
            "regime": "id",
            "indices": [0, 1]
        },
        {
            "tool": "patch_trial",
            "edits": [B_NEUTRAL_EDIT]
        },
        {
            "tool": "submit_patch",
            "edits": []
        },
    ]
}

def b_mock_decision(messages, arm, turn):
    raw = json.dumps(B_MOCK_ACTIONS[arm][turn-1])
    return {
        "text": raw,
        "thinking_completed": True,
        "generated_tokens": 0,
        "generation_seed": b_turn_seed(arm, turn),
        "prompt_sha256": hashlib.sha256(
            json.dumps(messages, sort_keys=True).encode()
        ).hexdigest(),
        "completion_sha256": hashlib.sha256(
            raw.encode()
        ).hexdigest(),
    }


B_MOCK_ROOT = ROOT / "MOCK_AUTONOMOUS_PREFLIGHT_V1"
assert not B_MOCK_ROOT.exists()

mock_diagnosis_result = b_run_arm(
    "diagnosis_first",
    mock_backend,
    b_mock_decision,
    B_MOCK_ROOT / "diagnosis_first"
)

mock_repair_result = b_run_arm(
    "repair_only",
    mock_backend,
    b_mock_decision,
    B_MOCK_ROOT / "repair_only"
)

assert mock_diagnosis_result["status"] == "COMPLETED"
assert mock_diagnosis_result["diagnostic_calls"] == 2
assert mock_diagnosis_result["patch_trials"] == 1
assert mock_diagnosis_result["diagnosis_committed"]
assert mock_diagnosis_result["final_patch_committed"]

assert mock_repair_result["status"] == "COMPLETED"
assert mock_repair_result["diagnostic_calls"] == 1
assert mock_repair_result["patch_trials"] == 1
assert mock_repair_result["final_patch_committed"]

# 8. Freeze runner configuration and implementation fingerprint.
B_RUNNER_CODE_SHA = hashlib.sha256(
    marshal.dumps(b_run_arm.__code__)
    + marshal.dumps(b_live_decision.__code__)
).hexdigest()

B_LOOP_SPEC = {
    "version": "EX0004B_AUTONOMOUS_LOOP_V1",
    "prompt_sha256": B_PROMPT_SHA,
    "code_sha256": B_RUNNER_CODE_SHA,
    "maximum_actions_per_arm": 20,
    "max_diagnostic_calls": 12,
    "max_patch_trials": 2,
    "per_turn_seed_derivation": "SHA256(base|arm|turn)",
    "incomplete_generation_policy": "STOP_NO_RETRY",
    "event_journal": "APPEND_ONLY_HASH_CHAIN",
    "feedback": "FIXED_TEMPLATE",
    "mock_diagnosis_status": mock_diagnosis_result["status"],
    "mock_repair_status": mock_repair_result["status"],
    "teacher_exposed": False,
}

B_LOOP_SPEC_PATH = ROOT / "AUTONOMOUS_LOOP_SPEC_V1.json"
B_LOOP_SHA = b_freeze_record(
    B_LOOP_SPEC_PATH, B_LOOP_SPEC
)

B_MANIFEST["loop_status"] = "FULL_PREFLIGHT_PASS"
B_MANIFEST["loop_sha256"] = B_LOOP_SHA
B_MANIFEST["runner_code_sha256"] = B_RUNNER_CODE_SHA

print("\nAUTONOMOUS PREFLIGHT RESULTS")
print("-" * 60)
print("Diagnosis-first mock: PASS")
print("Repair-only mock: PASS")
print("Complete diagnosis JSON: PASS")
print("Diagnosis before patch feedback: PASS")
print("Final patch commitment: PASS")
print("Per-turn event journaling: PASS")
print("Journal hash-chain verification: PASS")
print("Complete transcript persistence: PASS")
print("Frozen per-turn seed derivation: PASS")
print("Qwen tokenizer compatibility: PASS")
print("Actual Qwen generations: 0")
print("Actual C06 observations: 0")
print("Sealed evaluation accessed: NO")

print("\nFROZEN PROMPT SHA-256:")
print(B_PROMPT_SHA)
print("\nFROZEN LOOP SHA-256:")
print(B_LOOP_SHA)

print("\n✅ CELL 8: AUTONOMOUS LOOP PREFLIGHT PASSED")