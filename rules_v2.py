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
import cv2

#: Import the original rules and append your new one.
RULES = rules.RULES + ("rule4_edges",)


def rule4_edges(target, input_path):
    """TODO: replace with your Phase 2 rule that fixes the V1 weakness.

    Starter returns a no-op so the pipeline still runs before you implement it.
    Parity with rules.py rule dict: rule/name/fired/score/out_of/note/metric.
    """
    out = {
        "rule": 4, "name": "Mult-scale","fired": False, "score": 0,
        "out_of": 10, "note": "no valid match", "metric": 0.0,}
    
    try:
      src_g = cv2.imread(str(target["path"]), 0)
      nd_g = cv2.imread(str(input_path), 0)
        
      if src_g is None or nd_g is None:
          return out
      
      factor = min(1.0, 600 / max(*src_g.shape, *nd_g.shape))
      src_g = cv2.resize(src_g, None, fx=factor, fy= factor)
      nd_g = cv2.resize(nd_g, None, fx=factor, fy= factor)

      metric = 0.0

      for scale in [.5, .75, 1.0, 1.18, 1.5, 2.0]:
        scaled = cv2.resize(nd_g, None, fx = scale, fy=scale)

        if (scaled.shape[0] <= src_g.shape[0] and scaled.shape[1] <= src_g.shape[1]):
          res = cv2.matchTemplate(src_g, scaled, cv2.TM_CCOEFF_NORMED)
          metric = max(metric, float(res.max()))
        
      out["metric"] = round(metric, 3)
      out["note"] = f"Match schore {out['metric']:.2f}"

      if metric >= .7:
        out["fired"] = True
        out["score"] = int(round(out["out_of"] * metric))

    except Exception:
        pass
    return out
      