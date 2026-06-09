"""Configuration helpers for environment-based settings."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from dev_job_finder.exceptions import ConfigurationError

DEFAULT_RAPIDAPI_HOST = "jsearch.p.rapidapi.com"
DEFAULT_TIMEOUT_SECONDS = 15


@dataclass(frozen=True)
class Settings:
    """Runtime settings required by the API client."""

    rapidapi_key: str
    rapidapi_host: str = DEFAULT_RAPIDAPI_HOST
    request_timeout: int = DEFAULT_TIMEOUT_SECONDS


def load_settings() -> Settings:
    """Load settings from environment variables.

    RAPIDAPI_KEY is the preferred variable name. API_KEY is supported only for
    backwards compatibility with the first version of the project.
    """

    load_dotenv()
    rapidapi_key = os.getenv("RAPIDAPI_KEY") or os.getenv("API_KEY")

    if not rapidapi_key:
        raise ConfigurationError(
            "Missing RapidAPI key. Add RAPIDAPI_KEY=your_key_here to a .env file."
        )

    return Settings(rapidapi_key=rapidapi_key)
