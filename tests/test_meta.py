"""Tests for tassi.meta — send_text_message (mocked httpx, no real HTTP)."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from tassi.meta import send_text_message

_PHONE_ID = "test-phone-id"
_TOKEN = "test-access-token"
_RECIPIENT = "237600000001"
_TEXT = "Hello from Tassi"


def _mock_client(status_code: int) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.raise_for_status = MagicMock(
        side_effect=(
            None
            if status_code < 400
            else httpx.HTTPStatusError("error", request=MagicMock(), response=resp)
        )
    )
    client = AsyncMock()
    client.post = AsyncMock(return_value=resp)
    client.__aenter__ = AsyncMock(return_value=client)
    client.__aexit__ = AsyncMock(return_value=False)
    return client


class TestSendTextMessage:
    async def test_success_does_not_raise(self) -> None:
        with patch("tassi.meta.httpx.AsyncClient", return_value=_mock_client(200)):
            await send_text_message(_PHONE_ID, _TOKEN, _RECIPIENT, _TEXT)

    async def test_http_error_raises(self) -> None:
        with patch("tassi.meta.httpx.AsyncClient", return_value=_mock_client(400)):
            with pytest.raises(httpx.HTTPStatusError):
                await send_text_message(_PHONE_ID, _TOKEN, _RECIPIENT, _TEXT)
