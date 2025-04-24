import requests
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
import pandas as pd

class AdzunaAPI:
    def __init__(self):
        self.app_id = "dd78fa64"
        self.api_key = "5884a0e76f0eaa7c69202ce052fdf10f"
        self.base_url = "https://api.adzuna.com/v1/api"

    def search_jobs(self, keywords: str, location: str = "us", page: int = 1, where: str = None) -> Dict:
        """Search for jobs based on keywords and location."""
        url = f"{self.base_url}/jobs/{location}/search/{page}"
        
        params = {
            "app_id": self.app_id,
            "app_key": self.api_key,
            "what": keywords,
            "content-type": "application/json",
            "results_per_page": 20
        }
        
        if where:
            params["where"] = where
            
        response = requests.get(url, params=params)
        return response.json()

    def get_salary_histogram(self, keywords: str, location: str = "us") -> Dict:
        """Get salary distribution for given keywords."""
        url = f"{self.base_url}/jobs/{location}/histogram"
        
        params = {
            "app_id": self.app_id,
            "app_key": self.api_key,
            "what": keywords,
            "content-type": "application/json"
        }
        
        response = requests.get(url, params=params)
        return response.json()

    def get_salary_insights(self, keywords: str, location: str = "us") -> Dict:
        """Get detailed salary insights for given keywords."""
        search_result = self.search_jobs(keywords, location)
        salaries = []
        
        if "results" in search_result:
            for job in search_result["results"]:
                if "salary_min" in job and "salary_max" in job:
                    salaries.append({
                        "min": job["salary_min"],
                        "max": job["salary_max"],
                        "avg": (job["salary_min"] + job["salary_max"]) / 2
                    })
        
        if salaries:
            df = pd.DataFrame(salaries)
            return {
                "min": df["min"].min(),
                "max": df["max"].max(),
                "avg": df["avg"].mean(),
                "median": df["avg"].median(),
                "p25": df["avg"].quantile(0.25),
                "p75": df["avg"].quantile(0.75)
            }
        return {}

    def get_top_companies(self, keywords: str, location: str = "us", limit: int = 5, where: str = None) -> List[Dict]:
        """Get top companies hiring for given keywords."""
        jobs_data = self.search_jobs(keywords, location, where=where)
        companies = {}
        
        if "results" in jobs_data:
            for job in jobs_data["results"]:
                company = job.get("company", {}).get("display_name", "Unknown")
                if company in companies:
                    companies[company]["count"] += 1
                    if "salary_max" in job:
                        companies[company]["salaries"].append(job["salary_max"])
                else:
                    companies[company] = {
                        "count": 1,
                        "salaries": [job.get("salary_max", 0)] if "salary_max" in job else []
                    }
        
        # Process company data
        company_insights = []
        for name, data in companies.items():
            avg_salary = sum(data["salaries"]) / len(data["salaries"]) if data["salaries"] else 0
            company_insights.append({
                "name": name,
                "job_count": data["count"],
                "avg_salary": avg_salary
            })
        
        # Sort by job count and get top N
        return sorted(company_insights, key=lambda x: x["job_count"], reverse=True)[:limit]

    def analyze_market_demand(self, skills: List[str], location: str = "us", cities: List[str] = None) -> Dict:
        """Analyze market demand for multiple skills across locations."""
        results = {}
        cities = cities or ["New York", "San Francisco", "Chicago", "Austin", "Seattle"]
        
        for skill in skills:
            skill_data = {
                "total_jobs": 0,
                "average_salary": 0,
                "by_location": {},
                "salary_insights": self.get_salary_insights(skill, location)
            }
            
            # Get national data
            national_data = self.search_jobs(skill, location)
            skill_data["total_jobs"] = national_data.get("count", 0)
            
            # Get location-specific data
            for city in cities:
                city_data = self.search_jobs(skill, location, where=city)
                skill_data["by_location"][city] = {
                    "job_count": city_data.get("count", 0),
                    "salary_insights": self.get_salary_insights(skill, location)
                }
            
            results[skill] = skill_data
        
        return results

    def get_trending_skills(self, base_skill: str, location: str = "us") -> List[Dict]:
        """Find trending related skills based on job postings."""
        jobs_data = self.search_jobs(base_skill, location)
        skills_mentioned = {}
        
        if "results" in jobs_data:
            for job in jobs_data["results"]:
                description = job.get("description", "").lower()
                # Common tech skills to look for
                tech_skills = ["python", "java", "javascript", "react", "aws", "azure", "docker", "kubernetes", "sql", "nosql", "machine learning", "ai"]
                
                for skill in tech_skills:
                    if skill in description:
                        skills_mentioned[skill] = skills_mentioned.get(skill, 0) + 1
        
        # Convert to list and sort by frequency
        trending = [{"skill": k, "mentions": v} for k, v in skills_mentioned.items()]
        return sorted(trending, key=lambda x: x["mentions"], reverse=True) 