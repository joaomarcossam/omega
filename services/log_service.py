from infra.database import SessionLocal
from infra.models import BotConfig


def set_log_channel(channel_id: int):

    """Define ou atualiza o canal de logs no banco de dados."""

    session = SessionLocal()

    try:
        config = session.query(BotConfig).filter(BotConfig.config_key == "log_channel").first()
        if config:
            config.config_value = str(channel_id)
        else:
            config = BotConfig(config_key="log_channel", config_value=str(channel_id))
            session.add(config)
        session.commit()
        return channel_id
    finally:
        session.close()

def get_log_channel() -> int | None:

    """Retorna o canal de logs configurado no banco de dados."""

    session = SessionLocal()
    try:
        config = session.query(BotConfig).filter(BotConfig.config_key == "log_channel").first()
        return int(config.config_value) if config else None
    finally:
        session.close()

def clear_log_channel():
    """Remove o canal de logs configurado no banco de dados."""

    session = SessionLocal()
    try:
        config = session.query(BotConfig).filter(BotConfig.config_key == "log_channel").first()
        session.delete(config)
    finally:
        session.close()