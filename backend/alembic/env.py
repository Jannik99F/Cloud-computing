from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool, MetaData
from alembic import context
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# We are using raw SQL in our migrations, so no metadata needed
target_metadata = None

# Load the DATABASE_URL from environment variables.
DATABASE_URL = database_url = os.getenv("DB_URL_LOCAL") if os.getenv("DEBUG") == "true" else os.getenv("DB_URL_PROD")
if DATABASE_URL is None:
    raise ValueError("DB_URL is not set in the .env file")

# Update the sqlalchemy.url in alembic.ini to use the DATABASE_URL
config.set_section_option('alembic', 'sqlalchemy.url', DATABASE_URL)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
