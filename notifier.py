import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials not configured. Skipping notification.")
        print(f"Message: {message}")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def notify_new_mission(mission_data: dict):
    # mission_data should have: title, company, url, platform, and optionally location
    location_str = f"<b>Lieu:</b> {mission_data['location']}\n" if 'location' in mission_data and mission_data['location'] else ""
    
    message = (
        f"🚀 <b>Nouvelle Mission ({mission_data['platform']})</b>\n\n"
        f"<b>Titre:</b> {mission_data['title']}\n"
        f"<b>Entreprise:</b> {mission_data.get('company', 'Non précisé')}\n"
        f"{location_str}"
        f"<a href='{mission_data['url']}'>Lien vers la mission</a>"
    )
    send_telegram_message(message)
