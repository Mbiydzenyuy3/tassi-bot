import hashlib
import hmac


def verify_meta_signature(payload: bytes, signature_header: str, app_secret: str) -> bool:
    """
    Verify the X-Hub-Signature-256 header on incoming Meta webhooks.
    Returns True if valid, False otherwise. Never raises.
    NFR-SEC-3: uses hmac.compare_digest to prevent timing attacks.
    """
    if not signature_header.startswith("sha256="):
        return False
    received = signature_header[len("sha256=") :]
    computed = hmac.new(app_secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, received)
