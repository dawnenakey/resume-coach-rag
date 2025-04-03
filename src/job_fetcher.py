# src/job_fetcher.py
import os
import json
from datetime import datetime
import requests
from dotenv import load_dotenv

# Load API credentials from .env file (create one in your repo root)
load_dotenv()

API_URL = "https://api.adzuna.com/v1/api/jobs/us/search/1"
API_ID = os.getenv("ADZUNA_APP_ID")
API_KEY = os.getenv("ADZUNA_APP_KEY")

def fetch_jobs(query="software developer", location="USA", results_per_page=10):
    params = {
        "app_id": API_ID,
        "app_key": API_KEY,
        "results_per_page": results_per_page,
        "what": query,
        "where": location,
        "content-type": "application/json"
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json()

def save_jobs_data(data, directory="data/sample_jobs"):
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(directory, f"sample_jobs_{timestamp}.json")
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Job data saved to {filename}")

if __name__ == "__main__":
    try:
        jobs_data = fetch_jobs()
        save_jobs_data(jobs_data)
    except Exception as e:
        print("Error fetching jobs:", e)
