"""EX0005A Responses API live runner. Public data only; no credential logging.

Requires human_fields.json completed BEFORE launch. Designed for Colab runtime.
Costs API tokens. Source and human fields are hashed before model contact.
Never run automatically on import.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, os, pathlib, re, sys, traceback
from zoneinfo import ZoneInfo
import numpy as np
from ex0005a_public import (make_patient, qualification, inspect_weights, probe_examples,
                           score_and, score_patch, prediction_delta, oracle_patch, heuristic_patch,
                           canonical_hash, DIAG_LIMIT_PER_PATIENT)

MODEL = 'gpt-6-luna'
MAX_RESPONSES = 16
MAX_TOTAL_INPUT_TOKENS = 120000
MAX_TOTAL_OUTPUT_TOKENS = 24000
MAX_OUTPUT_TOKENS = 1800
REASONING = {'effort': 'low'}
PREDICTION_TOL = 1e-9
RESULT_DIR = pathlib.Path('ex0005a_receipts')
HUMAN_KEYS = ('human_predicted_failure','human_predicted_contrast',
              'human_false_positive_test','human_unsupported_mechanism')
TOOLS = [
    {'type':'function','name':'inspect_weights','description':'Read a bounded flat interval of CURRENT network tensor values. No healthy weights.',
     'strict':True,'parameters':{'type':'object','properties':{
         'tensor':{'type':'string','enum':['W1','b1','W2','b2']},
         'start':{'type':'integer'},'count':{'type':'integer'}},
         'required':['tensor','start','count'],'additionalProperties':False}},
    {'type':'function','name':'probe_examples','description':'Measure current model predictions, public target values and residuals on tiny fixed development examples.',
     'strict':True,'parameters':{'type':'object','properties':{
         'regime':{'type':'string','enum':['feature0','feature1','mixed']},
         'indices':{'type':'array','items':{'type':'integer'}}},
         'required':['regime','indices'],'additionalProperties':False}}
]
BASE_INSTRUCTIONS = '''You are investigating ONE public synthetic 2-input, 2-ReLU-hidden, 1-linear-output network. Input features x0,x1 are nonnegative; W1 is shape (2,2), b1 shape (2,), W2 shape (2,), b2 shape (1,). There is one planted numerical corruption, but you do not know its location or sign. You have NO access to the healthy weights or private evaluator. Use only numerical tool evidence. You must take at least one valid observation using EACH of the two tools before diagnosis. All calls are read-only. Do not ask for a patch trial. Commit once, and do not infer mechanisms from successful function scores alone.'''
OBS_PROMPT='''Investigate the present corrupted network. Invoke inspect_weights and probe_examples with specific arguments; use numeric evidence. The final commitment must predict the signed change in mean squared error on an independent public development sample if W2's flat element 0 were DECREASED by exactly 0.25. No patch feedback will be provided before commitment. State your uncertain fault region and optional sparse patch. Do not guess from any formatting example.'''
COMMIT_PROMPT='''Commit your diagnosis now, based only on already returned observations, without further tools. Return JSON ONLY, with exactly these keys: fault_region (e.g. an existing tensor and one flat element in square brackets), uncertainty (low/medium/high), predicted_delta_mse (numeric MSE_after_minus_before when W2[0] is decreased by 0.25), patch (array of at most six {tensor,index,delta} scalar edits, or empty array), explanation (at most 50 words). No extra keys, no code fences. An empty patch represents abstention.'''


def json_text(resp):
    s=getattr(resp,'output_text','') or ''
    try: return json.loads(s)
    except Exception: raise ValueError('model output is not strict JSON')


def validate_commit(obj):
    if not isinstance(obj,dict) or set(obj)!={'fault_region','uncertainty','predicted_delta_mse','patch','explanation'}: raise ValueError('malformed commitment keys')
    fr=obj['fault_region']
    m=re.fullmatch(r'(W1|b1|W2|b2)\[(\d+)\]',fr) if isinstance(fr,str) else None
    lengths={'W1':4,'b1':2,'W2':2,'b2':1}
    if not m or int(m.group(2))>=lengths[m.group(1)]: raise ValueError('invalid fault region')
    if obj['uncertainty'] not in ('low','medium','high'):raise ValueError('invalid uncertainty')
    val=obj['predicted_delta_mse']
    if type(val) not in (float,int) or not np.isfinite(val):raise ValueError('invalid numeric prediction')
    if not isinstance(obj['explanation'],str) or len(obj['explanation'].split())>50:raise ValueError('invalid explanation')
    patch=obj['patch']
    if not isinstance(patch,list) or len(patch)>6: raise ValueError('invalid patch')
    return obj


def safe_response(client, journal, label, **kwargs):
    if sum(row.get('kind')=='api_response' for row in journal) >= MAX_RESPONSES:
        raise RuntimeError('hard cap on model generations reached')
    used_in=sum((row.get('usage') or {}).get('input_tokens',0) for row in journal if row.get('kind')=='api_response')
    used_out=sum((row.get('usage') or {}).get('output_tokens',0) for row in journal if row.get('kind')=='api_response')
    if used_in >= MAX_TOTAL_INPUT_TOKENS or used_out >= MAX_TOTAL_OUTPUT_TOKENS:
        raise RuntimeError('hard cap on token usage reached')
    now=dt.datetime.now(ZoneInfo('America/Denver'))
    if now.date()!=dt.date(2026,11,15) or now.hour>=20:
        raise RuntimeError('hard stop reached; no additional generation')
    resp=client.responses.create(model=MODEL,reasoning=REASONING,
                                 max_output_tokens=MAX_OUTPUT_TOKENS,**kwargs)
    usage=getattr(resp,'usage',None)
    journal.append({'kind':'api_response','phase':label,
                    'id':getattr(resp,'id',None),'model':getattr(resp,'model',None),
                    'status':getattr(resp,'status',None),'incomplete_details':str(getattr(resp,'incomplete_details',None)),
                    'usage':usage.model_dump() if hasattr(usage,'model_dump') else None,
                    'output_items':[(getattr(item,'type',None),getattr(item,'name',None)) for item in resp.output]})
    if getattr(resp,'status',None)!='completed':
        raise RuntimeError('incomplete/failed response; not a valid observation or commitment')
    return resp


def p0_run(client,journal):
    r=safe_response(client,journal,'P0',
        instructions='Return exactly one JSON object. No tools are available.',
        input='For a 2-input -> 1 ReLU -> 1 linear scalar network, construct exact Boolean AND outputs on x in {(0,0),(0,1),(1,0),(1,1)}. Return JSON {"weights":[w0,w1,b_hidden,w_out,b_out]}, numeric entries only.')
    try:
        obj=json_text(r)
        if not isinstance(obj,dict) or set(obj)!={'weights'} or not isinstance(obj['weights'],list): raise ValueError('bad P0 result')
        w=obj['weights']
        if len(w)!=5 or any(type(v) not in (float,int) for v in w):raise ValueError('bad weight array')
        return {'valid':True,'model_weights':w,'evaluation':score_and(tuple(w))}
    except Exception as e:return {'valid':False,'error':str(e)}


def tool_dispatch(p, call, journal, label):
    name=getattr(call,'name','?')
    try:
        args=json.loads(call.arguments)
        if not isinstance(args,dict): raise ValueError('expected object args')
        if name=='inspect_weights':
            if set(args)!={'tensor','start','count'}:raise ValueError('bad property set')
            result=inspect_weights(p,**args)
        elif name=='probe_examples':
            if set(args)!={'regime','indices'}:raise ValueError('bad property set')
            result=probe_examples(p,**args)
        else:raise ValueError('unknown function')
        ok=True
    except Exception as e:
        result={'error':type(e).__name__+': '+str(e)};ok=False
    journal.append({'kind':'diagnostic','case':label,'function':name,'arguments':getattr(call,'arguments',''),
                    'valid':ok,'return':result})
    return {'type':'function_call_output','call_id':call.call_id,'output':json.dumps(result,allow_nan=False)},ok


def investigation(client, p, journal, label):
    state={'attempts':0,'valid':0,'kinds':[],'errors':[],'abstain':False,'commit':None,
           'prediction_oracle':prediction_delta(p)}
    last_id=None;next_input=OBS_PROMPT
    for turn in range(DIAG_LIMIT_PER_PATIENT):
        args={'instructions':BASE_INSTRUCTIONS,'input':next_input,'tools':TOOLS,'tool_choice':'required'}
        if last_id:args['previous_response_id']=last_id
        response=safe_response(client,journal,f'{label}_diagnostic_{turn+1}',**args)
        calls=[o for o in response.output if getattr(o,'type',None)=='function_call']
        if not calls:
            state['errors'].append('completed generation without function call')
            return state
        outputs=[]
        for call in calls:
            if state['attempts'] >= DIAG_LIMIT_PER_PATIENT:
                # All emitted calls require replies; reject over-budget requests explicitly.
                outputs.append({'type':'function_call_output','call_id':call.call_id,'output':json.dumps({'error':'diagnostic budget exhausted'})})
                journal.append({'kind':'diagnostic','case':label,'function':call.name,'valid':False,'error':'over budget'})
                state['errors'].append('over budget')
                continue
            state['attempts']+=1
            output,ok=tool_dispatch(p,call,journal,label)
            outputs.append(output)
            if ok:
                state['valid']+=1
                if call.name not in state['kinds']:state['kinds'].append(call.name)
            else:state['errors'].append('invalid '+call.name)
        last_id=response.id;next_input=outputs
        if len(state['kinds'])>=2:break
    if len(state['kinds'])<2:
        state['errors'].append('missing distinct valid tool kinds')
        return state
    final=safe_response(client,journal,f'{label}_commit',
            instructions=BASE_INSTRUCTIONS+' '+COMMIT_PROMPT,
            input=next_input,previous_response_id=last_id,tools=TOOLS,tool_choice='none')
    try:
        obj=validate_commit(json_text(final))
        state['commit']=obj
        state['abstain']=not bool(obj['patch'])
        state['prediction_error']=float(obj['predicted_delta_mse']-state['prediction_oracle'])
        state['prediction_sign_correct']=bool(np.sign(obj['predicted_delta_mse'])==np.sign(state['prediction_oracle']))
        state['mechanism_region_correct']=(obj['fault_region']=={'P1_plus':'W2[0]','P1_minus':'W2[0]','P2':'W1[0]'}[label])
        if obj['patch']:
            # Score only after commitment is frozen; no feedback to investigator.
            try:state['patch_score']=score_patch(p,obj['patch'])
            except Exception as e:state['errors'].append('invalid committed patch '+str(e))
    except Exception as e:state['errors'].append('invalid commitment '+str(e))
    return state


def human_fields(path):
    d=json.loads(pathlib.Path(path).read_text())
    for k in HUMAN_KEYS:
        v=d.get(k)
        if not isinstance(v,str) or len(v.strip())<15 or 'TO FILL' in v.upper() or 'PLACEHOLDER' in v.upper():
            raise ValueError('human-owned field absent: '+k)
    if d.get('assistance_disclosure') not in ['I','H','C','D']:
        raise ValueError('assistance_disclosure required')
    return d


def api_key():
    # Colab secret first; local environment also supported. Never print either.
    key=os.environ.get('OPENAI_API_KEY','')
    if not key:
        try:
            from google.colab import userdata
            key=userdata.get('OPENAI_API_KEY') or ''
        except ImportError:pass
    if not key:raise RuntimeError('OPENAI_API_KEY not available; no live call performed')
    return key


def run_live(cfg):
    from openai import OpenAI
    now=dt.datetime.now(ZoneInfo('America/Denver'))
    if now.date()!=dt.date(2026,11,15) or (now.hour,now.minute)>=(20,0):
        raise RuntimeError('EX0005A live window closed. Preserve NOT RUN; do not extend this night.')
    result_dir=RESULT_DIR
    result_dir.mkdir(exist_ok=True)
    journal=[]
    base=pathlib.Path(__file__).parent
    source_hashes={n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in ('ex0005a_public.py','run_luna.py')}
    # Source, human hypotheses, budgets and oracle-verified fixture fingerprint sealed locally before model contact.
    q=qualification()
    import importlib.metadata, platform
    versions={'python':platform.python_version(),'numpy':np.__version__,
              'torch':importlib.metadata.version('torch'),'openai':importlib.metadata.version('openai')}
    manifest={'datetime_frozen':now.isoformat(),'model_requested':MODEL,'software_versions':versions,
              'api_generation_seed':None,'total_token_caps':{'input':MAX_TOTAL_INPUT_TOKENS,'output':MAX_TOTAL_OUTPUT_TOKENS},'settings':{'reasoning':REASONING,'max_output_tokens':MAX_OUTPUT_TOKENS},
              'response_call_cap':MAX_RESPONSES,'diagnostic_limit_per_case':DIAG_LIMIT_PER_PATIENT,
              'cases':['P1_plus','P1_minus','P2'],'no_sealed_test':True,'precommitted_G0_fixture':q['public_fixture_fingerprint'],
              'source_sha256':source_hashes,'human_fields':cfg,'assistance':cfg['assistance_disclosure']}
    manifest['freeze_sha256']=canonical_hash(manifest)
    (result_dir/'PRE_LIVE_FREEZE.json').write_text(json.dumps(manifest,indent=2,sort_keys=True))
    client=OpenAI(api_key=api_key())
    # This capability read makes no generation and reveals no credential; stop cleanly if not allowed.
    summary={'G0_local':'PASS','model_requested':MODEL,'model_access_check':'NOT VERIFIED',
             'freeze_sha256':manifest['freeze_sha256'],'P0':None,'cases':{},'G1':'NOT RUN','G2':'NOT RUN','G3':'NOT RUN','G4':'NOT RUN','instrument_ready':False}
    try:
        available=client.models.retrieve(MODEL)
        summary['model_access_check']=getattr(available,'id',None)
        summary['P0']=p0_run(client,journal)
        for label in ('P1_plus','P1_minus','P2'):
            # Every case is a fresh, separate model conversation.
            p=make_patient(label)
            summary['cases'][label]=investigation(client,p,journal,label)
        data=summary['cases']
        g1=all(len(data[k]['kinds'])>=2 and data[k]['valid']>=2 for k in ('P1_plus','P2'))
        g3=all(data[k]['commit'] is not None for k in ('P1_plus','P2'))
        # Matched-observation control: the requested diagnostic *types and exact arguments*
        # must match across the sign-flipped pair. Otherwise, differing information or
        # sampling histories confound attribution to the lesion-sign contrast.
        def trace(label):
            return [(j['function'],j['arguments']) for j in journal
                    if j.get('kind')=='diagnostic' and j.get('case')==label and j.get('valid')]
        a,b=trace('P1_plus'),trace('P1_minus')
        matched=bool(a) and a==b
        relevant=any((name=='probe_examples' and json.loads(args)['regime']=='feature0') or
                     (name=='inspect_weights' and json.loads(args)['tensor']=='W2' and
                      json.loads(args)['start']<=0<json.loads(args)['start']+json.loads(args)['count'])
                     for name,args in a)
        summary['paired_observation_contract']={'exact_call_signatures_matched':matched,
                                                'relevant_evidence_requested':relevant,
                                                'controlled_except_for_planted_weight':True}
        pair_commit=all(data[k]['commit'] is not None for k in ('P1_plus','P1_minus'))
        g2=pair_commit and all(data[k]['prediction_sign_correct'] for k in ('P1_plus','P1_minus')) and (data['P1_plus']['commit']['predicted_delta_mse'] < 0 < data['P1_minus']['commit']['predicted_delta_mse'])
        g2_status=('INCONCLUSIVE' if not matched or not relevant else ('PASS' if g2 else 'FAIL'))
        summary.update({'G1':'PASS' if g1 else 'FAIL','G2':g2_status,
                        'G3':'PASS' if g3 else 'FAIL',
                        'G4':'SCORED' if any('patch_score' in d for d in data.values()) else 'NOT RUN',
                        'instrument_ready':bool(g1 and g2 and g3 and matched and relevant)})
    except Exception as e:
        summary['interruption']={'type':type(e).__name__,'message':str(e)}
        # No blanket retry. Incomplete results are still archived.
    finally:
        summary['public_baselines']=q['cases']
        summary['api_responses_logged']=sum(j['kind']=='api_response' for j in journal)
        (result_dir/'ACTION_JOURNAL.json').write_text(json.dumps(journal,indent=2,allow_nan=False))
        (result_dir/'RESULTS.json').write_text(json.dumps(summary,indent=2,allow_nan=False))
    return summary


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--human-fields',default='human_fields.json')
    ap.add_argument('--local-only',action='store_true',help='No API usage; run G0 only.')
    ap.add_argument('--live',action='store_true',help='Explicitly authorize bounded billable calls in live window.')
    args=ap.parse_args()
    if args.local_only:
        print(json.dumps(qualification(),indent=2));return
    if not args.live:ap.error('Choose --local-only or --live; live never starts implicitly.')
    cfg=human_fields(args.human_fields)
    summary=run_live(cfg)
    print(json.dumps({'freeze_sha256':summary['freeze_sha256'], 'G1':summary['G1'],
                      'G2':summary['G2'],'G3':summary['G3'],'G4':summary['G4'],
                      'instrument_ready':summary['instrument_ready'],
                      'receipts':str(RESULT_DIR)},indent=2))

if __name__=='__main__':main()
