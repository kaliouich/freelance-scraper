from abc import ABC, abstractmethod
from typing import List, Dict

class BaseScraper(ABC):
    def __init__(self):
        self.keywords = ["aws", "docker", "cloud", "devops", "kubernetes", "k8s"]
    
    @abstractmethod
    def scrape(self) -> List[Dict]:
        """
        Scrapes the target website and returns a list of dictionaries.
        Each dictionary should represent a mission with keys:
        - id: Unique identifier (often the URL)
        - title: Mission title
        - company: Company name (if available)
        - url: URL to the mission
        - platform: Name of the platform (e.g., 'Freelance-info')
        - date_published: Date string
        """
        pass

    def matches_keywords(self, text: str) -> bool:
        """
        Checks if the given text contains any of our target keywords.
        """
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.keywords)
