"""Tests for tassi.chat — handle_message stub (Milestone 3)."""

from tassi.chat import handle_message
from tassi.config import Settings


class TestHandleMessage:
    async def test_handle_message_runs_without_error(self) -> None:
        cfg = Settings(environment="test")
        await handle_message({"id": "wamid.test001", "from": "237600000000"}, cfg)

    async def test_handle_message_missing_id_does_not_raise(self) -> None:
        cfg = Settings(environment="test")
        await handle_message({}, cfg)
