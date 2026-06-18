"""
Tests for webhook endpoints — GET /webhook (verification) and POST /webhook (ingestion).
Task 3.1 and 3.3 from TASKS.md Milestone 3.
"""

import hashlib
import hmac
import json
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient


def _sign(payload: bytes, secret: str) -> str:
    digest = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def _webhook_payload(message_id: str = "wamid.test001") -> dict:
    return {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    "id": message_id,
                                    "from": "237600000000",
                                    "type": "text",
                                    "text": {"body": "2350000"},
                                }
                            ]
                        }
                    }
                ]
            }
        ],
    }


class TestVerifyWebhook:
    def test_valid_token_returns_challenge(self, client: TestClient) -> None:
        resp = client.get(
            "/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "test-verify-token",
                "hub.challenge": "abc123",
            },
        )
        assert resp.status_code == 200
        assert resp.text == "abc123"

    def test_wrong_token_returns_403(self, client: TestClient) -> None:
        resp = client.get(
            "/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "wrong-token",
                "hub.challenge": "abc123",
            },
        )
        assert resp.status_code == 403

    def test_wrong_mode_returns_403(self, client: TestClient) -> None:
        resp = client.get(
            "/webhook",
            params={
                "hub.mode": "unsubscribe",
                "hub.verify_token": "test-verify-token",
                "hub.challenge": "abc123",
            },
        )
        assert resp.status_code == 403


class TestReceiveWebhook:
    def _post(self, client: TestClient, payload: dict, secret: str = "test-app-secret") -> object:
        body = json.dumps(payload).encode()
        return client.post(
            "/webhook",
            content=body,
            headers={
                "Content-Type": "application/json",
                "X-Hub-Signature-256": _sign(body, secret),
            },
        )

    def test_invalid_signature_returns_403(self, client: TestClient) -> None:
        body = json.dumps(_webhook_payload()).encode()
        resp = client.post(
            "/webhook",
            content=body,
            headers={
                "Content-Type": "application/json",
                "X-Hub-Signature-256": "sha256=badhash",
            },
        )
        assert resp.status_code == 403

    def test_valid_request_acks_immediately(self, client: TestClient) -> None:
        with patch("tassi.main.handle_message", new_callable=AsyncMock):
            resp = self._post(client, _webhook_payload())
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    def test_duplicate_message_id_handle_called_once(self, client: TestClient) -> None:
        payload = _webhook_payload(message_id="wamid.dup001")
        with patch("tassi.main.handle_message", new_callable=AsyncMock) as mock_handle:
            with patch("tassi.main.is_duplicate_message", new_callable=AsyncMock) as mock_dedup:
                mock_dedup.side_effect = [False, True]
                self._post(client, payload)
                self._post(client, payload)
        assert mock_handle.call_count == 1

    def test_invalid_json_body_returns_400(self, client: TestClient) -> None:
        body = b"not-valid-json"
        resp = client.post(
            "/webhook",
            content=body,
            headers={
                "Content-Type": "application/json",
                "X-Hub-Signature-256": _sign(body, "test-app-secret"),
            },
        )
        assert resp.status_code == 400

    def test_rate_limited_message_is_skipped(self, client: TestClient) -> None:
        with patch("tassi.main.handle_message", new_callable=AsyncMock) as mock_handle:
            with patch("tassi.main.is_rate_limited", new_callable=AsyncMock) as mock_limit:
                mock_limit.return_value = True
                resp = self._post(client, _webhook_payload())
        assert resp.status_code == 200
        mock_handle.assert_not_called()
