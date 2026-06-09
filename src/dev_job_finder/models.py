"""Data models used by the job finder."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Job:
    """Normalized job listing returned by the app."""

    title: str
    company: str
    location: str
    country: str
    link: str
    date_posted: str
    source: str = "JSearch"
    job_id: str = ""
    employment_type: str = ""

    @classmethod
    def from_api_payload(cls, payload: dict) -> "Job":
        """Create a Job from a JSearch API payload."""

        city = payload.get("job_city") or ""
        state = payload.get("job_state") or ""
        country = payload.get("job_country") or ""
        location_parts = [part for part in (city, state, country) if part]

        return cls(
            title=payload.get("job_title") or "",
            company=payload.get("employer_name") or "",
            location=", ".join(location_parts) or payload.get("job_location") or "Remote/Not specified",
            country=country,
            link=payload.get("job_apply_link") or payload.get("job_google_link") or "",
            date_posted=payload.get("job_posted_at_datetime_utc") or "",
            source="JSearch",
            job_id=payload.get("job_id") or "",
            employment_type=payload.get("job_employment_type") or "",
        )

    def to_row(self) -> dict:
        """Return a CSV and dataframe-friendly representation."""

        return {
            "Job Title": self.title,
            "Company": self.company,
            "Location": self.location,
            "Country": self.country,
            "Link": self.link,
            "Date Posted": self.date_posted,
            "Source": self.source,
        }
