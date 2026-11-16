"""EX0005A public synthetic instrument and evaluator. No sealed cases.

The model sees only tool-returned values, not oracle, healthy or lesion metadata.
Run `python ex0005a_public.py` for local checker qualification.
"""
from __future__ import annotations
import copy, hashlib, json
from dataclasses import dataclass
from typing import Any
import numpy as np
import torch

SEEDS = {"p1_eval": 150511, "p2_eval": 150527, "p1_probe": 150503}
DIAG_LIMIT_PER_PATIENT = 4
MAX_SCALARS_PER_PATCH = 6
MAX_PATCH_ABS_DELTA = 2.0


def json_safe(obj: Any) -> Any:
    if isinstance(obj, dict): return {str(k): json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)): return [json_safe(v) for v in obj]
    if isinstance(obj, np.ndarray): return obj.tolist()
    if isinstance(obj, np.generic): return obj.item()
    return obj


def canonical_hash(payload: Any) -> str:
    return hashlib.sha256(json.dumps(json_safe(payload), sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def params() -> dict[str, np.ndarray]:
    return {"W1": np.eye(2, dtype=float), "b1": np.zeros(2),
            "W2": np.array([1.0, 0.5]), "b2": np.array([0.1])}


def predict_torch(w: dict, x: np.ndarray) -> np.ndarray:
    with torch.no_grad():
        t = torch.tensor(x, dtype=torch.float64)
        h = torch.relu(t @ torch.tensor(w["W1"], dtype=torch.float64).T + torch.tensor(w["b1"], dtype=torch.float64))
        out = h @ torch.tensor(w["W2"], dtype=torch.float64) + torch.tensor(w["b2"], dtype=torch.float64)[0]
        return out.numpy()


def predict_numpy(w: dict, x: np.ndarray) -> np.ndarray:
    return np.maximum(x @ w["W1"].T + w["b1"], 0) @ w["W2"] + w["b2"][0]


def mse(w: dict, x: np.ndarray, y: np.ndarray) -> float:
    return float(np.mean((predict_torch(w, x) - y)**2))


def rows(seed: int, n: int = 80) -> np.ndarray:
    return np.random.default_rng(seed).uniform(0.2, 1.5, size=(n, 2))


def and_predict(weights: tuple[float, float, float, float, float]) -> np.ndarray:
    a, b, bias, out_w, out_b = weights
    x = np.array([[0,0], [0,1], [1,0], [1,1]], dtype=float)
    return np.maximum(0, x @ np.array([a,b]) + bias)*out_w + out_b


def score_and(weights: tuple[float, ...], tol: float = 1e-8) -> dict:
    assert len(weights) == 5 and all(np.isfinite(weights))
    got = and_predict(weights)
    target = np.array([0,0,0,1], dtype=float)
    return {"outputs": got.tolist(), "max_abs_error": float(np.max(np.abs(got-target))),
            "pass": bool(np.allclose(got, target, atol=tol, rtol=0))}


@dataclass
class Patient:
    name: str
    w: dict
    healthy: dict
    x_eval: np.ndarray
    y_eval: np.ndarray
    x_probe: np.ndarray
    y_probe: np.ndarray


def make_patient(name: str) -> Patient:
    if name not in ("P1_plus", "P1_minus", "P2"):
        raise ValueError("unknown public case")
    healthy = params()
    w = copy.deepcopy(healthy)
    if name == "P1_plus": w["W2"][0] += .75
    elif name == "P1_minus": w["W2"][0] -= .75
    elif name == "P2": w["W1"][0, 0] -= .60
    seed = SEEDS["p1_eval"] if name.startswith("P1") else SEEDS["p2_eval"]
    x_eval = rows(seed)
    # Same input and target data for the two causal-contrast variants.
    x_probe = np.array([[.5,0.], [1.,0.], [1.5,0.], [0.,.5], [0.,1.], [1.,1.]], dtype=float)
    return Patient(name,w,healthy,x_eval,predict_numpy(healthy,x_eval),x_probe,predict_numpy(healthy,x_probe))


def probe_examples(p: Patient, regime: str, indices: list[int]) -> dict:
    regimes = {"feature0": [0,1,2], "feature1": [3,4], "mixed": [5]}
    if regime not in regimes or not isinstance(indices,list) or not indices or len(indices)>3:
        raise ValueError("invalid regime or indices")
    if any(type(i) is not int or i not in regimes[regime] for i in indices):
        raise ValueError("out of range for regime")
    values = predict_torch(p.w,p.x_probe[indices]); targets=p.y_probe[indices]
    return {"regime": regime, "rows": [{"index":i,"x":p.x_probe[i].tolist(),"target":float(t),"prediction":float(v),"residual":float(v-t)} for i,v,t in zip(indices,values,targets)],"provenance":"public development probe; not sealed"}


def inspect_weights(p: Patient, tensor: str, start: int, count: int) -> dict:
    if tensor not in ("W1","b1","W2","b2") or type(start) is not int or type(count) is not int or count<=0 or count>4:
        raise ValueError("invalid tensor/start/count")
    a = p.w[tensor]; flat=a.ravel()
    if start < 0 or start+count>len(flat): raise ValueError("tensor index out of bounds")
    return {"tensor":tensor,"shape":list(a.shape),"flat_start":start,"values":flat[start:start+count].tolist(),"provenance":"current corrupted checkpoint"}


def apply_patch(p: Patient, patch: list[dict]) -> dict:
    if not isinstance(patch,list) or not patch or len(patch)>MAX_SCALARS_PER_PATCH: raise ValueError("invalid patch edit count")
    w=copy.deepcopy(p.w);seen=set()
    for edit in patch:
        if not isinstance(edit,dict) or set(edit)!={"tensor","index","delta"}: raise ValueError("patch requires tensor/index/delta")
        t,i,d=edit["tensor"],edit["index"],edit["delta"]
        if t not in w or type(i) is not int or type(d) not in (float,int) or not np.isfinite(d) or abs(d)>MAX_PATCH_ABS_DELTA: raise ValueError("invalid patch field")
        if i<0 or i>=w[t].size or (t,i) in seen: raise ValueError("bad or duplicate index")
        seen.add((t,i));w[t].flat[i]+=d
    return w


def oracle_patch(p: Patient) -> list[dict]:
    out=[]
    for t in p.w:
        for i,(a,b) in enumerate(zip(p.w[t].ravel(), p.healthy[t].ravel())):
            if abs(a-b)>1e-12:out.append({"tensor":t,"index":i,"delta":float(b-a)})
    return out


def heuristic_patch(p: Patient) -> list[dict]:
    # Public, simple algebraic diagnostic baseline. Fix first-output feature response
    # via output-layer coefficient; not designed to restore the internal mechanism.
    r=probe_examples(p,"feature0",[1])["rows"][0]
    slope_err=r["residual"] / r["x"][0]
    return [{"tensor":"W2","index":0,"delta":-slope_err}]


def score_patch(p: Patient, patch: list[dict]) -> dict:
    out=apply_patch(p,patch)
    before=mse(p.w,p.x_eval,p.y_eval);after=mse(out,p.x_eval,p.y_eval)
    return {"mse_before":before,"mse_after":after,"improvement":before-after,"patch":patch}


def prediction_delta(p: Patient, delta: float=-0.25) -> float:
    trial=apply_patch(p,[{"tensor":"W2","index":0,"delta":delta}])
    return mse(trial,p.x_eval,p.y_eval)-mse(p.w,p.x_eval,p.y_eval)


def qualification() -> dict:
    # Independent analytical P0 solution, plus deliberately wrong all-zero negative.
    p0=score_and((1,1,-1,1,0))
    p0bad=score_and((0,0,0,0,0))
    if not p0["pass"] or p0bad["pass"]: raise AssertionError("P0 checker flawed")
    patients={n:make_patient(n) for n in ("P1_plus","P1_minus","P2")}
    results={}
    for name,p in patients.items():
        x=p.x_eval
        assert np.allclose(predict_torch(p.healthy,x),predict_numpy(p.healthy,x),atol=1e-12)
        assert np.allclose(predict_torch(p.w,x),predict_numpy(p.w,x),atol=1e-12)
        before=mse(p.w,x,p.y_eval)
        oracle=score_patch(p,oracle_patch(p))
        heuristic=score_patch(p,heuristic_patch(p))
        # No-edit and direct-zero controls are deliberately included.
        zero=[{"tensor":"W2","index":0,"delta":-float(p.w["W2"][0])}]
        zero_score=score_patch(p,zero)
        assert before>1e-4 and oracle["mse_after"]<1e-20
        results[name]={"corrupt_mse":before,"oracle_mse":oracle["mse_after"],
                       "no_edit_mse":before,"zero_mse":zero_score["mse_after"],
                       "heuristic_mse":heuristic["mse_after"],
                       "decrease_w2_0_0p25_delta_mse":prediction_delta(p)}
    assert results["P1_plus"]["decrease_w2_0_0p25_delta_mse"] < 0
    assert results["P1_minus"]["decrease_w2_0_0p25_delta_mse"] > 0
    for malformed in [lambda:inspect_weights(patients["P1_plus"],"W2",2,1),
                      lambda:probe_examples(patients["P1_plus"],"feature0",[4]),
                      lambda:apply_patch(patients["P1_plus"],[{"tensor":"W2","index":0,"delta":5.}])]:
        try: malformed(); raise AssertionError("malformed call accepted")
        except ValueError: pass
    # Deliberately incomplete/aborted response simulation cannot count as G1 success.
    simulated_incomplete={"status":"incomplete","output":[]}
    assert simulated_incomplete["status"]!="completed"
    return {"status":"G0_LOCAL_PASS_ONLY","seeds":SEEDS,"p0_oracle":p0,"p0_bad":p0bad,
            "cases":results,"paired_prediction": "delta_mse(P1_plus)<0; delta_mse(P1_minus)>0",
            "malformed_requests_rejected":3,"simulated_truncation_rejected":True,
            "public_fixture_fingerprint":canonical_hash({n:{t:a.tolist() for t,a in p.w.items()} for n,p in patients.items()}),
            "live_model_tests":"NOT RUN"}


if __name__=="__main__":
    print(json.dumps(qualification(),indent=2,sort_keys=True))
