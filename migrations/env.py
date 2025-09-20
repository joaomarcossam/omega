from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# importa Base e os models do seu projeto
from infra.database import Base
import infra.models  # garante que todos os models sejam carregados

# Alembic Config object
config = context.config

# Configuração de logging do Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Aqui o Alembic vai olhar para os metadados do seu Base
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Rodar migrations em 'offline mode'."""
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
    """Rodar migrations em 'online mode'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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
