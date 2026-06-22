# 🤖 YOKUBO — Bot Telegram

Assistant IA Telegram (FR/EN), avec mode groupe, génération de prompts
logo/image, et commande `/broadcast` réservée à l'administrateur.

## 📁 Contenu

```
yokubo-bot/
├── main.py            # point d'entrée
├── handlers.py         # commandes et logique des messages
├── ai.py                # appels à l'API Anthropic (Claude)
├── config.py            # configuration via variables d'environnement
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── .gitignore / .dockerignore
```

## ⚙️ Configuration

1. Copie `.env.example` en `.env` :
   ```bash
   cp .env.example .env
   ```
2. Remplis les valeurs dans `.env` :
   - `TELEGRAM_BOT_TOKEN` → crée un bot via [@BotFather](https://t.me/BotFather)
     et récupère le token.
   - `ANTHROPIC_API_KEY` → clé API depuis [console.anthropic.com](https://console.anthropic.com)
   - `ADMIN_ID` → déjà pré-rempli à `8305367220`
   - `CHANNEL_ID` → déjà pré-rempli à `-1004390236547` (canal développeur)

⚠️ Le bot doit être **ajouté comme administrateur** du canal/groupe
développeur pour pouvoir y poster via `/broadcast`.

## 🚀 Lancer avec Docker

```bash
docker compose up -d --build
```

Ou sans docker-compose :

```bash
docker build -t yokubo-bot .
docker run -d --name yokubo-bot --env-file .env yokubo-bot
```

## 🐍 Lancer sans Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export $(cat .env | xargs)   # charge les variables d'environnement
python main.py
```

## 💬 Commandes disponibles

| Commande | Description |
|---|---|
| `/start`, `/menu` | Affiche le menu principal |
| `/chat <message>` | Discuter avec YOKUBO |
| `/logo <description>` | Génère un prompt de logo prêt pour une IA image |
| `/image <description>` | Génère un prompt d'image prêt pour une IA image |
| `/help` | Aide |
| `/tools` | Liste des outils IA |
| `/group` | Explique le mode groupe |
| `/ask <message>` | Pour interpeller YOKUBO dans un groupe |
| `/broadcast <message>` | **Admin uniquement** — diffuse un message sur le canal développeur |

## 👥 Mode groupe

Dans un groupe, YOKUBO répond uniquement quand on le mentionne
(`YOKUBO`, `@YOKUBO`) ou via `/ask`, pour éviter le spam.

## 🔒 Sécurité

- Le token du bot et la clé API ne sont jamais codés en dur : ils viennent
  des variables d'environnement (`.env`, non commité).
- `/broadcast` vérifie l'ID Telegram de l'expéditeur contre `ADMIN_ID`
  avant toute action.
- Le conteneur Docker tourne avec un utilisateur non-root.

## 📝 Notes

- Le bot utilise [python-telegram-bot](https://docs.python-telegram-bot.org/)
  (polling, pas de webhook — suffisant pour un déploiement simple).
- Les réponses sont générées via l'API Anthropic (modèle Claude). YOKUBO
  ne génère pas d'image directement : pour `/logo` et `/image`, il rédige
  un prompt prêt à coller dans un outil comme Midjourney ou DALL·E.
