import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from tassi.models import Base

alembic_config = context.config

if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# Override the database URL from the environment so alembic.ini never contains
# credentials. All other config (script_location etc.) still comes from alembic.ini.
database_url = os.environ.get("DATABASE_URL")
if database_url:
    # Alembic uses a sync engine. Strip the +psycopg_async suffix if present;
    # plain postgresql+psycopg works for both sync (migrations) and async (app).
    sync_url = database_url.replace("+psycopg_async", "+psycopg")
    alembic_config.set_main_option("sqlalchemy.url", sync_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
