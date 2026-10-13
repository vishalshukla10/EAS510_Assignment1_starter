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
                best_template, best_location = template, location

    out["metric"] = round(best, 3)
    edge_metric = 0.0
    if out["metric"] >= 0.8 and best_template is not None:
        x, y = best_location
        th, tw = best_template.shape
        patch_edges = cv2.Canny(src[y:y + th, x:x + tw], 50, 150)
        template_edges = cv2.Canny(best_template, 50, 150)
        # Empty or nearly empty edge maps are not positive matching evidence.
        if min(cv2.countNonZero(patch_edges), cv2.countNonZero(template_edges)) >= 20:
            # Allow small edge displacements caused by resizing and JPEG noise.
            patch_edges = cv2.GaussianBlur(patch_edges, (5, 5), 0)
            template_edges = cv2.GaussianBlur(template_edges, (5, 5), 0)
            edge_response = cv2.matchTemplate(
                patch_edges, template_edges, cv2.TM_CCOEFF_NORMED
            )
            value = float(edge_response[0, 0])
            if np.isfinite(value):
                edge_metric = round(max(0.0, min(1.0, value)), 3)

    out["note"] = (
        f"Multiscale correlation {out['metric']:.2f}; "
        f"edge correlation {edge_metric:.2f}; scale {best_scale:.2f}"
    )
    if out["metric"] >= 0.8 and edge_metric >= 0.3:
        out["fired"] = True
        out["score"] = int(round(out["out_of"] * out["metric"]))
    return out


RULES = [
    "rule1_metadata_v2",
    "rule2_histogram_v2",
    "rule3_template_v2",
    "rule4_edges",
]
