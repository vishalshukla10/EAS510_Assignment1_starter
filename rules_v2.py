"""EAS 510 - Project 1 - Phase 2: the V2 rule set.

Rules 1-3 are kept exactly as in `rules.py`. Your job is to ADD Rule 4 that
targets the systematic weakness you diagnosed from results_v1_hard.txt.

Constraint: the rules' `out_of` weights must still sum to 100 so the Final
Score stays on a /100 scale (the format validator enforces "Final Score:
<s>/100" equals the sum of the block's rule scores).

Example split that keeps the original spirit: Rules 1-3 -> 25/25/40 and
Rule 4 -> 10 (or trim the losers more aggressively).
"""

import rules

#: Import the original rules and append your new one.
RULES = rules.RULES + ("rule4_edges",)

def _reweight(rule_function, target, input_path, maximum):
    # Copy the result so the original rule output is not modified
    evidence = dict(rule_function(target, input_path))

    old_maximum = evidence["out_of"]
    evidence["score"]= int(
	round(evidence["score"] * maximum / old_maximum )
    )
    evidence["out_of"]= maximum
    return evidence

def rule1_metadata_v2(target, input_path):
    return _reweight(
	rules.rule1_metadata, target, input_path, 25
    )

def rule2_histogram_v2(target, input_path):
    return _reweight(
        rules.rule2_histogram, target, input_path, 25
    )

def rule3_template_v2(target, input_path):
    return _reweight(
        rules.rule3_template, target, input_path, 40
    )

def rule4_edges(target, input_path):
    """TODO: replace with your Phase 2 rule that fixes the V1 weakness.

    Starter returns a no-op so the pipeline still runs before you implement it.
    Parity with rules.py rule dict: rule/name/fired/score/out_of/note/metric.
    """
    return {
        "rule": 4,
        "name": "Edges",
        "fired": False,
        "score": 0,
        "out_of": 10,
        "note": "Not implemented",
        "metric": 0.0,
    }

RULES = [
    "rule1_metadata_v2",
    "rule2_histogram_v2",
    "rule3_template_v2",
    "rule4_edges"
]
