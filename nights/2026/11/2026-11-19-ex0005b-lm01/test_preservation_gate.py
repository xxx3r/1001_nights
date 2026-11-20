import math, unittest
import preservation_gate as g

class OfflineCheckerTests(unittest.TestCase):
    def test_snapshot(self):
        self.assertEqual(g.digest(g.SETS), g.digest(g.SETS))
        self.assertEqual(len(g.SETS),4)
        self.assertEqual({len(v) for v in g.SETS.values()}, {6})
    def test_negative_recovery_retained(self):
        self.assertLess(g.recovery_fraction(3,4,1),0)
    def test_zero_gap_not_scored(self):
        self.assertIsNone(g.recovery_fraction(1.001, 1, 1))
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError):g.recovery_fraction(math.inf,2,1)
    def test_finite_bound(self):
        for v in [math.inf,math.nan,7,True,'1']:
            with self.assertRaises(ValueError):g.validate_gain(v)
    def test_valid_gain(self):
        self.assertEqual(g.validate_gain(0.5),0.5)
    def test_valid_abstention(self):
        self.assertIsNone(g.validate_commit({'gain':None,'confidence':'low','explanation':'Missing reliable evidence', 'predicted_target_improvement':0})['gain'])
    def test_schema_extra_key(self):
        with self.assertRaises(ValueError):g.validate_commit({'gain':1,'confidence':'high','explanation':'This is supported', 'predicted_target_improvement':0,'oracle':True})
    def test_schema_bad_gain(self):
        with self.assertRaises(ValueError):g.validate_commit({'gain':9,'confidence':'high','explanation':'This is supported', 'predicted_target_improvement':0})
    def test_patch_repair_preserve_pass(self):
        out=g.score_result(2,3,2.05,1,1.01,1,2.9)
        self.assertEqual(out['G3_repair'],'PASS')
        self.assertEqual(out['G4_preservation'],'PASS')
        self.assertEqual(out['G5_simple_baselines'],'PASS')
    def test_target_improves_preserve_fails(self):
        out=g.score_result(2,3,2.1,1,1.1,0.80,2.9)
        self.assertEqual(out['G3_repair'],'PASS')
        self.assertEqual(out['G4_preservation'],'FAIL')
    def test_baseline_margin_not_silent(self):
        out=g.score_result(2,3,2.1,1,1,1,2.105)
        self.assertEqual(out['G5_simple_baselines'],'FAIL')
    def test_evidence_requires_two_distinct_probes(self):
        p=[{'tool':'probe_gain','args':{'gain':2},'observed':{'target_dev_loss':1.2,'preserve_dev_loss':0.9}}]
        self.assertEqual(g.assess_evidence(2,p),'FAIL')
        self.assertEqual(g.assess_evidence(None,p),'ABSTAIN')
    def test_evidence_requires_improvement_and_preservation(self):
        base={'tool':'probe_gain','args':{'gain':1},'observed':{'target_dev_loss':2,'preserve_dev_loss':1}}
        good={'tool':'probe_gain','args':{'gain':2},'observed':{'target_dev_loss':1.5,'preserve_dev_loss':1.01}}
        bad={'tool':'probe_gain','args':{'gain':2},'observed':{'target_dev_loss':1.5,'preserve_dev_loss':1.4}}
        self.assertEqual(g.assess_evidence(2,[base,good]),'PASS')
        self.assertEqual(g.assess_evidence(2,[base,bad]),'FAIL')
    def test_manifest_tamper(self):
        m={'G0':'PASS','code_sha256':g.sha_file(g.__file__),'sets_sha256':g.digest(g.SETS),'model_id':g.MODEL_ID}
        m['freeze_sha256']=g.freeze_fingerprint(m)
        self.assertTrue(g.verify_manifest(m))
        m['model_id']='wrong'
        with self.assertRaises(RuntimeError):g.verify_manifest(m)

if __name__=='__main__':unittest.main()
