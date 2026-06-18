import logging

from tassi.config import Settings

_log = logging.getLogger(__name__)


async def handle_message(message: dict[str, object], _cfg: Settings) -> None:
    """
    Process a single inbound WhatsApp message.
    Milestone 3: stub only — logs the message ID.
    Full conversation logic is implemented in Milestone 4.
    """
    message_id = message.get("id", "<unknown>")
    _log.info("handle_message called for message_id=%s", message_id)
