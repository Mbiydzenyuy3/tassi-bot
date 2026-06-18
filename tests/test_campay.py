"""Tests for tassi.campay — mocked httpx, no real Campay calls."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from tassi.campay import get_transaction_status, initiate_ussd_push

_USER = "campay-user"
_PASS = "campay-pass"
_APP_TOKEN = "campay-app-token"
_MSISDN = "237600000001"
_REFERENCE = "CPY-REF-001"


def _mock_response(status_code: int, json_body: dict) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.json.return_value = json_body
    resp.raise_for_status = MagicMock(
        side_effect=(
            None
            if status_code < 400
            else httpx.HTTPStatusError("error", request=MagicMock(), response=resp)
        )
    )
    return resp


def _mock_client(*responses: MagicMock) -> MagicMock:
    client = AsyncMock()
    client.post = AsyncMock(side_effect=list(responses))
    client.get = AsyncMock(side_effect=list(responses))
    client.__aenter__ = AsyncMock(return_value=client)
    client.__aexit__ = AsyncMock(return_value=False)
    return client


class TestInitiateUssdPush:
    async def test_success_returns_reference(self) -> None:
        token_resp = _mock_response(200, {"token": "jwt-token"})
        collect_resp = _mock_response(200, {"reference": _REFERENCE})

        token_client = _mock_client(token_resp)
        collect_client = _mock_client(collect_resp)

        with patch(
            "tassi.campay.httpx.AsyncClient",
            side_effect=[token_client, collect_client],
        ):
            ref = await initiate_ussd_push(
                _USER, _PASS, _APP_TOKEN, 500, _MSISDN, "Tassi Plus", "ext-001"
            )

        assert ref == _REFERENCE

    async def test_http_error_on_token_raises(self) -> None:
        error_resp = _mock_response(401, {"detail": "unauthorized"})
        client = _mock_client(error_resp)

        with patch("tassi.campay.httpx.AsyncClient", return_value=client):
            with pytest.raises(httpx.HTTPStatusError):
                await initiate_ussd_push(
                    _USER, _PASS, _APP_TOKEN, 500, _MSISDN, "Tassi Plus", "ext-001"
                )

    async def test_http_error_on_collect_raises(self) -> None:
        token_resp = _mock_response(200, {"token": "jwt-token"})
        error_resp = _mock_response(400, {"detail": "bad request"})

        token_client = _mock_client(token_resp)
        collect_client = _mock_client(error_resp)

        with patch(
            "tassi.campay.httpx.AsyncClient",
            side_effect=[token_client, collect_client],
        ):
            with pytest.raises(httpx.HTTPStatusError):
                await initiate_ussd_push(
                    _USER, _PASS, _APP_TOKEN, 500, _MSISDN, "Tassi Plus", "ext-001"
                )


class TestGetTransactionStatus:
    async def test_successful_normalised_to_success(self) -> None:
        resp = _mock_response(200, {"status": "SUCCESSFUL"})
        client = _mock_client(resp)

        with patch("tassi.campay.httpx.AsyncClient", return_value=client):
            status = await get_transaction_status(_APP_TOKEN, _REFERENCE)

        assert status == "SUCCESS"

    async def test_pending_returned_as_pending(self) -> None:
        resp = _mock_response(200, {"status": "PENDING"})
        client = _mock_client(resp)

        with patch("tassi.campay.httpx.AsyncClient", return_value=client):
            status = await get_transaction_status(_APP_TOKEN, _REFERENCE)

        assert status == "PENDING"

    async def test_failed_returned_as_failed(self) -> None:
        resp = _mock_response(200, {"status": "FAILED"})
        client = _mock_client(resp)

        with patch("tassi.campay.httpx.AsyncClient", return_value=client):
            status = await get_transaction_status(_APP_TOKEN, _REFERENCE)

        assert status == "FAILED"

    async def test_unknown_status_falls_back_to_pending(self) -> None:
        resp = _mock_response(200, {"status": "PROCESSING"})
        client = _mock_client(resp)

        with patch("tassi.campay.httpx.AsyncClient", return_value=client):
            status = await get_transaction_status(_APP_TOKEN, _REFERENCE)

        assert status == "PENDING"

    async def test_http_error_raises(self) -> None:
        resp = _mock_response(404, {})
        client = _mock_client(resp)

        with patch("tassi.campay.httpx.AsyncClient", return_value=client):
            with pytest.raises(httpx.HTTPStatusError):
                await get_transaction_status(_APP_TOKEN, _REFERENCE)
