"""Backwards-compatible wrapper for the CLI and earlier helper functions.

Preferred command:
    python -m dev_job_finder.cli "remote python"
"""

from pathlib import Path

from dev_job_finder.cli import main
from dev_job_finder.client import JSearchClient
from dev_job_finder.exporter import export_jobs_to_csv


def fetch_jobs_api(query, page=1, country="", num_pages=1, date_posted="all"):
    """Compatibility helper that returns dictionaries like the first project version."""

    client = JSearchClient()
    jobs = client.search(
        query=query,
        pages=num_pages or page,
        country=country,
        date_posted=date_posted,
    )
    return [job.to_row() for job in jobs]


def save_jobs_to_csv(jobs, filename):
    """Compatibility helper for writing job dictionaries to CSV."""

    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not jobs:
        print("No jobs found. Try another keyword.")
        return None

    # Convert dictionary rows back through a tiny adapter so old imports keep working.
    from dev_job_finder.models import Job

    normalized_jobs = [
        Job(
            title=job.get("Job Title", ""),
            company=job.get("Company", ""),
            location=job.get("Location", ""),
            country=job.get("Country", ""),
            link=job.get("Link", ""),
            date_posted=job.get("Date Posted", ""),
            source=job.get("Source", "JSearch"),
        )
        for job in jobs
    ]
    export_jobs_to_csv(normalized_jobs, filename=output_path)
    print(f"Saved {len(jobs)} job(s) to {output_path}")
    return output_path


if __name__ == "__main__":
    raise SystemExit(main())
