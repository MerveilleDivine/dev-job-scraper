from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from app import create_download, search_jobs  # noqa: E402
from scraper import JSearchError  # noqa: E402


class AppTests(unittest.TestCase):
    @patch("app.fetch_jobs_api")
    def test_search_returns_status_and_dataframe(self, fetch_jobs_api):
        fetch_jobs_api.return_value = [
            {
                "Job Title": "Engineer",
                "Company": "Example",
                "Location": "Remote",
                "Remote": "Yes",
                "Employment Type": "FULLTIME",
                "Link": "https://example.com/job",
                "Date Posted": "2026-07-16T00:00:00Z",
            }
        ]

        message, dataframe = search_jobs("engineer", 2, "us", True)

        self.assertEqual(message, "Found 1 unique job listings.")
        self.assertIsInstance(dataframe, pd.DataFrame)
        fetch_jobs_api.assert_called_once_with(
            "engineer",
            num_pages=2,
            country="us",
            remote_only=True,
        )

    @patch("app.fetch_jobs_api", side_effect=JSearchError("rate limit reached"))
    def test_search_surfaces_safe_client_errors(self, _fetch_jobs_api):
        message, dataframe = search_jobs("engineer", 1, "", False)

        self.assertEqual(message, "Error: rate limit reached")
        self.assertIsNone(dataframe)

    def test_downloads_use_isolated_files(self):
        dataframe = pd.DataFrame(
            [
                {
                    "Job Title": "Engineer",
                    "Company": "Example",
                    "Location": "Remote",
                    "Remote": "Yes",
                    "Employment Type": "FULLTIME",
                    "Link": "https://example.com/job",
                    "Date Posted": "2026-07-16T00:00:00Z",
                }
            ]
        )

        first = create_download(dataframe)
        second = create_download(dataframe)

        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        self.assertNotEqual(first, second)
        self.assertTrue(Path(first).is_file())
        self.assertTrue(Path(second).is_file())


if __name__ == "__main__":
    unittest.main()
