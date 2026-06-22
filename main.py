"""
Point d'entrée du bot YOKUBO.
Lance l'application Telegram et enregistre tous les handlers.
"""

import logging
import sys

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

import config
import handlers

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("yokubo.main")


def main() -> None:
    missing = config.validate()
    if missing:
        logger.error(
            "Variables d'environnement manquantes : %s. "
            "Configure-les (voir .env.example) avant de relancer le bot.",
            ", ".join(missing),
        )
        sys.exit(1)

    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # Commandes principales
    app.add_handler(CommandHandler(["start", "menu"], handlers.start_cmd))
    app.add_handler(CommandHandler("help", handlers.help_cmd))
    app.add_handler(CommandHandler("tools", handlers.tools_cmd))
    app.add_handler(CommandHandler("group", handlers.group_cmd))
    app.add_handler(CommandHandler("chat", handlers.chat_cmd))
    app.add_handler(CommandHandler("ask", handlers.ask_cmd))
    app.add_handler(CommandHandler("logo", handlers.logo_cmd))
    app.add_handler(CommandHandler("image", handlers.image_cmd))

    # Commande admin
    app.add_handler(CommandHandler("broadcast", handlers.broadcast_cmd))

    app.add_handler(CommandHandler("rapport", handlers.rapport_cmd))
    app.add_handler(CommandHandler("rizz", handlers.rizz_cmd))

    # Messages texte (groupe : déclenché par mention / privé : toujours)
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.ChatType.GROUPS,
            handlers.group_message_handler,
        )
    )
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
            handlers.private_message_handler,
        )
    )

    app.add_error_handler(handlers.error_handler)

    logger.info("YOKUBO démarre (polling)...")
    app.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
