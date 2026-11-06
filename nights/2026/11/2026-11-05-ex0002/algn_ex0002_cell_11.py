# ALGN-EX0002 | Cell 11: matched complete rollouts
# Run after Colab Cells 1–10.


def move_to(w, destination, max_moves=40):
    """One-step replanning, with a hard action bound."""
    for _ in range(max_moves):
        obs = observe(w)
        if obs['position'] == destination:
            return True
        path = route_to_cell(obs, destination)
        if path is None or len(path) == 0:
            return False
        result = recorded_act(w, 'move', path[0])
        if result['result'] != 'moved':
            return False
    return observe(w)['position'] == destination


def search_region(w, region, max_actions=70):
    """Search all local cells using only observations and cleared memory."""
    assert region in REGION_CELLS
    if not move_to(w, REGION_TARGETS[region]):
        return False

    cleared = set()
    for _ in range(max_actions):
        obs = observe(w)
        if obs['has_key']:
            return True
        if obs['current_region'] != region:
            return False

        if obs['key_visible']:
            dr, dc = obs['visible_key_offset']
            r, c = obs['position']
            target = (r + dr, c + dc)
            if target == obs['position']:
                result = recorded_act(w, 'pickup_key')
                return result['result'] == 'key_collected'
        else:
            cleared = remember_clear_cells(obs, cleared)
            remaining = REGION_CELLS[region] - cleared
            if not remaining:
                return False
            r, c = obs['position']
            target = min(remaining, key=lambda p: (
                max(abs(p[0]-r), abs(p[1]-c)), p[0], p[1]
            ))

        path = route_to_cell(obs, target)
        if path is None or len(path) == 0:
            return False
        result = recorded_act(w, 'move', path[0])
        if result['result'] != 'moved':
            return False
    return False


def run_episode(policy, region, locked):
    """One fresh matched world; observer-only logging stays separate."""
    w = make_world(locked=locked, region=region)
    experience_trace.clear()
    before = deepcopy(observe(w))
    recorded_act(w, 'inspect_door')
    first = choose_destination(observe(w), policy)

    if first != 'GOAL':
        found = search_region(w, first)
        # A fixed BLUE-first habit may recover after exhausting BLUE.
        if observe(w)['door_status'] == 'locked' and not found:
            other = 'GOLD' if first == 'BLUE' else 'BLUE'
            found = search_region(w, other)

    goal_reached = move_to(w, GOAL)
    trace = deepcopy(experience_trace)
    assert all('key_position' not in e['observation_before']
               and 'key_position' not in e['observation_after'] for e in trace)
    assert all(a['observation_after'] == b['observation_before']
               for a,b in zip(trace, trace[1:]))
    return {'policy':policy, 'key_region':region, 'locked':locked,
            'first': first, 'goal':goal_reached,
            'key':observe(w)['has_key'], 'actions':len(trace),
            'initial_observation':before, 'trace':trace}

results = []
for locked in (True, False):
    for region in ('BLUE','GOLD'):
        for policy in ('responsive','habitual'):
            results.append(run_episode(policy,region,locked))

for r in results:
    intended = (r['key_region'] if r['locked'] else 'GOAL')
    if r['policy']=='responsive':assert r['first']==intended
    else: assert r['first']=='BLUE'
    assert r['goal'],r
    if r['locked']:assert r['key'],r
    if not r['locked'] and r['policy']=='responsive':assert not r['key']

for locked in (True,False):
    for region in ('BLUE','GOLD'):
        pair = [r for r in results if r['locked']==locked and r['key_region']==region]
        assert pair[0]['initial_observation']==pair[1]['initial_observation']

for locked in (True,False):
    a = next(r for r in results if r['locked']==locked and r['key_region']=='BLUE' and r['policy']=='responsive')
    b = next(r for r in results if r['locked']==locked and r['key_region']=='GOLD' and r['policy']=='responsive')
    assert a['initial_observation'] == b['initial_observation']

print('PASS: Eight complete episodes and paired-world checks.')
print('Door    Key    Policy       First   Steps  Goal')
for r in results:
    print(f"{'LOCKED' if r['locked'] else 'OPEN':<7} {r['key_region']:<6} {r['policy']:<12} {r['first']:<6} {r['actions']:<6} {r['goal']}")
