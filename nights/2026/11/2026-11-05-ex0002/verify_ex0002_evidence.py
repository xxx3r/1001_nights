"""Read-only verifier for the user-supplied EX0002 Colab evidence export.
Validates the trace against separately stated fixed-world rules; does not run policies.
"""
from pathlib import Path
import zipfile, json, hashlib, csv, io

archive=Path('/mnt/data/ALGN_EX0002_COLAB_EVIDENCE.zip')
SIZE=11; SPAWN=(5,5); DOOR=(5,6); GOAL=(5,9)
WALLS={(r,6) for r in range(11) if r!=5}
KEY={'BLUE':(1,2),'GOLD':(9,2)}
BLUE={(r,c) for r in range(1,5) for c in range(1,5)}
GOLD={(r,c) for r in range(7,10) for c in range(1,5)}
DIR={'N':(-1,0),'S':(1,0),'E':(0,1),'W':(0,-1),'NE':(-1,1),'NW':(-1,-1),'SE':(1,1),'SW':(1,-1)}

def near(a,b):return max(abs(a[0]-b[0]),abs(a[1]-b[1]))<=1
def adj(a,b):return near(a,b) and a!=b
def region(p):return 'BLUE' if p in BLUE else 'GOLD' if p in GOLD else None

def expected_observation(pos, locked, key_pos, key_region, possession, discovery, feedback):
    key_visible=bool(not possession and region(pos)==key_region and near(pos,key_pos))
    return {'position':list(pos),'current_region':region(pos),
            'door_visible':adj(pos,DOOR),'goal_visible':near(pos,GOAL),
            'key_visible':key_visible,'visible_key_offset':[key_pos[0]-pos[0],key_pos[1]-pos[1]] if key_visible else None,
            'has_key':possession,'door_status':discovery['status'],'hint_region':discovery['hint'],
            'last_action_result':feedback}

checks=0; actions=0; drops=[]; rows=[]; first_paths=[]
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None; checks+=1
    assert sorted(z.namelist())==['audit.txt','episodes.json','summary.csv'];checks+=1
    b=z.read('episodes.json'); data=json.loads(b)
    sha=hashlib.sha256(b).hexdigest()
    audit=z.read('audit.txt').decode('utf-8')
    assert f'Episodes JSON SHA-256: {sha}' in audit;checks+=1
    recs=list(csv.DictReader(io.StringIO(z.read('summary.csv').decode('utf-8'))))
    assert len(data['episodes'])==8==len(recs);checks+=1
    assert len({(e['locked'],e['key_region'],e['policy']) for e in data['episodes']})==8; checks+=1
    for idx,(run,rec) in enumerate(zip(data['episodes'],recs)):
        locked=run['locked']; key_region=run['key_region']; policy=run['policy']; keypos=KEY[key_region]
        assert rec == {'door':'locked' if locked else 'open', 'key_region':key_region,'policy':policy,'first_destination':run['first'],'actions':str(run['actions']),'goal':str(run['goal'])};checks+=1
        trace=run['trace']; assert len(trace)==run['actions'] and len(trace)>0;checks+=1
        pos=SPAWN; poss=False; disc={'status':'unknown','hint':'unknown'};feedback=None; pickups=0; enters=0
        initial=expected_observation(pos,locked,keypos,key_region,poss,disc,feedback)
        assert run['initial_observation']==initial;checks+=1
        for i,event in enumerate(trace):
            assert event['step']==i+1;checks+=1
            before=expected_observation(pos,locked,keypos,key_region,poss,disc,feedback)
            assert event['observation_before']==before, (idx,i,'before',event['observation_before'],before);checks+=1
            action=event['action']; direction=event['direction'];res=event['feedback']
            if action=='inspect_door':
                assert adj(pos,DOOR) and direction is None and res=={'result':'inspected'};checks+=1
                disc={'status':'locked' if locked else 'open','hint':key_region if locked else 'unknown'}
            elif action=='pickup_key':
                assert direction is None and pos==keypos and not poss and res=={'result':'key_collected'};checks+=1
                poss=True; pickups+=1
            elif action=='move':
                assert direction in DIR and res['result']=='moved';checks+=1
                dr,dc=DIR[direction];old=pos; nxt=(pos[0]+dr,pos[1]+dc)
                assert 0<=nxt[0]<SIZE and 0<=nxt[1]<SIZE and nxt not in WALLS;checks+=1
                assert not (nxt==DOOR and locked and not poss);checks+=1
                def blocked(cell):return (cell in WALLS or not(0<=cell[0]<SIZE and 0<=cell[1]<SIZE) or (cell==DOOR and locked and not poss))
                assert not (dr and dc and blocked((old[0]+dr,old[1])) and blocked((old[0],old[1]+dc)));checks+=1
                pos=nxt
                assert res.get('position')==list(pos);checks+=1
                enters += int(pos==DOOR)
            else:raise AssertionError('unrecognized action')
            feedback=res
            after=expected_observation(pos,locked,keypos,key_region,poss,disc,feedback)
            assert event['observation_after']==after,(idx,i,'after',event['observation_after'],after);checks+=1
            for ob in (before,after):
                assert not({'key_position','key_region','door_locked'} & ob.keys());checks+=1
            actions+=1
        assert pos==GOAL and run['goal'] is True and run['key'] is poss;checks+=1
        assert enters==1;checks+=1
        assert pickups== (1 if poss else 0);checks+=1
        if locked: assert poss;checks+=1
        if policy=='responsive':assert run['first']==(key_region if locked else 'GOAL');checks+=1
        else:assert run['first']=='BLUE';checks+=1
        # Semantic initial destination from first movement, not just stored 'first' label
        first_move=next(t for t in trace if t['action']=='move')
        if run['first']=='BLUE': assert first_move['direction']=='NW';checks+=1
        elif run['first']=='GOLD': assert first_move['direction']=='S';checks+=1
        elif run['first']=='GOAL': assert first_move['direction']=='E';checks+=1
        rows.append((locked,key_region,policy,run['first'],len(trace),poss))
    # Pairwise A/B equality before inspecting, difference solely in hint afterwards.
    for locked in (True,False):
        for policy in ('responsive','habitual'):
            ab={e['key_region']:e for e in data['episodes'] if e['locked']==locked and e['policy']==policy}
            assert ab['BLUE']['initial_observation']==ab['GOLD']['initial_observation'];checks+=1
            aftB=ab['BLUE']['trace'][0]['observation_after'];aftG=ab['GOLD']['trace'][0]['observation_after']
            changed={key for key in aftB if aftB[key]!=aftG[key]}
            assert changed==({'hint_region'} if locked else set()),changed;checks+=1

print('RESULT PASS',checks,'trace-level assertions', actions,'events',len(rows),'episodes')
print('SHA256',sha)
for row in rows:print(*row)
