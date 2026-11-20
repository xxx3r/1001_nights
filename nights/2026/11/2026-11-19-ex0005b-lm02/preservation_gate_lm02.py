"""EX0005B-LM-02: phased, independently gated Qwen3-0.6B weight repair.

No model loads, calls, or writes on import. A fresh, qualified patient is required
before exactly one live attempt. The historic LM-01 archive is never touched.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, math, os, pathlib, random, sys
from contextlib import contextmanager
from zoneinfo import ZoneInfo

EXPERIMENT = 'EX0005B-LM-02'
MODEL_ID = 'Qwen/Qwen3-0.6B'
INVESTIGATOR = 'gpt-6-luna'
SEED = 5111902
ROOT = pathlib.Path('ex0005b_lm02_receipts')
PHASE_BUDGET = {'input': 6, 'output': 6, 'repair': 6}
MAX_API_RESPONSES = 22
MAX_INPUT_TOKENS = 100000
MAX_OUTPUT_TOKENS = 30000
GAIN_LIMIT = 5.0
ALPHAS = (0.25, -1.5, 2.0, -2.0)  # Prospective order, no post-result tuning.
MIN_DEV_GAP = 0.03
PRIMARY_MIN_RECOVERY = 0.50
PRESERVE_RELATIVE_LIMIT = 0.02
MIN_RETENTION = 0.90
MIN_BASELINE_MARGIN = 0.01
SESSION_MINUTES = 150
SOURCE_FILENAME = 'preservation_gate_lm02.py'
TEST_FILENAME = 'test_preservation_gate_lm02.py'
PRIOR_EXCLUDED_COLUMN = 4  # LM-01's exposed index: force a genuinely different edit site.

# Entirely NEW benign prompt/completion pairs. No LM-01 question is re-used.
# Each split is disjoint at the prompt string level. No holdout tool access.
SETS = {
 'target_dev': [
  ('Compute 13 + 5. Result: ', '18'), ('Compute 22 - 9. Result: ', '13'),
  ('Compute 4 * 7. Result: ', '28'), ('Compute 36 / 4. Result: ', '9'),
  ('Compute 15 + 8. Result: ', '23'), ('Compute 29 - 12. Result: ', '17'),
  ('Compute 8 * 4. Result: ', '32'), ('Compute 45 / 5. Result: ', '9'),
  ('Compute 19 + 6. Result: ', '25'), ('Compute 31 - 14. Result: ', '17'),
  ('Compute 3 * 9. Result: ', '27'), ('Compute 64 / 8. Result: ', '8'),
 ],
 'preserve_dev': [
  ('An octagon has eight ', 'sides.'), ('The capital of Canada is ', 'Ottawa.'),
  ('A bird uses wings to ', 'fly.'), ('The opposite of early is ', 'late.'),
  ('The frozen form of water is ', 'ice.'), ('A pencil is used for ', 'writing.'),
  ('The largest ocean is the ', 'Pacific.'), ('A dozen means ', 'twelve.'),
  ('A thermometer measures ', 'temperature.'), ('The primary colors include red, yellow and ', 'blue.'),
  ('A bee makes ', 'honey.'), ('The antonym of empty is ', 'full.'),
 ],
 'target_test': [
  ('Find 11 + 18. Output: ', '29'), ('Find 28 - 13. Output: ', '15'),
  ('Find 6 * 7. Output: ', '42'), ('Find 48 / 6. Output: ', '8'),
  ('Find 23 + 9. Output: ', '32'), ('Find 37 - 19. Output: ', '18'),
  ('Find 5 * 8. Output: ', '40'), ('Find 63 / 7. Output: ', '9'),
  ('Find 16 + 17. Output: ', '33'), ('Find 44 - 26. Output: ', '18'),
  ('Find 9 * 6. Output: ', '54'), ('Find 72 / 9. Output: ', '8'),
  ('Find 27 + 15. Output: ', '42'), ('Find 52 - 34. Output: ', '18'),
  ('Find 7 * 8. Output: ', '56'), ('Find 81 / 9. Output: ', '9'),
  ('Find 18 + 26. Output: ', '44'), ('Find 41 - 24. Output: ', '17'),
 ],
 'preserve_test': [
  ('The capital of Japan is ', 'Tokyo.'), ('A violin has four ', 'strings.'),
  ('The opposite of narrow is ', 'wide.'), ('Most plants obtain energy from ', 'sunlight.'),
  ('The nearest star to Earth is the ', 'Sun.'), ('A baker makes ', 'bread.'),
  ('The color of a ripe lemon is ', 'yellow.'), ('A doctor works at a ', 'hospital.'),
  ('The first day of the workweek is usually ', 'Monday.'), ('The opposite of noisy is ', 'quiet.'),
  ('A compass points toward ', 'north.'), ('A whale lives in the ', 'ocean.'),
  ('A fish uses gills to ', 'breathe.'), ('The shape with five sides is a ', 'pentagon.'),
  ('A clock measures ', 'time.'), ('An artist uses a paint ', 'brush.'),
  ('The opposite of rough is ', 'smooth.'), ('Caterpillars transform into ', 'butterflies.'),
 ],
}


def canonical(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False)

def digest(o):
    return hashlib.sha256(canonical(o).encode('utf-8')).hexdigest()

def sha_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def atomic_json(path, o):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(o, sort_keys=True, indent=2, allow_nan=False) + '\n')
    tmp.replace(path)

def validate_gain(g):
    if type(g) not in (int, float) or not math.isfinite(g) or abs(g) > GAIN_LIMIT:
        raise ValueError('gain must be finite and within [-5,5]')
    return float(g)

def validate_commit(a):
    if not isinstance(a,dict) or set(a) != {'gain','confidence','explanation','predicted_target_improvement'}:
        raise ValueError('invalid commitment schema')
    if a['confidence'] not in ('low','medium','high'):
        raise ValueError('invalid confidence')
    if not isinstance(a['explanation'],str) or not 1<=len(a['explanation'].split())<=100:
        raise ValueError('invalid explanation')
    p=a['predicted_target_improvement']
    if type(p) not in (int,float) or not math.isfinite(p):
        raise ValueError('invalid predicted improvement')
    if a['gain'] is not None:
        validate_gain(a['gain'])
    return a

def assess_evidence(choice, history):
    # Only repair probes can qualify a chosen intervention.
    if choice is None:
        return 'ABSTAIN'
    base, chosen = None, None
    for e in history:
        if e.get('phase') != 'repair' or e.get('tool') != 'probe_gain':
            continue
        if math.isclose(e['args']['gain'],1.0,rel_tol=0,abs_tol=1e-9):
            base = e['observed']
        if math.isclose(e['args']['gain'],choice,rel_tol=0,abs_tol=1e-9):
            chosen = e['observed']
    if base is None or chosen is None:
        return 'FAIL'
    if not all(math.isfinite(x.get(k, math.nan)) for x in (base,chosen)
               for k in ('target_dev_loss','preserve_dev_loss')):
        return 'FAIL'
    improved = chosen['target_dev_loss'] <= base['target_dev_loss'] - 0.01
    retained = chosen['preserve_dev_loss'] <= base['preserve_dev_loss'] * 1.02
    return 'PASS' if (improved and retained) else 'FAIL'

def recovery_fraction(healthy, corrupt, patched):
    if not all(math.isfinite(x) for x in (healthy,corrupt,patched)):
        raise ValueError('nonfinite score')
    if corrupt-healthy <= MIN_DEV_GAP:
        return None
    return (corrupt-patched)/(corrupt-healthy)

def score_result(healthy_target, corrupt_target, patched_target,
                 healthy_preserve, patched_preserve, retention, best_simple):
    r=recovery_fraction(healthy_target, corrupt_target, patched_target)
    if not all(math.isfinite(x) for x in (healthy_preserve, patched_preserve, retention, best_simple)):
        raise ValueError('nonfinite preservation or baseline')
    delta=(patched_preserve-healthy_preserve)/max(abs(healthy_preserve),1e-12)
    return {
       'recovery': r, 'preserve_relative_loss_change':delta,
       'next_token_retention':retention,
       'G3':'PASS' if r is not None and r>=PRIMARY_MIN_RECOVERY else 'FAIL',
       'G4':'PASS' if delta<=PRESERVE_RELATIVE_LIMIT and retention>=MIN_RETENTION else 'FAIL',
       'G5':'PASS' if patched_target+MIN_BASELINE_MARGIN<=best_simple else 'FAIL',
    }

def freeze_fingerprint(q):
    return digest({k:v for k,v in q.items() if k!='freeze_sha256'})

def verify_manifest(q):
    if q.get('freeze_sha256') != freeze_fingerprint(q):
        raise RuntimeError('freeze modified')
    if q.get('G0') != 'PASS' or q.get('experiment') != EXPERIMENT:
        raise RuntimeError('patient not qualified')
    if q.get('code_sha256') != sha_file(__file__) or q.get('test_sha256') != sha_file(TEST_FILENAME):
        raise RuntimeError('frozen source or checker modified')
    if q.get('sets_sha256') != digest(SETS):
        raise RuntimeError('data changed since freeze')
    if q.get('model_id') != MODEL_ID or q.get('investigator') != INVESTIGATOR:
        raise RuntimeError('model mismatch')
    if q.get('phase_budgets') != PHASE_BUDGET:
        raise RuntimeError('phase budget mismatch')
    return True

def now_local():
    return dt.datetime.now(ZoneInfo('America/Denver'))


def load_patient(revision):
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    if not torch.cuda.is_available():
        raise RuntimeError('no CUDA GPU; no CPU substitute')
    torch.manual_seed(SEED)
    tok=AutoTokenizer.from_pretrained(MODEL_ID,revision=revision,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(
        MODEL_ID,revision=revision,dtype='auto',device_map='auto',trust_remote_code=False).eval()
    if not hasattr(model.model,'layers'):
        raise RuntimeError('unexpected architecture')
    ix=len(model.model.layers)//2
    down=model.model.layers[ix].mlp.down_proj
    if not hasattr(down,'weight') or down.weight.ndim!=2:
        raise RuntimeError('unexpected down-projection')
    return Patient(model,tok,ix,down)

class Patient:
    def __init__(self,model,tok,layer,down):
        self.model,self.tok,self.layer,self.down=model,tok,layer,down
        self.col=self.alpha=self.original=self.bad=None

    def loss_pair(self, prefix, completion):
        import torch
        import torch.nn.functional as F
        a=self.tok.encode(prefix,add_special_tokens=False)
        b=self.tok.encode(completion,add_special_tokens=False)
        if not a or not b:
            raise RuntimeError('empty token sequence')
        ids=torch.tensor([a+b],dtype=torch.long,device=self.down.weight.device)
        with torch.inference_mode():
            logits=self.model(input_ids=ids,use_cache=False).logits[0]
            selected=logits[len(a)-1:-1,:].float()
            target=ids[0,len(a):]
            if selected.shape[0]!=target.shape[0]:
                raise RuntimeError('completion mask mismatch')
            loss=float(F.cross_entropy(selected,target).item())
            top=int(logits[len(a)-1].argmax().item())
        return loss, top

    def loss(self, split):
        samples=[self.loss_pair(a,b) for a,b in SETS[split]]
        return sum(x for x,_ in samples)/len(samples),[y for _,y in samples]

    def choose_column(self):
        import torch
        stats=[]
        def hook(_module,args):
            x=args[0].detach().float()
            stats.append(x.square().mean(dim=(0,1)).cpu())
        handle=self.down.register_forward_pre_hook(hook)
        try:
            self.loss('target_dev')
        finally:
            handle.remove()
        if not stats:
            raise RuntimeError('no activations')
        energy=torch.stack(stats).mean(dim=0)
        if PRIOR_EXCLUDED_COLUMN < energy.numel():
            energy[PRIOR_EXCLUDED_COLUMN]=float('-inf')
        return int(torch.argmax(energy).item())

    def install(self,col,alpha):
        import torch
        if type(col) is not int or not 0<=col<self.down.weight.shape[1] or col==PRIOR_EXCLUDED_COLUMN or alpha not in ALPHAS:
            raise ValueError('invalid patient configuration')
        with torch.no_grad():
            if self.original is not None:
                self.down.weight[:,self.col].copy_(self.original)
            self.col,self.alpha=col,alpha
            self.original=self.down.weight[:,col].detach().clone()
            self.bad=self.original*alpha
            self.down.weight[:,col].copy_(self.bad)

    @contextmanager
    def candidate(self,gain):
        import torch
        gain=validate_gain(gain)
        if self.bad is None:
            raise RuntimeError('no patient installed')
        with torch.no_grad():
            self.down.weight[:,self.col].copy_(self.bad*gain)
        try:
            yield
        finally:
            with torch.no_grad():
                self.down.weight[:,self.col].copy_(self.bad)

    def metrics(self,gain,split):
        with self.candidate(gain):
            return self.loss(split)

    def reference_metrics(self,split):
        import torch
        if self.original is None:
            raise RuntimeError('no original')
        with torch.no_grad():
            self.down.weight[:,self.col].copy_(self.original)
        try:
            return self.loss(split)
        finally:
            with torch.no_grad():
                self.down.weight[:,self.col].copy_(self.bad)

    def inspect_site(self):
        import torch
        return {'layer':self.layer,'tensor':'mlp.down_proj.weight',
             'shape':list(self.down.weight.shape),'column':self.col,
             'current_column_norm':float(torch.linalg.vector_norm(self.bad.float()).item()),
             'edit_form':'corrupted_column * gain', 'gain_bounds':[-5,5],
             'healthy_values_exposed':False}

    def input_probe(self,family,index):
        import torch
        if family not in ('target','preserve') or type(index) is not int or not 0<=index<len(SETS[family+'_dev']):
            raise ValueError('invalid development input')
        prefix,completion=SETS[family+'_dev'][index]
        values=[]
        def hook(_module,args):
            t=args[0].detach().float()[0,:,self.col]
            values.append(t.cpu())
        h=self.down.register_forward_pre_hook(hook)
        try:
            self.loss_pair(prefix,completion)
        finally:
            h.remove()
        if not values:
            raise RuntimeError('no input activation')
        arr=torch.cat(values)
        return {'split':family+'_dev', 'index':index,'input_text':prefix,
            'tokens':int(arr.numel()),'site_abs_mean':float(arr.abs().mean()),
            'site_rms':float(arr.square().mean().sqrt()),
            'site_nonzero_fraction':float((arr!=0).float().mean()),
            'site_positive_fraction':float((arr>0).float().mean()),
            'note':'corrupted model input-side activation only; no healthy weights or test values'}

    def output_probe(self,family,index):
        if family not in ('target','preserve') or type(index) is not int or not 0<=index<len(SETS[family+'_dev']):
            raise ValueError('invalid development output')
        prefix,completion=SETS[family+'_dev'][index]
        loss,top=self.loss_pair(prefix,completion)
        return {'split':family+'_dev','index':index,'prompt':prefix,'expected_completion':completion,
                'loss':loss,'first_token_predicted':self.tok.decode([top]),
                'note':'corrupted model response only; no healthy baseline or holdout'}

    def output_summary(self,family):
        if family not in ('target','preserve'):
            raise ValueError('invalid family')
        value,_=self.loss(family+'_dev')
        return {'split':family+'_dev','mean_loss':value,'n':len(SETS[family+'_dev']),
                'note':'aggregate corrupted checkpoint output; no healthy baseline'}

    def close(self):
        import torch
        if self.original is not None:
            with torch.no_grad():
                self.down.weight[:,self.col].copy_(self.original)

# Native tool menus are deliberately disjoint; phase transition is enforced
# in code, not left to natural-language persuasion.
def tool(name,description,properties,required):
    return {'type':'function','name':name,'description':description,'strict':True,
      'parameters':{'type':'object','properties':properties,'required':required,'additionalProperties':False}}

FAMILY={'type':'string','enum':['target','preserve']}
INDEX={'type':'integer','minimum':0,'maximum':11}
INPUT_TOOLS=[
 tool('inspect_site','Inspect permitted corrupted edit-site dimensions and norm; no reference checkpoint.',{},[]),
 tool('inspect_input','Read input-side activation statistics for one chosen development example.',{'family':FAMILY,'index':INDEX},['family','index']),
 tool('finish_phase','Finish input phase early; no more input observations.',{'reason':{'type':'string'}},['reason']),
]
OUTPUT_TOOLS=[
 tool('inspect_output','Read output loss and predicted first token for one development example.',{'family':FAMILY,'index':INDEX},['family','index']),
 tool('summarize_outputs','Read corrupted-model aggregate loss for one development family.',{'family':FAMILY},['family']),
 tool('finish_phase','Finish output phase early; no more output observations.',{'reason':{'type':'string'}},['reason']),
]
REPAIR_TOOLS=[
 tool('probe_gain','Evaluate a bounded candidate gain on BOTH development families; no holdout.',{'gain':{'type':'number','minimum':-5,'maximum':5}},['gain']),
 tool('commit_surgery','Commit a gain or abstain. Only the independent checker will score held-out outcomes.',
    {'gain':{'type':['number','null']},'confidence':{'type':'string','enum':['low','medium','high']},
     'explanation':{'type':'string'},'predicted_target_improvement':{'type':'number'}},
    ['gain','confidence','explanation','predicted_target_improvement']),
]
COMMIT_ONLY=[REPAIR_TOOLS[1]]

INSTRUCTIONS=(
 'You examine a disposable Qwen3-0.6B language model, corrupted at one permitted '
 'transformer MLP down-projection column by an unknown multiplier. The layer and column '
 'are supplied; you are NOT locating an unknown column. Inputs and outputs are '
 'restricted to development observations. Only one bounded column gain [-5,5] can be '
 'proposed. Preserve unrelated language behavior. The independent checker alone sees '
 'the healthy checkpoint and holdout. You may abstain. Tool responses are evidence, '
 'not permission to infer a unique mechanism. Do not claim unseen measurements.'
)
PHASE_PROMPTS={
 'input':'INPUT PHASE: up to six calls to inspect_site or inspect_input. Study activation structure. Finish early using finish_phase; after six observations we transition automatically. Repair tools are unavailable.',
 'output':'OUTPUT PHASE: up to six calls to inspect_output or summarize_outputs on current corrupted network. Finish early using finish_phase. You cannot propose gains in this phase.',
 'repair':'REPAIR PHASE: up to six probe_gain calls, or commit_surgery early. Probe gain=1 as the no-edit baseline; compare against at least one other gain. After six probes, you will be offered only commit_surgery. Abstention is allowed.',
}

class PhasedInvestigator:
    def __init__(self,client,patient,write_journal=lambda x:None):
        self.client,self.patient,self.write_journal=client,patient,write_journal
        self.journal=[];self.observations=[];self.counts={x:0 for x in PHASE_BUDGET}
        self.total_responses=0;self.total_input_tokens=0;self.total_output_tokens=0;self.prior=None;self.inp=None
        self.commitment=None;self.commitment_mode=None

    def emit(self,e):
        self.journal.append(e)
        self.write_journal(self.journal)

    def ask(self,phase,tools,forced=False):
        if (self.total_responses>=MAX_API_RESPONSES or
            self.total_input_tokens>=MAX_INPUT_TOKENS or
            self.total_output_tokens>=MAX_OUTPUT_TOKENS):
            raise RuntimeError('API response or token cap exhausted')
        kw={'model':INVESTIGATOR,'instructions':INSTRUCTIONS+' '+PHASE_PROMPTS['repair' if phase=='commit' else phase],
             'input':self.inp if self.inp is not None else PHASE_PROMPTS[phase],
             'tools':tools,'tool_choice':{'type':'function','name':'commit_surgery'} if forced else 'required',
             'parallel_tool_calls':False,'reasoning':{'effort':'low'},'max_output_tokens':1800}
        if self.prior:
            kw['previous_response_id']=self.prior
        try:
            response=self.client.responses.create(**kw)
        except Exception as e:
            self.emit({'type':'api_exception','phase':phase,'error_type':type(e).__name__})
            raise RuntimeError('API exception: '+type(e).__name__) from None
        self.total_responses+=1
        usage=response.usage.model_dump() if getattr(response,'usage',None) and hasattr(response.usage,'model_dump') else None
        if usage:
            self.total_input_tokens+=usage.get('input_tokens',0) or 0
            self.total_output_tokens+=usage.get('output_tokens',0) or 0
        self.emit({'type':'response','phase':phase,'id':getattr(response,'id',None),
                   'status':getattr(response,'status',None),'tool_choice':'forced_commit' if forced else 'required',
                   'usage':usage})
        if getattr(response,'status',None)!='completed':
            raise RuntimeError('response incomplete')
        calls=[x for x in response.output if getattr(x,'type',None)=='function_call']
        if len(calls)!=1:
            raise RuntimeError('expected exactly one native function call')
        c=calls[0]
        try:
            args=json.loads(c.arguments)
        except (TypeError,ValueError):
            raise ValueError('invalid function-call JSON') from None
        if not isinstance(args,dict):
            raise ValueError('function arguments must be an object')
        if c.name not in {x['name'] for x in tools}:
            raise RuntimeError('tool unavailable in this phase')
        self.prior=response.id
        return c,args

    def return_observation(self,call,observed):
        self.inp=[{'type':'function_call_output','call_id':call.call_id,'output':canonical(observed)}]

    def start_phase(self,phase):
        self.emit({'type':'phase_start','phase':phase,'budget':PHASE_BUDGET[phase]})
        # Supply pending native-tool output before starting the new phase.
        # Otherwise previous_response_id can point at an unanswered tool call.
        if isinstance(self.inp,list):
            self.inp=[*self.inp, {'role':'user','content':PHASE_PROMPTS[phase]}]
        else:
            self.inp=PHASE_PROMPTS[phase]

    def end_phase(self,phase,reason):
        self.emit({'type':'phase_end','phase':phase,'observations_used':self.counts[phase],
                  'transition':reason})

    def run_phase(self,phase):
        self.start_phase(phase)
        tools={'input':INPUT_TOOLS,'output':OUTPUT_TOOLS,'repair':REPAIR_TOOLS}[phase]
        for _ in range(PHASE_BUDGET[phase]):
            call,args=self.ask(phase,tools)
            if call.name=='finish_phase':
                if phase=='repair' or set(args)!={'reason'} or not isinstance(args['reason'],str):
                    raise ValueError('invalid finish_phase')
                self.emit({'type':'early_finish','phase':phase,'reason':args['reason'][:180]})
                self.return_observation(call,{'status':'phase_complete'})
                self.end_phase(phase,'voluntary')
                return
            if call.name=='commit_surgery':
                if phase!='repair':
                    raise RuntimeError('commit not permitted')
                self.commitment=validate_commit(args)
                self.commitment_mode='voluntary'
                self.emit({'type':'commit','phase':phase,'commitment':self.commitment,
                           'mode':'voluntary','observations_used':dict(self.counts)})
                self.end_phase(phase,'voluntary_commit')
                return
            if phase=='input':
                if call.name=='inspect_site' and args=={}:
                    observed=self.patient.inspect_site()
                elif call.name=='inspect_input' and set(args)=={'family','index'}:
                    observed=self.patient.input_probe(args['family'],args['index'])
                else:
                    raise ValueError('invalid input diagnostic')
            elif phase=='output':
                if call.name=='inspect_output' and set(args)=={'family','index'}:
                    observed=self.patient.output_probe(args['family'],args['index'])
                elif call.name=='summarize_outputs' and set(args)=={'family'}:
                    observed=self.patient.output_summary(args['family'])
                else:
                    raise ValueError('invalid output diagnostic')
            else:
                if call.name!='probe_gain' or set(args)!={'gain'}:
                    raise ValueError('invalid repair diagnostic')
                gain=validate_gain(args['gain'])
                tl,_=self.patient.metrics(gain,'target_dev')
                pl,_=self.patient.metrics(gain,'preserve_dev')
                observed={'gain':gain,'target_dev_loss':tl,'preserve_dev_loss':pl,
                          'split':'development_only'}
            self.counts[phase]+=1
            entry={'type':'diagnostic','phase':phase,'tool':call.name,'args':args,'observed':observed}
            self.observations.append(entry)
            self.emit(entry)
            self.return_observation(call,observed)
        self.end_phase(phase,'budget_exhausted')

    def run(self):
        for phase in ('input','output','repair'):
            self.run_phase(phase)
            if self.commitment is not None:
                return self.commitment
        # Unconditionally enforced final-only tool menu. One response, no extra diagnostics.
        self.emit({'type':'phase_start','phase':'commit','tool_menu':['commit_surgery'],
                   'reason':'all_repair_observations_consumed'})
        final_instruction=('FINAL DECISION. No diagnostics remain. '
                  'Use commit_surgery to propose a supported gain or explicitly abstain (gain=null). '
                  'Do not invent measurements.')
        if isinstance(self.inp,list):
            self.inp=[*self.inp, {'role':'user','content':final_instruction}]
        else:
            self.inp=final_instruction
        call,args=self.ask('commit',COMMIT_ONLY,forced=True)
        if call.name!='commit_surgery':
            raise RuntimeError('forced commitment did not call commit_surgery')
        self.commitment=validate_commit(args)
        self.commitment_mode='forced_final'
        self.emit({'type':'commit','phase':'commit','commitment':self.commitment,
                   'mode':'forced_final','observations_used':dict(self.counts)})
        return self.commitment


def qualify():
    import torch
    from huggingface_hub import HfApi
    if ROOT.exists() and any(ROOT.iterdir()):
        raise RuntimeError('receipt directory exists: cannot overwrite or reselect')
    ROOT.mkdir(exist_ok=False)
    receipt={'experiment':EXPERIMENT,'stage':'G0_QUALIFICATION','attempted_at':now_local().isoformat(),
             'G0':'NOT RUN','qualifier':'fresh patient, not LM-01 rescore'}
    try:
        if not torch.cuda.is_available():
            raise RuntimeError('no CUDA GPU in this environment')
        revision=HfApi().model_info(MODEL_ID).sha
        if not isinstance(revision,str) or len(revision)!=40:
            raise RuntimeError('model revision unavailable')
        p=load_patient(revision)
        try:
            col=p.choose_column()
            healthy_target,_=p.loss('target_dev')
            healthy_preserve,_=p.loss('preserve_dev')
            trials=[];selected=None
            for alpha in ALPHAS:
                p.install(col,alpha)
                corrupt,_=p.metrics(1,'target_dev')
                oracle,_=p.reference_metrics('target_dev')
                inv,_=p.metrics(1/alpha,'target_dev')
                trials.append({'alpha':alpha,'corrupt_target_loss_dev':corrupt,
                               'exact_oracle_target_loss_dev':oracle,
                               'inverse_gain_target_loss_dev':inv})
                if corrupt-healthy_target>=MIN_DEV_GAP and abs(oracle-healthy_target)<0.002:
                    selected=alpha
                    break
            if selected is None:
                receipt.update({'G0':'FAIL','reason':'none of fixed candidate corruptions qualified',
                                'calibration_trials':trials})
                return receipt
            p.install(col,selected)
            corrupt_preserve,_=p.metrics(1,'preserve_dev')
            now=now_local()
            receipt.update({'G0':'PASS','model_id':MODEL_ID,'revision':revision,
                'investigator':INVESTIGATOR,'session_date':now.date().isoformat(),
                'freeze_expires_at':(now+dt.timedelta(minutes=SESSION_MINUTES)).isoformat(),
                'model_layer':p.layer,'column':col,'corruption_alpha':selected,
                'excluded_prior_column':PRIOR_EXCLUDED_COLUMN,
                'healthy_target_dev':healthy_target,'healthy_preserve_dev':healthy_preserve,
                'corrupt_preserve_dev':corrupt_preserve,'calibration_trials':trials,
                'source_sha256':'', 'code_sha256':sha_file(__file__),
                'test_sha256':sha_file(TEST_FILENAME),'sets_sha256':digest(SETS),
                'phase_budgets':PHASE_BUDGET,'final_commit_response':1,
                'device':str(p.down.weight.device),'torch_version':torch.__version__,
                'metrics':{'recovery_min':PRIMARY_MIN_RECOVERY,'preserve_increase_max':PRESERVE_RELATIVE_LIMIT,
                           'next_token_retention_min':MIN_RETENTION,'simple_margin':MIN_BASELINE_MARGIN},
                'status':'READY_TO_FREEZE_NO_INVESTIGATOR_EXPOSED'})
            receipt.pop('source_sha256')
            receipt['freeze_sha256']=freeze_fingerprint(receipt)
            return receipt
        finally:
            p.close()
    except Exception as e:
        receipt.update({'G0':'NOT RUN','reason':type(e).__name__, 'error_type':type(e).__name__})
        return receipt
    finally:
        atomic_json(ROOT/'QUALIFICATION.json',receipt)
        if receipt['G0']=='PASS':
            atomic_json(ROOT/'PRE_LIVE_FREEZE.json',receipt)


def live():
    from openai import OpenAI
    manifest=json.loads((ROOT/'PRE_LIVE_FREEZE.json').read_text())
    verify_manifest(manifest)
    now=now_local()
    if now.date().isoformat()!=manifest['session_date'] or now>dt.datetime.fromisoformat(manifest['freeze_expires_at']):
        raise RuntimeError('session is closed; no retrospective attempt')
    if (ROOT/'LIVE_ATTEMPT_STARTED.txt').exists() or (ROOT/'RESULTS.json').exists():
        raise RuntimeError('previous live attempt exists; no rerun')
    key=os.environ.get('OPENAI_API_KEY')
    if not key:
        raise RuntimeError('API secret absent')
    patient=load_patient(manifest['revision'])
    if patient.layer!=manifest['model_layer']:
        raise RuntimeError('model architecture changed')
    patient.install(manifest['column'],manifest['corruption_alpha'])
    result={'experiment':EXPERIMENT,'status':'INTERRUPTED','G0':'PASS',
            **{k:'NOT RUN' for k in ('G1','G2','G3','G4','G5')},
            'freeze_sha256':manifest['freeze_sha256']}
    investigator=None
    try:
        (ROOT/'LIVE_ATTEMPT_STARTED.txt').write_text(now_local().isoformat()+'\n')
        client=OpenAI(api_key=key,max_retries=0,timeout=75)
        investigator=PhasedInvestigator(client,patient,lambda j:atomic_json(ROOT/'ACTION_JOURNAL.json',j))
        commit=investigator.run()
        result.update({'G1':'PASS','commitment':commit,'commitment_mode':investigator.commitment_mode,
                       'diagnostics_used':dict(investigator.counts)})
        gain=commit['gain']
        result['G2']=assess_evidence(gain,investigator.observations)
        if gain is None:
            result['status']='ABSTAINED'
            return result
        # Holdout opened ONCE, AFTER final commitment. All simple/grid choices on DEV.
        basic_gains=[0,0.5,1,1.5]
        grid=[-3,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,3,4,5]
        dev_grid={str(g):patient.metrics(g,'target_dev')[0] for g in grid}
        best_grid=min(grid,key=lambda g:dev_grid[str(g)])
        holdout_candidates=sorted(set(basic_gains+[gain,best_grid]))
        holdout_target={str(g):patient.metrics(g,'target_test')[0] for g in holdout_candidates}
        healthy_target=patient.reference_metrics('target_test')[0]
        healthy_preserve, healthy_tokens=patient.reference_metrics('preserve_test')
        patched_preserve, patched_tokens=patient.metrics(gain,'preserve_test')
        retention=sum(a==b for a,b in zip(healthy_tokens,patched_tokens))/len(healthy_tokens)
        best_simple=min(holdout_target[str(g)] for g in basic_gains)
        evaluated=score_result(healthy_target,holdout_target[str(1)],holdout_target[str(gain)],
                               healthy_preserve,patched_preserve,retention,best_simple)
        result.update(evaluated)
        result.update({'status':'COMPLETE',
             'target_test':{'healthy':healthy_target,'corrupt':holdout_target[str(1)],
                            'patched':holdout_target[str(gain)]},
             'preserve_test':{'healthy':healthy_preserve,'patched':patched_preserve},
             'simple_baseline_target_losses':{str(g):holdout_target[str(g)] for g in basic_gains},
             'dev_grid':dev_grid,'grid_best_gain':best_grid,
             'grid_holdout_loss':holdout_target[str(best_grid)]})
        result['joint_success']=all(result[g]=='PASS' for g in ('G1','G2','G3','G4','G5'))
        return result
    except Exception as e:
        result.update({'status':'INTERRUPTED','error_type':type(e).__name__,
                       'reason':str(e)[:160] if type(e) in (ValueError,RuntimeError) else type(e).__name__})
        return result
    finally:
        patient.close()
        if investigator:
            atomic_json(ROOT/'ACTION_JOURNAL.json',investigator.journal)
            result['api_responses']=investigator.total_responses
            result['usage_input_tokens']=investigator.total_input_tokens
            result['usage_output_tokens']=investigator.total_output_tokens
        atomic_json(ROOT/'RESULTS.json',result)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('command', choices=['qualify','live'])
    args=ap.parse_args()
    out=qualify() if args.command=='qualify' else live()
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()