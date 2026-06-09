"""Gradio web interface for Remote Dev Job Finder."""

import gradio as gr
import pandas as pd

from dev_job_finder.client import JSearchClient, MAX_RESULT_PAGES
from dev_job_finder.exceptions import JobFinderError
from dev_job_finder.exporter import CSV_COLUMNS, export_jobs_to_csv

EMPTY_RESULTS = pd.DataFrame(columns=CSV_COLUMNS)


def search_jobs(query: str, pages: int, country: str, date_posted: str):
    """Run a job search and return UI-friendly outputs."""

    try:
        client = JSearchClient()
        jobs = client.search(query=query, pages=pages, country=country, date_posted=date_posted)
    except JobFinderError as exc:
        return (
            f"Error: {exc}",
            EMPTY_RESULTS,
            gr.update(visible=False, value=None),
        )

    if not jobs:
        return (
            "No jobs found. Try another keyword, country, or date filter.",
            EMPTY_RESULTS,
            gr.update(visible=False, value=None),
        )

    dataframe = pd.DataFrame([job.to_row() for job in jobs], columns=CSV_COLUMNS)
    csv_path = export_jobs_to_csv(jobs, query=query)
    return (
        f"Found {len(jobs)} job(s). Review the table below or download the CSV.",
        dataframe,
        gr.update(visible=True, value=str(csv_path)),
    )


with gr.Blocks(title="Remote Dev Job Finder") as demo:
    gr.Markdown(
        """
        # Remote Dev Job Finder

        Search remote developer jobs, review normalized results, and export a clean CSV file.
        """
    )

    with gr.Row():
        query = gr.Textbox(
            label="Search keywords",
            placeholder="remote python, backend engineer, react developer",
            value="remote developer",
        )
        pages = gr.Number(
            label=f"Result pages (1-{MAX_RESULT_PAGES})",
            value=1,
            precision=0,
            minimum=1,
            maximum=MAX_RESULT_PAGES,
        )

    with gr.Row():
        country = gr.Textbox(label="Country code", placeholder="us, gb, ae, or blank", value="")
        date_posted = gr.Dropdown(
            label="Date posted",
            choices=["all", "today", "3days", "week", "month"],
            value="all",
        )

    search_button = gr.Button("Search jobs")
    status = gr.Markdown("Results will appear after your first search.")
    results = gr.Dataframe(value=EMPTY_RESULTS, label="Job results", interactive=False)
    download = gr.DownloadButton("Download CSV", visible=False)

    search_button.click(
        fn=search_jobs,
        inputs=[query, pages, country, date_posted],
        outputs=[status, results, download],
    )


if __name__ == "__main__":
    demo.launch()
