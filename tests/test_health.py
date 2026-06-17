"""
Tests for the health endpoint and app factory.

Coverage goals:
  - /health response shape (all users)
  - docs/redoc hidden in production (debug=False)
  - docs/redoc visible in debug mode (debug=True)
  - create_app() with no settings argument (exercises the `settings or Settings()` branch)
"""

from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

import tassi
from tassi.main import create_app


class TestHealthEndpoint:
    def test_returns_200(self, client: TestClient) -> None:
        assert client.get("/health").status_code == HTTPStatus.OK

    def test_returns_status_ok(self, client: TestClient) -> None:
        assert client.get("/health").json()["status"] == "ok"

    def test_returns_service_name(self, client: TestClient) -> None:
        assert client.get("/health").json()["service"] == "tassi"


class TestApiDocs:
    def test_docs_accessible_in_debug_mode(self, client: TestClient) -> None:
        assert client.get("/docs").status_code == HTTPStatus.OK

    def test_redoc_accessible_in_debug_mode(self, client: TestClient) -> None:
        assert client.get("/redoc").status_code == HTTPStatus.OK

    def test_docs_hidden_in_production(self, client_production: TestClient) -> None:
        assert client_production.get("/docs").status_code == HTTPStatus.NOT_FOUND

    def test_redoc_hidden_in_production(self, client_production: TestClient) -> None:
        assert client_production.get("/redoc").status_code == HTTPStatus.NOT_FOUND


class TestAppFactory:
    def test_create_app_without_settings_uses_defaults(self) -> None:
        """Exercises the `settings or Settings()` fallback branch in create_app."""
        app = create_app()
        assert app.title == "Tassi"

    def test_create_app_with_settings_uses_provided_config(self) -> None:
        from tassi.config import Settings

        custom = Settings(debug=True, environment="staging")
        app = create_app(settings=custom)
        # docs_url is set when debug=True
        assert app.docs_url == "/docs"

    def test_create_app_production_hides_docs(self) -> None:
        from tassi.config import Settings

        prod = Settings(debug=False)
        app = create_app(settings=prod)
        assert app.docs_url is None
        assert app.redoc_url is None


class TestLifespan:
    def test_engine_on_app_state_after_startup(self, client: TestClient) -> None:
        assert client.app.state.engine is not None  # type: ignore[union-attr]

    def test_engine_is_async_engine(self, client: TestClient) -> None:
        assert isinstance(client.app.state.engine, AsyncEngine)  # type: ignore[union-attr]

    def test_db_factory_on_app_state_after_startup(self, client: TestClient) -> None:
        assert client.app.state.db_factory is not None  # type: ignore[union-attr]

    def test_db_factory_is_async_sessionmaker(self, client: TestClient) -> None:
        assert isinstance(client.app.state.db_factory, async_sessionmaker)  # type: ignore[union-attr]


class TestVersion:
    def test_version_string_exists(self) -> None:
        assert isinstance(tassi.__version__, str)

    def test_version_not_empty(self) -> None:
        assert tassi.__version__ != ""
