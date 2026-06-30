import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from .base import BaseScraper
import datetime

class LinkedInScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        # URL publique de recherche d'emploi sur LinkedIn (sans authentification)
        self.search_url = "https://www.linkedin.com/jobs/search/?keywords=freelance%20devops%20cloud&location=France"
        
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
            
            # Sur la version non connectée, LinkedIn utilise des classes spécifiques
            for card in soup.find_all('div', class_='base-search-card__info'):
                title_elem = card.find('h3', class_='base-search-card__title')
                company_elem = card.find('a', class_='hidden-nested-link') or card.find('h4', class_='base-search-card__subtitle')
                
                parent_card = card.find_parent('div', class_='base-search-card')
                link_elem = parent_card.find('a', class_='base-card__full-link') if parent_card else None
                
                if title_elem and link_elem:
                    title = title_elem.text.strip()
                    company = company_elem.text.strip() if company_elem else "Non spécifié"
                    location_elem = card.find('span', class_='job-search-card__location')
                    location = location_elem.text.strip() if location_elem else "Non spécifié"
                    href = link_elem.get('href', '').split('?')[0] # Nettoyer les paramètres de tracking
                    
                    # Filter out CDIs and enforce Freelance/Mission
                    title_lower = title.lower()
                    
                    # Exclude CDIs
                    is_cdi = 'cdi' in title_lower.split() or 'cdi' in title_lower.replace('-', ' ').split()
                    
                    # Enforce freelance terminology
                    is_freelance = any(word in title_lower for word in ["freelance", "mission", "indépendant", "independant", "contract", "tj", "tjm"])
                    
                    if self.matches_keywords(title) and not is_cdi and is_freelance:
                        missions.append({
                            "id": href,
                            "title": title,
                            "company": company,
                            "location": location,
                            "url": href,
                            "platform": "LinkedIn",
                            "date_published": datetime.datetime.now().strftime("%Y-%m-%d")
                        })
                        
        except Exception as e:
            print(f"Error scraping LinkedIn: {e}")
            
        unique_missions = {m['id']: m for m in missions}.values()
        return list(unique_missions)
