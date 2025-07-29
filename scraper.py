# dev_job_scraper/scraper.py

import requests
from bs4 import BeautifulSoup
import csv
import argparse
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_remoteok_jobs(keyword):
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f"[RemoteOK] Failed: {resp.status_code}")
        return []
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []
    for tr in soup.find_all('tr', class_='job'):
        title_tag = tr.find('h2')
        company_tag = tr.find('h3')
        link_tag = tr.find('a', class_='preventLink')
        date_tag = tr.find('time')
        if title_tag and company_tag and link_tag:
            jobs.append({
                "title": title_tag.get_text(strip=True),
                "company": company_tag.get_text(strip=True),
                "link": f"https://remoteok.com{link_tag['href']}",
                "date": date_tag.get('datetime') if date_tag else "N/A",
                "source": "RemoteOK"
            })
    return jobs

def get_weworkremotely_jobs(keyword):
    url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f"[WeWorkRemotely] Failed: {resp.status_code}")
        return []
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []
    sections = soup.find_all('section', class_='jobs')
    for section in sections:
        for li in section.find_all('li', class_=False):
            anchor = li.find('a', href=True)
            if anchor:
                company = li.find('span', class_='company')
                title = li.find('span', class_='title')
                jobs.append({
                    "title": title.get_text(strip=True) if title else "N/A",
                    "company": company.get_text(strip=True) if company else "N/A",
                    "link": f"https://weworkremotely.com{anchor['href']}",
                    "date": datetime.today().strftime('%Y-%m-%d'),
                    "source": "WeWorkRemotely"
                })
    return jobs

def get_remoteco_jobs(keyword):
    url = f"https://remote.co/remote-jobs/developer/?search_term={keyword}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f"[Remote.co] Failed: {resp.status_code}")
        return []
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []
    for li in soup.find_all("li", class_="job_listing"):
        title = li.find("a", class_="job_listing-title")
        company = li.find("span", class_="company")
        date = li.find("time")
        if title:
            jobs.append({
                "title": title.get_text(strip=True),
                "company": company.get_text(strip=True) if company else "N/A",
                "link": title["href"],
                "date": date.get("datetime") if date else datetime.today().strftime('%Y-%m-%d'),
                "source": "Remote.co"
            })
    return jobs

def get_justremote_jobs(keyword):
    url = f"https://justremote.co/remote-jobs/search?term={keyword}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f"[JustRemote] Failed: {resp.status_code}")
        return []
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []
    # Jobs are in divs with class 'job' or 'JobCard'
    for div in soup.find_all('div', class_='job'):
        title_tag = div.find('h3')
        company_tag = div.find('p', class_='company')
        link_tag = div.find('a', href=True)
        if title_tag and company_tag and link_tag:
            jobs.append({
                "title": title_tag.get_text(strip=True),
                "company": company_tag.get_text(strip=True),
                "link": f"https://justremote.co{link_tag['href']}",
                "date": datetime.today().strftime('%Y-%m-%d'),
                "source": "JustRemote"
            })
    return jobs

def get_remotive_jobs(keyword):
    url = f"https://remotive.io/remote-jobs/search?search={keyword}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f"[Remotive] Failed: {resp.status_code}")
        return []
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []
    for div in soup.find_all('div', class_='job-tile'):
        title_tag = div.find('h2')
        company_tag = div.find('span', class_='company-name')
        link_tag = div.find('a', href=True)
        if title_tag and company_tag and link_tag:
            jobs.append({
                "title": title_tag.get_text(strip=True),
                "company": company_tag.get_text(strip=True),
                "link": link_tag['href'],
                "date": datetime.today().strftime('%Y-%m-%d'),
                "source": "Remotive"
            })
    return jobs

def get_workingnomads_jobs(keyword):
    url = f"https://www.workingnomads.co/jobs?category=development&search={keyword}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f"[WorkingNomads] Failed: {resp.status_code}")
        return []
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []
    for div in soup.find_all('div', class_='job'):
        title_tag = div.find('h2')
        company_tag = div.find('div', class_='company')
        link_tag = div.find('a', href=True)
        if title_tag and company_tag and link_tag:
            jobs.append({
                "title": title_tag.get_text(strip=True),
                "company": company_tag.get_text(strip=True),
                "link": link_tag['href'],
                "date": datetime.today().strftime('%Y-%m-%d'),
                "source": "WorkingNomads"
            })
    return jobs

def get_jobspresso_jobs(keyword):
    url = f"https://jobspresso.co/remote-jobs/search/?search={keyword}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f"[Jobspresso] Failed: {resp.status_code}")
        return []
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []
    for li in soup.find_all('li', class_='job'):
        title_tag = li.find('h2', class_='job-title')
        company_tag = li.find('span', class_='company-name')
        link_tag = li.find('a', href=True)
        if title_tag and company_tag and link_tag:
            jobs.append({
                "title": title_tag.get_text(strip=True),
                "company": company_tag.get_text(strip=True),
                "link": link_tag['href'],
                "date": datetime.today().strftime('%Y-%m-%d'),
                "source": "Jobspresso"
            })
    return jobs

def save_to_csv(jobs, keyword):
    filename = f"{keyword}_jobs.csv"
    # remove duplicates by link to avoid repeat jobs
    unique_jobs = {job['link']: job for job in jobs}
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "link", "date", "source"])
        writer.writeheader()
        writer.writerows(unique_jobs.values())
    print(f"\nSaved {len(unique_jobs)} jobs to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Scrape remote dev jobs by keyword")
    parser.add_argument('--keyword', required=True, help='Job keyword to search for (e.g., python, react)')
    args = parser.parse_args()

    keyword = args.keyword.lower().strip()
    print(f"Searching for '{keyword}' across multiple remote job boards...\n")

    jobs = []
    jobs.extend(get_remoteok_jobs(keyword))
    jobs.extend(get_weworkremotely_jobs(keyword))
    jobs.extend(get_remoteco_jobs(keyword))
    jobs.extend(get_justremote_jobs(keyword))
    jobs.extend(get_remotive_jobs(keyword))
    jobs.extend(get_workingnomads_jobs(keyword))
    jobs.extend(get_jobspresso_jobs(keyword))

    if jobs:
        save_to_csv(jobs, keyword)
    else:
        print("No jobs found or scraping failed.")

if __name__ == "__main__":
    main()
