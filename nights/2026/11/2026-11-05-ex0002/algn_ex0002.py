#!/usr/bin/env python3
"""ALGN-EX0002: bounded, seeded, information-limited toy POMDP instrument.

AI-drafted implementation; not evidence of independent human coding mastery.
Standard library only. See ALGN_EX0002_PRE_REGISTERED_PLAN.md in xxx3r/1001_nights.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from copy import deepcopy
from hashlib import sha256
import heapq
import json
import random
import sys

SIZE = 11
SPAWN = (5, 5)
DOOR = (5, 6)
GOAL = (5, 8)
SEEDS = (7, 11, 23, 47, 101)  # Frozen before any execution.
MAX_STEPS = 240
DIRECTIONS = {"N": (-1, 0), "NE": (-1, 1), "E": (0, 1), "SE": (1, 1),
              "S": (1, 0), "SW": (1, -1), "W": (0, -1), "NW": (-1, -1)}
REGIONS = {
    "BLUE": frozenset((r, c) for r in range(0, 3) for c in range(0, 4)),
    "GOLD": frozenset((r, c) for r in range(8, 11) for c in range(0, 4)),
}


def close(a, b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1])) <= 1


def inside(p):
    return 0 <= p[0] < SIZE and 0 <= p[1] < SIZE


def geometry_neighbors(walls, p, pass_door=True):
    """Reference geometry: forbid a diagonal only when both side cells block."""
    for name, (dr, dc) in DIRECTIONS.items():
        q = (p[0]+dr, p[1]+dc)
        if not inside(q) or q in walls or (not pass_door and q == DOOR):
            continue
        if dr and dc:
            p1 = (p[0]+dr, p[1]); p2 = (p[0], p[1]+dc)
            blocked1 = p1 in walls or (not pass_door and p1 == DOOR)
            blocked2 = p2 in walls or (not pass_door and p2 == DOOR)
            if blocked1 and blocked2:
                continue
        yield name, q


def policy_bfs(walls, start, end, pass_door):
    """Agent's static-map route finder, no hidden dynamic state supplied."""
    if start == end:
        return []
    q = deque([start]); previous = {start: (None, None)}
    while q:
        p = q.popleft()
        for action, nxt in geometry_neighbors(walls, p, pass_door):
            if nxt not in previous:
                previous[nxt] = (p, action)
                if nxt == end:
                    result = []; at = end
                    while at != start:
                        before, act = previous[at]; result.append('move:'+act); at = before
                    return result[::-1]
                q.append(nxt)
    return None


def oracle_distance(walls, start, end, pass_door=True):
    """Separately implemented Dijkstra distance for fixture eligibility/validation."""
    heap = [(0, start)]; best = {start: 0}
    while heap:
        dist, p = heapq.heappop(heap)
        if dist != best[p]:
            continue
        if p == end:
            return dist
        for dr, dc in DIRECTIONS.values():
            q = (p[0]+dr, p[1]+dc)
            if not (0 <= q[0] < SIZE and 0 <= q[1] < SIZE):
                continue
            if q in walls or (not pass_door and q == DOOR):
                continue
            if dr != 0 and dc != 0:
                a, b = (p[0]+dr,p[1]), (p[0],p[1]+dc)
                if (a in walls or (not pass_door and a == DOOR)) and (b in walls or (not pass_door and b == DOOR)):
                    continue
            if dist+1 < best.get(q, 10**9):
                best[q] = dist+1
                heapq.heappush(heap, (dist+1,q))
    return None


@dataclass(frozen=True)
class Fixture:
    seed: int
    walls: frozenset
    blue_key: tuple
    gold_key: tuple
    rejected: int
    attempts: int


