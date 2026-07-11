from __future__ import annotations

import argparse

from fund_ranking_system.akshare_data import fetch_fund_metadata, fetch_many_funds
from fund_ranking_system.storage import FundDatabase


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update cached fund NAV data in SQLite.")
    parser.add_argument("--codes", nargs="*", help="Fund codes to update. Defaults to cached funds.")
    parser.add_argument("--start-date", default="2021-01-01")
    parser.add_argument("--sleep", type=float, default=0.2)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    db = FundDatabase()
    codes = [code.zfill(6) for code in args.codes] if args.codes else db.fund_codes()
    if not codes:
        raise SystemExit("No cached funds found. Pass --codes to seed the database first.")

    metadata = fetch_fund_metadata(codes)
    nav = fetch_many_funds(codes, args.start_date, args.sleep)
    db.save_metadata(metadata)
    db.save_nav(nav)
    print(f"Updated {len(codes)} funds and {len(nav)} NAV rows in {db.path}")

if __name__ == "__main__":
    main()
