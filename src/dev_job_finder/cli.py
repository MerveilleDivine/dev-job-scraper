"""Command-line interface for Remote Dev Job Finder."""

import argparse
import sys

from dev_job_finder.client import JSearchClient, VALID_DATE_FILTERS
from dev_job_finder.exceptions import JobFinderError
from dev_job_finder.exporter import export_jobs_to_csv


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""

    parser = argparse.ArgumentParser(description="Search remote developer jobs and export results.")
    parser.add_argument("keyword", type=str, help="Job search keyword(s), e.g. 'remote python'.")
    parser.add_argument("--pages", type=int, default=1, help="Number of result pages to fetch.")
    parser.add_argument(
        "--country",
        type=str,
        default="",
        help="Optional 2-letter country code, e.g. us, gb, ca, ae. Leave blank worldwide.",
    )
    parser.add_argument(
        "--date-posted",
        choices=sorted(VALID_DATE_FILTERS),
        default="all",
        help="Filter jobs by posting date.",
    )
    parser.add_argument("--output", type=str, default=None, help="Optional output CSV path.")
    return parser


def run(args: argparse.Namespace) -> int:
    """Execute the search workflow."""

    client = JSearchClient()
    jobs = client.search(
        query=args.keyword,
        pages=args.pages,
        country=args.country,
        date_posted=args.date_posted,
    )

    if not jobs:
        print("No jobs found. Try another keyword, country, or date filter.")
        return 0

    output_path = export_jobs_to_csv(jobs, filename=args.output, query=args.keyword)
    print(f"Saved {len(jobs)} job(s) to {output_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        return run(args)
    except JobFinderError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
