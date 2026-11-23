"""EX0005Cc independent difficulty-calibration pilot. No model/heldout access here.

Apple rows are retrieved only at runtime (license CC BY-NC-ND 4.0); no source
questions are distributed in this module. The historical EX0005C manifest is
read-only, referenced by SHA and excluded from source-family selection.
"""
from __future__ import annotations
import hashlib
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from ex0005c_scorer import reference

RUN_ID = 'EX0005Cc-AET-2026-11-22-v1'
MODEL = 'Qwen/Qwen3-0.6B'
MODEL_REV = 'c1899de289a04d12100db370d81485cdf75e47ca'
APPLE = 'apple/GSM-Symbolic'
APPLE_REV = '93b5b3758d9d9841ffe81d6cd2ae2b030685b078'
HISTORICAL_RECEIPT_SHA256 = '6d07111bcaf81af2a123f12ea12887b3d222e162347b111d7ef2d92b0a80ce01'
# Historical EX0005C identifiers only. Never load old held-out prompt/answer text.
EXCLUDED_TEMPLATE = frozenset([96,34,72,47,54,24,27,26,93,56,67,33,81,3,11,18,90,77,48,19,73,64,10,30])
EXCLUDED_GSM_ORIG = frozenset([1183,1184,605,1316,919,893,980,910,912,453,1,1020,1194,1200,240,478,902,1142,224,13,76,1238,338,684])
STRATA = ('main','p1','p2','synthetic')
PILOT_N = {'main':8,'p1':8,'p2':8,'synthetic':8}
# Ordered candidate mixtures. Ties favor earlier mixture. No additional candidates after pilot.
MIXTURES = (
    ('A', (4,8,8,4)),
    ('B', (4,4,12,4)),
    ('C', (0,8,8,8)),
    ('D', (0,4,12,8)),
    ('E', (0,4,8,12)),
    ('F', (0,0,12,12)),
)
TARGET = 0.55
ACCURACY_RANGE = (0.30, 0.75)
MIN_COMPLETE = 0.75

