"""CSV export helpers."""

from collections.abc import Iterable
import csv
from datetime import datetime
from pathlib import Path
import re

from dev_job_finder.models import Job

CSV_COLUMNS = ["Job Title", "Company", "Location", "Country", "Link", "Date Posted", "Source"]


def slugify(value: str) -> str:
    """Create a filesystem-friendly slug from a search query."""

    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return slug or "jobs"


def build_csv_filename(query: str, output_dir: str | Path = "exports") -> Path:
    """Build a predictable CSV filename using the query and timestamp."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{slugify(query)}_jobs_{timestamp}.csv"
    return Path(output_dir) / filename


def export_jobs_to_csv(
    jobs: Iterable[Job],
    filename: str | Path | None = None,
    query: str = "jobs",
) -> Path:
    """Write jobs to CSV and return the generated path."""

    output_path = Path(filename) if filename else build_csv_filename(query)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open(mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(job.to_row() for job in jobs)

    return output_path
