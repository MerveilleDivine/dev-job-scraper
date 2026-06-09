# Remote Dev Job Finder

A Python-based remote developer job search tool that uses the JSearch API to fetch job listings, normalize results, display them in a Gradio web interface, and export clean CSV files for personal job tracking.

The project started as a small job scraper and has been refactored into a structured API-powered application with clearer architecture, safer configuration, tests, and CI.

## Why this project matters

Searching for remote developer roles often means repeating the same searches, opening many tabs, and losing track of useful opportunities. Remote Dev Job Finder gives a simple workflow:

1. Search by role, skill, location, or keyword.
2. Fetch structured job results through the JSearch API.
3. Normalize the results into a consistent format.
4. Review them in a web interface or terminal.
5. Export them to CSV for tracking applications.

## Features

- Search remote developer jobs using the JSearch API.
- Optional country filtering with ISO 3166-1 alpha-2 country codes.
- Configurable number of API result pages.
- Date filter support for all, today, last 3 days, week, and month.
- Gradio web interface for quick interactive search.
- CLI for terminal-based workflows.
- CSV export with clean filenames and stable column order.
- Input validation for safer user experience.
- Friendly errors for missing API keys, rate limits, and failed requests.
- Basic test suite for client behavior and CSV export.
- GitHub Actions workflow for linting and tests.

## Tech stack

| Area | Tools |
| --- | --- |
| Language | Python 3.10+ |
| API | JSearch API through RapidAPI |
| UI | Gradio |
| Data handling | pandas, CSV |
| Configuration | python-dotenv, environment variables |
| Testing | pytest |
| Code quality | ruff |
| CI | GitHub Actions |

## Project structure

```text
.
├── src/dev_job_finder/
│   ├── app.py
│   ├── cli.py
│   ├── client.py
│   ├── config.py
│   ├── exceptions.py
│   ├── exporter.py
│   └── models.py
├── tests/
├── code/
├── .github/workflows/ci.yml
├── .env.example
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/MerveilleDivine/dev-job-scraper.git
cd dev-job-scraper
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install the project:

```bash
pip install -e .
```

For development, tests, and linting:

```bash
pip install -e ".[dev]"
```

## Configuration

Create a `.env` file in the project root:

```env
RAPIDAPI_KEY=your_rapidapi_key_here
```

For backwards compatibility, the app also accepts `API_KEY`, but `RAPIDAPI_KEY` is preferred because it is more explicit.

## Usage

### Web app

```bash
python -m dev_job_finder.app
```

Backwards-compatible wrapper:

```bash
python code/app.py
```

### CLI

```bash
dev-job-finder "remote python" --pages 2 --country us
```

Equivalent module command:

```bash
python -m dev_job_finder.cli "remote python" --pages 2 --country us
```

Save to a custom CSV file:

```bash
dev-job-finder "backend engineer" --pages 2 --country gb --output exports/backend_uk.csv
```

Use date filtering:

```bash
dev-job-finder "python developer" --date-posted week
```

## Example CSV output

| Job Title | Company | Location | Country | Link | Date Posted | Source |
| --- | --- | --- | --- | --- | --- | --- |
| Backend Engineer | Example Co | London | GB | https://... | 2026-06-09T08:30:00Z | JSearch |
| Full Stack Developer | Startup Inc | Remote | US | https://... | 2026-06-08T15:10:00Z | JSearch |

## Error handling

The project handles common failure cases:

- Missing RapidAPI key.
- Invalid country code.
- Empty search query.
- Too many pages requested.
- Unauthorized or forbidden API responses.
- API rate limiting.
- Network failures and malformed API responses.

## Testing

```bash
pytest
ruff check .
```

## Roadmap

- Add job deduplication by source job ID and apply link.
- Add a local search history database.
- Add optional JSON export.
- Add saved searches.
- Add skill-based matching score.
- Add a demo GIF to the README.
- Add a small dashboard showing result counts by company, country, and date.

## Limitations

- Results depend on the JSearch API and may not include every remote job available online.
- Some listings may be remote, hybrid, or location-specific depending on source data.
- Country filtering depends on the API response and is not the same as city-level filtering.
- This project is intended for educational and personal job-search workflows.

## License

MIT License © Mervine Muganguzi
