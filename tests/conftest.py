from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from tassi.config import Settings
from tassi.main import create_app

# Shared test values — avoids repeating placeholder secrets across fixtures
_TEST_SETTINGS = {
    "database_url": "postgresql+psycopg://tassi:tassi@localhost:5432/test_tassi",
    "redis_url": "redis://localhost:6379/1",
    "meta_verify_token": "test-verify-token",
    "meta_app_secret": "test-app-secret",
    "meta_phone_number_id": "test-phone-id",
    "meta_access_token": "test-access-token",
    "campay_username": "test-user",
    "campay_password": "test-pass",
    "campay_application_token": "test-token",
    "environment": "test",
}


@pytest.fixture
def settings() -> Settings:
    """Debug-enabled settings — /docs and /redoc are accessible."""
    return Settings(**_TEST_SETTINGS, debug=True)


@pytest.fixture
def settings_production() -> Settings:
    """Production-mode settings — /docs and /redoc are hidden."""
    return Settings(**_TEST_SETTINGS, debug=False)


@pytest.fixture
def client(settings: Settings) -> Generator[TestClient, None, None]:
    app = create_app(settings=settings)
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def client_production(settings_production: Settings) -> Generator[TestClient, None, None]:
    app = create_app(settings=settings_production)
    with TestClient(app) as test_client:
        yield test_client
