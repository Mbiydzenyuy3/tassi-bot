import logging

import httpx

_log = logging.getLogger(__name__)

_META_API_URL = "https://graph.facebook.com/v19.0/{phone_number_id}/messages"


async def send_text_message(
    phone_number_id: str,
    access_token: str,
    recipient_msisdn: str,
    text: str,
) -> None:
    """
    Send a text message via WhatsApp Cloud API.
    Uses a fresh httpx.AsyncClient per call (context manager — no module-level globals).
    Raises httpx.HTTPStatusError on non-2xx. Caller (BackgroundTasks) logs the error.
    NFR-PERF-2: always called from BackgroundTasks, never from the ack path.
    """
    url = _META_API_URL.format(phone_number_id=phone_number_id)
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_msisdn,
        "type": "text",
        "text": {"body": text},
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10.0,
        )
        resp.raise_for_status()
        _log.info("message sent to %s (status %s)", recipient_msisdn, resp.status_code)
