import unittest

import pandas as pd

from fund_ranking_system.scoring import DEFAULT_PROFILES, score_funds


class ScoringTest(unittest.TestCase):
    def test_score_funds_ranks_all_funds(self):
        metrics = pd.DataFrame(
            {
                "annual_return": [0.12, 0.08, 0.15],
                "annual_volatility": [0.18, 0.09, 0.35],
                "max_drawdown": [-0.18, -0.08, -0.40],
                "sharpe": [0.56, 0.67, 0.37],
                "calmar": [0.67, 1.00, 0.38],
                "rolling_positive_ratio": [0.61, 0.72, 0.55],
            },
            index=["Fund_A", "Fund_B", "Fund_C"],
        )

        scored = score_funds(metrics, DEFAULT_PROFILES["balanced"])

        self.assertIn("composite_score", scored.columns)
        self.assertIn("rank", scored.columns)
        self.assertEqual(set(scored.index), {"Fund_A", "Fund_B", "Fund_C"})


if __name__ == "__main__":
    unittest.main()

