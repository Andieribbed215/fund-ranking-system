from __future__ import annotations

import argparse
from pathlib import Path

from fund_ranking_system.akshare_data import fetch_fund_metadata, fetch_many_funds


DEFAULT_FUND_CODES = [
    "000001",
    "000003",
    "000011",
    "000021",
    "000031",
    "000051",
    "000071",
    "000083",
    "000173",
    "000209",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch open-end fund NAV data from AkShare and save a wide CSV."
    )
    parser.add_argument(
        "--codes",
        nargs="+",
        default=DEFAULT_FUND_CODES,
        help="Fund codes to fetch, for example: 000001 000003 000011.",
    )
    parser.add_argument(
        "--start-date",
        default="2021-01-01",
        help="Start date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/raw/real_fund_nav.csv"),
        help="Output CSV path.",
    )
    parser.add_argument(
        "--metadata-output",
        type=Path,
        default=Path("data/raw/fund_metadata.csv"),
        help="Output fund metadata CSV path.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.5,
        help="Seconds to wait between requests.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    codes = [code.zfill(6) for code in args.codes]
    metadata = fetch_fund_metadata(codes)
    nav = fetch_many_funds(codes, args.start_date, args.sleep)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.metadata_output.parent.mkdir(parents=True, exist_ok=True)
    nav.to_csv(args.output, index_label="Date")
    metadata.to_csv(args.metadata_output, index=False)

    print(f"Saved {len(nav)} rows and {len(nav.columns)} funds to {args.output}")
    print(f"Saved {len(metadata)} fund metadata rows to {args.metadata_output}")


if __name__ == "__main__":
    main()
