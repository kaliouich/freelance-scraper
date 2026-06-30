import requests
from typing import List, Dict
from .base import BaseScraper
import datetime

class FreeWorkScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.free-work.com"
        
    def scrape(self) -> List[Dict]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }
        
        missions = []
        seen_ids = set()
        
        for keyword in self.keywords:
            # We don't want to send special characters like / in the search query directly if it breaks the API
            clean_keyword = keyword.replace("/", " ")
            api_url = f"{self.base_url}/api/jobs?contracts=contractor&search={clean_keyword}&itemsPerPage=100"
            
            try:
                response = requests.get(api_url, headers=headers, timeout=10)
                if response.status_code != 200:
                    continue
                
                data = response.json()
                
                if isinstance(data, dict):
                    jobs = data.get("hydra:member", [])
                elif isinstance(data, list):
                    jobs = data
                else:
                    jobs = []
                
                for job in jobs:
                    title = job.get("title", job.get("name", ""))
                    slug = job.get("slug", "")
                    if not title or not slug:
                        continue
                    
                    # Format: https://www.free-work.com/fr/tech-it/jobs/{slug}
                    full_url = f"{self.base_url}/fr/tech-it/jobs/{slug}"
                    job_id = str(job.get("id", full_url))
                    
                    if job_id in seen_ids:
                        continue
                    
                    seen_ids.add(job_id)
                    
                    company_name = "Client Free-Work"
                    if job.get("company") and isinstance(job["company"], dict):
                        company_name = job["company"].get("name", "Client Free-Work")
                        
                    location_name = "Non spécifié"
                    if job.get("location") and isinstance(job["location"], dict):
                        location_name = job["location"].get("name", "Non spécifié")
                    
                    if self.matches_keywords(title):
                        missions.append({
                            "id": job_id,
                            "title": title,
                            "company": company_name,
                            "location": location_name,
                            "url": full_url,
                            "platform": "Free-Work",
                            "date_published": datetime.datetime.now().strftime("%Y-%m-%d")
                        })
                            
            except Exception as e:
                print(f"Error scraping Free-work API for keyword {keyword}: {e}")
            
        unique_missions = {m['id']: m for m in missions}.values()
        return list(unique_missions)
