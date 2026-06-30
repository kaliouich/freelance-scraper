import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from .base import BaseScraper
import datetime

class FreelanceInfoScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.freelance-info.fr"
        self.search_url = f"{self.base_url}/missions?keywords=devops+cloud"
        
    def scrape(self) -> List[Dict]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        
        missions = []
        try:
            response = requests.get(self.search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Note: Selectors might need adjustment based on the actual HTML structure of freelance-info.fr
            # Typically, jobs are in a list or table
            job_cards = soup.select(".mission-card, .card-job, .offer") # Placeholder selectors, let's use a generic approach
            
            # Since freelance-info updates its DOM, let's look for standard 'a' tags that look like missions
            # /missions/xxx
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/mission-' in href or '/missions/' in href and not href.endswith('/missions'):
                    title = link.text.strip()
                    if not title or len(title) < 5:
                        continue
                        
                    full_url = href if href.startswith("http") else f"{self.base_url}{href}"
                    
                    if self.matches_keywords(title):
                        missions.append({
                            "id": full_url,
                            "title": title,
                            "company": "Non spécifié",
                            "url": full_url,
                            "platform": "Freelance-info",
                            "date_published": datetime.datetime.now().strftime("%Y-%m-%d")
                        })
                        
        except Exception as e:
            print(f"Error scraping Freelance-info: {e}")
            
        # Deduplicate
        unique_missions = {m['id']: m for m in missions}.values()
        return list(unique_missions)
