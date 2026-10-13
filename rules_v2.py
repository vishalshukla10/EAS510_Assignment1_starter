
import cv2
import numpy as np
import rules


def _reweight(rule_function, target, input_path, maximum):
    evidence = dict(rule_function(target, input_path))
    old_maximum = evidence["out_of"]
    evidence["score"] = int(round(evidence["score"] * maximum / old_maximum))
    evidence["out_of"] = maximum
    return evidence


def rule1_metadata_v2(target, input_path):
    return _reweight(rules.rule1_metadata, target, input_path, 15)


def rule2_histogram_v2(target, input_path):
    return _reweight(rules.rule2_histogram, target, input_path, 30)


def rule3_template_v2(target, input_path):
    return _reweight(rules.rule3_template, target, input_path, 25)


def rule4_edges(target, input_path):
    
    out = {
        "rule": 4, "name": "Edges", "fired": False, "score": 0,
        "out_of": 30, "note": "Multiscale correlation 0.00; edge correlation 0.00",
        "metric": 0.0,
    }
    src = rules._gray(target["path"])
    suspect = rules._gray(input_path)
    if src is None or suspect is None:
        return out

    best, best_scale = 0.0, 0.0
    best_template, best_location = None, None
    h, w = suspect.shape

    # Test 20%-100% of the cached suspect size, preserving its aspect ratio.
    for percent in range(20, 101, 2):
        scale = percent / 100.0
        tw, th = int(round(w * scale)), int(round(h * scale))
        if min(tw, th) < 16 or tw > src.shape[1] or th > src.shape[0]:
            continue
        template = cv2.resize(suspect, (tw, th), interpolation=cv2.INTER_AREA)
        if float(template.std()) < 1.0:
            continue
        response = cv2.matchTemplate(src, template, cv2.TM_CCOEFF_NORMED)
        _, metric, _, location = cv2.minMaxLoc(response)
        if np.isfinite(metric) and metric > best:
            best, best_scale = min(1.0, metric), scale
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
