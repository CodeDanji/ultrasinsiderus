import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from review import assess, AXES

class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.r={'criteria_approved':True,'target_images':['a','b','c'], 'reject_images':['d','e','f'], 'disqualifying_errors':[], 'reviewers':[{'reviewer_id':'a','scores':dict.fromkeys(AXES,4)}, {'reviewer_id':'b','scores':dict.fromkeys(AXES,4)}]}
    def test_pass_and_disqualify(self):
        self.assertEqual(assess(self.r)['status'],'image_review_pass')
        self.r['disqualifying_errors']=['missing muscle']
        self.assertEqual(assess(self.r)['status'],'fail')
    def test_unapproved_cannot_pass(self):
        self.r['criteria_approved']=False
        with self.assertRaises(ValueError): assess(self.r)
    def test_low_score_fails(self):
        self.r['reviewers'][0]['scores']['internal_detail']=2
        result=assess(self.r)
        self.assertEqual(result['status'],'fail')
        self.assertEqual(result['review_disagreement_axes'],['internal_detail'])
    def test_unique_reviewers_and_score_type(self):
        self.r['reviewers'][1]['reviewer_id']='a'
        with self.assertRaises(ValueError): assess(self.r)
        self.r['reviewers'][1]['reviewer_id']='b'
        self.r['reviewers'][0]['scores']['internal_detail']=True
        with self.assertRaises(ValueError): assess(self.r)
if __name__=='__main__': unittest.main()
