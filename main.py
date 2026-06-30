import time
from db import init_db, is_mission_exists, save_mission
from notifier import notify_new_mission
from scrapers import FreelanceInfoScraper, FreeWorkScraper, LinkedInScraper, MaltScraper

def main():
    print("Initializing database...")
    init_db()
    
    scrapers = [
        FreelanceInfoScraper(),
        FreeWorkScraper(),
        LinkedInScraper(),
        MaltScraper()
    ]
    
    total_new_missions = 0
    
    for scraper in scrapers:
        print(f"Running scraper: {scraper.__class__.__name__}")
        try:
            missions = scraper.scrape()
            print(f"Found {len(missions)} potential missions on {scraper.__class__.__name__}.")
            
            for mission in missions:
                if not is_mission_exists(mission["id"]):
                    print(f"New mission found: {mission['title']}")
                    # Save to database
                    save_mission(
                        mission_id=mission["id"],
                        title=mission["title"],
                        company=mission["company"],
                        url=mission["url"],
                        platform=mission["platform"],
                        date_published=mission["date_published"]
                    )
                    
                    # Notify
                    notify_new_mission(mission)
                    total_new_missions += 1
                    
                    # Small delay to avoid spamming the Telegram API
                    time.sleep(1)
        except Exception as e:
            print(f"Failed during execution of {scraper.__class__.__name__}: {e}")
            
    print(f"Scraping completed. {total_new_missions} new missions found.")

if __name__ == "__main__":
    main()
