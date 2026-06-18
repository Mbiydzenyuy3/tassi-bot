"""
Campay API client — USSD push payments for MTN MoMo and Orange Money.

FR-PAY-2: initiate_ussd_push
FR-PAY-4: get_transaction_status
"""

import logging

import httpx

_log = logging.getLogger(__name__)

_CAMPAY_BASE = "https://campay.net/api"


async def _get_token(username: str, password: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{_CAMPAY_BASE}/token/",
            json={"username": username, "password": password},
            timeout=10.0,
        )
        resp.raise_for_status()
        return str(resp.json()["token"])


async def initiate_ussd_push(
    username: str,
    password: str,
    application_token: str,
    amount: int,
    msisdn: str,
    description: str,
    external_reference: str,
) -> str:
    """
    Initiate a USSD push payment via Campay API.
    Returns the Campay transaction reference.
    Raises httpx.HTTPStatusError on failure.
    FR-PAY-2.
    """
    token = await _get_token(username, password)
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{_CAMPAY_BASE}/collect/",
            json={
                "amount": str(amount),
                "currency": "XAF",
                "from": msisdn,
                "description": description,
                "external_reference": external_reference,
                "app_name": "Tassi",
                "redirect_url": "",
                "app_token": application_token,
            },
            headers={"Authorization": f"Token {token}"},
            timeout=30.0,
        )
        resp.raise_for_status()
        reference = str(resp.json()["reference"])
        _log.info("campay push initiated reference=%s msisdn=%s", reference, msisdn)
        return reference


async def get_transaction_status(
    application_token: str,
    campay_reference: str,
) -> str:
    """
    Poll Campay for the status of a transaction.
    Returns "SUCCESS", "FAILED", or "PENDING".
    FR-PAY-4.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{_CAMPAY_BASE}/transaction/{campay_reference}/",
            headers={"Authorization": f"Token {application_token}"},
            timeout=10.0,
        )
        resp.raise_for_status()
        raw = str(resp.json().get("status", "PENDING")).upper()
        # Campay uses "SUCCESSFUL"; normalise to "SUCCESS"
        if raw == "SUCCESSFUL":
            return "SUCCESS"
        return raw if raw in {"SUCCESS", "FAILED"} else "PENDING"
