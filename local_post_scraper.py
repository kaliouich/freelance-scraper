import os
import time
import datetime
from dotenv import load_dotenv
from linkedin_api import Linkedin
from db import init_db, is_mission_exists, save_mission
from notifier import notify_new_mission

# Load environment variables
load_dotenv()

LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def main():
    print("Initialisation de la base de données...")
    init_db()

    if not LINKEDIN_USERNAME or not LINKEDIN_PASSWORD:
        print("ERREUR : Veuillez définir LINKEDIN_USERNAME et LINKEDIN_PASSWORD dans votre fichier .env")
        print("RAPPEL : Utilisez un compte 'burner' (faux compte) pour éviter que votre compte principal ne soit banni.")
        return

    print("Connexion à LinkedIn (cela peut prendre quelques secondes)...")
    try:
        # Authenticate using any Linkedin account credentials
        api = Linkedin(LINKEDIN_USERNAME, LINKEDIN_PASSWORD)
    except Exception as e:
        print(f"Échec de la connexion à LinkedIn: {e}")
        return

    # Keywords to search in posts
    search_keywords = "recherche freelance devops OR cloud"
    
    print(f"Recherche de posts avec les mots-clés : '{search_keywords}'...")
    
    try:
        # Search for posts
        # The API method search_posts might not be directly available, usually search(query, limit, type='post') or similar
        # Let's use search_posts if available, otherwise search with appropriate type
        # According to linkedin-api docs: search_posts(keywords)
        posts = api.search_posts(search_keywords, limit=20)
        print(f"{len(posts)} posts trouvés. Analyse en cours...")
        
        total_new = 0
        for post in posts:
            post_urn = post.get("urn", "")
            post_text = post.get("text", "")
            post_author = post.get("author", {}).get("name", "Auteur inconnu")
            
            # Simple URN extraction to create a clickable link
            # Post URN looks like urn:li:activity:123456789
            activity_id = post_urn.split(":")[-1] if ":" in post_urn else post_urn
            post_url = f"https://www.linkedin.com/feed/update/urn:li:activity:{activity_id}/"
            
            if not activity_id:
                continue

            text_lower = post_text.lower()
            
            # Strict filtering: MUST NOT be a CDI, SHOULD mention freelance/mission
            is_cdi = "cdi" in text_lower.split() or " cdi " in text_lower
            is_freelance = any(word in text_lower for word in ["freelance", "mission", "indépendant", "independant", "tj", "tjm"])
            
            if is_freelance and not is_cdi:
                if not is_mission_exists(post_url):
                    print(f"Nouveau Post pertinent trouvé de {post_author}!")
                    
                    mission_data = {
                        "id": post_url,
                        "title": f"Post de {post_author}: {post_text[:60]}...",
                        "company": post_author,
                        "url": post_url,
                        "platform": "LinkedIn (Post)"
                    }
                    
                    save_mission(
                        mission_id=post_url,
                        title=mission_data["title"],
                        company=mission_data["company"],
                        url=post_url,
                        platform="LinkedIn (Post)",
                        date_published=datetime.datetime.now().strftime("%Y-%m-%d")
                    )
                    
                    notify_new_mission(mission_data)
                    total_new += 1
                    time.sleep(2) # Avoid spamming Telegram API
                    
        print(f"Recherche terminée. {total_new} nouveaux posts pertinents trouvés.")
        
    except Exception as e:
        print(f"Erreur lors de la recherche de posts: {e}")

if __name__ == "__main__":
    main()
