"""Tests for tassi.meta — send_text_message (mocked httpx, no real HTTP)."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from tassi.meta import mark_as_read, send_text_message, send_typing_indicator

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


_MSG_ID = "wamid.HBgLMjM3NjAwMDAwMDAxFQIAERgSM"


class TestSendTextMessage:
    async def test_success_does_not_raise(self) -> None:
        with patch("tassi.meta.httpx.AsyncClient", return_value=_mock_client(200)):
            await send_text_message(_PHONE_ID, _TOKEN, _RECIPIENT, _TEXT)

    async def test_http_error_raises(self) -> None:
        with patch("tassi.meta.httpx.AsyncClient", return_value=_mock_client(400)):
            with pytest.raises(httpx.HTTPStatusError):
                await send_text_message(_PHONE_ID, _TOKEN, _RECIPIENT, _TEXT)


class TestMarkAsRead:
    async def test_sends_correct_payload(self) -> None:
        client = _mock_client(200)
        with patch("tassi.meta.httpx.AsyncClient", return_value=client):
            await mark_as_read(_PHONE_ID, _TOKEN, _MSG_ID)

        client.post.assert_called_once()
        call_kwargs = client.post.call_args
        assert call_kwargs.kwargs["json"] == {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": _MSG_ID,
        }
        assert call_kwargs.kwargs["headers"] == {"Authorization": f"Bearer {_TOKEN}"}
        assert "test-phone-id/messages" in call_kwargs.args[0]

    async def test_raises_on_non_2xx(self) -> None:
        with patch("tassi.meta.httpx.AsyncClient", return_value=_mock_client(400)):
            with pytest.raises(httpx.HTTPStatusError):
                await mark_as_read(_PHONE_ID, _TOKEN, _MSG_ID)


_TYPING_MSG_ID = "wamid.test001"


class TestSendTypingIndicator:
    async def test_sends_correct_payload(self) -> None:
        client = _mock_client(200)
        with patch("tassi.meta.httpx.AsyncClient", return_value=client):
            await send_typing_indicator(_PHONE_ID, _TOKEN, _RECIPIENT, _TYPING_MSG_ID)

        client.post.assert_called_once()
        call_kwargs = client.post.call_args
        captured_payload = call_kwargs.kwargs["json"]
        assert captured_payload["messaging_product"] == "whatsapp"
        assert captured_payload["to"] == _RECIPIENT
        assert captured_payload["message_id"] == _TYPING_MSG_ID
        assert "typing_indicator" in captured_payload
        assert "type" not in captured_payload
        assert call_kwargs.kwargs["headers"] == {"Authorization": f"Bearer {_TOKEN}"}
        assert "test-phone-id/messages" in call_kwargs.args[0]

    async def test_raises_on_non_2xx(self) -> None:
        with patch("tassi.meta.httpx.AsyncClient", return_value=_mock_client(500)):
            with pytest.raises(httpx.HTTPStatusError):
                await send_typing_indicator(_PHONE_ID, _TOKEN, _RECIPIENT, _TYPING_MSG_ID)
