import unittest
from ex0005cc_calibration import (
    STRATA,PILOT_N,MIXTURES,EXCLUDED_TEMPLATE,build_synthetic,
    construct_apple,select_distribution,validate_selection,sh,synthetic_one)

class CalibrationTests(unittest.TestCase):
    def test_synthetic_oracle_and_determinism(self):
        p=build_synthetic('pilot',8)
        v=build_synthetic('validation',12)
        self.assertEqual(len(p),8)
        self.assertEqual(len(v),12)
        self.assertEqual(p,build_synthetic('pilot',8))
        self.assertFalse(set(r['id'] for r in p)&set(r['id'] for r in v))
        self.assertTrue(all(r['truth'].lstrip('-').isdigit() for r in p+v))
        self.assertTrue(all(r['oracle']=='two_formula_python' for r in p+v))
        for fam in ('inventory','tickets','rates','equations'):
            for i in range(50):
                r=synthetic_one(fam,i,'test')
                self.assertGreaterEqual(int(r['truth']),0)
    def test_apple_pilot_and_validation_disjoint(self):
        sample={}
        for s in ('main','p1','p2'):
            sample[s]=[{'id':i,'instance':j,'original_id':i+200,
                        'question':f'{s}: number {i}:{j}',
                        'original_question':f'Question {i}',
                        'answer':f'Solution.\n#### {i+3*j+5}'}
                       for i in range(100) for j in range(3)]
        pilot,val=construct_apple(sample)
        self.assertEqual([len(pilot[s]) for s in STRATA],[8,8,8,8])
        self.assertEqual([len(val[s]) for s in STRATA],[4,8,12,12])
        total=[r for s in STRATA if s!='synthetic' for r in pilot[s]+val[s]]
        self.assertEqual(len(set(r['family'] for r in total)),48)
        self.assertTrue(all(r['template_id'] not in EXCLUDED_TEMPLATE for r in total))
        self.assertEqual(pilot,construct_apple(sample)[0])
    def score_rows(self,cc):
        return [{'id':f'{s}:{i}','stratum':s,
                 'score':{'correct':i<cc[s], 'completed':True}}
                for s in STRATA for i in range(8)]
    def test_chooses_by_stratum_not_individual_rows(self):
        cc={'main':8,'p1':6,'p2':4,'synthetic':2}
        d=select_distribution(self.score_rows(cc))
        self.assertEqual(d['disposition'],'PROVISIONAL_DISTRIBUTION_SELECTED')
        self.assertGreaterEqual(d['choice']['predicted_accuracy'],0.30)
        self.assertLessEqual(d['choice']['predicted_accuracy'],0.75)
        self.assertEqual(sum(d['choice']['weights'].values()),24)
    def test_no_rescue_for_ceiling(self):
        d=select_distribution(self.score_rows({s:8 for s in STRATA}))
        self.assertEqual(d['disposition'],'NO_QUALIFIED_DISTRIBUTION')
        self.assertIsNone(d['choice'])
    def test_no_rescue_for_floor(self):
        d=select_distribution(self.score_rows({s:0 for s in STRATA}))
        self.assertEqual(d['disposition'],'NO_QUALIFIED_DISTRIBUTION')
    def test_invalid_status(self):
        rows=self.score_rows({s:3 for s in STRATA})
        rows[0]['score']['completed']=False
        with self.assertRaises(ValueError):select_distribution(rows)
    def test_validation_selection(self):
        sample={s:[{'id':i,'instance':j,'original_id':i+200,'question':str(i),
                    'original_question':str(i),'answer':f'#### {i+j}'}
                  for i in range(100) for j in range(3)] for s in ('main','p1','p2')}
        _,val=construct_apple(sample)
        c=select_distribution(self.score_rows({'main':8,'p1':6,'p2':4,'synthetic':2}))['choice']
        manifest,rows=validate_selection(c,val)
        self.assertEqual(len(rows),24)
        self.assertEqual(len(set(r['id'] for r in rows)),24)
        self.assertEqual(manifest['validation_content_hash'],sh(rows))

if __name__=='__main__':unittest.main()
