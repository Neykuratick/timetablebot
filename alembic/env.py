from logging.config import fileConfig
from time import sleep

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.exc import OperationalError

from app.backend.db import Base
from alembic import context

from config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=settings.POSTGRES_URL,
        target_metadata=target_metadata,
        compare_type=True,
        file_template="%%(year)s_%%(month)02d_%%(day)02d_%%(hour)02d%%(minute)02d_%%(slug)s",
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.POSTGRES_URL
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    try:
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
                file_template="%%(year)s_%%(month)02d_%%(day)02d_%%(hour)02d%%(minute)02d_%%(slug)s",
            )

            with context.begin_transaction():
                context.run_migrations()
    except OperationalError:
        print(f"Cannot connect to database, retrying connection url={settings.POSTGRES_URL}")
        sleep(3)
        run_migrations_online()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