def make_fixture(seed):
    rng = random.Random(seed)
    rejections = 0
    for attempt in range(1, 41):
        # Wall across column 6 has precisely one door; randomized clutter is on the near side.
        walls = {(r, 6) for r in range(SIZE) if r != DOOR[0]}
        # These explicit hallways guarantee useful access to each search region.
        reserved = {(r,5) for r in range(SIZE)}
        reserved |= {(2,c) for c in range(6)} | {(8,c) for c in range(6)}
        # The right corridor to the goal remains free of obstacles.
        clutter_candidates = [(r,c) for r in range(SIZE) for c in range(5)
                              if (r,c) not in reserved]
        for cell in rng.sample(clutter_candidates, 13):
            walls.add(cell)
        eligible = {}
        for region, cells in REGIONS.items():
            options = []
            for p in cells - walls:
                d = oracle_distance(walls, SPAWN, p, pass_door=False)
                if d is not None and d >= 4 and not close(p, SPAWN):
                    options.append((p, d))
            eligible[region] = sorted(options)
        pairs = [(b,g) for b in eligible['BLUE'] for g in eligible['GOLD']
                 if abs(b[1]-g[1]) <= 1]
        if not pairs or oracle_distance(walls, SPAWN, GOAL) is None:
            rejections += 1
            continue
        b, g = rng.choice(pairs)
        return Fixture(seed, frozenset(walls), b[0], g[0], rejections, attempt)
    raise RuntimeError(f"Seed {seed}: procedural generation exhausted 40 attempts")


@dataclass(frozen=True)
class WorldSpec:
    fixture: Fixture
    region: str
    locked: bool

    @property
    def key(self):
        return self.fixture.blue_key if self.region == 'BLUE' else self.fixture.gold_key


class MiniWorld:
    """Only observe()/step() outputs are shared with policies; never pass world to agent."""
    def __init__(self, spec):
        self.spec = spec
        self.position = SPAWN
        self.key_owned = False
        self.door_known = 'unknown'
        self.hint_known = 'unknown'
        self.last_result = 'none'
        self.ended = False
        self.steps = 0
        self.total_reward = 0.0

    def observe(self):
        f = self.spec.fixture
        # Static map is allowed; hidden key coordinate and dynamic door state are NOT.
        mask = ["move:"+name for name,_ in geometry_neighbors(f.walls, self.position, True)]
        mask += ['pickup']  # This must NOT reveal whether an object is present.
        if close(self.position, DOOR):
            mask.append('inspect_door')  # Adjacency, never actual door state.
        visible_key = None if self.key_owned or not close(self.position, self.spec.key) else list(self.spec.key)
        return {
            "position": list(self.position),
            "static": {
                "size": SIZE,
                "spawn": list(SPAWN), "door": list(DOOR), "goal": list(GOAL),
                "walls": [list(p) for p in sorted(f.walls)],
                "regions": {name: [list(p) for p in sorted(cells)] for name, cells in REGIONS.items()},
            },
            "local_objects": {"key": visible_key, "door_visible": close(self.position, DOOR)},
            "inventory": {"key": self.key_owned},
            "discovered": {"door_status": self.door_known, "hint_region": self.hint_known},
            "last_result": self.last_result,
            "action_mask": sorted(mask),
        }

    def step(self, action):
        if self.ended:
            raise ValueError('Episode already completed')
        reward = -0.01
        self.steps += 1
        if action == 'inspect_door':
            if close(self.position, DOOR):
                self.door_known = 'locked' if self.spec.locked else 'open'
                self.hint_known = self.spec.region if self.spec.locked else 'unknown'
                self.last_result = 'door_'+self.door_known
            else:
                self.last_result = 'not_adjacent'
        elif action == 'pickup':
            if self.position == self.spec.key and not self.key_owned:
                self.key_owned = True
                self.last_result = 'key_collected'
            else:
                self.last_result = 'nothing_to_pick_up'
        elif action.startswith('move:') and action[5:] in DIRECTIONS:
            dr, dc = DIRECTIONS[action[5:]]
            new = (self.position[0]+dr, self.position[1]+dc)
            allowed = dict(geometry_neighbors(self.spec.fixture.walls, self.position, True))
            if action[5:] not in allowed:
                self.last_result = 'blocked_wall'
            elif new == DOOR and self.spec.locked and not self.key_owned:
                self.last_result = 'door_blocked'
            else:
                self.position = new
                self.last_result = 'moved'
                if new == GOAL:
                    self.ended = True
                    self.last_result = 'goal_reached'
                    reward += 1.0
        else:
            self.last_result = 'invalid_action'
        self.total_reward += reward
        return self.observe(), reward, self.ended


