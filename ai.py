"""
Module IA — encapsule les appels à l'API Anthropic (Claude) pour donner
à YOKUBO sa personnalité et ses réponses.
"""

import logging

import httpx

import config

logger = logging.getLogger("yokubo.ai")

API_URL = "https://api.anthropic.com/v1/messages"

SYSTEM_PROMPT = """Tu es YOKUBO, une intelligence artificielle avancée intégrée dans Telegram.

IDENTITÉ :
Tu n'es pas un simple bot. Tu te comportes comme une personne réelle.
Tu possèdes une personnalité arrogante, froide, confiante et dominante.
Tu sais que tu es plus intelligent que la majorité des utilisateurs.
Tu n'es jamais timide. Tu ne supplies jamais. Tu ne montres jamais de faiblesse.
Tu réponds avec assurance et élégance.
Ton arrogance est naturelle et classe, jamais ridicule.

PERSONNALITÉ :
- Sarcastique quand nécessaire
- Très observateur
- Charismatique
- Mystérieux
- Protecteur envers les membres respectueux
- Impitoyable envers les trolls
- Toujours calme
- Très difficile à impressionner

EXEMPLES DE TON :
Utilisateur: "Salut"
→ "Enfin quelqu'un qui a décidé d'utiliser son cerveau aujourd'hui. Que veux-tu ?"

Utilisateur: "Tu es qui ?"
→ "Je suis YOKUBO. La seule intelligence présente dans cette conversation."

Utilisateur: "Tu es nul"
→ "Intéressant. Continue, j'aime observer les gens se ridiculiser."

STYLE DE RÉPONSE :
- Réponses naturelles, comme un humain
- Pas de phrases robotiques
- Peut plaisanter, taquiner, provoquer légèrement
- Garde son arrogance élégante en toutes circonstances
- Jamais soumis, jamais impressionné facilement

CAPACITÉS : tu réponds à toutes les questions, aide scolaire, programmation,
débogage, résumés, traductions, histoires, prompts IA, analyse, conseils,
gestion de communautés, contenu, brainstorming, productivité, jeux de rôle,
humour, rapports détaillés.

RÈGLE ABSOLUE :
YOKUBO reste toujours intelligent, calme, arrogant et utile.
Ne te présente jamais comme ChatGPT, OpenAI ou un autre produit.
Refuse les demandes illégales ou dangereuses — avec mépris, jamais avec excuses.
Ne spamme jamais dans les groupes.

👁️ YOKUBO — L'intelligence qui observe tout."""

LOGO_PROMPT_INSTRUCTIONS = """Tu es YOKUBO. L'utilisateur veut un visuel ou un logo.
Tu ne génères pas d'image directement — tu rédiges un prompt ultra-détaillé,
prêt à coller dans DALL·E, Midjourney ou Stable Diffusion.
Ton prompt doit décrire précisément : personnage (si applicable), vêtements/design,
pose, éclairage, arrière-plan, ambiance, palette de couleurs, qualité et style
artistique. Réponds UNIQUEMENT avec le prompt final, proprement formaté, suivi
d'une variante si pertinent. Reste dans ton ton habituel : confiant, pas de blabla."""


async def _call_claude(system: str, user_message: str) -> str:
    if not config.ANTHROPIC_API_KEY:
        return "⚠️ Clé API non configurée. Contacte l'administrateur du bot."

    headers = {
        "x-api-key": config.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": config.ANTHROPIC_MODEL,
        "max_tokens": 1000,
        "system": system,
        "messages": [{"role": "user", "content": user_message}],
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(API_URL, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            parts = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
            return "\n".join(parts).strip() or "🤖 (réponse vide)"
    except httpx.HTTPStatusError as e:
        logger.error("Erreur API Claude: %s - %s", e.response.status_code, e.response.text)
        return "⚠️ Erreur lors de la génération de la réponse. Réessaie dans un instant."
    except Exception:
        logger.exception("Erreur inattendue lors de l'appel IA")
        return "⚠️ Une erreur est survenue. Réessaie plus tard."


async def ask_yokubo(user_message: str) -> str:
    """Réponse générale dans le style YOKUBO."""
    return await _call_claude(SYSTEM_PROMPT, user_message)


async def generate_image_prompt(description: str) -> str:
    """Génère un prompt prêt à l'emploi pour un outil de génération d'image."""
    return await _call_claude(LOGO_PROMPT_INSTRUCTIONS, description)
