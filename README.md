# Freelance Mission Scraper (DevOps & Cloud)

Ce projet est un script automatisé en Python qui récupère les nouvelles missions freelance pour des profils DevOps / Cloud sur plusieurs plateformes et vous notifie via Telegram.

## Plateformes supportées :
- Freelance-info
- Free-work
- LinkedIn (via recherche publique en HTML)
- Malt (via recherche en HTML)

*(Note : LinkedIn et Malt ont de fortes protections anti-bots. Si l'action GitHub se fait bloquer, il faudra envisager de rajouter des proxies ou des délais).*

## Prérequis

1. Avoir un bot Telegram et connaître son Token. (Créez-en un via @BotFather sur Telegram).
2. Connaître votre `chat_id` Telegram (vous pouvez utiliser des bots comme @userinfobot pour le trouver).
3. Python 3.10+

## Installation Locale

1. Clonez ce dossier ou naviguez dedans.
2. Créez un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Créez un fichier `.env` à la racine :
   ```env
   TELEGRAM_BOT_TOKEN=votre_token_ici
   TELEGRAM_CHAT_ID=votre_chat_id_ici
   ```
5. Lancez le script :
   ```bash
   python main.py
   ```

## Automatisation avec GitHub Actions

Ce projet contient un workflow GitHub Actions (`.github/workflows/scrape.yml`) configuré pour tourner tous les jours à 8h00 UTC.

Pour l'utiliser :
1. Créez un dépôt sur GitHub et poussez ce code.
2. Dans votre dépôt GitHub, allez dans **Settings > Secrets and variables > Actions**.
3. Ajoutez deux "Repository secrets" :
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
4. L'action s'exécutera automatiquement selon le cron, ou vous pouvez la lancer manuellement depuis l'onglet **Actions**.

*(Le workflow est configuré pour commit et push automatiquement la base de données `missions.db` afin de garder la mémoire des missions déjà vues entre les exécutions).*