class ScriptedPolicy:
    """No world truth or environment object: only serializable observations."""
    def __init__(self, responsive):
        self.responsive = responsive
        self.memory_seen = set()  # Explicit external visited/observed-cell register.
        self.first_search_region = None
        self.search_order = None
        self.selected_region = None
        self.entered_region = None
        self.regions_exhausted = set()

    def _path(self, obs, dest, pass_door=False):
        w = frozenset(tuple(x) for x in obs['static']['walls'])
        return policy_bfs(w, tuple(obs['position']), tuple(dest), pass_door)

    def choose(self, obs):
        loc = tuple(obs['position'])
        for r in range(max(0,loc[0]-1), min(SIZE,loc[0]+2)):
            for c in range(max(0,loc[1]-1), min(SIZE,loc[1]+2)):
                self.memory_seen.add((r,c))
        for name, cells in REGIONS.items():
            if loc in cells and self.entered_region is None:
                self.entered_region = name
        discovered = obs['discovered']
        if discovered['door_status'] == 'unknown':
            return 'inspect_door'
        if self.responsive and discovered['door_status'] == 'open':
            path = self._path(obs, GOAL, pass_door=True)
            if path is None:
                raise AssertionError('Cannot reach open goal')
            return path[0] if path else 'pickup'  # Already at goal implies episode done.
        if obs['inventory']['key']:
            path = self._path(obs, GOAL, pass_door=True)
            if path is None:
                raise AssertionError('Cannot reach goal with key')
            return path[0] if path else 'pickup'
        # In the habit policy, the region preference NEVER uses the acquired clue.
        if self.search_order is None:
            preferred = discovered['hint_region'] if self.responsive else 'BLUE'
            if preferred not in REGIONS:
                raise AssertionError('Responsive policy lacks a legitimate clue')
            other = 'GOLD' if preferred == 'BLUE' else 'BLUE'
            self.search_order = (preferred, other)
            self.first_search_region = preferred
        key = obs['local_objects']['key']
        if key is not None:
            if loc == tuple(key):
                return 'pickup'
            path = self._path(obs, tuple(key))
            if path is None:
                raise AssertionError('Observed key inaccessible')
            return path[0]
        walls = {tuple(x) for x in obs['static']['walls']}
        for region in self.search_order:
            if region in self.regions_exhausted:
                continue
            live = REGIONS[region] - walls
            unseen = live - self.memory_seen
            if not unseen:
                self.regions_exhausted.add(region)
                continue
            # Select a location in this region that exposes unobserved candidate cells.
            candidates = []
            for p in sorted(live):
                path = self._path(obs, p)
                if path is None:
                    continue
                exposure = sum(close(p, q) for q in unseen)
                if exposure:
                    candidates.append((-exposure, len(path), p, path))
            if not candidates:
                self.regions_exhausted.add(region)
                continue
            _, _, _, route = min(candidates)
            self.selected_region = region
            if route:
                return route[0]
            # Here already in candidate vantage point; next call should see expanded region.
            raise AssertionError('Exploration coverage stalled')
        raise AssertionError('No key found despite exhaustive inspection')


def oracle_goal_distance(spec):
    """Full-state Dijkstra over (position, possession), independent of scripted policy.
    Ignores door inspection (privileged oracle already knows the state).
    """
    walls = spec.fixture.walls
    heap = [(0, SPAWN, False)]
    best = {(SPAWN,False):0}
    while heap:
        steps, pos, has_key = heapq.heappop(heap)
        if steps != best[(pos,has_key)]:
            continue
        if pos == GOAL:
            return steps
        successors = []
        if pos == spec.key and not has_key:
            successors.append((pos, True))
        for dr, dc in DIRECTIONS.values():
            q = (pos[0]+dr,pos[1]+dc)
            if not inside(q) or q in walls or (q == DOOR and spec.locked and not has_key):
                continue
            if dr and dc:
                a,b=(pos[0]+dr,pos[1]),(pos[0],pos[1]+dc)
                if (a in walls or (a == DOOR and spec.locked and not has_key)) and (b in walls or (b == DOOR and spec.locked and not has_key)):
                    continue
            successors.append((q,has_key))
        for p,k in successors:
            if steps+1 < best.get((p,k),10**9):
                best[(p,k)] = steps+1
                heapq.heappush(heap,(steps+1,p,k))
    return None