def sh(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def ordered(values, namespace):
    return sorted(values,key=lambda v: hashlib.sha256(f'{RUN_ID}|{namespace}|{v}'.encode()).hexdigest())

def prompt_id(row):
    return (int(row['id']),int(row['original_id']),int(row['instance']))

def synthetic_one(family: str, index: int, phase: str):
    rng = random.Random(int(sh([RUN_ID,'synthetic',phase,family,index])[:16],16))
    if family=='inventory':
        # Ensure exact integral shipment and a realistic remainder.
        cartons = rng.randrange(8,19)
        units = rng.randrange(9,20)
        extras = rng.randrange(3,10)
        extra_units = rng.randrange(6,16)
        f = rng.choice([2,3,4])
        whole = cartons*units + extras*extra_units
        # Add a small integer remainder to make the inventory exactly divisible by f.
        adjustments = (-whole)%f
        removed = rng.randrange(2,6)
        remove_units = rng.randrange(2,8)
        restock = rng.randrange(7,22)
        answer = (whole+adjustments)*(f-1)//f - removed*remove_units + restock
        q=(f'A workshop stocked {cartons} cartons with {units} gears each, then {extras} cartons with '
           f'{extra_units} gears each, and found {adjustments} loose gears. It shipped exactly 1/{f} '
           f'of its entire stock. After shipping, {removed} repair kits used {remove_units} gears each, '
           f'and a late delivery brought {restock} gears. How many gears remain?')
        check = whole+adjustments-(whole+adjustments)//f-removed*remove_units+restock
    elif family=='tickets':
        adults=rng.randrange(24,47); children=rng.randrange(13,30)
        adult_price=rng.randrange(9,22); child_price=rng.randrange(5,10)
        refund_a=rng.randrange(2,7); refund_c=rng.randrange(2,6)
        costs=rng.randrange(22,49); bonus=rng.randrange(9,23)
        answer=(adults-refund_a)*adult_price+(children-refund_c)*child_price-costs+bonus
        q=(f'A club sold {adults} adult tickets for ${adult_price} each and {children} child tickets '
           f'for ${child_price} each. Before the event it fully refunded {refund_a} adult tickets '
           f'and {refund_c} child tickets. It then paid ${costs} to rent equipment and received '
           f'a ${bonus} contribution. What is its net amount of money in dollars?')
        check=adults*adult_price+children*child_price-refund_a*adult_price-refund_c*child_price-costs+bonus
    elif family=='rates':
        teams=rng.randrange(3,7); drivers=rng.randrange(3,7)
        per=rng.randrange(8,19); days=rng.randrange(3,8)
        used=rng.randrange(20,48); loss=rng.randrange(6,17); reserve=rng.randrange(13,31)
        answer=teams*drivers*per*days - used*days - loss + reserve
        q=(f'A depot has {teams} teams with {drivers} drivers on each team. Every driver delivers '
           f'{per} packages per day for {days} days. Each day the depot uses {used} delivered '
           f'packages for testing. Another {loss} packages were damaged at the end, but the depot '
           f'also receives {reserve} reserve packages. How many usable packages does the depot have?')
        check=(teams*drivers*per-used)*days-loss+reserve
    elif family=='equations':
        b=rng.randrange(8,19); mult=rng.choice([2,3,4]); more=rng.randrange(4,15)
        moved=rng.randrange(2,8); join=rng.randrange(1,8)
        total=b + mult*b + (b+more)
        answer=(b+more)-moved+join
        q=(f'Before a workshop, three classrooms A, B and C contain {total} students altogether. '
           f'Room A has exactly {mult} times as many students as room B; room C has exactly '
           f'{more} more students than room B. Later {moved} students leave room C and '
           f'{join} students join room C. How many students are in C afterward?')
        recovered=(total-more)//(mult+2)
        check=recovered+more-moved+join
    else:
        raise ValueError('unknown synthetic family')
    assert isinstance(answer,int) and answer==check and answer>=0
    return {'id':f'synthetic:{phase}:{family}:{index}',
            'stratum':'synthetic','kind':'math','family':f'synthetic:{family}',
            'question':q,'truth':str(answer),'oracle':'two_formula_python',
            'parameters_hash':sh([family,phase,index])}

def build_synthetic(phase: str, count: int):
    families=['inventory','tickets','rates','equations']
    return [synthetic_one(families[i%len(families)],i//len(families),phase)
            for i in range(count)]

def load_apple():
    from datasets import load_dataset
    return {name:list(load_dataset(APPLE,name=name,split='test',revision=APPLE_REV))
            for name in ('main','p1','p2')}

def construct_apple(calibrations: dict):
    """Disjoint GSM source families across pilot/validation and all three Apple variants."""
    pool={}
    for stratum,rows in calibrations.items():
        assert stratum in ('main','p1','p2')
        families=defaultdict(list)
        for row in rows:
            keys=('id','instance','original_id','question','answer','original_question')
            if any(k not in row for k in keys): raise ValueError(f'Apple schema mismatch {stratum}')
            template,orig,inst=prompt_id(row)
            if template in EXCLUDED_TEMPLATE or orig in EXCLUDED_GSM_ORIG:
                continue
            families[(template,orig)].append(row)
        pool[stratum]=families
        if len(families)<32:
            raise ValueError(f'insufficient eligible Apple source families in {stratum}: {len(families)}')
    used=set()
    pilot={name:[] for name in STRATA}
    validate={name:[] for name in STRATA}
    for stage,required in [('pilot',PILOT_N),('validation',{'main':4,'p1':8,'p2':12})]:
        for stratum in ('main','p1','p2'):
            eligible=ordered(pool[stratum],f'{stage}|{stratum}|family')
            count=0
            for family in eligible:
                _,orig=family
                if orig in used: continue
                instances=sorted(pool[stratum][family],key=lambda r:hashlib.sha256(
                    f'{RUN_ID}|{stage}|{stratum}|instance|{r["instance"]}'.encode()).hexdigest())
                row=instances[0]
                record={'id':f'apple:{stratum}:{row["id"]}:{row["instance"]}',
                        'stratum':stratum,'family':f'gsm8k_test:{orig}',
                        'kind':'math','question':row['question'],
                        'truth':str(reference(row['answer'])),
                        'oracle':'apple_benchmark_key','template_id':int(row['id']),
                        'original_id':orig,'instance':int(row['instance']),
                        'source':f'{APPLE}:{stratum}@{APPLE_REV}'}
                (pilot if stage=='pilot' else validate)[stratum].append(record)
                used.add(orig); count+=1
                if count==required[stratum]: break
            if count != required[stratum]:
                raise ValueError(f'could not reserve {required[stratum]} unique families for {stage}/{stratum}; got {count}')
    pilot['synthetic']=build_synthetic('pilot',8)
    validate['synthetic']=build_synthetic('validation',12)
    flat_pilot=[r for stratum in STRATA for r in pilot[stratum]]
    assert len(flat_pilot)==32
    assert len(set(r['family'] for r in flat_pilot if r['stratum']!='synthetic'))==24
    assert not (set(r['family'] for r in flat_pilot if r['stratum']!='synthetic') &
                set(r['family'] for name in ('main','p1','p2') for r in validate[name]))
    return pilot, validate

def select_distribution(results):
    """Pilot results contain {'stratum','score':{'completed','correct'},'id'}.

    Select on *stratum averages*, never on which individual calibration items were wrong.
    No hyperparameter repair or post-score extra mixture proposals.
    """
    if len(results)!=32 or len({r['id'] for r in results})!=32:
        raise ValueError('must supply exactly the precommitted 32 unique pilot outputs')
    strata={}
    for name in STRATA:
        rows=[r for r in results if r['stratum']==name]
        if len(rows)!=8: raise ValueError(f'missing or duplicate {name} stratum')
        if not all(isinstance(r['score']['correct'],bool) and
                   isinstance(r['score']['completed'],bool) for r in rows):
            raise ValueError('invalid scored values')
        if any(r['score']['correct'] and not r['score']['completed'] for r in rows):
            raise ValueError('inconsistent correctness/completion')
        strata[name]={'n':8,'correct':sum(r['score']['correct'] for r in rows),
                      'complete':sum(r['score']['completed'] for r in rows)}
    summary=[]
    for name,weights in MIXTURES:
        predicted_correct=sum(weights[j]*strata[s]['correct']/8 for j,s in enumerate(STRATA))
        predicted_complete=sum(weights[j]*strata[s]['complete']/8 for j,s in enumerate(STRATA))
        p=predicted_correct/24; c=predicted_complete/24
        eligible = ACCURACY_RANGE[0]<=p<=ACCURACY_RANGE[1] and c>=MIN_COMPLETE
        summary.append({'mixture':name,'weights':dict(zip(STRATA,weights)),
                        'predicted_correct_of_24':predicted_correct,
                        'predicted_accuracy':p,'predicted_completion':c,
                        'eligible':eligible})
    candidates=[x for x in summary if x['eligible']]
    if candidates:
        choice=min(candidates,key=lambda x:(abs(x['predicted_accuracy']-TARGET),
                                            next(j for j,(n,_) in enumerate(MIXTURES) if x['mixture']==n)))
        disposition='PROVISIONAL_DISTRIBUTION_SELECTED'
    else:
        choice=None
        disposition='NO_QUALIFIED_DISTRIBUTION'
    return {'protocol':RUN_ID,'pilot':strata,'candidates':summary,
            'choice':choice,'disposition':disposition,
            'caveat':'Only 8 pilot outputs per stratum; this is a model-based provisional mixture, not validated generalization.'}

def write_qualification_pack(root, pilot, validation):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    pilot_rows=[r for s in STRATA for r in pilot[s]]
    # Validation source pool may be generated, and IDs sealed, but never scored here.
    meta={'protocol':RUN_ID,'status':'CALIBRATION_PREPARED',
          'historical_receipt_sha256':HISTORICAL_RECEIPT_SHA256,
          'model':MODEL,'model_revision':MODEL_REV,
          'apple_revision':APPLE_REV,
          'pilot_ids':[r['id'] for r in pilot_rows],
          'validation_pool_ids':[r['id'] for s in STRATA for r in validation[s]],
          'pilot_content_hash':sh(pilot_rows),
          'validation_pool_hash':sh(validation)}
    (root/'pilot.json').write_text(json.dumps(pilot_rows,indent=2,ensure_ascii=False))
    (root/'validation_pool_DO_NOT_SCORE.json').write_text(json.dumps(validation,indent=2,ensure_ascii=False))
    (root/'manifest.json').write_text(json.dumps(meta,indent=2))
    return meta

def validate_selection(choice, validation):
    """Seal 24 disjoint qualification IDs based on stratum weights, never pilot outcomes."""
    if not choice: return None
    picked=[]
    for s in STRATA:
        n=choice['weights'][s]
        selected=validation[s][:n]
        if len(selected)!=n:raise ValueError(f'insufficient fresh {s} validation rows')
        picked.extend(selected)
    if len(picked)!=24:raise ValueError('selected validation must total 24')
    if len({r['id'] for r in picked})!=24:raise ValueError('duplicate validation ID')
    return {'protocol':RUN_ID,'status':'PROSPECTIVE_QUALIFICATION_ONLY_NOT_SCORED',
            'distribution':choice,'validation_ids':[r['id'] for r in picked],
            'validation_content_hash':sh(picked)},picked
