"""Tests for tassi.security — Meta HMAC signature verification (NFR-SEC-3)."""

import hashlib
import hmac

from tassi.security import verify_meta_signature

_SECRET = "test-secret"
_PAYLOAD = b'{"object":"whatsapp_business_account"}'


def _sign(payload: bytes, secret: str) -> str:
    digest = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


class TestVerifyMetaSignature:
    def test_valid_signature_returns_true(self) -> None:
        assert verify_meta_signature(_PAYLOAD, _sign(_PAYLOAD, _SECRET), _SECRET) is True

    def test_wrong_signature_returns_false(self) -> None:
        assert verify_meta_signature(_PAYLOAD, _sign(_PAYLOAD, "wrong-secret"), _SECRET) is False

    def test_tampered_payload_returns_false(self) -> None:
        sig = _sign(_PAYLOAD, _SECRET)
        assert verify_meta_signature(b"tampered", sig, _SECRET) is False

    def test_missing_prefix_returns_false(self) -> None:
        raw_hex = hmac.new(_SECRET.encode(), _PAYLOAD, hashlib.sha256).hexdigest()
        assert verify_meta_signature(_PAYLOAD, raw_hex, _SECRET) is False
