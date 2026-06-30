import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from .base import BaseScraper
import datetime

class FreeWorkScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.free-work.com"
        # Search for jobs, maybe API is better but let's try HTML first
        self.search_url = f"{self.base_url}/fr/tech-it/jobs?query=devops"
        
    def scrape(self) -> List[Dict]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "fr-FR,fr;q=0.9",
        }
        
        missions = []
        try:
            response = requests.get(self.search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Simple heuristic: find all links to jobs
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/jobs/' in href and not href.endswith('/jobs'):
                    title = link.text.strip()
                    # Clean up title if it contains newlines
                    title = " ".join(title.split())
                    if not title or len(title) < 5:
                        continue
                        
                    full_url = href if href.startswith("http") else f"{self.base_url}{href}"
                    
                    if self.matches_keywords(title):
                        missions.append({
                            "id": full_url,
                            "title": title,
                            "company": "Free-Work Client",
                            "url": full_url,
                            "platform": "Free-Work",
                            "date_published": datetime.datetime.now().strftime("%Y-%m-%d")
                        })
                        
        except Exception as e:
            print(f"Error scraping Free-work: {e}")
            
        # Deduplicate
        unique_missions = {m['id']: m for m in missions}.values()
        return list(unique_missions)
