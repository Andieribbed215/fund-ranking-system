import unittest

import pandas as pd

from fund_ranking_system.sensitivity import build_sensitivity_table


class SensitivityTest(unittest.TestCase):
    def test_build_sensitivity_table_adds_rank_spread(self):
        all_profiles = pd.DataFrame(
            {
                "aggressive_score": [90.0, 70.0, 80.0],
                "aggressive_rank": [1, 3, 2],
                "balanced_score": [82.0, 88.0, 75.0],
                "balanced_rank": [2, 1, 3],
                "conservative_score": [78.0, 85.0, 72.0],
                "conservative_rank": [2, 1, 3],
            },
            index=["Fund_A", "Fund_B", "Fund_C"],
        )

        sensitivity = build_sensitivity_table(all_profiles)

        self.assertIn("rank_spread", sensitivity.columns)
        self.assertEqual(sensitivity.loc["Fund_A", "rank_spread"], 1)
        self.assertEqual(sensitivity.loc["Fund_B", "best_rank"], 1)


if __name__ == "__main__":
    unittest.main()
