"""Independent small negative controls; no OpenAI calls."""
import json
import unittest
import numpy as np
from ex0005a_public import *
from run_luna import validate_commit, human_fields

class PublicChecker(unittest.TestCase):
    def test_and_oracle_and_bad(self):
        self.assertTrue(score_and((1,1,-1,1,0))['pass'])
        self.assertFalse(score_and((0,0,0,0,0))['pass'])
    def test_torch_numpy_agree(self):
        for n in ['P1_plus','P1_minus','P2']:
            p=make_patient(n)
            np.testing.assert_allclose(predict_numpy(p.w,p.x_eval),predict_torch(p.w,p.x_eval),atol=1e-12)
    def test_paired_is_matched_except_one_scalar(self):
        a,b=make_patient('P1_plus'),make_patient('P1_minus')
        np.testing.assert_array_equal(a.x_eval,b.x_eval)
        np.testing.assert_array_equal(a.y_eval,b.y_eval)
        for t in ('W1','b1','b2'):np.testing.assert_array_equal(a.w[t],b.w[t])
        self.assertEqual(float(a.w['W2'][1]),float(b.w['W2'][1]))
        self.assertAlmostEqual(float(a.w['W2'][0]-b.w['W2'][0]),1.5)
        self.assertLess(prediction_delta(a),0)
        self.assertGreater(prediction_delta(b),0)
    def test_negative_control_scoring(self):
        r=qualification()
        self.assertEqual(r['status'],'G0_LOCAL_PASS_ONLY')
        for x in r['cases'].values():
            self.assertGreater(x['no_edit_mse'],1e-4)
            self.assertLess(x['oracle_mse'],1e-15)
            self.assertGreater(x['zero_mse'],x['oracle_mse'])
    def test_malformed_tool_contract(self):
        p=make_patient('P1_plus')
        for f in [lambda:inspect_weights(p,'W2',3,1),
                  lambda:inspect_weights(p,'W2',0,50),
                  lambda:probe_examples(p,'feature0',[3]),
                  lambda:probe_examples(p,'feature1',[]),
                  lambda:apply_patch(p,[{'tensor':'W2','index':0,'delta':0.5},{'tensor':'W2','index':0,'delta':0.3}]),
                  lambda:apply_patch(p,[{'tensor':'W2','index':0,'delta':float('nan')}])]:
            with self.assertRaises(ValueError): f()
    def test_commit_checker(self):
        correct={'fault_region':'W2[0]','uncertainty':'high','predicted_delta_mse':-.2,'patch':[],'explanation':'A tentative numerical diagnosis.'}
        self.assertEqual(validate_commit(correct),correct)
        for wrong in [{**correct,'fault_region':'W2[99]'},
                      {**correct,'predicted_delta_mse':float('nan')},
                      {**correct,'fault_region':'not-a-tensor'}]:
            with self.assertRaises(ValueError):validate_commit(wrong)
    def test_human_gate_is_closed(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'human_fields.json'
            path.write_text(json.dumps({
                'human_predicted_failure':'[HUMAN TO FILL]',
                'human_predicted_contrast':'[HUMAN TO FILL]',
                'human_false_positive_test':'[HUMAN TO FILL]',
                'human_unsupported_mechanism':'[HUMAN TO FILL]',
                'assistance_disclosure':'D'}))
            with self.assertRaises(ValueError):human_fields(path)

if __name__ == '__main__':unittest.main(verbosity=2)
