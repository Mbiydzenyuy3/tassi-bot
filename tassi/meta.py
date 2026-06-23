import logging

import httpx

_log = logging.getLogger(__name__)

_META_API_URL = "https://graph.facebook.com/v22.0/{phone_number_id}/messages"


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


async def mark_as_read(
    phone_number_id: str,
    access_token: str,
    message_id: str,
) -> None:
    """
    Mark an incoming message as read (turns double-grey ticks to blue).
    Raises httpx.HTTPStatusError on non-2xx. Caller handles best-effort wrapping.
    """
    url = _META_API_URL.format(phone_number_id=phone_number_id)
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10.0,
        )
        resp.raise_for_status()


async def send_typing_indicator(
    phone_number_id: str,
    access_token: str,
    recipient_msisdn: str,
    message_id: str,
) -> None:
    """
    Show the three-dot typing animation to the recipient.
    Uses the WhatsApp Cloud API typing_indicator status operation (requires v21.0+).
    message_id must be the wamid of the inbound message being replied to.
    Raises httpx.HTTPStatusError on non-2xx. Caller handles best-effort wrapping.
    """
    url = _META_API_URL.format(phone_number_id=phone_number_id)
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_msisdn,
        "message_id": message_id,
        "typing_indicator": {"type": "text"},
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10.0,
        )
        resp.raise_for_status()
        _log.info("typing indicator sent to %s", recipient_msisdn)
