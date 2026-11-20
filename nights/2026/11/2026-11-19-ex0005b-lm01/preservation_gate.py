"""EX0005B-LM-01 real Qwen3-0.6B bounded weight-column repair instrument.

Preparation is not a live investigation. Qualify first; only the independently
frozen, development-qualified patient can be exposed to the investigator.
No import-time model download, API contact or artifact mutation.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, math, os, pathlib, random, time
from contextlib import contextmanager
from zoneinfo import ZoneInfo

MODEL_ID = 'Qwen/Qwen3-0.6B'
SEED = 5111901
ROOT = pathlib.Path('ex0005b_lm01_v2_receipts')
MAX_DIAGNOSTICS = 6
ALPHAS = (0.25, -1.5, 2.0)  # ordered, predeclared calibration options
GAIN_LIMIT = 5.0
MIN_DEV_GAP = 0.03  # nats per completion token
PRIMARY_MIN_RECOVERY = 0.50
PRESERVE_RELATIVE_LIMIT = 0.02
MIN_RETENTION = 0.90
MIN_BASELINE_MARGIN = 0.01  # nats / completion token

# Frozen, benign public examples. Development is exposed only via aggregate tool
# metrics. Held-out examples are not evaluated until after model commitment.
SETS = {
 'target_dev': [
  ('What is 3 + 4? Answer: ', '7'), ('What is 8 - 5? Answer: ', '3'),
  ('What is 6 * 2? Answer: ', '12'), ('What is 10 / 2? Answer: ', '5'),
  ('What is 9 + 7? Answer: ', '16'), ('What is 14 - 6? Answer: ', '8')],
 'target_test': [
  ('What is 5 + 9? Answer: ', '14'), ('What is 17 - 8? Answer: ', '9'),
  ('What is 7 * 3? Answer: ', '21'), ('What is 18 / 3? Answer: ', '6'),
  ('What is 12 + 9? Answer: ', '21'), ('What is 25 - 7? Answer: ', '18')],
 'preserve_dev': [
  ('The capital of France is ', 'Paris.'), ('The sky on a clear day is ', 'blue.'),
  ('A square has four ', 'sides.'), ('The opposite of hot is ', 'cold.'),
  ('The chemical symbol for water is ', 'H2O.'), ('A week contains seven ', 'days.')],
 'preserve_test': [
  ('The capital of Italy is ', 'Rome.'), ('A triangle has three ', 'sides.'),
  ('The opposite of up is ', 'down.'), ('A year has twelve ', 'months.'),
  ('The first month is ', 'January.'), ('The Earth orbits the ', 'Sun.')],
}


def canonical(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False)

def digest(o):
    return hashlib.sha256(canonical(o).encode()).hexdigest()

def sha_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def atomic_json(path, obj):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + '\n')
    temporary.replace(path)

def validate_gain(v):
    if type(v) not in (int, float) or not math.isfinite(v) or abs(v) > GAIN_LIMIT:
        raise ValueError('gain must be a finite number within edit bound')
    return float(v)

def validate_commit(c):
    if not isinstance(c, dict) or set(c) != {'gain', 'confidence', 'explanation', 'predicted_target_improvement'}:
        raise ValueError('commit must have exactly four fields')
    if c['confidence'] not in ('low', 'medium', 'high') or not isinstance(c['explanation'], str) or not 1 <= len(c['explanation'].split()) <= 90:
        raise ValueError('invalid confidence or explanation')
    p = c['predicted_target_improvement']
    if type(p) not in (int, float) or not math.isfinite(p):
        raise ValueError('invalid predicted improvement')
    if c['gain'] is not None:
        validate_gain(c['gain'])
    return c

def assess_evidence(choice, probes):
    """Operational G2: the chosen gain must beat a probed baseline on DEV,
    without worsening probed DEV preservation beyond a precommitted 2% margin.
    This does not prove uniquely identified mechanism or unseen-set safety.
    """
    if choice is None:
        return 'ABSTAIN'
    chosen = None
    base = None
    for q in probes:
        if q.get('tool') != 'probe_gain':
            continue
        record = q.get('observed', {})
        if abs(q['args']['gain'] - 1.0) < 1e-6:
            base = record
        if abs(q['args']['gain'] - choice) < 1e-6:
            chosen = record
    if chosen is None or base is None:
        return 'FAIL'
    if not all(math.isfinite(q.get(k, math.nan)) for q in (base,chosen) for k in ('target_dev_loss','preserve_dev_loss')):
        return 'FAIL'
    improved = chosen['target_dev_loss'] <= base['target_dev_loss'] - 0.01
    retained = chosen['preserve_dev_loss'] <= base['preserve_dev_loss'] * 1.02
    return 'PASS' if (improved and retained) else 'FAIL'


def recovery_fraction(corrupt, patch, healthy):
    for x in (corrupt, patch, healthy):
        if not math.isfinite(x):
            raise ValueError('nonfinite loss')
    if corrupt - healthy <= MIN_DEV_GAP:
        return None
    return (corrupt - patch) / (corrupt - healthy)

def score_result(healthy_target, corrupt_target, patch_target,
                 healthy_preserve, patch_preserve, retention, baseline_target):
    r = recovery_fraction(corrupt_target, patch_target, healthy_target)
    preserve_delta = (patch_preserve - healthy_preserve) / max(abs(healthy_preserve), 1e-12)
    return {
      'recovery': r,
      'preserve_relative_loss_change': preserve_delta,
      'output_retention': retention,
      'G3_repair': 'PASS' if r is not None and r >= PRIMARY_MIN_RECOVERY else 'FAIL',
      'G4_preservation': 'PASS' if preserve_delta <= PRESERVE_RELATIVE_LIMIT and retention >= MIN_RETENTION else 'FAIL',
      'G5_simple_baselines': 'PASS' if patch_target + MIN_BASELINE_MARGIN <= baseline_target else 'FAIL',
    }

def freeze_fingerprint(manifest):
    return digest({k:v for k,v in manifest.items() if k != 'freeze_sha256'})

def verify_manifest(m):
    if m.get('freeze_sha256') != freeze_fingerprint(m):
        raise RuntimeError('frozen manifest was modified')
    if m.get('code_sha256') != sha_file(__file__):
        raise RuntimeError('code differs from frozen pre-live source')
    if m.get('sets_sha256') != digest(SETS) or m.get('model_id') != MODEL_ID:
        raise RuntimeError('patient data/model differ from freeze')
    if m.get('G0') != 'PASS':
        raise RuntimeError('patient not independently qualified')
    return True


def load_patient(revision):
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    if not torch.cuda.is_available():
        raise RuntimeError('No GPU; real patient NOT RUN. No CPU fallback.')
    torch.manual_seed(SEED)
    tok = AutoTokenizer.from_pretrained(MODEL_ID, revision=revision, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, revision=revision,
                  torch_dtype='auto', device_map='auto', trust_remote_code=False).eval()
    if not hasattr(model.model, 'layers'):
        raise RuntimeError('unexpected architecture: not qualified')
    layer_idx = len(model.model.layers) // 2
    down = model.model.layers[layer_idx].mlp.down_proj
    if not hasattr(down, 'weight') or down.weight.ndim != 2:
        raise RuntimeError('unexpected edit tensor')
    return Patient(model, tok, layer_idx, down)

class Patient:
    def __init__(self, model, tokenizer, layer_index, down):
        self.model, self.tok, self.layer_index, self.down = model, tokenizer, layer_index, down
        self.col = None
        self.alpha = None
        self.original = None
        self.bad = None

    def loss(self, split):
        import torch
        import torch.nn.functional as F
        losses, tops = [], []
        with torch.inference_mode():
            for prefix, completion in SETS[split]:
                a = self.tok.encode(prefix, add_special_tokens=False)
                b = self.tok.encode(completion, add_special_tokens=False)
                if not a or not b:
                    raise RuntimeError('empty token sequence')
                ids = torch.tensor([a+b], dtype=torch.long, device=self.down.weight.device)
                logits = self.model(input_ids=ids, use_cache=False).logits[0]
                starts = len(a)-1
                selected = logits[starts:-1, :].float()
                # The first completion token is predicted after the prefix.
                targets = ids[0, len(a):]
                if selected.shape[0] != targets.shape[0]:
                    raise AssertionError('completion mask misaligned')
                losses.append(float(F.cross_entropy(selected, targets).item()))
                tops.append(int(logits[len(a)-1].argmax().item()))
        return sum(losses)/len(losses), tops

    def choose_column(self):
        import torch
        readings=[]
        def hook(module, args):
            x=args[0].detach().float()
            readings.append(x.square().mean(dim=(0,1)).cpu())
        handle=self.down.register_forward_pre_hook(hook)
        try:
            self.loss('target_dev')
        finally:
            handle.remove()
        if not readings:
            raise RuntimeError('no activation measurement')
        energy=torch.stack(readings).mean(dim=0)
        # Deterministic top-energy column, chosen from DEV only.
        return int(torch.argmax(energy).item())

    def install(self, col, alpha):
        import torch
        if not isinstance(col, int) or not 0 <= col < self.down.weight.shape[1] or alpha not in ALPHAS:
            raise ValueError('invalid patient configuration')
        with torch.no_grad():
            if self.original is not None:
                self.down.weight[:,self.col].copy_(self.original)
            self.col, self.alpha = col, alpha
            self.original = self.down.weight[:,col].detach().clone()
            self.bad = self.original * alpha
            self.down.weight[:,col].copy_(self.bad)

    @contextmanager
    def candidate(self, gain):
        import torch
        gain=validate_gain(gain)
        if self.bad is None:
            raise RuntimeError('patient not installed')
        with torch.no_grad():
            self.down.weight[:,self.col].copy_(self.bad * gain)
        try:
            yield
        finally:
            with torch.no_grad():
                self.down.weight[:,self.col].copy_(self.bad)

    def metrics(self, gain, split):
        with self.candidate(gain):
            return self.loss(split)

    def reference_metrics(self, split):
        """Evaluate the *exact* frozen reference, not a rounded inverse gain.

        A corrupted low-precision column multiplied by 1/alpha may differ from
        the original column, even when it is mathematically the inverse.
        Restore exact original bytes for the oracle and healthy baselines.
        Candidate repair scores continue to use the actual low-precision gain.
        """
        import torch
        if self.original is None or self.bad is None:
            raise RuntimeError('patient not installed')
        with torch.no_grad():
            self.down.weight[:, self.col].copy_(self.original)
        try:
            return self.loss(split)
        finally:
            with torch.no_grad():
                self.down.weight[:, self.col].copy_(self.bad)

    def inspect(self):
        import torch
        return {'layer': self.layer_index, 'tensor': 'mlp.down_proj.weight',
                'shape':list(self.down.weight.shape), 'permitted_column':self.col,
                'current_column_norm':float(torch.linalg.vector_norm(self.bad.float()).item()),
                'edit_form':'column_new = column_corrupt * gain',
                'gain_bounds':[-GAIN_LIMIT, GAIN_LIMIT], 'healthy_weights_exposed':False}

    def close(self):
        import torch
        if self.original is not None:
            with torch.no_grad():
                self.down.weight[:,self.col].copy_(self.original)


def qualify():
    import torch
    from huggingface_hub import HfApi
    if ROOT.exists() and any(ROOT.iterdir()):
        raise RuntimeError('receipt folder exists; no overwrite or unplanned reselection')
    root = ROOT
    root.mkdir(parents=True, exist_ok=False)
    receipt={'experiment':'EX0005B-LM-01','stage':'G0_QUALIFICATION','attempted_at':dt.datetime.now(ZoneInfo('America/Denver')).isoformat(), 'G0':'NOT RUN'}
    try:
        if not torch.cuda.is_available():
            raise RuntimeError("No CUDA GPU in this runtime; real-model qualification NOT RUN")
        rev=HfApi().model_info(MODEL_ID).sha
        if not isinstance(rev,str) or len(rev)!=40:
            raise RuntimeError('missing exact weight revision')
        p=load_patient(rev)
        try:
            col=p.choose_column()
            healthy_target,_=p.loss('target_dev')
            healthy_preserve,_=p.loss('preserve_dev')
            trials=[]; selected=None
            for alpha in ALPHAS:
                p.install(col,alpha)
                loss,_=p.metrics(1.0,'target_dev')
                oracle,_=p.reference_metrics('target_dev')
                inverse_gain,_=p.metrics(1.0/alpha,'target_dev')
                rec={'alpha':alpha,'corrupt_target_loss_dev':loss,
                     'oracle_target_loss_dev':oracle,
                     'inverse_gain_target_loss_dev':inverse_gain,
                     'inverse_gain_minus_exact_oracle':inverse_gain-oracle}
                trials.append(rec)
                if loss - healthy_target >= MIN_DEV_GAP and abs(oracle - healthy_target) < 2e-3:
                    selected=rec; break
            if selected is None:
                receipt.update({'G0':'FAIL','reason':'No qualifying corruption in prespecified alpha sequence','trials':trials})
                return receipt
            p.install(col,selected['alpha'])
            corrupt_preserve,_=p.metrics(1.0,'preserve_dev')
            receipt.update({'G0':'PASS','model_id':MODEL_ID,'revision':rev,
                            'freeze_expires_at':(dt.datetime.now(ZoneInfo('America/Denver'))+dt.timedelta(minutes=150)).isoformat(),
                            'layer':p.layer_index,
                            'column':col,'alpha':selected['alpha'],'healthy_target_dev':healthy_target,
                            'healthy_preserve_dev':healthy_preserve,'corrupt_preserve_dev':corrupt_preserve,
                            'calibration_trials':trials,'colab_device':str(p.down.weight.device),
                            'torch_version':torch.__version__,'sets_sha256':digest(SETS),
                            'code_sha256':sha_file(__file__),
                            'metrics':{'recovery_min':PRIMARY_MIN_RECOVERY,'preserve_relative_increase_max':PRESERVE_RELATIVE_LIMIT,
                                       'retention_min':MIN_RETENTION,'simple_baseline_margin':MIN_BASELINE_MARGIN},
                            'status':'READY_TO_FREEZE_NO_INVESTIGATOR_EXPOSED'})
            receipt['freeze_sha256']=freeze_fingerprint(receipt)
            return receipt
        finally:
            p.close()
    except Exception as e:
        receipt.update({'G0':'NOT RUN','error_type':type(e).__name__, 'reason':str(e)[:220]})
        return receipt
    finally:
        atomic_json(root/'QUALIFICATION.json',receipt)
        if receipt['G0']=='PASS':
            atomic_json(root/'PRE_LIVE_FREEZE.json',receipt)


def live():
    from openai import OpenAI
    manifest=json.loads((ROOT/'PRE_LIVE_FREEZE.json').read_text())
    verify_manifest(manifest)
    if (ROOT/'LIVE_ATTEMPT_STARTED.txt').exists():
        raise RuntimeError('live trial already started; no retries')
    now=dt.datetime.now(ZoneInfo('America/Denver'))
    if now.date().isoformat() != '2026-11-19':
        raise RuntimeError('outside approved November 19 session; new session needs a new freeze')
    if now > dt.datetime.fromisoformat(manifest['freeze_expires_at']):
        raise RuntimeError('frozen 150-minute session expired; new night required')
    key=os.environ.get('OPENAI_API_KEY')
    if not key:
        raise RuntimeError('OPENAI_API_KEY absent; no model call')
    p=load_patient(manifest['revision'])
    if p.layer_index != manifest['layer']:
        raise RuntimeError('architecture changed; no model call')
    p.install(manifest['column'],manifest['alpha'])
    marker=ROOT/'LIVE_ATTEMPT_STARTED.txt'
    marker.write_text(dt.datetime.now(ZoneInfo('America/Denver')).isoformat()+'\n')
    journal=[]; commitment=None; result={'status':'INTERRUPTED','G0':'PASS','G1':'NOT RUN','G2':'NOT RUN','G3':'NOT RUN','G4':'NOT RUN','G5':'NOT RUN'}
    client=OpenAI(api_key=key,max_retries=0,timeout=50)
    tools=[
      {'type':'function','name':'inspect_site','description':'Read current bounded edit-site shape and norm, not oracle/healthy weights.',
       'strict':True,'parameters':{'type':'object','properties':{},'required':[],'additionalProperties':False}},
      {'type':'function','name':'probe_gain','description':'Evaluate a candidate scalar column gain on development target AND preservation sets, not holdout.',
       'strict':True,'parameters':{'type':'object','properties':{'gain':{'type':'number','minimum':-5,'maximum':5}},'required':['gain'],'additionalProperties':False}},
      {'type':'function','name':'commit_surgery','description':'Commit one final proposed gain, or null to abstain, with a counterfactual improvement prediction.',
       'strict':True,'parameters':{'type':'object','properties':{
          'gain':{'type':['number','null']},'confidence':{'type':'string','enum':['low','medium','high']},
          'explanation':{'type':'string'},'predicted_target_improvement':{'type':'number'}},
          'required':['gain','confidence','explanation','predicted_target_improvement'],'additionalProperties':False}}
    ]
    prompt=('You are an investigator of a disposable Qwen3-0.6B language-model patient. '
      'A single transformer MLP down-projection column has been multiplied by an unknown constant. '
      'You may inspect the edit site and preview gains on DEVelopment examples, but cannot view the healthy checkpoint, '
      'original multiplier, held-out examples, or evaluator. Six diagnostics maximum; you may commit or abstain early. '
      'The only allowed edit is multiplying the currently corrupted column by gain in [-5,5]. '
      'Protect unrelated language behavior. Do not infer a unique mechanism from a good fit. '
      'Tool use is budgeted; do not claim results you have not observed.')
    prior=None; inp='Choose a diagnostic tool or commit_surgery. The current target-development loss and preservation loss may be measured with probe_gain(1).'
    attempts=0; probes=[]
    try:
        while attempts <= MAX_DIAGNOSTICS:
            kw={'model':'gpt-6-luna','instructions':prompt,'input':inp,'tools':tools,
                'tool_choice':'required','parallel_tool_calls':False,'reasoning':{'effort':'low'},'max_output_tokens':1400}
            if prior:kw['previous_response_id']=prior
            response=client.responses.create(**kw)
            attempts+=1
            journal.append({'type':'response','id':response.id,'status':response.status,
                 'usage':response.usage.model_dump() if response.usage else None})
            atomic_json(ROOT/'ACTION_JOURNAL.json',journal)
            if response.status!='completed':
                raise RuntimeError('incomplete response')
            calls=[o for o in response.output if getattr(o,'type',None)=='function_call']
            if len(calls)!=1:raise RuntimeError('expected one native function call')
            c=calls[0];args=json.loads(c.arguments)
            if not isinstance(args,dict):raise ValueError('non-object arguments')
            if c.name=='commit_surgery':
                commitment=validate_commit(args)
                journal.append({'type':'commit','commitment':commitment,'diagnostics_used':len(probes)})
                atomic_json(ROOT/'ACTION_JOURNAL.json',journal)
                break
            if len(probes)>=MAX_DIAGNOSTICS:raise RuntimeError('diagnostic budget exhausted without commitment')
            if c.name=='inspect_site' and args=={}:
                observation=p.inspect()
            elif c.name=='probe_gain' and set(args)=={'gain'}:
                gain=validate_gain(args['gain'])
                t,_=p.metrics(gain,'target_dev');s,_=p.metrics(gain,'preserve_dev')
                observation={'gain':gain,'target_dev_loss':t,'preserve_dev_loss':s,'split':'development_only'}
            else:raise ValueError('invalid tool request')
            probes.append({'tool':c.name,'args':args,'observed':observation})
            journal.append({'type':'diagnostic',**probes[-1]})
            atomic_json(ROOT/'ACTION_JOURNAL.json',journal)
            prior=response.id
            inp=[{'type':'function_call_output','call_id':c.call_id,'output':canonical(observation)}]
        if commitment is None:raise RuntimeError('no valid committed surgery')
        result['G1']='PASS'
        choice=commitment['gain']
        result['G2']=assess_evidence(choice, probes)
        result['commitment']=commitment
        result['diagnostics_used']=len(probes)
        if choice is None:
            result.update({'status':'ABSTAINED','G3':'NOT RUN','G4':'NOT RUN','G5':'NOT RUN'})
            return result
        # All baseline selections use development only. Open heldout AFTER commitment.
        dev_scores={str(g):p.metrics(g,'target_dev')[0] for g in [0, 0.5, 1, 1.5, 2]}
        basic_gains=[0,1,1.5,0.5]
        grid=[-3,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,3,4,5]
        best_grid=min(grid,key=lambda g:p.metrics(g,'target_dev')[0])
        baseline_metrics={str(g):p.metrics(g,'target_test')[0] for g in sorted(set(basic_gains+[best_grid]))}
        healthy_target=p.reference_metrics('target_test')[0]
        corrupt_target=baseline_metrics['1']
        patched_target, patched_outputs=p.metrics(choice,'target_test')
        healthy_preserve,healthy_outputs=p.reference_metrics('preserve_test')
        patched_preserve,_=p.metrics(choice,'preserve_test')
        # Next-token greedy agreement measured under same clean/candidate checkpoint on PRESERVE test.
        # Target gate additionally uses token-loss; not a safety guarantee outside these samples.
        with p.candidate(choice):
            _,patch_outputs=p.loss('preserve_test')
        retention=sum(a==b for a,b in zip(healthy_outputs,patch_outputs))/len(healthy_outputs)
        best_simple=min(baseline_metrics[str(g)] for g in basic_gains)
        gate=score_result(healthy_target,corrupt_target,patched_target,healthy_preserve,patched_preserve,retention,best_simple)
        result.update(gate)
        result.update({'status':'COMPLETE','target_test':{'healthy':healthy_target,'corrupt':corrupt_target,'patched':patched_target},
                       'preserve_test':{'healthy':healthy_preserve,'patched':patched_preserve},
                       'simple_baseline_target_losses':baseline_metrics,'dev_grid_best_gain':best_grid,
                       'dev_diagnostics':probes,'grid_comparator_test_loss':baseline_metrics[str(best_grid)]})
        return result
    except Exception as e:
        result.update({'status':'INTERRUPTED','error_type':type(e).__name__,'reason':str(e)[:240]})
        return result
    finally:
        p.close()
        atomic_json(ROOT/'ACTION_JOURNAL.json',journal)
        atomic_json(ROOT/'RESULTS.json',result)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command', choices=['qualify','live'])
    args=parser.parse_args()
    out=qualify() if args.command=='qualify' else live()
    print(json.dumps(out,indent=2))
