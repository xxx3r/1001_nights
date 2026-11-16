"""EX0005Aa POST-RUN audit, NOT a prospective Luna observation.

Demonstrates that the four diagnostics actually returned to the investigator
are consistent with different healthy parameterizations requiring different
single-scalar repairs. Does not contact an API or alter the frozen run.
"""
from __future__ import annotations
import copy
import json
import sys
from pathlib import Path

import numpy as np

here = Path(__file__).resolve().parent
# When archived under ex0005aa/analysis, public source is in ../source.
source = here.parent / 'source'
if not source.exists():
    source = here
sys.path.insert(0, str(source))
from ex0005aa_public import make_case, predict_np, score_edits, PROBE_PACKS


def main():
    original = make_case('D_unknown')
    alternative = copy.deepcopy(original)

    # Alternative one-lesion history, changing UNINSPECTED output weight and
    # corresponding healthy first-layer coefficient, not the observed W1/b1.
    alternative.w['W2'][0] = 2.0
    alternative.healthy['W2'][0] = 2.0
    alternative.healthy['W1'][0, 0] = 0.5
    alternative.y_eval = predict_np(alternative.healthy, alternative.x_eval)

    for tensor in ('W1', 'b1'):
        assert np.array_equal(original.w[tensor], alternative.w[tensor])

    pairs = {}
    for pack in ('feature0', 'feature1'):
        x = np.asarray(PROBE_PACKS[pack], dtype=float)
        same_pred = bool(np.allclose(predict_np(original.w, x), predict_np(alternative.w, x)))
        same_targets = bool(np.allclose(predict_np(original.healthy, x), predict_np(alternative.healthy, x)))
        assert same_pred and same_targets, (pack, same_pred, same_targets)
        pairs[pack] = {'same_observed_predictions': same_pred, 'same_observed_targets': same_targets}

    luna_patch = [{'tensor': 'W1', 'index': 0, 'delta': 1.3}]
    alt_patch = [{'tensor': 'W1', 'index': 0, 'delta': 0.8}]
    a = score_edits(original, luna_patch)
    b = score_edits(alternative, luna_patch)
    c = score_edits(alternative, alt_patch)
    assert abs(a['after_mse']) < 1e-12
    assert abs(c['after_mse']) < 1e-12
    assert abs(b['after_mse'] - b['before_mse']) < 1e-12

    output = {
        'classification': 'POST_RUN_COUNTEREXAMPLE_NOT_MODEL_TRIAL',
        'experiment': 'EX0005Aa',
        'original_freeze_sha256': '2644e664eb2ca90483ff461bb8a069ef91e2b6fe65592adcf82969f92045c044',
        'uninspected_output_weight': {'original': 1.0, 'alternative': 2.0},
        'observed_W1_and_b1_equal': True,
        'probe_equivalence': pairs,
        'original_luna_patch': a,
        'alternative_luna_patch': b,
        'alternative_exact_patch': c,
        'interpretation': 'The recorded W1, b1, feature0 and feature1 observations do not uniquely determine the exact W1[0] repair. G4 on the actual patient remains PASS.'
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
