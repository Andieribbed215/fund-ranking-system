import unittest

import pandas as pd

from fund_ranking_system.metadata import attach_fund_metadata, display_fund


class MetadataTest(unittest.TestCase):
    def test_attach_fund_metadata_adds_name_column(self):
        metrics = pd.DataFrame({"annual_return": [0.1]}, index=["000001"])
        metadata = pd.DataFrame({"fund_name": ["华夏成长混合"]}, index=["000001"])

        enriched = attach_fund_metadata(metrics, metadata)

        self.assertEqual(enriched.loc["000001", "fund_name"], "华夏成长混合")
        self.assertEqual(display_fund("000001", enriched.loc["000001"]), "000001 华夏成长混合")


if __name__ == "__main__":
    unittest.main()
