import argparse
import csv
from dotenv import load_dotenv
import os
import os
import requests
load_dotenv()

api_key = os.getenv("API_KEY")
RAPIDAPI_KEY = api_key if api_key else print("⚠️ No API key found!")

def fetch_jobs_api(query, page=1, country="", num_pages=1):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY,
    }
    params = {
        "query": query,
        "page": page,
        "num_pages": num_pages,
        "country": country,
        "date_posted": "all"
    }
    resp = requests.get(url, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    jobs = []
    for job in data.get("data", []):
        jobs.append({
            "Job Title": job.get("job_title", ""),
            "Company": job.get("employer_name", ""),
            "Location": job.get("job_city", ""),
            "Link": job.get("job_apply_link", ""),
            "Date Posted": job.get("job_posted_at_datetime_utc", "")
        })
    return jobs

def save_jobs_to_csv(jobs, filename):
    if not jobs:
        print("No jobs found. Try another keyword.")
        return
    fields = ["Job Title", "Company", "Location", "Link", "Date Posted"]
    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(jobs)
    print(f"\n Saved {len(jobs)} jobs to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Remote Job Scraper (API version)")
    parser.add_argument("keyword", type=str, help="Job search keyword(s)")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to fetch")
    parser.add_argument("--country", type=str, default="us", help="Country code (e.g. us, gb, ca)")
    parser.add_argument("--output", type=str, default=None, help="Output CSV filename")
    args = parser.parse_args()

    print(f"\n🔍 Searching for jobs with keyword: {args.keyword}")
    jobs = fetch_jobs_api(args.keyword, num_pages=args.pages, country=args.country)
    filename = args.output or f"{args.keyword.replace(' ','_').lower()}_jobs.csv"
    save_jobs_to_csv(jobs, filename)

if __name__ == "__main__":
    main()