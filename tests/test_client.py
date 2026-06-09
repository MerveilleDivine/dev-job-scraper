import requests
import pytest

from dev_job_finder.client import JSearchClient
from dev_job_finder.config import Settings
from dev_job_finder.exceptions import ApiError, ValidationError


class FakeResponse:
    def __init__(self, payload=None, status_code=200):
        self.payload = payload or {"data": []}
        self.status_code = status_code

    def json(self):
        return self.payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError("request failed")


class FakeSession:
    def __init__(self, response=None, exception=None):
        self.response = response or FakeResponse()
        self.exception = exception
        self.last_request = None

    def get(self, url, headers, params, timeout):
        self.last_request = {
            "url": url,
            "headers": headers,
            "params": params,
            "timeout": timeout,
        }
        if self.exception:
            raise self.exception
        return self.response


def test_search_normalizes_api_payload():
    payload = {
        "data": [
            {
                "job_id": "abc123",
                "job_title": "Backend Engineer",
                "employer_name": "Acme Corp",
                "job_city": "London",
                "job_state": "England",
                "job_country": "GB",
                "job_apply_link": "https://example.com/apply",
                "job_posted_at_datetime_utc": "2026-06-09T08:30:00Z",
                "job_employment_type": "FULLTIME",
            }
        ]
    }
    session = FakeSession(FakeResponse(payload))
    client = JSearchClient(settings=Settings(rapidapi_key="test-key"), session=session)

    jobs = client.search(" remote python ", pages=2, country="GB", date_posted="week")

    assert len(jobs) == 1
    assert jobs[0].title == "Backend Engineer"
    assert jobs[0].company == "Acme Corp"
    assert jobs[0].location == "London, England, GB"
    assert jobs[0].source == "JSearch"
    assert session.last_request["params"]["query"] == "remote python"
    assert session.last_request["params"]["country"] == "gb"
    assert session.last_request["params"]["num_pages"] == 2


def test_search_deduplicates_jobs_by_id():
    payload = {
        "data": [
            {"job_id": "same", "job_title": "Python Dev", "employer_name": "One"},
            {"job_id": "same", "job_title": "Python Dev", "employer_name": "One"},
        ]
    }
    client = JSearchClient(
        settings=Settings(rapidapi_key="test-key"),
        session=FakeSession(FakeResponse(payload)),
    )

    jobs = client.search("python")

    assert len(jobs) == 1


def test_empty_query_raises_validation_error():
    client = JSearchClient(settings=Settings(rapidapi_key="test-key"), session=FakeSession())

    with pytest.raises(ValidationError, match="Search query cannot be empty"):
        client.search("   ")


def test_invalid_country_raises_validation_error():
    client = JSearchClient(settings=Settings(rapidapi_key="test-key"), session=FakeSession())

    with pytest.raises(ValidationError, match="Country must be"):
        client.search("python", country="usa")


def test_rate_limit_raises_api_error():
    client = JSearchClient(
        settings=Settings(rapidapi_key="test-key"),
        session=FakeSession(FakeResponse(status_code=429)),
    )

    with pytest.raises(ApiError, match="rate limit"):
        client.search("python")


def test_network_failure_raises_api_error():
    client = JSearchClient(
        settings=Settings(rapidapi_key="test-key"),
        session=FakeSession(exception=requests.Timeout("timeout")),
    )

    with pytest.raises(ApiError, match="Unable to reach"):
        client.search("python")