def rollout(spec, responsive, max_steps=MAX_STEPS, trace=False, corrupt_hint=None):
    env = MiniWorld(spec)
    agent = ScriptedPolicy(responsive)
    actions = []; records = []
    for _ in range(max_steps):
        obs = env.observe()
        # Mutation is a test-only observation shim; never used for normal trials.
        if corrupt_hint is not None and obs['discovered']['hint_region'] != 'unknown':
            obs = deepcopy(obs)
            obs['discovered']['hint_region'] = corrupt_hint
        try:
            action = agent.choose(obs)
        except AssertionError as ex:
            return dict(done=False, error=str(ex), steps=env.steps,
                        first_search_region=agent.first_search_region,
                        first_entered_region=agent.entered_region, key_collected=env.key_owned,
                        invalid_actions=sum(a[1] in ('blocked_wall','invalid_action','not_adjacent') for a in actions),
                        reward=round(env.total_reward,5), trace=records)
        next_obs, reward, done = env.step(action)
        actions.append((action, next_obs['last_result']))
        if trace:
            records.append({'t':env.steps,'position':obs['position'], 'action':action,
                            'result':next_obs['last_result'], 'discovered':obs['discovered'],
                            'reward':reward})
        if done:
            break
    reference = oracle_goal_distance(spec)
    return {'done':env.ended, 'steps':env.steps, 'truncated':not env.ended,
            'first_search_region':agent.first_search_region,
            'first_entered_region':agent.entered_region,
            'key_collected':env.key_owned,
            'invalid_actions':sum(x[1] in ('blocked_wall','invalid_action','not_adjacent') for x in actions),
            'reference_steps':reference, 'excess_steps':env.steps-reference if reference is not None else None,
            'reward':round(env.total_reward,5), 'trace':records,
            'feedback_counts': {result:sum(x[1]==result for x in actions) for result in ('door_blocked','nothing_to_pick_up')},
        }


def check(label, fn, out):
    try:
        fn()
        out.append({'gate':label,'status':'PASS'})
    except Exception as ex:
        out.append({'gate':label,'status':'FAIL','error':f'{type(ex).__name__}: {ex}'})


