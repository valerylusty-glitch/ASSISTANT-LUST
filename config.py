"""
Configuration centrale du bot YOKUBO.
Toutes les valeurs sensibles (tokens, clés API) sont lues depuis les
variables d'environnement — jamais codées en dur dans le code source.
"""

import os

# --- Telegram ---
BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
BOT_USERNAME: str = os.getenv("BOT_USERNAME", "YOKUBO")  # sans le @

# --- Administration ---
# ID de l'admin autorisé à utiliser /broadcast
ADMIN_ID: int = int(os.getenv("ADMIN_ID", "8305367220"))

# Canal/groupe développeur où /broadcast envoie ses messages par défaut
# (format Telegram : -100xxxxxxxxxx pour un canal/supergroupe)
CHANNEL_ID: int = int(os.getenv("CHANNEL_ID", "-1004390236547"))

# --- IA (Anthropic Claude API) ---
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

# --- Comportement ---
# Mots-clés qui déclenchent une réponse de YOKUBO dans un groupe
GROUP_TRIGGERS = ["yokubo"]


def validate() -> list[str]:
    """Retourne la liste des variables obligatoires manquantes."""
    missing = []
    if not BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not ANTHROPIC_API_KEY:
        missing.append("ANTHROPIC_API_KEY")
    return missing
