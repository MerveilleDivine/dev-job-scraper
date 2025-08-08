# 🌎 Remote Job Search App (API & GUI)

A modern Python app to search remote jobs worldwide using the [JSearch API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch/).  
Includes a Gradio web interface and CSV export.  
Just fast API-powered job search!

---

## Features

- **Search remote jobs worldwide** (or by country) using the JSearch API
- **Filter by keywords** (e.g. `python`, `react`, `dubai`)
- **Set number of result pages** to fetch
- **Export results to CSV**
- **Easy-to-use Gradio web GUI**
- **Command-line interface (CLI) also available**

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MerveilleDivine/dev-job-scraper.git
   cd dev-job-scraper
   ```

2. **(Optional) Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your RapidAPI key:**
   - Create a `.env` file in the project root:
     ```
     API_KEY=your_rapidapi_key_here
     ```
   - Get your key from [RapidAPI JSearch](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch/).

---

## Usage

### Gradio Web App

Launch the GUI:
```bash
python code/app.py
```
- Enter your keywords (e.g. `remote python`), number of pages, and (optionally) a 2-letter country code (e.g. `us`, `gb`, `ae`).  
- Leave country blank for worldwide search.
- View results in the browser and download as CSV.

### Command-Line Interface

Run:
```bash
python code/scraper.py "remote python" --pages 2 --country ""
```
- Replace `"remote python"` with your keywords.
- Use `--pages` to set number of result pages (default: 1).
- Use `--country` for a 2-letter country code (default: `us`). Use `""` for worldwide.

Example for Dubai jobs:
```bash
python code/scraper.py "python dubai" --country ae
```

---

## Example Output

The CSV file contains columns:

| Job Title        | Company     | Location | Link                                   | Date Posted          |
|------------------|------------|----------|----------------------------------------|----------------------|
| Backend Engineer | Acme Corp   | Dubai    | https://...                            | 2025-07-29T12:34:56Z |
| Frontend Dev     | Startup XYZ | London   | https://...                            | 2025-07-29T09:12:34Z |
| ...              | ...         | ...      | ...                                    | ...                  |

---

## Configuration

- **API Key:**  
  Set your RapidAPI key in a `.env` file as `API_KEY=...`.

- **Country Codes:**  
  Use [ISO 3166-1 alpha-2 codes](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes) (e.g. `us`, `gb`, `ae`).  
  Leave blank for worldwide.

---

## Limitations

- Results depend on the JSearch API (not all jobs may be fully remote).
- Location filtering is by country code, not city. For city, include it in your keywords.
- Intended for educational and personal use.

---

## License

MIT License © Mervine Muganguzi

---

## Contact

For questions or suggestions, please open an issue or contact [mervinemuganguzi1@outlook.com](mailto:mervinemuganguzi1@outlook.com).

---
