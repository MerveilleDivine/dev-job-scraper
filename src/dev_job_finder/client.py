"""JSearch API client and search validation."""

import requests

from dev_job_finder.config import Settings, load_settings
from dev_job_finder.exceptions import ApiError, ValidationError
from dev_job_finder.models import Job

JSEARCH_URL = "https://jsearch.p.rapidapi.com/search"
MAX_RESULT_PAGES = 5
VALID_DATE_FILTERS = {"all", "today", "3days", "week", "month"}


def normalize_country(country: str | None) -> str:
    """Normalize and validate an optional ISO alpha-2 country code."""

    if not country:
        return ""

    normalized = country.strip().lower()
    if not normalized:
        return ""

    if len(normalized) != 2 or not normalized.isalpha():
        raise ValidationError("Country must be a 2-letter ISO code such as us, gb, ca, or ae.")

    return normalized


def validate_pages(pages: int) -> int:
    """Validate the number of API result pages requested."""

    try:
        value = int(pages)
    except (TypeError, ValueError) as exc:
        raise ValidationError("Pages must be a whole number.") from exc

    if value < 1:
        raise ValidationError("Pages must be at least 1.")

    if value > MAX_RESULT_PAGES:
        raise ValidationError(f"Pages cannot exceed {MAX_RESULT_PAGES} for safe API usage.")

    return value


def validate_query(query: str) -> str:
    """Validate and normalize the user's search query."""

    normalized = (query or "").strip()
    if not normalized:
        raise ValidationError("Search query cannot be empty.")

    return normalized


def validate_date_filter(date_posted: str) -> str:
    """Validate the JSearch date_posted filter."""

    normalized = (date_posted or "all").strip().lower()
    if normalized not in VALID_DATE_FILTERS:
        allowed = ", ".join(sorted(VALID_DATE_FILTERS))
        raise ValidationError(f"date_posted must be one of: {allowed}.")

    return normalized


def deduplicate_jobs(jobs: list[Job]) -> list[Job]:
    """Remove repeated jobs using stable identifiers where available."""

    unique_jobs = []
    seen = set()

    for job in jobs:
        key = job.job_id or job.link or f"{job.title}|{job.company}|{job.location}".lower()
        if key in seen:
            continue

        seen.add(key)
        unique_jobs.append(job)

    return unique_jobs


class JSearchClient:
    """Small client around the JSearch API."""

    def __init__(self, settings: Settings | None = None, session: requests.Session | None = None):
        self.settings = settings or load_settings()
        self.session = session or requests.Session()

    def search(
        self,
        query: str,
        pages: int = 1,
        country: str = "",
        date_posted: str = "all",
    ) -> list[Job]:
        """Search jobs and return normalized Job objects."""

        clean_query = validate_query(query)
        clean_pages = validate_pages(pages)
        clean_country = normalize_country(country)
        clean_date_filter = validate_date_filter(date_posted)

        headers = {
            "x-rapidapi-host": self.settings.rapidapi_host,
            "x-rapidapi-key": self.settings.rapidapi_key,
        }
        params = {
            "query": clean_query,
            "page": 1,
            "num_pages": clean_pages,
            "date_posted": clean_date_filter,
        }

        if clean_country:
            params["country"] = clean_country

        try:
            response = self.session.get(
                JSEARCH_URL,
                headers=headers,
                params=params,
                timeout=self.settings.request_timeout,
            )
        except requests.RequestException as exc:
            raise ApiError("Unable to reach the job search API. Check your connection.") from exc

        self._raise_for_status(response)

        try:
            payload = response.json()
        except ValueError as exc:
            raise ApiError("The job search API returned an invalid JSON response.") from exc

        data = payload.get("data", [])
        if not isinstance(data, list):
            raise ApiError("The job search API returned an unexpected response format.")

        jobs = [Job.from_api_payload(item) for item in data if isinstance(item, dict)]
        return deduplicate_jobs(jobs)

    @staticmethod
    def _raise_for_status(response: requests.Response) -> None:
        """Translate HTTP failures into clearer application errors."""

        if response.status_code in {401, 403}:
            raise ApiError("RapidAPI rejected the request. Check your RAPIDAPI_KEY value.")

        if response.status_code == 429:
            raise ApiError("RapidAPI rate limit reached. Try again later or reduce the search size.")

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise ApiError(f"Job search API request failed with status {response.status_code}.") from exc
