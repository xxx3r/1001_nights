import unittest
from ex0005c_prepare import build_split,preservation

class SplitTests(unittest.TestCase):
    def test_preservation(self):
        dev,held=preservation()
        self.assertEqual(len(dev),12); self.assertEqual(len(held),48)
        self.assertEqual(len(set(x['id'] for x in dev+held)),60)
    def test_family_partition(self):
        train=[dict(question=f'Train question {i}',answer=f'Solution\n#### {i}') for i in range(40)]
        test=[dict(question=f'Test question {i}',answer=f'Solution\n#### {i}') for i in range(80)]
        symbolic=[dict(id=i,instance=0,original_id=i,question=f'Variant question {i}',answer=f'Solution\n#### {i+1}', original_question=f'Test question {i}') for i in range(30)]
        dev,ordinary,shift=build_split(train,test,symbolic)
        self.assertEqual((len(dev),len(ordinary),len(shift)),(24,24,24))
        self.assertTrue(set(s['original_gsm_test_id'] for s in shift).isdisjoint(int(o['id'].split(':')[1]) for o in ordinary))
        symbolic[0]['original_question']='NOT the corresponding question'
        with self.assertRaises(ValueError): build_split(train,test,symbolic)
if __name__ == '__main__':unittest.main()
