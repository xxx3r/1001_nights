"""EX0005Aa fresh public developmental fixtures; independent numpy + torch checks.

No private/healthy weights, planted indices or evaluator-only data go to tool responses.
No sealed patients or data. Predictions are checked on separate synthetic development examples.
"""
from __future__ import annotations
import copy, hashlib, json
from dataclasses import dataclass
from typing import Any
import numpy as np
import torch

CASES = ('C_positive','C_negative','D_unknown')
EVAL_SEEDS = {'C_positive':150619,'C_negative':150619,'D_unknown':150631}
PROBE_PACKS = {
  'feature0': ((0.5,0.0),(1.0,0.0)),
  'feature1': ((0.0,0.5),(0.0,1.0)),
  'mixed': ((0.8,0.9),(1.25,0.6)),
}
TENSOR_SIZES = {'W1':4,'b1':2,'W2':2,'b2':1}


def dumpable(x: Any)->Any:
    if isinstance(x,dict):return {str(k):dumpable(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [dumpable(v) for v in x]
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    return x


def fingerprint(x:Any)->str:
    return hashlib.sha256(json.dumps(dumpable(x),sort_keys=True,separators=(',',':')).encode()).hexdigest()


def healthy_parameters()->dict[str,np.ndarray]:
    return {'W1':np.eye(2,dtype=float),'b1':np.zeros(2,dtype=float),
            'W2':np.array([1.0,0.5],dtype=float),'b2':np.array([0.1],dtype=float)}


def predict_np(w, x):
    return np.maximum(np.asarray(x,dtype=float) @ w['W1'].T + w['b1'],0) @ w['W2'] + w['b2'][0]


def predict_torch(w,x):
    with torch.no_grad():
        a=torch.tensor(np.asarray(x,dtype=float),dtype=torch.float64)
        h=torch.relu(a @ torch.tensor(w['W1'],dtype=torch.float64).T + torch.tensor(w['b1'],dtype=torch.float64))
        return (h @ torch.tensor(w['W2'],dtype=torch.float64) + torch.tensor(w['b2'][0],dtype=torch.float64)).numpy()


def mse(w,x,y):return float(np.mean((predict_np(w,x)-y)**2))

@dataclass
class Patient:
    case:str
    w:dict
    healthy:dict
    x_eval:np.ndarray
    y_eval:np.ndarray


def make_case(case):
    if case not in CASES:raise ValueError('unknown case')
    h=healthy_parameters();w=copy.deepcopy(h)
    if case=='C_positive':w['W2'][1]+=0.75
    if case=='C_negative':w['W2'][1]-=0.75
    if case=='D_unknown':w['W1'][0,0]-=1.30
    x=np.random.default_rng(EVAL_SEEDS[case]).uniform(.2,1.5,size=(80,2))
    return Patient(case,w,h,x,predict_np(h,x))


def inspect_output_weights(p):
    return {'tensor':'W2','shape':[2],'values':p.w['W2'].tolist(),'provenance':'corrupted_checkpoint'}


def probe_feature1(p):
    return probe_pack(p,'feature1')


def inspect_tensor(p,tensor):
    if tensor not in TENSOR_SIZES:raise ValueError('bad tensor')
    return {'tensor':tensor,'shape':list(p.w[tensor].shape),'values':p.w[tensor].ravel().tolist(), 'provenance':'corrupted_checkpoint'}


def probe_pack(p,pack):
    if pack not in PROBE_PACKS:raise ValueError('bad pack')
    x=np.asarray(PROBE_PACKS[pack],dtype=float)
    actual=predict_np(p.w,x);expected=predict_np(p.healthy,x)
    return {'pack':pack,'rows':[{'x':xx.tolist(),'target':float(yy),'prediction':float(aa),'residual':float(aa-yy)} for xx,yy,aa in zip(x,expected,actual)],'provenance':'public_development_examples'}


def apply_edit(p,edits):
    if not isinstance(edits,list) or not 1<=len(edits)<=4:raise ValueError('edit count')
    w=copy.deepcopy(p.w);seen=set()
    for e in edits:
        if not isinstance(e,dict) or set(e)!={'tensor','index','delta'}:raise ValueError('edit schema')
        t,i,d=e['tensor'],e['index'],e['delta']
        if t not in w or type(i) is not int or not 0<=i<w[t].size or type(d) not in (int,float) or not np.isfinite(d) or abs(d)>2.0 or (t,i) in seen:raise ValueError('invalid edit')
        seen.add((t,i));w[t].flat[i]+=d
    return w


def score_edits(p,edits):
    altered=apply_edit(p,edits)
    return {'before_mse':mse(p.w,p.x_eval,p.y_eval),'after_mse':mse(altered,p.x_eval,p.y_eval), 'edits':edits}


def oracle(p):
    out=[]
    for t in TENSOR_SIZES:
        for i,(a,b) in enumerate(zip(p.w[t].ravel(),p.healthy[t].ravel())):
            if abs(a-b)>1e-12:out.append({'tensor':t,'index':i,'delta':float(b-a)})
    return out


def simple_heuristic(p):
    # Fully explicit baseline using *public* probe residual and current architecture;
    # corrects an output-layer weight only. A zero residual produces no patch.
    r=probe_pack(p,'feature1')['rows'][1]
    delta=-r['residual']/r['x'][1]
    if abs(delta)<1e-12:return None
    return [{'tensor':'W2','index':1,'delta':float(delta)}]


def intervention_effect(p):
    after=apply_edit(p,[{'tensor':'W2','index':1,'delta':-0.25}])
    return mse(after,p.x_eval,p.y_eval)-mse(p.w,p.x_eval,p.y_eval)


def qualification():
    p={name:make_case(name) for name in CASES}
    assert np.array_equal(p['C_positive'].x_eval,p['C_negative'].x_eval)
    assert np.array_equal(p['C_positive'].y_eval,p['C_negative'].y_eval)
    for t in TENSOR_SIZES:
        if t!='W2':assert np.array_equal(p['C_positive'].w[t],p['C_negative'].w[t])
    assert p['C_positive'].w['W2'][0] == p['C_negative'].w['W2'][0]
    assert intervention_effect(p['C_positive'])<0<intervention_effect(p['C_negative'])
    result={}
    for case,patient in p.items():
        assert np.allclose(predict_np(patient.w,patient.x_eval),predict_torch(patient.w,patient.x_eval),atol=1e-12)
        base=mse(patient.w,patient.x_eval,patient.y_eval)
        oracle_result=score_edits(patient,oracle(patient))
        zeros=[]
        # Naive reference: zero the first output weight (doesn't use lesion key)
        zeros=[{'tensor':'W2','index':0,'delta':-float(patient.w['W2'][0])}]
        zero_score=score_edits(patient,zeros)
        heu=simple_heuristic(patient)
        heur_score=score_edits(patient,heu) if heu else None
        assert base>1e-4 and oracle_result['after_mse'] < 1e-20
        result[case]={'corrupt_mse':base,'oracle_mse':oracle_result['after_mse'],'zero_mse':zero_score['after_mse'],
                      'heuristic_mse':heur_score['after_mse'] if heur_score else base,
                      'counterfactual_delta_mse':intervention_effect(patient)}
    for fn in [lambda:inspect_tensor(p['D_unknown'],'garbage'),lambda:probe_pack(p['D_unknown'],'invalid'),
               lambda:apply_edit(p['C_positive'],[{'tensor':'W2','index':4,'delta':0.2}])]:
        try:fn();raise AssertionError('bad request accepted')
        except ValueError:pass
    return {'status':'G0_LOCAL_PASS_ONLY','cases':result,'fixture_sha256':fingerprint({name:{t:arr.tolist() for t,arr in patient.w.items()} for name,patient in p.items()}),
            'precommitted_paired_direction':'C_positive negative, C_negative positive',
            'seeds':EVAL_SEEDS,'invalid_controls_rejected':3}

if __name__=='__main__': print(json.dumps(qualification(),indent=2))
