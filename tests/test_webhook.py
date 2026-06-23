"""
Tests for webhook endpoints — GET /webhook (verification) and POST /webhook (ingestion).
Task 3.1 and 3.3 from TASKS.md Milestone 3.
/campay/webhook tests in TestCampayWebhook (Milestone 5 Task 5.3).
"""

import hashlib
import hmac
import json
from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from tassi.config import Settings
from tassi.deps import get_db
from tassi.main import create_app


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

    def test_non_text_message_is_skipped(self, client: TestClient) -> None:
        image_payload = {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "messages": [
                                    {
                                        "id": "wamid.img001",
                                        "from": "237600000000",
                                        "type": "image",
                                        "image": {
                                            "id": "img_123",
                                            "mime_type": "image/jpeg",
                                        },
                                    }
                                ]
                            }
                        }
                    ]
                }
            ],
        }
        with patch("tassi.main.handle_message", new_callable=AsyncMock) as mock_handle:
            resp = self._post(client, image_payload)
        assert resp.status_code == 200
        mock_handle.assert_not_called()


@pytest.fixture
def campay_client(settings: Settings) -> TestClient:
    """TestClient with get_db overridden so no real DB session is needed."""

    async def _mock_db() -> AsyncGenerator[AsyncMock, None]:
        yield AsyncMock(spec=AsyncSession)

    app = create_app(settings=settings)
    app.dependency_overrides[get_db] = _mock_db
    with TestClient(app) as tc:
        yield tc


class TestCampayWebhook:
    _APP_TOKEN = "test-token"

    def _post(self, client: TestClient, body: dict) -> object:
        return client.post(
            "/campay/webhook",
            content=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
        )

    def test_valid_callback_returns_ok(self, campay_client: TestClient) -> None:
        with patch("tassi.main.process_payment_callback", new_callable=AsyncMock):
            resp = self._post(
                campay_client,
                {
                    "app_token": self._APP_TOKEN,
                    "reference": "CPY-001",
                    "status": "SUCCESSFUL",
                },
            )
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    def test_invalid_app_token_returns_403(self, campay_client: TestClient) -> None:
        resp = self._post(
            campay_client,
            {
                "app_token": "wrong-token",
                "reference": "CPY-001",
                "status": "SUCCESSFUL",
            },
        )
        assert resp.status_code == 403

    def test_missing_reference_returns_400(self, campay_client: TestClient) -> None:
        with patch("tassi.main.process_payment_callback", new_callable=AsyncMock):
            resp = self._post(
                campay_client,
                {"app_token": self._APP_TOKEN, "status": "SUCCESSFUL"},
            )
        assert resp.status_code == 400

    def test_invalid_json_returns_400(self, campay_client: TestClient) -> None:
        resp = campay_client.post(
            "/campay/webhook",
            content=b"not-json",
            headers={"Content-Type": "application/json"},
        )
        assert resp.status_code == 400

    def test_successful_status_normalized_before_dispatch(self, campay_client: TestClient) -> None:
        with patch("tassi.main.process_payment_callback", new_callable=AsyncMock) as mock_cb:
            self._post(
                campay_client,
                {
                    "app_token": self._APP_TOKEN,
                    "reference": "CPY-002",
                    "status": "SUCCESSFUL",
                },
            )
        # Background tasks run synchronously inside TestClient context
        assert mock_cb.call_args[0][1] == "SUCCESS"
