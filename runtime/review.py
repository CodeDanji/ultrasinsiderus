#!/usr/bin/env python3
"""Evaluate documented PRD image review without declaring technical or clinical success."""
import argparse
import json
import sys
from pathlib import Path

AXES = ('outer_alignment', 'internal_detail', 'view_consistency', 'brand_quality')

def assess(review):
    if review.get('criteria_approved') is not True:
        raise ValueError('G0 reference set must be approved before scoring')
    for key in ('target_images', 'reject_images'):
        values = review.get(key)
        if not isinstance(values, list) or len(values) != 3 or any(not isinstance(v, str) or not v.strip() for v in values):
            raise ValueError(f'{key} requires three references')
    reviewers = review.get('reviewers')
    if not isinstance(reviewers, list) or len(reviewers) != 2:
        raise ValueError('exactly two reviewers are required')
    ids = [r.get('reviewer_id') for r in reviewers]
    if any(not isinstance(i, str) or not i.strip() for i in ids) or len(set(ids)) != 2:
        raise ValueError('reviewers must have distinct IDs')
    if not isinstance(review.get('disqualifying_errors'), list) or any(not isinstance(v, str) or not v.strip() for v in review['disqualifying_errors']):
        raise ValueError('disqualifying_errors must be a list of descriptions')
    averages, concerns = {}, []
    for axis in AXES:
        values = [r.get('scores', {}).get(axis) for r in reviewers]
        if any(type(v) is not int or not 1 <= v <= 5 for v in values):
            raise ValueError(f'{axis} requires two integer scores from 1 to 5')
        averages[axis] = sum(values)/2
        if min(values) <= 2:
            concerns.append(axis)
    failed = bool(review['disqualifying_errors']) or any(v < 4 for v in averages.values())
    return {'status': 'fail' if failed else ('review_disagreement' if concerns else 'image_review_pass'),
            'averages': averages, 'review_disagreement_axes': concerns,
            'disqualifying_errors': review['disqualifying_errors'],
            'interpretation': 'Image review only. Not proof of personal anatomy, automated operation, clinical performance, or market demand.'}

def main():
    p=argparse.ArgumentParser(); p.add_argument('review',type=Path); p.add_argument('--output',type=Path,required=True); a=p.parse_args()
    try:
        result=assess(json.loads(a.review.read_text(encoding='utf-8')))
        with a.output.open('x',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2); f.write('\n')
    except (ValueError, OSError, TypeError, AttributeError) as e:
        print(f'Review failed: {e}',file=sys.stderr); return 1
    print(result['status']); return 0
if __name__=='__main__': sys.exit(main())
