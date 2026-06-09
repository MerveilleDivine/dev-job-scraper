import csv

from dev_job_finder.exporter import export_jobs_to_csv, slugify
from dev_job_finder.models import Job


def test_slugify_creates_safe_file_fragment():
    assert slugify("Remote Python Developer!") == "remote_python_developer"
    assert slugify("   ") == "jobs"


def test_export_jobs_to_csv_writes_expected_columns(tmp_path):
    jobs = [
        Job(
            title="Backend Engineer",
            company="Acme Corp",
            location="London, GB",
            country="GB",
            link="https://example.com/apply",
            date_posted="2026-06-09T08:30:00Z",
        )
    ]
    output_path = tmp_path / "jobs.csv"

    returned_path = export_jobs_to_csv(jobs, filename=output_path)

    assert returned_path == output_path
    with output_path.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    assert rows == [
        {
            "Job Title": "Backend Engineer",
            "Company": "Acme Corp",
            "Location": "London, GB",
            "Country": "GB",
            "Link": "https://example.com/apply",
            "Date Posted": "2026-06-09T08:30:00Z",
            "Source": "JSearch",
        }
    ]
