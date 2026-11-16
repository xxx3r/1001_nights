"""Offline tests, including mock Response API protocol checks. No API token read."""
import json, pathlib, tempfile, types, unittest
from unittest.mock import patch
import numpy as np
import ex0005aa_public as p
import run_luna_aa as r

class FakeUsage:
    def model_dump(self):return {'input_tokens':50,'output_tokens':30}

class FakeResp:
    def __init__(self,i,name=None,arguments='{}',text=None,status='completed'):
        self.id=f'fake_{i}';self.model='FAKE_NOT_LUNA';self.status=status
        self.incomplete_details='max_messages' if status!='completed' else None
        self.usage=FakeUsage();self.output_text=text or ''
        self.output=([types.SimpleNamespace(type='function_call',name=name,arguments=arguments,call_id=f'call_{i}')] if name else [])

class FakeResponses:
    def __init__(self,queue):self.queue=list(queue);self.request_log=[]
    def create(self,**kwargs):
        self.request_log.append(kwargs)
        return self.queue.pop(0)

class Tests(unittest.TestCase):
    def test_fixture_and_oracles(self):
        q=p.qualification()
        self.assertEqual(q['status'],'G0_LOCAL_PASS_ONLY')
        self.assertLess(q['cases']['C_positive']['counterfactual_delta_mse'],0)
        self.assertGreater(q['cases']['C_negative']['counterfactual_delta_mse'],0)
        self.assertGreater(q['cases']['D_unknown']['heuristic_mse'],0.5)
        self.assertEqual(q['cases']['D_unknown']['oracle_mse'],0)
    def test_paired_single_change(self):
        a=p.make_case('C_positive');b=p.make_case('C_negative')
        self.assertTrue(np.array_equal(a.x_eval,b.x_eval))
        self.assertTrue(np.array_equal(a.y_eval,b.y_eval))
        for t in ('W1','b1','b2'):
            self.assertTrue(np.array_equal(a.w[t],b.w[t]))
        self.assertEqual(a.w['W2'][0],b.w['W2'][0])
    def test_bad_values_rejected(self):
        patient=p.make_case('D_unknown')
        for fn in [lambda:p.inspect_tensor(patient,'bad'),lambda:p.probe_pack(patient,'oops'),
                   lambda:p.apply_edit(patient,[{'tensor':'W1','index':0,'delta':500}]),
                   lambda:p.apply_edit(patient,[{'tensor':'W1','index':0,'delta':0.2},{'tensor':'W1','index':0,'delta':0.3}])]:
            with self.assertRaises(ValueError):fn()
    def test_numeric_commit_reject_wrong(self):
        ok={'predicted_delta_mse':-.2,'uncertainty':'high','explanation':'Tentatively correct sign'}
        self.assertEqual(r.validate_pair_commit(ok),ok)
        for bad in [{**ok,'predicted_delta_mse':float('nan')},{**ok,'explanation':''},{**ok,'unrecognized':1}]:
            with self.assertRaises(ValueError):r.validate_pair_commit(bad)
    def test_discovery_commit_validator(self):
        ok={'fault_region':'W1[0]','uncertainty':'high','patch':[],'explanation':'Insufficient evidence'}
        self.assertEqual(r.validate_discovery_commit(ok),ok)
        with self.assertRaises(ValueError):r.validate_discovery_commit({**ok,'fault_region':'W1[99]'})
    def test_human_origin_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            f=pathlib.Path(tmp)/'fields.json'
            d={k:'This prediction belongs to the earlier completed session.' for k in r.human_fields.__code__.co_consts if False}
            d={k:'This is an existing human hypothesis from our earlier session.' for k in ('human_predicted_failure','human_predicted_contrast','human_false_positive_test','human_unsupported_mechanism')}
            d.update(assistance_disclosure='C',origin='carried_from_EX0005A_pre_live',approved_as_prior_for_aa=False)
            f.write_text(json.dumps(d))
            with self.assertRaises(ValueError):r.human_fields(f)
            d['approved_as_prior_for_aa']=True;f.write_text(json.dumps(d))
            self.assertEqual(r.human_fields(f)['assistance_disclosure'],'C')
    def test_time_window_reject_closed_session(self):
        with self.assertRaises(RuntimeError):r.time_window({'session_date':'2026-11-15','session_start':'18:00','session_end':'21:00'})
    def test_pair_real_call_contract_mock(self):
        responses=FakeResponses([
            FakeResp(1,'inspect_output_weights'),FakeResp(2,'probe_feature1'),
            FakeResp(3,text=json.dumps({'predicted_delta_mse':-0.2,'uncertainty':'high','explanation':'Observed feature1 overprediction.'}))
        ])
        with tempfile.TemporaryDirectory() as tmp,patch.object(r,'time_window',lambda manifest:None):
            sess=r.Session(types.SimpleNamespace(responses=responses),{'session_date':'2026-11-19'})
            sess.outdir=pathlib.Path(tmp)
            state=sess.pair('C_positive')
            self.assertEqual(state['valid_calls'],2)
            self.assertEqual(state['kinds'],['inspect_output_weights','probe_feature1'])
            self.assertTrue(state['sign_correct'])
            self.assertEqual(len(responses.request_log),3)
            self.assertTrue(all(req['parallel_tool_calls'] is False for req in responses.request_log))
            self.assertTrue((pathlib.Path(tmp)/'ACTION_JOURNAL.json').exists())
    def test_discovery_can_beat_baseline_mock(self):
        picks=[('inspect_weights','{"tensor":"W1"}'),('probe_examples','{"pack":"feature0"}'),
               ('inspect_weights','{"tensor":"W2"}'),('probe_examples','{"pack":"mixed"}')]
        queue=[FakeResp(i+1,name,arguments) for i,(name,arguments) in enumerate(picks)]
        queue.append(FakeResp(5,text=json.dumps({'fault_region':'W1[0]','uncertainty':'high',
                   'patch':[{'tensor':'W1','index':0,'delta':1.3}],
                   'explanation':'The first hidden feature is suppressed; the edit would restore response.'})))
        responses=FakeResponses(queue)
        with tempfile.TemporaryDirectory() as tmp,patch.object(r,'time_window',lambda manifest:None):
            sess=r.Session(types.SimpleNamespace(responses=responses),{'session_date':'2026-11-19'})
            sess.outdir=pathlib.Path(tmp)
            state=sess.discovery()
            self.assertEqual(state['valid_calls'],4)
            self.assertTrue(state['patch_evaluation']['G4_pass'])
            self.assertTrue(all(req['parallel_tool_calls'] is False for req in responses.request_log))
    def test_incomplete_retained_not_passed(self):
        responses=FakeResponses([FakeResp(1,'inspect_output_weights',status='incomplete')])
        with tempfile.TemporaryDirectory() as tmp,patch.object(r,'time_window',lambda manifest:None):
            sess=r.Session(types.SimpleNamespace(responses=responses),{'session_date':'2026-11-19'})
            sess.outdir=pathlib.Path(tmp)
            with self.assertRaises(RuntimeError):sess.pair('C_positive')
            j=json.loads((pathlib.Path(tmp)/'ACTION_JOURNAL.json').read_text())
            self.assertEqual(j[0]['status'],'incomplete')
            self.assertEqual(j[0]['incomplete_details'],'max_messages')
    def test_summary_does_not_infer_success_from_incomplete(self):
        results={'cases':{'C_positive':{'valid_calls':2,'kinds':['inspect_output_weights','probe_feature1'],
                   'commit':{'predicted_delta_mse':-0.1},'sign_correct':True},
                   'C_negative':{'valid_calls':0,'kinds':[],'commit':None,'interruption':{'reason':'incomplete'}}}}
        out=r.evaluate(results,[])
        self.assertEqual(out['G1'],'FAIL')
        self.assertEqual(out['G3'],'FAIL')
        self.assertFalse(out['instrument_ready'])

if __name__=='__main__':unittest.main(verbosity=2)