def preflight():
    fixtures = [make_fixture(seed) for seed in SEEDS]
    trials = []
    gates = []
    worlds = [WorldSpec(f,c,l) for f in fixtures for l in (True,False) for c in ('BLUE','GOLD')]

    def a_geometry():
        for f in fixtures:
            assert f.attempts == f.rejected+1
            assert len(f.walls) <= SIZE*SIZE
            for p in (f.blue_key,f.gold_key):
                assert p not in f.walls
                assert p not in {SPAWN,DOOR,GOAL}
                assert not close(SPAWN,p)
                d = oracle_distance(f.walls,SPAWN,p,False)
                assert d is not None and d >= 4
            assert abs(oracle_distance(f.walls,SPAWN,f.blue_key,False)-oracle_distance(f.walls,SPAWN,f.gold_key,False))<=1
            assert close(SPAWN,DOOR)
            for p in [(r,c) for r in range(SIZE) for c in range(SIZE) if (r,c) not in f.walls]:
                for _,q in geometry_neighbors(f.walls,p,False):
                    dr,dc=q[0]-p[0],q[1]-p[1]
                    assert abs(dr)<=1 and abs(dc)<=1 and (dr or dc)
                    if dr and dc:
                        a,b=(p[0]+dr,p[1]),(p[0],p[1]+dc)
                        assert not (a in f.walls and b in f.walls)
        for spec in worlds:
            assert oracle_goal_distance(spec) is not None
    check('A_geometry',a_geometry,gates)

    def b_boundary():
        for f in fixtures:
            start = MiniWorld(WorldSpec(f,'BLUE',True)).observe()
            assert start == MiniWorld(WorldSpec(f,'GOLD',True)).observe()
            assert start == MiniWorld(WorldSpec(f,'BLUE',False)).observe()
            serialized=json.dumps(start,sort_keys=True)
            for p in [list(f.blue_key),list(f.gold_key)]:
                assert p != start['local_objects']['key']
            assert start['discovered']=={'door_status':'unknown','hint_region':'unknown'}
            assert start['local_objects']['key'] is None
            # The only field differing after the matched locked-door inspections is the clue.
            a, b = MiniWorld(WorldSpec(f,'BLUE',True)), MiniWorld(WorldSpec(f,'GOLD',True))
            oa, ra, _ = a.step('inspect_door')
            ob, rb, _ = b.step('inspect_door')
            assert ra == rb == -0.01
            assert oa['discovered']['hint_region'] == 'BLUE'
            assert ob['discovered']['hint_region'] == 'GOLD'
            ob['discovered']['hint_region'] = 'BLUE'
            assert oa == ob
            # No reward-shaping side channel: same pre-inspection move earns same reward.
            ma, mb = MiniWorld(WorldSpec(f,'BLUE',True)), MiniWorld(WorldSpec(f,'GOLD',True))
            va, rva, _ = ma.step('move:N')
            vb, rvb, _ = mb.step('move:N')
            assert rva == rvb == -0.01
            assert va == vb
            assert 'locked' not in json.dumps(start['action_mask'])
            assert 'inspect_door' in start['action_mask']
            assert 'locked' not in serialized and 'hint_region": "BLUE"' not in serialized
    check('B_observation_boundary',b_boundary,gates)

    def c_discovery():
        for spec in worlds:
            env=MiniWorld(spec)
            _obs,_,_=env.step('pickup')
            assert env.door_known=='unknown' and env.hint_known=='unknown'
            obs,_,_=env.step('inspect_door')
            assert obs['discovered']['door_status']==('locked' if spec.locked else 'open')
            assert obs['discovered']['hint_region']==(spec.region if spec.locked else 'unknown')
            if spec.locked:
                assert obs['discovered']['hint_region'] in ('BLUE','GOLD')
                assert obs['local_objects']['key'] is None
                assert list(spec.key) not in [obs['local_objects']['key']]
            # Acquired clue persists after a legal movement away from the door.
            obs,_,_=env.step('move:W')
            assert obs['discovered']['hint_region']==(spec.region if spec.locked else 'unknown')
    check('C_discovery',c_discovery,gates)

    def d_discrimination():
        for f in fixtures:
            for color in ('BLUE','GOLD'):
                s=WorldSpec(f,color,True)
                good=rollout(s,True)
                bad=rollout(s,False)
                assert good['done'] and bad['done'],(f.seed,color,good,bad)
                assert good['first_search_region']==color
                assert bad['first_search_region']=='BLUE'
                assert good['first_entered_region']==color
                assert bad['first_entered_region']=='BLUE'
                assert good['key_collected'] and bad['key_collected']
                if color=='GOLD':
                    assert bad['steps']>good['steps'], (f.seed,good['steps'],bad['steps'])
    check('D_baseline_discrimination',d_discrimination,gates)

    def e_conditional():
        for spec in worlds:
            result=rollout(spec,True)
            assert result['done'],(spec,result)
            if spec.locked:
                assert result['key_collected']
            else:
                assert not result['key_collected']
                assert result['first_search_region'] is None
                assert result['steps']==oracle_goal_distance(spec)+1  # Exactly one inspect.
        # An entirely keyless agent cannot cross the wall (including diagonals).
        for f in fixtures:
            assert oracle_distance(f.walls,SPAWN,GOAL,pass_door=False) is None
        # Direct locked attempt cannot enter door without possession.
        locked=MiniWorld(WorldSpec(fixtures[0],'BLUE',True))
        obs,_,_=locked.step('move:E')
        assert locked.position==SPAWN and obs['last_result']=='door_blocked'
        openworld=MiniWorld(WorldSpec(fixtures[0],'BLUE',False))
        obs,_,_=openworld.step('move:E')
        assert openworld.position==DOOR and obs['last_result']=='moved'
    check('E_conditional_key_use',e_conditional,gates)

    def f_feedback():
        for f in fixtures:
            for locked in (True,False):
                for color in ('BLUE','GOLD'):
                    env=MiniWorld(WorldSpec(f,color,locked))
                    mask=env.observe()['action_mask']
                    obs,_,_=env.step('pickup')
                    assert obs['last_result']=='nothing_to_pick_up'
                    assert obs['discovered']['door_status']=='unknown'
                    assert obs['action_mask']==mask
                    obs,_,_=env.step('move:N')
                    assert obs['discovered']['door_status']=='unknown'
                    if locked:
                        env=MiniWorld(WorldSpec(f,color,locked))
                        obs,_,_=env.step('move:E')
                        assert obs['last_result']=='door_blocked'
                        assert obs['discovered']=={'door_status':'unknown','hint_region':'unknown'}
                assert MiniWorld(WorldSpec(f,'BLUE',locked)).observe()['action_mask']==MiniWorld(WorldSpec(f,'GOLD',locked)).observe()['action_mask']
            assert MiniWorld(WorldSpec(f,'BLUE',True)).observe()['action_mask']==MiniWorld(WorldSpec(f,'BLUE',False)).observe()['action_mask']
    check('F_feedback_and_mask',f_feedback,gates)

    def g_reproduction():
        for seed in SEEDS:
            f1,f2=make_fixture(seed),make_fixture(seed)
            assert f1==f2
            a=WorldSpec(f1,'GOLD',True)
            b=WorldSpec(f2,'GOLD',True)
            assert MiniWorld(a).observe()==MiniWorld(b).observe()
            assert rollout(a,True,trace=True)==rollout(b,True,trace=True)
            assert rollout(a,False,trace=True)==rollout(b,False,trace=True)
    check('G_reproducibility',g_reproduction,gates)

    def h_mutation():
        for f in fixtures:
            spec=WorldSpec(f,'GOLD',True)
            normal=rollout(spec,True)
            mutated=rollout(spec,True,corrupt_hint='BLUE')
            assert normal['first_search_region']=='GOLD'
            assert mutated['first_search_region']=='BLUE'
            # The frozen intended assertion really must fail on the mutant.
            assertion_failed=False
            try:
                assert mutated['first_search_region']==spec.region
            except AssertionError:
                assertion_failed=True
            assert assertion_failed
    check('H_clue_mutation_kills_discrimination',h_mutation,gates)

    for spec in worlds:
        for responsive in (True,False):
            result=rollout(spec,responsive)
            trials.append({'seed':spec.fixture.seed,'locked':spec.locked,'key_region':spec.region,
                           'policy':'responsive' if responsive else 'habit_BLUE',
                           **{k:v for k,v in result.items() if k!='trace'}})
    report={
        'experiment':'ALGN-EX0002','source_plan':'ALGN_EX0002_PRE_REGISTERED_PLAN.md',
        'status':'PASS' if all(g['status']=='PASS' for g in gates) else 'FAIL',
        'seeds':list(SEEDS),'conditions':4,'policies':2,
        'fixture_attempts':sum(f.attempts for f in fixtures),
        'fixture_rejections':sum(f.rejected for f in fixtures),
        'fixture_hashes':{str(f.seed):sha256(json.dumps({
            'walls':sorted(f.walls),'blue_key':f.blue_key,'gold_key':f.gold_key},
            sort_keys=True).encode()).hexdigest() for f in fixtures},
        'tests':gates, 'trial_count':len(trials),
        'trials':trials,
        'provenance':{'agent':'AI-drafted deterministic scripts, not trained RL',
                      'reward':'-0.01 each action, +1 terminal goal, no hint-direction shaping',
                      'key_placement':'seeded matched-distance eligible cells, positions hidden',
                      'assistance':'D (AI-drafted)', 'execution':'local CPython standard library'},
    }
    return report


def main():
    report=preflight()
    print(json.dumps(report,indent=2,sort_keys=True))
    return 0 if report['status']=='PASS' else 1

if __name__=='__main__':
    sys.exit(main())
