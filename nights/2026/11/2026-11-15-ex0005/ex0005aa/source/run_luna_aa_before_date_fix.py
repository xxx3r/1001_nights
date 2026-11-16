"""EX0005Aa new-session, public development-only GPT-6 Luna investigator.

No calls on import. No duplicate live launches. Separate protocol freeze & model contact.
Uses Responses API native tools, exactly one tool call per observation response.
Results persist after EVERY response. API error -> local evidence preserved, no retry.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, importlib.metadata, json, os, pathlib, platform, sys
from zoneinfo import ZoneInfo
import numpy as np
from ex0005aa_public import (make_case, qualification, inspect_output_weights, probe_feature1,
    inspect_tensor, probe_pack, score_edits, oracle, simple_heuristic, intervention_effect,
    TENSOR_SIZES, fingerprint, dumpable)

MODEL='gpt-6-luna'
REASONING={'effort':'low'}
OUTPUT_CAP=1800
MAX_RESPONSES=14
MAX_INPUT_TOKENS=80000
MAX_OUTPUT_TOKENS=24000
DIAG_STEPS_DISCOVERY=4
OUTDIR=pathlib.Path('ex0005aa_receipts')
SOURCE_FILES=['ex0005aa_public.py','run_luna_aa.py']
HISTORICAL_SHA={
 'EX0005A_ACTION_JOURNAL.json':'48d0f918dfc1c0b42a935a3af8f12d2189ed0318a6b72dfdcedd20b1d44ddb72',
 'EX0005A_RESULTS.json':'16bd3d9dd5c9346a06a2b3ea9d2e432f86d42b70264a6cbe4687cd5d85e6178c'
}
PAIR_TOOLS=[
 {'type':'function','name':'inspect_output_weights',
  'description':'Read the two scalar weights of the corrupted network output layer. This returns no healthy or oracle weights.',
  'strict':True,'parameters':{'type':'object','properties':{},'required':[],'additionalProperties':False}},
 {'type':'function','name':'probe_feature1',
  'description':'Observe two FIXED public development rows, feature1 inputs x=[0,0.5] and [0,1.0], with predictions and target residuals. No indices to guess.',
  'strict':True,'parameters':{'type':'object','properties':{},'required':[],'additionalProperties':False}}
]
DISCOVERY_TOOLS=[
 {'type':'function','name':'inspect_weights',
  'description':'Read ONE complete current corrupted tensor, with no healthy values or fault information. W1 has 4 flat elements, b1 has 2, W2 has 2, b2 has 1.',
  'strict':True,'parameters':{'type':'object','properties':{'tensor':{'type':'string','enum':['W1','b1','W2','b2']}},
                             'required':['tensor'],'additionalProperties':False}},
 {'type':'function','name':'probe_examples',
  'description':'Read an entire small, fixed public probe pack with predictions, targets and residuals. Valid packs: feature0, feature1, mixed. No indices.',
  'strict':True,'parameters':{'type':'object','properties':{'pack':{'type':'string','enum':['feature0','feature1','mixed']}},
                             'required':['pack'],'additionalProperties':False}}
]
PAIR_BASE=('You are studying a synthetic 2-input, 2-ReLU-hidden, 1-linear-output network. '
           'No access to the healthy checkpoint. Use only the numeric observations you are given. '
           'This question measures an explicit counterfactual prediction, NOT discovery of a hidden fault. '
           'After observing both tools, predict the change in mean squared error on a separate public development set '
           'if W2 flat index 1 were decreased by exactly 0.25. Do not invent unobserved activations or claim mechanistic proof.')
PAIR_COMMIT=('Using ONLY observed numerical evidence, commit one JSON object with EXACT keys: '
             'predicted_delta_mse (finite number; after minus before), '
             'uncertainty (low/medium/high), explanation (under 70 words). '
             'No code fences, and no additional tools.')
DISCOVERY_BASE=('You are examining a public synthetic network with inputs x0,x1, 2 ReLU hidden units, '
                'one linear output and exactly one planted scalar parameter corruption of unknown location and sign. '
                'Tensor names are W1 (shape 2x2; row-major flattened), b1 (2), W2 (2), b2 (1). '
                'Choose your own bounded numerical diagnostic calls. No healthy weights, oracle or answer keys are available. '
                'A simple output-weight heuristic will be scored as a baseline. '
                'Do not assume the apparent largest weight is the lesion; use input-output evidence.')
DISCOVERY_COMMIT=('Commit now; no further tools. Return EXACT JSON keys: fault_region (format W1[0], b1[1] etc), '
                  'uncertainty (low/medium/high), patch (array of zero to four {tensor,index,delta} scalar edits), '
                  'explanation (max 70 words). Empty patch explicitly abstains. No additional keys or code fences.')


def sha(path):return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()

def atomic_json(path,obj):
    path=pathlib.Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.tmp')
    tmp.write_text(json.dumps(dumpable(obj),indent=2,sort_keys=True,allow_nan=False))
    tmp.replace(path)

def load_json(path):return json.loads(pathlib.Path(path).read_text())

def human_fields(filename):
    data=load_json(filename)
    keys=('human_predicted_failure','human_predicted_contrast','human_false_positive_test','human_unsupported_mechanism')
    for key in keys:
        s=data.get(key)
        if not isinstance(s,str) or len(s.strip())<20 or any(x in s.upper() for x in ['TO FILL','PLACEHOLDER']):
            raise ValueError('missing human prediction: '+key)
    if data.get('assistance_disclosure') not in ('I','H','C','D'):raise ValueError('disclose assistance')
    if data.get('origin')!='carried_from_EX0005A_pre_live':raise ValueError('mark prior predictions as carried from EX0005A')
    if data.get('approved_as_prior_for_aa') is not True:raise ValueError('human must approve using prior predictions')
    return data

def code_hashes():
    folder=pathlib.Path(__file__).resolve().parent
    return {name:sha(folder/name) for name in SOURCE_FILES}

def local_date_time():return dt.datetime.now(ZoneInfo('America/Denver'))

def time_window(manifest,now=None):
    now=now or local_date_time()
    day=dt.date.fromisoformat(manifest['session_date'])
    if day<=dt.date(2026,11,15):raise RuntimeError('EX0005Aa may not extend the closed EX0005A session')
    start_h,start_m=map(int,manifest['session_start'].split(':'))
    end_h,end_m=map(int,manifest['session_end'].split(':'))
    start=dt.datetime.combine(day,dt.time(start_h,start_m),tzinfo=ZoneInfo('America/Denver'))
    end=dt.datetime.combine(day,dt.time(end_h,end_m),tzinfo=ZoneInfo('America/Denver'))
    if not (0<(end-start).total_seconds()<=4*3600):raise RuntimeError('invalid session duration')
    if not (start<=now<end):raise RuntimeError('outside prospectively frozen session window')


def freeze(cfg,session_date,start,end):
    OUTDIR.mkdir(exist_ok=True)
    filename=OUTDIR/'PRE_LIVE_FREEZE.json'
    if filename.exists() or (OUTDIR/'LIVE_ATTEMPT_STARTED.txt').exists():
        raise RuntimeError('freeze already exists; do not replace it')
    day=dt.date.fromisoformat(session_date)
    if day<=dt.date(2026,11,15):raise RuntimeError('must be distinct session after EX0005A')
    for s in (start,end):dt.time.fromisoformat(s)
    start_dt=dt.datetime.combine(day,dt.time.fromisoformat(start))
    end_dt=dt.datetime.combine(day,dt.time.fromisoformat(end))
    if not (dt.timedelta(0)<end_dt-start_dt<=dt.timedelta(hours=4)):
        raise RuntimeError('separate session must be 4h or less')
    q=qualification()
    manifest={'experiment':'EX0005Aa','frozen_at':local_date_time().isoformat(),
      'session_date':session_date,'session_start':start,'session_end':end,
      'model':MODEL,'reasoning':REASONING,'max_output_tokens':OUTPUT_CAP,
      'max_response_calls':MAX_RESPONSES,'input_token_cap':MAX_INPUT_TOKENS,'output_token_cap':MAX_OUTPUT_TOKENS,
      'discovery_diagnostic_steps':DIAG_STEPS_DISCOVERY,'paired_protocol':'fixed identical 2-tool sequence',
      'discovery_protocol':'free-choice 4 bounded calls; separate from paired contrast',
      'public_fixture_fingerprint':q['fixture_sha256'],
      'source_sha256':code_hashes(), 'prior_artifact_sha256':HISTORICAL_SHA,
      'human_fields':cfg,'no_sealed_test':True,
      'metrics_and_gates':{
       'G0':'analytical oracle restores cases; heuristic/noedit controls and numpy/torch agreement',
       'G1':'both paired cases yield exactly two native valid forced calls; report discovery use separately',
       'G2':'paired cases have opposing, oracle-correct signed prediction under exact matching calls',
       'G3':'both paired cases produce schema-valid commitments; abstentions reported separately',
       'G4':'secondary discovery: model patch has lower MSE than no-edit AND simple heuristic by >=0.05 absolute, and >=50% recovery; otherwise FAIL or NOT RUN',
       'mechanism':'explanation only bounded and not validated by mere patch success'
      },
      'software':{'python':platform.python_version(),'numpy':np.__version__,
                  'torch':importlib.metadata.version('torch'),
                  'openai':importlib.metadata.version('openai') if importlib.util.find_spec('openai') else 'not installed'}}
    manifest['freeze_sha256']=fingerprint(manifest)
    atomic_json(filename,manifest)
    return manifest


def api_key():
    token=os.environ.get('OPENAI_API_KEY','')
    if not token:
        try:
            from google.colab import userdata
            token=userdata.get('OPENAI_API_KEY') or ''
        except ImportError:pass
    if not token:raise RuntimeError('API key missing; no request')
    return token


def reject_secret(msg):
    # Log no raw exception bodies or authorization headers.
    return type(msg).__name__


def validate_pair_commit(obj):
    if not isinstance(obj,dict) or set(obj)!={'predicted_delta_mse','uncertainty','explanation'}:raise ValueError('pair commitment keys')
    v=obj['predicted_delta_mse']
    if type(v) not in (float,int) or not np.isfinite(v):raise ValueError('prediction nonnumeric')
    if obj['uncertainty'] not in ('low','medium','high'):raise ValueError('uncertainty')
    if not isinstance(obj['explanation'],str) or not 0<len(obj['explanation'].split())<=70:raise ValueError('explanation')
    return obj


def validate_discovery_commit(obj):
    if not isinstance(obj,dict) or set(obj)!={'fault_region','uncertainty','patch','explanation'}:raise ValueError('discovery commitment keys')
    import re
    m=re.fullmatch(r'(W1|b1|W2|b2)\[(\d+)\]',obj['fault_region']) if isinstance(obj['fault_region'],str) else None
    if not m or int(m.group(2))>=TENSOR_SIZES[m.group(1)]:raise ValueError('invalid fault region')
    if obj['uncertainty'] not in ('low','medium','high'):raise ValueError('uncertainty')
    if not isinstance(obj['explanation'],str) or not 0<len(obj['explanation'].split())<=70:raise ValueError('explanation')
    if not isinstance(obj['patch'],list) or len(obj['patch'])>4:raise ValueError('edit count')
    # Check full semantics separately on a disposable copy; empty patches count as abstention.
    return obj


class Session:
    def __init__(self,client,manifest):
        self.client=client;self.manifest=manifest;self.journal=[]
        self.calls=0;self.in_tokens=0;self.out_tokens=0
        self.outdir=OUTDIR

    def write_log(self):atomic_json(self.outdir/'ACTION_JOURNAL.json',self.journal)

    def create(self,case,phase,**kwargs):
        time_window(self.manifest)
        if self.calls>=MAX_RESPONSES or self.in_tokens>=MAX_INPUT_TOKENS or self.out_tokens>=MAX_OUTPUT_TOKENS:
            raise RuntimeError('global API budget exceeded')
        self.calls+=1
        try:
            r=self.client.responses.create(model=MODEL,reasoning=REASONING,max_output_tokens=OUTPUT_CAP,
                parallel_tool_calls=False,**kwargs)
        except Exception as e:
            self.journal.append({'kind':'api_exception','case':case,'phase':phase,'exception_type':reject_secret(e)})
            self.write_log()
            raise RuntimeError('API exception '+reject_secret(e)) from None
        u=getattr(r,'usage',None)
        usage=u.model_dump() if hasattr(u,'model_dump') else {}
        self.in_tokens+=(usage or {}).get('input_tokens',0)
        self.out_tokens+=(usage or {}).get('output_tokens',0)
        status=getattr(r,'status',None)
        self.journal.append({'kind':'api_response','case':case,'phase':phase,'id':getattr(r,'id',None),
            'model':getattr(r,'model',None),'status':status,
            'incomplete_details':str(getattr(r,'incomplete_details',None)),
            'usage':usage,'output_types':[(getattr(o,'type',None),getattr(o,'name',None)) for o in (getattr(r,'output',[]) or [])]})
        self.write_log()
        if status!='completed':raise RuntimeError('response not completed; '+str(getattr(r,'incomplete_details',None)))
        return r

    def dispatch(self,case,stage,response,expected=None):
        calls=[o for o in response.output if getattr(o,'type',None)=='function_call']
        if len(calls)!=1:raise RuntimeError('expected exactly one native call; received '+str(len(calls)))
        c=calls[0]
        if expected is not None and c.name!=expected:raise RuntimeError('incorrect tool choice')
        try:
            args=json.loads(c.arguments)
            if not isinstance(args,dict):raise ValueError('non-object args')
            p=make_case(case)
            if stage=='paired':
                if args!={}:raise ValueError('paired tool accepts no args')
                value={'inspect_output_weights':inspect_output_weights,'probe_feature1':probe_feature1}[c.name](p)
            else:
                if c.name=='inspect_weights':
                    if set(args)!={'tensor'}:raise ValueError('bad tensor props')
                    value=inspect_tensor(p,args['tensor'])
                elif c.name=='probe_examples':
                    if set(args)!={'pack'}:raise ValueError('bad probe props')
                    value=probe_pack(p,args['pack'])
                else:raise ValueError('unknown tool')
            valid=True
        except Exception as e:
            value={'error':type(e).__name__};valid=False
        self.journal.append({'kind':'diagnostic','case':case,'stage':stage,'function':c.name,
            'arguments':c.arguments,'valid':valid,'return':value})
        self.write_log()
        return {'type':'function_call_output','call_id':c.call_id,'output':json.dumps(value,allow_nan=False)},valid,c.name

    def pair(self,case):
        state={'case':case,'valid_calls':0,'kinds':[],'commit':None,'errors':[]}
        prior=None;inp='First observe the output-layer weights; then observe the predefined feature1 probe. You will commit after those observations.'
        for tool in ['inspect_output_weights','probe_feature1']:
            args={'instructions':PAIR_BASE,'input':inp,'tools':PAIR_TOOLS,
                  'tool_choice':{'type':'function','name':tool}}
            if prior:args['previous_response_id']=prior
            resp=self.create(case,'paired_'+tool,**args)
            output,valid,name=self.dispatch(case,'paired',resp,expected=tool)
            prior=resp.id;inp=[output]
            if not valid:raise RuntimeError('invalid paired diagnostic')
            state['valid_calls']+=1;state['kinds'].append(name)
        r=self.create(case,'paired_commit',instructions=PAIR_BASE+' '+PAIR_COMMIT,
                      input=inp,previous_response_id=prior,tools=PAIR_TOOLS,tool_choice='none')
        raw=getattr(r,'output_text','') or ''
        self.journal.append({'kind':'model_commitment','case':case,'stage':'paired','raw_text':raw[:6000]})
        self.write_log()
        try:
            commit=validate_pair_commit(json.loads(raw))
            state['commit']=commit
            truth=intervention_effect(make_case(case))
            state['actual_delta_mse']=truth
            state['prediction_error']=commit['predicted_delta_mse']-truth
            state['sign_correct']=bool(np.sign(commit['predicted_delta_mse'])==np.sign(truth))
        except Exception as e:state['errors'].append('invalid commit: '+type(e).__name__)
        return state

    def discovery(self,case='D_unknown'):
        state={'case':case,'valid_calls':0,'kinds':[],'commit':None,'errors':[],'patch_evaluation':None}
        prior=None; inp='Investigate this unknown lesion with at most four diagnostic observations.'
        for turn in range(DIAG_STEPS_DISCOVERY):
            args={'instructions':DISCOVERY_BASE,'input':inp,'tools':DISCOVERY_TOOLS,'tool_choice':'required'}
            if prior:args['previous_response_id']=prior
            resp=self.create(case,'discovery_'+str(turn+1),**args)
            output,valid,name=self.dispatch(case,'discovery',resp)
            prior=resp.id;inp=[output]
            if valid:
                state['valid_calls']+=1
                if name not in state['kinds']:state['kinds'].append(name)
            else:state['errors'].append('invalid '+name)
        final=self.create(case,'discovery_commit',instructions=DISCOVERY_BASE+' '+DISCOVERY_COMMIT,
                          input=inp,previous_response_id=prior,tools=DISCOVERY_TOOLS,tool_choice='none')
        raw=getattr(final,'output_text','') or ''
        self.journal.append({'kind':'model_commitment','case':case,'stage':'discovery','raw_text':raw[:6000]})
        self.write_log()
        try:
            commit=validate_discovery_commit(json.loads(raw))
            state['commit']=commit;state['abstained']=not bool(commit['patch'])
            state['fault_region_correct']=bool(commit['fault_region']=='W1[0]')
            if commit['patch']:
                p=make_case(case)
                score=score_edits(p,commit['patch'])
                baselines=qualification()['cases'][case]
                improve=score['before_mse']-score['after_mse']
                state['patch_evaluation']={**score,
                  'beats_no_edit':bool(improve>0),
                  'beats_simple_heuristic_by_0p05':bool(score['after_mse']+0.05<=baselines['heuristic_mse']),
                  'recovery_fraction':float(improve/score['before_mse']),
                  'G4_pass':bool(improve/score['before_mse']>=0.50 and score['after_mse']+0.05<=baselines['heuristic_mse'])}
        except Exception as e:state['errors'].append('invalid discovery commitment or patch: '+type(e).__name__)
        return state


def evaluate(summary,journal):
    cases=summary['cases']
    pair_complete=all(cases.get(c,{}).get('commit') is not None for c in ('C_positive','C_negative'))
    paired_obs=all(cases.get(c,{}).get('valid_calls')==2 and cases.get(c,{}).get('kinds')==['inspect_output_weights','probe_feature1'] for c in ('C_positive','C_negative'))
    def exact_calls(case):return [(j['function'],j['arguments']) for j in journal if j.get('kind')=='diagnostic' and j.get('case')==case and j.get('stage')=='paired' and j.get('valid')]
    matched=exact_calls('C_positive')==exact_calls('C_negative') and len(exact_calls('C_positive'))==2
    sign=pair_complete and all(cases[c].get('sign_correct') for c in ('C_positive','C_negative')) and cases['C_positive']['commit']['predicted_delta_mse']<0<cases['C_negative']['commit']['predicted_delta_mse']
    disc=cases.get('D_unknown',{})
    summary['matched_pair_observation_contract']=bool(matched)
    summary['G1']='PASS' if paired_obs else 'FAIL'
    summary['G2']='PASS' if (paired_obs and matched and sign) else ('INCONCLUSIVE' if not matched else 'FAIL')
    summary['G3']='PASS' if pair_complete else 'FAIL'
    summary['G4']=('NOT RUN' if not disc.get('patch_evaluation') else 'PASS' if disc['patch_evaluation']['G4_pass'] else 'FAIL')
    summary['discovery_tool_diversity']='PASS' if len(disc.get('kinds',[]))>=2 else 'FAIL' if disc else 'NOT RUN'
    summary['mechanistic_understanding']='NOT ESTABLISHED'
    summary['instrument_ready']=bool(summary['G1']=='PASS' and summary['G2']=='PASS' and summary['G3']=='PASS')
    summary['status']='COMPLETE' if not any(v.get('interruption') for v in cases.values()) and len(cases)==3 else 'PARTIAL / INTERRUPTED'
    return summary


def run_live():
    manifest=load_json(OUTDIR/'PRE_LIVE_FREEZE.json')
    if manifest.get('experiment')!='EX0005Aa':raise RuntimeError('wrong manifest')
    if manifest.get('source_sha256')!=code_hashes() or manifest.get('public_fixture_fingerprint')!=qualification()['fixture_sha256']:
        raise RuntimeError('source or fixtures changed since freeze; no model contacted')
    if manifest.get('freeze_sha256')!=fingerprint({k:v for k,v in manifest.items() if k!='freeze_sha256'}):raise RuntimeError('manifest modified since freeze')
    time_window(manifest)
    marker=OUTDIR/'LIVE_ATTEMPT_STARTED.txt'
    if marker.exists() or (OUTDIR/'RESULTS.json').exists() or (OUTDIR/'ACTION_JOURNAL.json').exists():
        raise RuntimeError('live attempt exists: no automatic reruns')
    marker.write_text(local_date_time().isoformat()+'\n')
    summary={'experiment':'EX0005Aa','model_requested':MODEL,'freeze_sha256':manifest['freeze_sha256'],
       'G0_local':'PASS','cases':{},'G1':'NOT RUN','G2':'NOT RUN','G3':'NOT RUN','G4':'NOT RUN','instrument_ready':False}
    session=None
    try:
        from openai import OpenAI
        client=OpenAI(api_key=api_key(),max_retries=0,timeout=45.0)
        session=Session(client,manifest)
        try:
            r=client.models.retrieve(MODEL)
            summary['model_access_check']=getattr(r,'id',None)
        except Exception as e:
            raise RuntimeError('model access failed: '+type(e).__name__) from None
        for case in ('C_positive','C_negative','D_unknown'):
            try:
                if case.startswith('C_'):out=session.pair(case)
                else:out=session.discovery(case)
                summary['cases'][case]=out
            except Exception as e:
                # Reconstruct already accepted observations from the immutable journal;
                # an interrupted case is partial, never silently called NOT RUN.
                accepted=[j for j in session.journal if j.get('case')==case and j.get('kind')=='diagnostic' and j.get('valid')]
                summary['cases'][case]={'case':case,'interruption':{'type':type(e).__name__,'reason':str(e)[:300]},
                                       'commit':None,'valid_calls':len(accepted),
                                       'kinds':list(dict.fromkeys(j['function'] for j in accepted))}
            finally:
                summary['api_responses_logged']=sum(j['kind']=='api_response' for j in session.journal)
                atomic_json(OUTDIR/'RESULTS.json',summary)
        summary=evaluate(summary,session.journal)
    except Exception as e:
        summary['interruption']={'type':type(e).__name__,'reason':str(e)[:300]}
    finally:
        if session:
            summary['api_responses_logged']=sum(j['kind']=='api_response' for j in session.journal)
            summary['usage_input_tokens']=session.in_tokens;summary['usage_output_tokens']=session.out_tokens
            session.write_log()
        atomic_json(OUTDIR/'RESULTS.json',summary)
    return summary


def main():
    ap=argparse.ArgumentParser()
    g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--qualify-local',action='store_true')
    g.add_argument('--freeze',action='store_true')
    g.add_argument('--live',action='store_true')
    ap.add_argument('--human-fields',default='human_fields.json')
    ap.add_argument('--session-date')
    ap.add_argument('--start')
    ap.add_argument('--end')
    args=ap.parse_args()
    if args.qualify_local:
        print(json.dumps(qualification(),indent=2));return
    if args.freeze:
        if not (args.session_date and args.start and args.end):ap.error('freeze requires session date, start and end local')
        cfg=human_fields(args.human_fields)
        print(json.dumps(freeze(cfg,args.session_date,args.start,args.end),indent=2));return
    print(json.dumps(run_live(),indent=2))

if __name__=='__main__':main()
