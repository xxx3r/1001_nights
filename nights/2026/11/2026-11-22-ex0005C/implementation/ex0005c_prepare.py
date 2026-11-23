"""EX0005C prospective split-and-hash builder. Requires frozen Hugging Face datasets.

No held-out text is printed. All preflight selections are determined by identifiers,
source revisions and the frozen seed, never by model performance.
"""
import hashlib, json, sys, platform
from collections import defaultdict
from pathlib import Path
from ex0005c_scorer import reference

SEED = 'EX0005C-2026-11-22-v0.3-family-seal'
MODEL = 'Qwen/Qwen3-0.6B'
MODEL_REV = 'c1899de289a04d12100db370d81485cdf75e47ca'
GSM_REV = '740312add88f781978c0658806c59bc2815b9866'
SYMBOLIC_REV = '93b5b3758d9d9841ffe81d6cd2ae2b030685b078'


def h(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')).hexdigest()


def sort_ids(ids, namespace):
    return sorted(ids, key=lambda x: hashlib.sha256(f'{SEED}|{namespace}|{x}'.encode()).hexdigest())


def normalize(s):
    return ' '.join(str(s).lower().split())


def load_one(name, config, rev):
    from datasets import load_dataset
    obj = load_dataset(name, name=config, revision=rev)
    # Use the documented split if available; fail rather than silently concatenate.
    if 'test' in obj: return list(obj['test'])
    if 'train' in obj and len(obj) == 1: return list(obj['train'])
    if len(obj) == 1: return list(next(iter(obj.values())))
    raise ValueError(f'unexpected split structure {name}: {list(obj.keys())}')


def preservation():
    """60 synthetic and small factual items; deterministic key. Each has one canonical answer."""
    fact_pairs = [
        ('What is the capital of France?', 'Paris'),
        ('What is the capital of Japan?', 'Tokyo'),
        ('What is the capital of Kenya?', 'Nairobi'),
        ('What is the capital of Canada?', 'Ottawa'),
        ('What is the capital of Italy?', 'Rome'),
        ('What is the capital of Spain?', 'Madrid'),
        ('What is the capital of Egypt?', 'Cairo'),
        ('What is the capital of Peru?', 'Lima'),
        ('What is the capital of Greece?', 'Athens'),
        ('What is the capital of India?', 'New Delhi'),
        ('What is the capital of Norway?', 'Oslo'),
        ('What is the capital of Sweden?', 'Stockholm'),
        ('What is the capital of Australia?', 'Canberra'),
        ('What is the capital of Portugal?', 'Lisbon'),
        ('What is the capital of Thailand?', 'Bangkok'),
        ('What is the capital of Chile?', 'Santiago'),
        ('What is the capital of Turkey?', 'Ankara'),
        ('What is the capital of Argentina?', 'Buenos Aires'),
        ('What is the capital of Morocco?', 'Rabat'),
        ('What is the capital of Finland?', 'Helsinki'),
    ]
    grammar = [
        ('She ___ to school every morning. Choose: walk / walks.', 'walks'),
        ('They ___ on the bus now. Choose: is / are.', 'are'),
        ('He has ___ the letter. Choose: wrote / written.', 'written'),
        ('We ___ ready. Choose: am / are.', 'are'),
        ('This is ___ umbrella. Choose: a / an.', 'an'),
        ('The children ___ outdoors. Choose: plays / play.', 'play'),
        ('Yesterday I ___ a book. Choose: read / reads.', 'read'),
        ('That tree ___ tall. Choose: is / are.', 'is'),
        ('Maya and Tom ___ friends. Choose: is / are.', 'are'),
        ('I have ___ oranges. Choose: much / many.', 'many'),
        ('The cat ___ sleeping. Choose: is / are.', 'is'),
        ('Neither answer ___ correct. Choose: is / are.', 'is'),
        ('A pair of shoes ___ on the floor. Choose: is / are.', 'is'),
        ('There ___ three lamps. Choose: is / are.', 'are'),
        ('My sister ___ coffee. Choose: likes / like.', 'likes'),
        ('Each student ___ a pencil. Choose: has / have.', 'has'),
        ('He ran ___ than I did. Choose: faster / fastest.', 'faster'),
        ('They were ___ loudly. Choose: talk / talking.', 'talking'),
        ('I ___ finished now. Choose: have / has.', 'have'),
        ('She spoke ___. Choose: clear / clearly.', 'clearly'),
    ]
    # Self-contained symbolic syllogisms: no mathematics or external facts.
    logic = []
    for i in range(20):
        a = f'zavi{i}'
        b = f'lumor{i}'
        c = f'tarin{i}'
        if i % 2 == 0:
            prompt = f'All {a} are {b}. All {b} are {c}. If something is a {a}, must it be a {c}? Answer yes or no.'
            answer = 'yes'
        else:
            prompt = f'All {a} are {b}. Some {b} are {c}. Must every {a} be a {c}? Answer yes or no.'
            answer = 'no'
        logic.append((prompt,answer))
    categories = dict(factual=fact_pairs, grammar=grammar, logic=logic)
    assert all(len(v)==20 for v in categories.values())
    dev, hold = [], []
    for category, pairs in categories.items():
        records = [dict(id=f'pres_{category}_{i:02d}',family=category,source='synthetic_preservation',
                        question=q,truth=a,kind='text') for i,(q,a) in enumerate(pairs)]
        ordered = sorted(records,key=lambda r: h([SEED,r['id']]))
        dev.extend(ordered[:4]); hold.extend(ordered[4:])
    assert len(dev)==12 and len(hold)==48
    return dev,hold


def build_split(gsm_train, gsm_test, symbolic):
    # Apple original_id maps to GSM8K test row index per official dataset card.
    assert len(gsm_train)>24 and len(gsm_test)>24
    families=defaultdict(list)
    for row in symbolic:
        for key in ['id','instance','original_id','question','answer','original_question']:
            if key not in row: raise ValueError(f'missing Apple key {key}')
        orig=int(row['original_id'])
        if not 0<=orig<len(gsm_test): raise ValueError('Apple original_id not in GSM8K test')
        if normalize(row['original_question']) != normalize(gsm_test[orig]['question']):
            raise ValueError(f'Apple/GSM8K source family mismatch: {orig}; stop instead of guessing')
        families[(str(row['id']),orig)].append(row)
    # One generated variant per 24 *different* source family IDs.
    fam_keys=sort_ids(list(families),'symbolic_family')[:24]
    if len(fam_keys)!=24: raise ValueError('not enough symbolic families')
    held_symbols=[]
    used_gsm_ids=set()
    for template_id,orig in fam_keys:
        if orig in used_gsm_ids: raise ValueError('two selected Apple templates share original GSM8K family')
        used_gsm_ids.add(orig)
        rows=sorted(families[(template_id,orig)],key=lambda r:h([SEED,'symbolic_instance',str(r['instance'])]))
        row=rows[0]
        held_symbols.append(dict(id=f'symbolic:{template_id}:{row["instance"]}',family=f'original_gsm8k_test:{orig}',
                            source='apple/GSM-Symbolic:main', question=row['question'], truth=str(reference(row['answer'])),kind='math',
                            original_gsm_test_id=orig, template_id=template_id, instance=str(row['instance'])))
    # The ordinary GSM8K test holdout excludes every selected Apple source family.
    candidates=[i for i in range(len(gsm_test)) if i not in used_gsm_ids]
    ordinary=sort_ids(candidates,'gsm8k_test')[:24]
    devids=sort_ids(list(range(len(gsm_train))),'gsm8k_train')[:24]
    mathdev=[dict(id=f'gsm8k_train:{i}',family=f'gsm8k_train:{i}',source='openai/gsm8k:main/train',
                  question=gsm_train[i]['question'], truth=str(reference(gsm_train[i]['answer'])),kind='math') for i in devids]
    mathordinary=[dict(id=f'gsm8k_test:{i}',family=f'gsm8k_test:{i}',source='openai/gsm8k:main/test',
                  question=gsm_test[i]['question'], truth=str(reference(gsm_test[i]['answer'])),kind='math') for i in ordinary]
    assert len(mathdev)==24 and len(mathordinary)==24 and len(held_symbols)==24
    assert len({r['family'] for r in mathordinary + held_symbols}) == 48
    assert len({r['question'] for r in mathdev + mathordinary + held_symbols}) == 72
    return mathdev, mathordinary, held_symbols


def write_vault(root, gsm_train, gsm_test, symbolic):
    root=Path(root); root.mkdir(parents=True,exist_ok=True)
    dev,ordinary,structural=build_split(gsm_train,gsm_test,symbolic)
    pdev,phold=preservation()
    held=ordinary+structural+phold
    # Hash content so accidental in-memory/data edits can be detected after seal.
    # Only sealed evaluator may load holdout_vault.json after investigator commitment.
    manifest=dict(protocol='EX0005C_v0.3',status='PREFLIGHT_ONLY',
                  seed=SEED, model=MODEL,model_revision=MODEL_REV,
                  gsm8k_revision=GSM_REV,symbolic_revision=SYMBOLIC_REV,
                  counts={'math_dev':24,'preservation_dev':12,'math_ordinary_held':24,'math_symbolic_held':24,'preservation_held':48},
                  development_ids=[x['id'] for x in dev+pdev],
                  heldout_ids=[x['id'] for x in held],
                  dev_data_hash=h(dev+pdev),holdout_data_hash=h(held))
    (root/'development.json').write_text(json.dumps(dev+pdev,indent=2,ensure_ascii=False))
    (root/'holdout_vault.json').write_text(json.dumps(held,indent=2,ensure_ascii=False))
    (root/'manifest.json').write_text(json.dumps(manifest,indent=2))
    # Print only identifiers, checksums and counts, not held-out questions/answers.
    print('PREFLIGHT SEAL GENERATED; NO HOLDOUT EVALUATION')
    print(json.dumps({k:manifest[k] for k in ['counts','dev_data_hash','holdout_data_hash']},indent=2))
    return manifest


def main():
    from datasets import load_dataset
    print('Loading source-pinned dataset versions; no model inference')
    train=list(load_dataset('openai/gsm8k',name='main',split='train',revision=GSM_REV))
    test=list(load_dataset('openai/gsm8k',name='main',split='test',revision=GSM_REV))
    sym=load_one('apple/GSM-Symbolic','main',SYMBOLIC_REV)
    write_vault('ex0005c_seal',train,test,sym)

if __name__ == '__main__': main()
