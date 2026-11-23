"""EX0005C v0.3 preflight scorer. Offline and side-effect free.

Do not count truncated, malformed, or unparseable responses as correct.
The evaluator records 'finished' and 'completed' separately.
"""
from dataclasses import dataclass, asdict
from decimal import Decimal, InvalidOperation
import re
from collections import Counter
import random

FINAL = re.compile(r"(?m)^Final answer:[ \t]*([^\r\n]*?)[ \t]*$")
NUM = re.compile(r"[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?")


def numeric(value):
    """Accept only signed numeric scalars with optional correctly placed commas."""
    value = value.strip()
    if not NUM.fullmatch(value):
        raise ValueError(f"invalid numeric answer: {value!r}")
    try:
        d = Decimal(value.replace(',', ''))
    except InvalidOperation as exc:
        raise ValueError('invalid decimal') from exc
    if not d.is_finite():
        raise ValueError('nonfinite decimal')
    return d


def reference(answer):
    """Extract GSM8K's authoritative #### final numeric answer."""
    hits = re.findall(r"(?m)^####\s*([^\r\n]+)\s*$", answer)
    if len(hits) != 1:
        raise ValueError('expected exactly one #### reference answer')
    return numeric(hits[0])


@dataclass
class Score:
    finished: bool
    completed: bool
    correct: bool
    parsed: str | None
    status: str

    def json(self):
        return asdict(self)


def score_math(output, truth, *, finished, require_think=True):
    """output must be raw generation text (excluding prompt); finished is EOS stop, not length cutoff.

    Only the text after the closed thinking tag counts as a final answer. No extra
    prose may follow Final answer: ... . The model need not show correct reasoning.
    """
    if not finished:
        return Score(False, False, False, None, 'truncated_or_unterminated')
    if require_think:
        if output.count('</think>') != 1 or output.count('<think>') != 1 or output.index('<think>') > output.index('</think>'):
            return Score(True, False, False, None, 'unclosed_or_multiple_thinking_blocks')
        answer_part = output.split('</think>', 1)[1]
    else:
        answer_part = output
    answer_part = answer_part.replace('<|im_end|>', '').strip()
    matches = list(FINAL.finditer(answer_part))
    if len(matches) != 1:
        return Score(True, False, False, None, 'missing_or_multiple_final_answers')
    match = matches[0]
    if answer_part[match.end():].strip():
        return Score(True, False, False, None, 'trailing_text_after_final')
    try:
        got = numeric(match.group(1))
        gold = numeric(str(truth))
    except ValueError:
        return Score(True, False, False, None, 'invalid_number')
    return Score(True, True, got == gold, str(got), 'valid_complete')


def score_text(output, truth, *, finished, require_think=True):
    if not finished:
        return Score(False, False, False, None, 'truncated_or_unterminated')
    if require_think:
        if output.count('</think>') != 1 or output.count('<think>') != 1 or output.index('<think>') > output.index('</think>'):
            return Score(True, False, False, None, 'unclosed_or_multiple_thinking_blocks')
        answer_part = output.split('</think>', 1)[1]
    else:
        answer_part = output
    answer_part = answer_part.replace('<|im_end|>', '').strip()
    matches = list(FINAL.finditer(answer_part))
    if len(matches) != 1 or answer_part[matches[0].end():].strip():
        return Score(True, False, False, None, 'missing_or_extra_final_text')
    value = ' '.join(matches[0].group(1).lower().split())
    if not value or len(value) > 80:
        return Score(True, False, False, None, 'invalid_final_text')
    expected = ' '.join(str(truth).lower().split())
    return Score(True, True, value == expected, value, 'valid_complete')


def decomposition(baseline, edited):
    """Paired units: each row has {'completed':bool,'correct':bool}; same item order."""
    if len(baseline) != len(edited) or not baseline:
        raise ValueError('nonempty equal-length paired data required')
    both, changed, r2w, w2r = 0, 0, 0, 0
    for b, e in zip(baseline, edited):
        if b['correct'] and not b['completed'] or e['correct'] and not e['completed']:
            raise ValueError('correct answers cannot be incomplete')
        diff = int(e['correct']) - int(b['correct'])
        if b['completed'] == e['completed']:
            both += diff
        else:
            changed += diff
        w2r += diff == 1
        r2w += diff == -1
    return dict(n=len(baseline), net_total=both+changed, both_complete=both,
                completion_changed=changed, wrong_to_right=w2r, right_to_wrong=r2w,
                baseline_correct=sum(x['correct'] for x in baseline),
                edited_correct=sum(x['correct'] for x in edited))


def paired_bootstrap_ci(baseline, edited, seed=20261122, reps=10000):
    """Exploratory percentile CI on fixed 48-item paired accuracy difference."""
    if len(baseline) != len(edited) or not baseline:
        raise ValueError('invalid pairing')
    diffs = [int(e['correct']) - int(b['correct']) for b, e in zip(baseline, edited)]
    rng = random.Random(seed)
    n = len(diffs)
    values = sorted(sum(rng.choice(diffs) for _ in range(n))/n for _ in range(reps))
    return (values[int(0.025*reps)], values[min(reps-1,int(0.975*reps))])
