from sqlalchemy import Column, String
from infra.database import Base

class BotConfig(Base):

    """
    Model de configuração do bot.
    Armazena chave/valor para configs diversas (ex.: canal de logs)
    """

    __tablename__ = "bot_config"

    config_key = Column(String(100), primary_key=True, index=True)
    config_value = Column(String(100), nullable=False)