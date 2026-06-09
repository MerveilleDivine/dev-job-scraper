"""Backwards-compatible wrapper for the Gradio app.

Preferred command:
    python -m dev_job_finder.app
"""

from dev_job_finder.app import demo

if __name__ == "__main__":
    demo.launch()
