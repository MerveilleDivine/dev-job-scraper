import gradio as gr
import pandas as pd
from scraper import fetch_jobs_api

def search_jobs(keywords, pages, country):
    try:
        jobs = fetch_jobs_api(keywords, num_pages=pages, country=country)
        if not jobs:
            return "No jobs found.", None
        df = pd.DataFrame(jobs)
        return df.to_markdown(), df
    except Exception as e:
        return f"Error: {e}", None

def download_csv(df):
    if df is not None:
        df.to_csv("jobs.csv", index=False)
        return "jobs.csv"
    return None

with gr.Blocks(title="Remote Job Scraper") as demo:
    gr.Markdown("# 🌎 Remote Job Scraper\nSearch remote jobs worldwide using the JSearch API.")

    with gr.Row():
        keywords = gr.Textbox(label="Keywords", placeholder="e.g. python, react, ai", value="remote developer")
        pages = gr.Number(label="Pages", value=1, precision=0)
        country = gr.Textbox(label="Country code (blank for worldwide)", value="")

    search_btn = gr.Button("🔍 Search")
    output_md = gr.Markdown("Results will appear here.")
    output_df = gr.Dataframe(visible=False, interactive=True, label="Results Table")
    download_btn = gr.DownloadButton("Download CSV", value=None, visible=False)

    def on_search(keywords, pages, country):
        md, df = search_jobs(keywords, int(pages), country)
        show_df = df is not None and not df.empty
        return (
            md,
            gr.update(visible=show_df, value=df if show_df else None),
            gr.update(visible=show_df, value=download_csv(df) if show_df else None)
        )

    search_btn.click(
        fn=on_search,
        inputs=[keywords, pages, country],
        outputs=[output_md, output_df, download_btn]
    )

if __name__ == "__main__":
    demo.launch()