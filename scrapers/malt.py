import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from .base import BaseScraper
import datetime

class MaltScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        # Recherche de missions sur Malt
        self.search_url = "https://www.malt.fr/s?q=devops+cloud"
        
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
            
            # Malt obfusque beaucoup ses classes (React), on utilise une heuristique sur les liens
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/mission/' in href or '/project/' in href:
                    title = link.text.strip()
                    title = " ".join(title.split()) # Nettoyer les sauts de ligne
                    
                    if not title or len(title) < 5:
                        continue
                        
                    full_url = href if href.startswith("http") else f"https://www.malt.fr{href}"
                    
                    if self.matches_keywords(title):
                        missions.append({
                            "id": full_url,
                            "title": title,
                            "company": "Client Malt",
                            "url": full_url,
                            "platform": "Malt",
                            "date_published": datetime.datetime.now().strftime("%Y-%m-%d")
                        })
                        
        except Exception as e:
            print(f"Error scraping Malt: {e}")
            
        unique_missions = {m['id']: m for m in missions}.values()
        return list(unique_missions)
