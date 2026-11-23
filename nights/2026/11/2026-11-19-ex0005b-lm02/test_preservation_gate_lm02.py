"""Offline tests only: no network, no GPU model, no investigator API contact."""
import json, math, unittest
from types import SimpleNamespace as NS
from unittest.mock import patch
import preservation_gate_lm02 as m

class FakePatient:
    def inspect_site(self):
        return {'shape':[1024,3072],'column':5}
    def input_probe(self,family,index):
        return {'family':family,'index':index,'site_rms':0.1}
    def output_probe(self,family,index):
        return {'family':family,'index':index,'loss':0.2}
    def output_summary(self,family):
        return {'family':family,'mean_loss':0.2}
    def metrics(self,gain,split):
        if split=='target_dev':
            return 0.22-0.04*(1-gain), []
        return 6.5+0.005*abs(gain), []

class NativeFake:
    def __init__(self,selection):
        self.selection=selection
        self.calls=[]
        self.responses=self
    def create(self,**kw):
        self.calls.append(kw)
        name,args=self.selection(kw,len(self.calls)-1)
        tools={t['name'] for t in kw['tools']}
        # Test enforces that advertised native menu disallows inappropriate tools.
        if name not in tools:
            raise AssertionError('fake attempted an unavailable tool: '+name)
        if isinstance(kw['tool_choice'],dict):
            assert name==kw['tool_choice']['name']
        call=NS(type='function_call',name=name,arguments=json.dumps(args),call_id=f'call-{len(self.calls)}')
        return NS(id=f'resp-{len(self.calls)}',status='completed',usage=None,output=[call])

def final(gain):
    return {'gain':gain,'confidence':'medium','explanation':'Based on the observed development comparison, this gain is supported.',
            'predicted_target_improvement':0.04}

