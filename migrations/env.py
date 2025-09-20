from logging.config import fileConfig
from alembic import context

from discord_bot.core.settings import Env
# importa Base e os models
from infra.database import Base, engine
import infra.models  # garante que todos os models sejam carregados


# carregar envs (.env ou variáveis do painel)
Env.load()

# Alembic Config object
config = context.config

# Configuração de logging do Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Rodar migrations em 'offline mode'."""
    url = str(engine.url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Rodar migrations em 'online mode'."""
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
