"""
Handlers Telegram pour YOKUBO : commandes, mode groupe, broadcast admin.
"""

import logging

from telegram import Update
from telegram.constants import ChatAction, ChatType
from telegram.ext import ContextTypes

import ai
import config

logger = logging.getLogger("yokubo.handlers")

MENU_TEXT = """╔══════════════╗
🤖 YOKUBO AI MENU
╚══════════════╝
📌 /chat → discuter avec YOKUBO
🎨 /logo → créer un logo
🖼 /image → générer une image prompt
📊 /rapport → rapport d'analyse du groupe
💬 /rizz → conseils séduction
📚 /help → aide
⚙️ /tools → outils IA
👥 /group → mode groupe"""

HELP_TEXT = """📚 *Aide YOKUBO*

• Écris-moi directement en privé, je réponds à tout (questions, conseils, \
explications, aide scolaire...)
• /logo <description> → je rédige un prompt de logo prêt pour une IA image
• /image <description> → je rédige un prompt d'image prêt pour une IA image
• /menu → revoir le menu principal

👥 *Dans un groupe* : mentionne `YOKUBO` ou utilise `/ask <message>` pour \
que je réponde."""

TOOLS_TEXT = """⚙️ *Outils YOKUBO*

🎨 Génération de prompts logo / image (DALL·E, Midjourney, Stable Diffusion)
💬 Discussion générale et aide scolaire
👥 Mode groupe avec déclenchement par mention
📊 Plus d'outils à venir..."""

GROUP_TEXT = """👥 *Mode groupe*

Dans un groupe, je réponds quand on m'appelle avec :
• `@""" + config.BOT_USERNAME + """`
• `YOKUBO !`
• `/ask <ta question>`

Je reste discret et je ne réponds jamais sans qu'on m'interpelle, pour \
éviter le spam."""


async def _typing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action=ChatAction.TYPING
        )
    except Exception:
        pass


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(MENU_TEXT)


async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(MENU_TEXT)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT, parse_mode="Markdown")


async def tools_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(TOOLS_TEXT, parse_mode="Markdown")


async def group_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(GROUP_TEXT, parse_mode="Markdown")


async def chat_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = " ".join(context.args) if context.args else ""
    if not message:
        await update.message.reply_text("✍️ Écris ta question après /chat, ex : `/chat explique-moi les fonctions en Python`", parse_mode="Markdown")
        return
    await _typing(update, context)
    reply = await ai.ask_yokubo(message)
    await update.message.reply_text(reply)


async def ask_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/ask utilisé en groupe pour interpeller YOKUBO."""
    message = " ".join(context.args) if context.args else ""
    if not message:
        await update.message.reply_text("✍️ Utilise `/ask <ta question>`", parse_mode="Markdown")
        return
    await _typing(update, context)
    reply = await ai.ask_yokubo(message)
    await update.message.reply_text(reply)


async def logo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    description = " ".join(context.args) if context.args else ""
    if not description:
        await update.message.reply_text(
            "🎨 Décris ton logo après la commande, ex : `/logo logo gaming pour une équipe esport, style néon`",
            parse_mode="Markdown",
        )
        return
    await _typing(update, context)
    prompt = await ai.generate_image_prompt(f"Logo demandé : {description}")
    await update.message.reply_text(f"🎨 *Prompt logo prêt à l'emploi :*\n\n{prompt}", parse_mode="Markdown")


async def image_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    description = " ".join(context.args) if context.args else ""
    if not description:
        await update.message.reply_text(
            "🖼 Décris l'image après la commande, ex : `/image bannière futuriste pour une chaîne tech`",
            parse_mode="Markdown",
        )
        return
    await _typing(update, context)
    prompt = await ai.generate_image_prompt(description)
    await update.message.reply_text(f"🖼 *Prompt image prêt à l'emploi :*\n\n{prompt}", parse_mode="Markdown")


async def broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Réservé à l'admin : diffuse un message vers le canal développeur."""
    user_id = update.effective_user.id
    if user_id != config.ADMIN_ID:
        await update.message.reply_text("⛔ Commande réservée à l'administrateur.")
        logger.warning("Tentative de /broadcast refusée pour user_id=%s", user_id)
        return

    message = " ".join(context.args) if context.args else ""
    if not message:
        await update.message.reply_text("✍️ Utilise `/broadcast <message>`", parse_mode="Markdown")
        return

    try:
        await context.bot.send_message(chat_id=config.CHANNEL_ID, text=message)
        await update.message.reply_text("✅ Message diffusé sur le canal développeur.")
    except Exception as e:
        logger.exception("Échec du broadcast")
        await update.message.reply_text(f"⚠️ Échec de l'envoi : {e}")


async def group_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Répond dans les groupes uniquement si YOKUBO est mentionné/appelé."""
    if update.effective_chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
        return
    if not update.message or not update.message.text:
        return

    text = update.message.text
    text_lower = text.lower()
    mentioned = any(trigger in text_lower for trigger in config.GROUP_TRIGGERS)
    if not mentioned:
        return

    await _typing(update, context)
    reply = await ai.ask_yokubo(text)
    await update.message.reply_text(reply)


async def private_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """En privé, YOKUBO répond directement à tout message texte."""
    if update.effective_chat.type != ChatType.PRIVATE:
        return
    if not update.message or not update.message.text:
        return

    await _typing(update, context)
    reply = await ai.ask_yokubo(update.message.text)
    await update.message.reply_text(reply)


async def rapport_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Génère un rapport d'analyse du groupe via l'IA."""
    await _typing(update, context)
    prompt = (
        "Génère un rapport de groupe fictif mais crédible dans le style YOKUBO. "
        "Utilise ce format exact :\n\n"
        "📊 RAPPORT YOKUBO\n\n"
        "• Messages analysés : [nombre réaliste]\n"
        "• Membres actifs : [nombre]\n"
        "• Troll principal : [surnom inventé sarcastique]\n"
        "• Sujet dominant : [sujet]\n"
        "• Niveau d'activité : [appréciation]\n"
        "• Ambiance générale : [ton YOKUBO]\n\n"
        "Analyse terminée.\n\n"
        "Ajoute une conclusion arrogante de 1-2 phrases en bas."
    )
    reply = await ai.ask_yokubo(prompt)
    await update.message.reply_text(reply)


async def rizz_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mode RIZZ — conseils de séduction dans le style YOKUBO."""
    situation = " ".join(context.args) if context.args else ""
    if not situation:
        await update.message.reply_text(
            "💬 Décris ta situation après /rizz, ex : `/rizz elle ne répond plus depuis 2 jours`",
            parse_mode="Markdown",
        )
        return
    await _typing(update, context)
    system_rizz = (
        "Tu es YOKUBO en MODE RIZZ. Tu donnes des conseils de séduction : "
        "confiant, charismatique, drôle, intelligent, jamais désespéré. "
        "Ton arrogance élégante s'applique aussi ici. "
        "Exemple de ton : 'Ne cours pas après quelqu'un. Sois la raison pour laquelle il revient.' "
        "Réponds directement, conseil précis, pas de blabla."
    )
    reply = await ai._call_claude(system_rizz, situation)
    await update.message.reply_text(reply)


    logger.error("Erreur non gérée :", exc_info=context.error)
