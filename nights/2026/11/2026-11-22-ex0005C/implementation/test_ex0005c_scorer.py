import unittest
from ex0005c_scorer import score_math, score_text, reference, decomposition, numeric

class ScorerTests(unittest.TestCase):
    def test_gold(self):
        self.assertEqual(str(reference('Work\n#### 1,250.5')), '1250.5')
        with self.assertRaises(ValueError): reference('no marked answer')
    def test_thinking_valid(self):
        r=score_math('<think>working</think>\nFinal answer: 1,200\n', '1200', finished=True)
        self.assertTrue(r.completed and r.correct)
    def test_fake_or_missing_think_and_answer_line(self):
        for response in ('</think>\nFinal answer: 4', '<think>stuff</think>\nFinal answer:\n4'):
            r=score_math(response,'4',finished=True)
            self.assertFalse(r.completed)
    def test_wrong_is_complete(self):
        r=score_math('<think>x</think>\nFinal answer: 3', '2', finished=True)
        self.assertTrue(r.completed); self.assertFalse(r.correct)
    def test_thinking_not_closed(self):
        r=score_math('<think>working forever', '4', finished=True)
        self.assertFalse(r.completed); self.assertFalse(r.correct)
    def test_length_cutoff(self):
        r=score_math('<think>x</think>\nFinal answer: 4', '4', finished=False)
        self.assertFalse(r.completed); self.assertFalse(r.correct)
    def test_no_multiple_answers(self):
        r=score_math('<think>x</think>\nFinal answer: 4\nFinal answer: 5', '5', finished=True)
        self.assertFalse(r.completed)
    def test_strict_numeric(self):
        for bad in ('12 dollars','2+2','1/2','1,23','NaN','4.0.0'):
            with self.assertRaises(ValueError): numeric(bad)
    def test_text(self):
        r=score_text('<think>x</think>\nFinal answer: Paris', 'paris', finished=True)
        self.assertTrue(r.completed and r.correct)
    def test_decompose(self):
        B=[(1,0),(1,0),(1,1),(0,0),(0,0),(1,1)]
        E=[(1,1),(1,1),(1,0),(1,1),(1,1),(0,0)]
        d=decomposition([dict(completed=bool(c),correct=bool(a)) for c,a in B],
                        [dict(completed=bool(c),correct=bool(a)) for c,a in E])
        self.assertEqual((d['net_total'],d['both_complete'],d['completion_changed']), (2,1,1))
        self.assertEqual((d['wrong_to_right'],d['right_to_wrong']), (4,2))
    def test_invalid_pair(self):
        with self.assertRaises(ValueError): decomposition([{'correct':True,'completed':False}], [{'correct':False,'completed':False}])
if __name__ == '__main__': unittest.main()