class GateTests(unittest.TestCase):
    def test_gain_rejections(self):
        for x in (float('inf'),float('nan'),True,'0',5.01,-5.01):
            with self.subTest(x=x),self.assertRaises(ValueError): m.validate_gain(x)
    def test_gain_boundaries(self):
        self.assertEqual(m.validate_gain(-5),-5.0)
        self.assertEqual(m.validate_gain(5),5.0)
    def test_commit_abstention(self):
        c=final(None)
        self.assertEqual(m.validate_commit(c),c)
    def test_commit_malformed(self):
        for c in ({'gain':1}, {**final(1),'extra':1},{**final(1),'gain':float('nan')},
                  {**final(1),'predicted_target_improvement':True},{**final(1),'explanation':''}):
            with self.subTest(c=c),self.assertRaises(ValueError):m.validate_commit(c)
    def test_repair_evidence(self):
        observations=[{'phase':'repair','tool':'probe_gain','args':{'gain':1.0},
                       'observed':{'target_dev_loss':0.22,'preserve_dev_loss':6.5}},
                      {'phase':'repair','tool':'probe_gain','args':{'gain':0.0},
                       'observed':{'target_dev_loss':0.18,'preserve_dev_loss':6.52}}]
        self.assertEqual(m.assess_evidence(0,observations),'PASS')
        self.assertEqual(m.assess_evidence(.5,observations),'FAIL')
        self.assertEqual(m.assess_evidence(None,observations),'ABSTAIN')
    def test_input_phase_cannot_count_as_repair_evidence(self):
        obs=[{'phase':'input','tool':'probe_gain','args':{'gain':1},'observed':{'target_dev_loss':0.22,'preserve_dev_loss':6.5}},
             {'phase':'input','tool':'probe_gain','args':{'gain':0},'observed':{'target_dev_loss':0.18,'preserve_dev_loss':6.5}}]
        self.assertEqual(m.assess_evidence(0,obs),'FAIL')
    def test_recovery_min_gap(self):
        self.assertIsNone(m.recovery_fraction(1,1.001,0.5))
    def test_recovery_negative_preserved(self):
        self.assertLess(m.recovery_fraction(0.15,0.22,0.25),0)
    def test_repair_pass_preservation_fail(self):
        x=m.score_result(.15,.22,.15,6.5,7.0,0.99,.18)
        self.assertEqual(x['G3'],'PASS')
        self.assertEqual(x['G4'],'FAIL')
    def test_repair_pass_retention_fail(self):
        x=m.score_result(.15,.22,.15,6.5,6.5,0.6,.18)
        self.assertEqual(x['G4'],'FAIL')
    def test_simple_baseline_must_be_beaten(self):
        x=m.score_result(.15,.22,.16,6.5,6.5,1,.16)
        self.assertEqual(x['G3'],'PASS')
        self.assertEqual(x['G4'],'PASS')
        self.assertEqual(x['G5'],'FAIL')
    def test_sealed_prompts_unique(self):
        all_prompts=[a for group in m.SETS.values() for a,_ in group]
        self.assertEqual(len(all_prompts),len(set(all_prompts)))
        self.assertEqual(len(m.SETS['target_dev']),12)
        self.assertEqual(len(m.SETS['target_test']),18)
        self.assertEqual(len(m.SETS['preserve_dev']),12)
        self.assertEqual(len(m.SETS['preserve_test']),18)
    def test_phase_menus_disjoint(self):
        self.assertNotIn('probe_gain',[t['name'] for t in m.INPUT_TOOLS])
        self.assertNotIn('probe_gain',[t['name'] for t in m.OUTPUT_TOOLS])
        self.assertNotIn('inspect_input',[t['name'] for t in m.REPAIR_TOOLS])
        self.assertEqual([t['name'] for t in m.COMMIT_ONLY],['commit_surgery'])
    def test_full_budget_auto_transition_then_forced_commit(self):
        def f(kw,i):
            if i<6:return 'inspect_input',{'family':'target','index':i}
            if i<12:return 'inspect_output',{'family':'preserve','index':i-6}
            if i<18:return 'probe_gain',{'gain':([1,0,.5,-.5,.25,-1][i-12])}
            return 'commit_surgery',final(-.5)
        fake=NativeFake(f)
        agent=m.PhasedInvestigator(fake,FakePatient())
        c=agent.run()
        self.assertEqual(c['gain'],-.5)
        self.assertEqual(agent.counts,{'input':6,'output':6,'repair':6})
        self.assertEqual(agent.commitment_mode,'forced_final')
        self.assertEqual(agent.total_responses,19)
        self.assertEqual(fake.calls[-1]['tool_choice'],{'type':'function','name':'commit_surgery'})
        self.assertEqual(agent.journal[-1]['mode'],'forced_final')
        # Final request must deliver the sixth repair probe result before asking to commit.
        self.assertEqual(fake.calls[-1]['input'][0]['type'],'function_call_output')
    def test_early_exit_and_voluntary_commit(self):
        def f(kw,i):
            seq=[('inspect_site',{}),('finish_phase',{'reason':'enough'}),
                 ('summarize_outputs',{'family':'target'}),('finish_phase',{'reason':'enough'}),
                 ('probe_gain',{'gain':1}),('probe_gain',{'gain':0}),('commit_surgery',final(0))]
            return seq[i]
        fake=NativeFake(f)
        agent=m.PhasedInvestigator(fake,FakePatient())
        agent.run()
        self.assertEqual(agent.counts,{'input':1,'output':1,'repair':2})
        self.assertEqual(agent.commitment_mode,'voluntary')
        self.assertEqual(agent.total_responses,7)
        self.assertEqual(m.assess_evidence(0,agent.observations),'PASS')
        self.assertEqual(fake.calls[2]['input'][0]['type'],'function_call_output')
        self.assertEqual(fake.calls[2]['input'][1]['role'],'user')
    def test_final_abstain(self):
        def f(kw,i):
            if i in (0,1):return 'finish_phase',{'reason':'no evidence'}
            return 'commit_surgery',final(None)
        agent=m.PhasedInvestigator(NativeFake(f),FakePatient())
        agent.run()
        self.assertEqual(agent.commitment['gain'],None)
        self.assertEqual(m.assess_evidence(None,agent.observations),'ABSTAIN')
    def test_no_seventh_repair_probe(self):
        def f(kw,i):
            if i<6:return 'inspect_site',{}
            if i<12:return 'summarize_outputs',{'family':'target'}
            return 'probe_gain',{'gain':1}
        fake=NativeFake(f)
        agent=m.PhasedInvestigator(fake,FakePatient())
        with self.assertRaisesRegex(RuntimeError,'API exception: AssertionError'):
            agent.run()
        self.assertEqual(agent.counts['repair'],6)
        self.assertEqual(agent.total_responses,18)
        self.assertEqual(fake.calls[-1]['tool_choice'],{'type':'function','name':'commit_surgery'})
    def test_no_import_side_effect(self):
        self.assertFalse(hasattr(m,'API_KEY'))
    def test_distinct_patient_excludes_lm01_column(self):
        self.assertEqual(m.PRIOR_EXCLUDED_COLUMN,4)
    def test_phase_budget_exact(self):
        self.assertEqual(m.PHASE_BUDGET,{'input':6,'output':6,'repair':6})

if __name__=='__main__':unittest.main()
