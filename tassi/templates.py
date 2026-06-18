"""
All bot message text in one place. No string literals in chat.py.
Structure: MESSAGES[language][key] = text
NFR-USE-1: every key must exist in all three supported languages (fr, en, pcm).
"""

from typing import Final

MESSAGES: Final[dict[str, dict[str, str]]] = {
    "fr": {
        "ask_language": (
            "👋 Bienvenue sur *Tassi* — votre assistant fiscal RSI.\n\n"
            "Choisissez votre langue / Choose your language / Choisir langue:\n"
            "1️⃣ Français\n"
            "2️⃣ English\n"
            "3️⃣ Pidgin"
        ),
        "ask_revenue_band": (
            "Quelle est votre chiffre d'affaires annuel approximatif ?\n\n"
            "1️⃣ Entre 10 M et 20 M XAF\n"
            "2️⃣ Entre 20 M et 30 M XAF\n"
            "3️⃣ Entre 30 M et 40 M XAF\n"
            "4️⃣ Entre 40 M et 50 M XAF\n\n"
            "_(Tapez 1, 2, 3 ou 4)_"
        ),
        "out_of_band": (
            "⚠️ Tassi prend en charge uniquement le Régime Simplifié d'Imposition (RSI), "
            "pour un chiffre d'affaires annuel entre *10 M et 50 M XAF*.\n\n"
            "Votre tranche n'est pas encore couverte. Retapez votre tranche (1-4) si vous "
            "êtes en RSI, ou contactez un comptable pour votre régime."
        ),
        "out_of_band_final": (
            "Nous ne pouvons pas vous aider pour ce régime pour le moment. "
            "Contactez un comptable agréé pour plus d'informations."
        ),
        "ask_revenue": (
            "✅ Parfait ! Quel est votre chiffre d'affaires du mois en cours ?\n"
            "_(Ex : 2 350 000 frs, 2.350.000, 2,350,000)_"
        ),
        "zero_return_guidance": (
            "*Déclaration Néant*\n\n"
            "Vous n'avez pas de chiffre d'affaires ce mois-ci. "
            "Déposez une *Déclaration Néant* auprès du Centre des Impôts avant le 15 du mois.\n\n"
            "Aucun paiement n'est dû."
        ),
        "calculation_result": "{tax_result}",
        "invalid_input": (
            "❌ Je n'ai pas reconnu ce montant. Veuillez entrer votre chiffre d'affaires "
            "en chiffres.\n_(Ex : 2 350 000 ou 2350000)_"
        ),
        "resend_no_history": (
            "Aucun calcul trouvé pour ce mois-ci. "
            "Envoyez votre chiffre d'affaires pour commencer."
        ),
        "resend_result": "Voici votre dernier calcul :\n\n{tax_result}",
    },
    "en": {
        "ask_language": (
            "👋 Welcome to *Tassi* — your RSI tax assistant.\n\n"
            "Choose your language / Choisissez votre langue / Choisir langue:\n"
            "1️⃣ Français\n"
            "2️⃣ English\n"
            "3️⃣ Pidgin"
        ),
        "ask_revenue_band": (
            "What is your approximate annual revenue?\n\n"
            "1️⃣ Between 10 M and 20 M XAF\n"
            "2️⃣ Between 20 M and 30 M XAF\n"
            "3️⃣ Between 30 M and 40 M XAF\n"
            "4️⃣ Between 40 M and 50 M XAF\n\n"
            "_(Type 1, 2, 3 or 4)_"
        ),
        "out_of_band": (
            "⚠️ Tassi only supports the Simplified Tax Regime (RSI) for annual revenues "
            "between *10 M and 50 M XAF*.\n\n"
            "Your range is not yet covered. Re-enter your band (1-4) if you are RSI, "
            "or contact an accountant for your tax regime."
        ),
        "out_of_band_final": (
            "We cannot help with your tax regime at this time. "
            "Please contact a certified accountant for more information."
        ),
        "ask_revenue": (
            "✅ Great! What is your revenue for the current month?\n"
            "_(E.g. 2 350 000 frs, 2.350.000, 2,350,000)_"
        ),
        "zero_return_guidance": (
            "*Nil Return (Déclaration Néant)*\n\n"
            "You have no revenue this month. "
            "File a *Nil Return* at your Tax Centre before the 15th of the month.\n\n"
            "No payment is due."
        ),
        "calculation_result": "{tax_result}",
        "invalid_input": (
            "❌ I didn't recognise that amount. Please enter your revenue in numbers.\n"
            "_(E.g. 2 350 000 or 2350000)_"
        ),
        "resend_no_history": (
            "No calculation found for this month. " "Send your revenue to get started."
        ),
        "resend_result": "Here is your last calculation:\n\n{tax_result}",
    },
    "pcm": {
        "ask_language": (
            "👋 Welcome for *Tassi* — e go help you calculate your RSI tax.\n\n"
            "Pick your language / Choisissez votre langue:\n"
            "1️⃣ Français\n"
            "2️⃣ English\n"
            "3️⃣ Pidgin"
        ),
        "ask_revenue_band": (
            "How much money you dey make for one year (approximate)?\n\n"
            "1️⃣ 10 M to 20 M XAF\n"
            "2️⃣ 20 M to 30 M XAF\n"
            "3️⃣ 30 M to 40 M XAF\n"
            "4️⃣ 40 M to 50 M XAF\n\n"
            "_(Type 1, 2, 3 or 4)_"
        ),
        "out_of_band": (
            "⚠️ Tassi only fit help people wey dey make between "
            "*10 M and 50 M XAF* for year (RSI).\n\n"
            "Your money no dey inside dis range. Type 1-4 if you dey RSI, "
            "or abeg call one accountant for your own tax."
        ),
        "out_of_band_final": (
            "We no fit help you for your tax now. " "Abeg find one good accountant wey go help you."
        ),
        "ask_revenue": (
            "✅ Good! How much money you make dis month?\n" "_(E.g. 2 350 000 frs, 2.350.000)_"
        ),
        "zero_return_guidance": (
            "*Déclaration Néant*\n\n"
            "You no make money dis month. "
            "You must go submit *Déclaration Néant* for Tax Centre before 15 of dis month.\n\n"
            "You no go pay anything."
        ),
        "calculation_result": "{tax_result}",
        "invalid_input": (
            "❌ I no understand dat amount. Abeg type your money as number.\n"
            "_(E.g. 2 350 000 or 2350000)_"
        ),
        "resend_no_history": (
            "No calculation dey for dis month. " "Send your money wey you make to start."
        ),
        "resend_result": "Na dis your last calculation:\n\n{tax_result}",
    },
}

_REQUIRED_KEYS: Final = frozenset(MESSAGES["fr"].keys())


def get_message(language: str, key: str, **kwargs: str) -> str:
    """Return a formatted message string. Falls back to French for unknown languages."""
    lang = language if language in MESSAGES else "fr"
    template = MESSAGES[lang][key]
    return template.format(**kwargs) if kwargs else template
