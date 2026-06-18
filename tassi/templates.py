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
        "ask_operator": (
            "💳 Tassi Plus — *{price_xaf} XAF/mois*\n\n"
            "Vous recevrez des rappels de déclaration et accèderez à votre historique.\n\n"
            "Choisissez votre opérateur :\n"
            "1️⃣ MTN MoMo\n"
            "2️⃣ Orange Money"
        ),
        "already_subscribed": "✅ Vous êtes déjà abonné à Tassi Plus.",
        "subscribe_initiated": (
            "⏳ Paiement en cours. Vérifiez votre téléphone pour le prompt USSD.\n"
            "Envoyez *STATUS* pour vérifier l'état."
        ),
        "subscribe_error": (
            "❌ Impossible d'initier le paiement pour le moment. Réessayez plus tard."
        ),
        "payment_confirmed": (
            "🎉 Paiement confirmé ! Vous êtes maintenant abonné à *Tassi Plus*.\n"
            "Envoyez *HISTORY* pour voir votre historique."
        ),
        "payment_failed": (
            "❌ Paiement échoué. Envoyez *SUBSCRIBE* pour réessayer."
        ),
        "payment_pending": (
            "⏳ Votre paiement est encore en cours. Réessayez *STATUS* dans quelques minutes."
        ),
        "payment_just_initiated": (
            "⏳ Paiement tout juste lancé. Attendez un moment puis envoyez *STATUS*."
        ),
        "no_pending_payment": (
            "Aucun paiement en attente trouvé. Envoyez *SUBSCRIBE* pour vous abonner."
        ),
        "history_not_plus": (
            "📊 L'historique est réservé aux abonnés *Tassi Plus*.\n"
            "Envoyez *SUBSCRIBE* pour vous abonner."
        ),
        "history_empty": "Aucun calcul enregistré pour ce compte.",
        "history_result": "{history_text}",
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
        "ask_operator": (
            "💳 Tassi Plus — *{price_xaf} XAF/month*\n\n"
            "Get filing reminders and access 12 months of history.\n\n"
            "Choose your operator:\n"
            "1️⃣ MTN MoMo\n"
            "2️⃣ Orange Money"
        ),
        "already_subscribed": "✅ You are already a Tassi Plus subscriber.",
        "subscribe_initiated": (
            "⏳ Payment in progress. Check your phone for the USSD prompt.\n"
            "Send *STATUS* to check the payment status."
        ),
        "subscribe_error": (
            "❌ Could not initiate payment right now. Please try again later."
        ),
        "payment_confirmed": (
            "🎉 Payment confirmed! You are now a *Tassi Plus* subscriber.\n"
            "Send *HISTORY* to view your filing history."
        ),
        "payment_failed": (
            "❌ Payment failed. Send *SUBSCRIBE* to try again."
        ),
        "payment_pending": (
            "⏳ Your payment is still processing. Try *STATUS* again in a few minutes."
        ),
        "payment_just_initiated": (
            "⏳ Payment just started. Wait a moment then send *STATUS*."
        ),
        "no_pending_payment": (
            "No pending payment found. Send *SUBSCRIBE* to subscribe."
        ),
        "history_not_plus": (
            "📊 Filing history is for *Tassi Plus* subscribers.\n"
            "Send *SUBSCRIBE* to join."
        ),
        "history_empty": "No calculations recorded for this account.",
        "history_result": "{history_text}",
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
            " Good! How much money you make dis month?\n" "_(E.g. 2 350 000 frs, 2.350.000)_"
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
        "ask_operator": (
            "💳 Tassi Plus — *{price_xaf} XAF/month*\n\n"
            "You go get reminder wey go tell you when to file, plus 12 months history.\n\n"
            "Pick your operator:\n"
            "1️⃣ MTN MoMo\n"
            "2️⃣ Orange Money"
        ),
        "already_subscribed": "✅ You don already subscribe for Tassi Plus.",
        "subscribe_initiated": (
            "⏳ Payment don start. Check your phone for USSD prompt.\n"
            "Send *STATUS* to check am."
        ),
        "subscribe_error": (
            "❌ We no fit start payment now. Abeg try again later."
        ),
        "payment_confirmed": (
            "🎉 Payment don confirm! You don join *Tassi Plus*.\n"
            "Send *HISTORY* to see your history."
        ),
        "payment_failed": (
            "❌ Payment fail. Send *SUBSCRIBE* to try again."
        ),
        "payment_pending": (
            "⏳ Your payment still dey process. Try *STATUS* again for few minutes."
        ),
        "payment_just_initiated": (
            "⏳ Payment just start. Wait small then send *STATUS*."
        ),
        "no_pending_payment": (
            "No pending payment dey. Send *SUBSCRIBE* to join."
        ),
        "history_not_plus": (
            "📊 History na for *Tassi Plus* subscribers only.\n"
            "Send *SUBSCRIBE* to join."
        ),
        "history_empty": "No calculation dey for dis account yet.",
        "history_result": "{history_text}",
    },
}

_REQUIRED_KEYS: Final = frozenset(MESSAGES["fr"].keys())


def get_message(language: str, key: str, **kwargs: str) -> str:
    """Return a formatted message string. Falls back to French for unknown languages."""
    lang = language if language in MESSAGES else "fr"
    template = MESSAGES[lang][key]
    return template.format(**kwargs) if kwargs else template
