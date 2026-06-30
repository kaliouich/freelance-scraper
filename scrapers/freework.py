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
            api_url = f"{self.base_url}/api/job_postings?contracts=contractor&search={clean_keyword}&itemsPerPage=100"
            headers = {"User-Agent": "Mozilla/5.0"}
            
            try:
                response = requests.get(api_url, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                # The API returns a hydra collection
                jobs = data.get("hydra:member", [])
                
                for job in jobs:
                    # For job_postings, the actual title is in 'title'
                    title = job.get("title", "")
                    
                    if not title:
                        continue
                        
                    # Filter out irrelevant jobs based on title matching
                    if not self.matches_keywords(title):
                        continue
                        
                    # The unique id
                    job_id = str(job.get("id", ""))
                    
                    # Ensure we don't process duplicates within the same run or if already in DB
                    if not job_id or job_id in seen_ids:
                        continue
                        
                    seen_ids.add(job_id)
                    slug = job.get("slug", "")
                    job_role_slug = job.get("job", {}).get("slug", "developpeur-it")
                    
                    # Format: https://www.free-work.com/fr/tech-it/job-mission/{job_role_slug}/{slug}
                    full_url = f"{self.base_url}/fr/tech-it/job-mission/{job_role_slug}/{slug}"
                    
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
