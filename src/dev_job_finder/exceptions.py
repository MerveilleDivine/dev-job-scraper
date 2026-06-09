"""Project-specific exceptions for Remote Dev Job Finder."""


class JobFinderError(Exception):
    """Base exception for the application."""


class ConfigurationError(JobFinderError):
    """Raised when required configuration is missing or invalid."""


class ValidationError(JobFinderError):
    """Raised when user input cannot be used safely."""


class ApiError(JobFinderError):
    """Raised when the upstream job search API cannot return usable results."""
