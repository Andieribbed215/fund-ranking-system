import unittest

import pandas as pd

from fund_ranking_system.metrics import calculate_metrics, max_drawdown


class MetricsTest(unittest.TestCase):
    def test_max_drawdown_known_series(self):
        dates = pd.bdate_range("2024-01-01", periods=4)
        nav = pd.Series([1.0, 1.2, 0.9, 1.1], index=dates)

        self.assertAlmostEqual(max_drawdown(nav), -0.25)

    def test_calculate_metrics_outputs_expected_columns(self):
        dates = pd.bdate_range("2024-01-01", periods=80)
        nav = pd.DataFrame(
            {
                "Fund_A": [1 + i * 0.001 for i in range(80)],
                "Fund_B": [1 + ((-1) ** i) * 0.001 + i * 0.0005 for i in range(80)],
            },
            index=dates,
        )

        metrics = calculate_metrics(nav, rolling_window=20)

        self.assertIn("annual_return", metrics.columns)
        self.assertIn("max_drawdown", metrics.columns)
        self.assertIn("rolling_positive_ratio", metrics.columns)
        self.assertEqual(len(metrics), 2)


if __name__ == "__main__":
    unittest.main()

