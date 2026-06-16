from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    All config is read from environment variables (or .env file).
    Every value has a safe default so the app starts cleanly in dev without a .env file.
    Per SRS NFR-MAINT-1: tax rates and feature flags are config, not code.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Database ─────────────────────────────────────────────────────────────
    database_url: str = Field("postgresql+psycopg://tassi:tassi@localhost:5432/tassi")

    # ── Redis ─────────────────────────────────────────────────────────────────
    redis_url: str = Field("redis://localhost:6379/0")

    # ── Meta / WhatsApp Cloud API ─────────────────────────────────────────────
    meta_verify_token: str = Field("change-me")
    meta_app_secret: str = Field("change-me")
    meta_phone_number_id: str = Field("change-me")
    meta_access_token: str = Field("change-me")

    # ── Campay (MTN MoMo / Orange Money) ──────────────────────────────────────
    campay_username: str = Field("change-me")
    campay_password: str = Field("change-me")
    campay_application_token: str = Field("change-me")

    # ── Tax engine (SRS NFR-MAINT-1, Validation Gates G1) ────────────────────
    # Stored as str so consuming code must explicitly cast to Decimal (never float)
    rate_rsi: str = Field("0.055")
    # ADDITIVE | INCLUDED | UNCONFIRMED  — see SRS §3 Gate G1
    cac_mode: str = Field("UNCONFIRMED")
    cac_rate: str = Field("0.10")

    # ── Tassi Plus (SRS §3 Gate G3) ───────────────────────────────────────────
    plus_price_xaf: int = Field(500)  # placeholder until G3 resolves
    feature_plus_reminders: bool = Field(False)  # off until G3 resolves

    # ── Application ───────────────────────────────────────────────────────────
    debug: bool = Field(False)
    environment: str = Field("production")
