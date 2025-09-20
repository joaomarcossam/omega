import logging
from infra.database import SessionLocal
from infra.models import BotConfig

logger = logging.getLogger(__name__)

def set_log_channel(channel_id: int):
    """Define ou atualiza o canal de logs no banco de dados."""
    session = SessionLocal()
    try:
        logger.info(f"[SET] Tentando definir canal de logs: {channel_id}")

        config = session.query(BotConfig).filter(BotConfig.config_key == "log_channel").first()
        if config:
            logger.info(f"[SET] Canal já existia ({config.config_value}), atualizando para {channel_id}")
            config.config_value = str(channel_id)
        else:
            logger.info("[SET] Nenhuma config encontrada, criando nova entrada")
            config = BotConfig(config_key="log_channel", config_value=str(channel_id))
            session.add(config)

        session.commit()
        logger.info(f"[SET] Canal de logs salvo com sucesso: {channel_id}")
        return channel_id
    except Exception as e:
        logger.error(f"[SET] Erro ao salvar canal de logs: {e}", exc_info=True)
        raise
    finally:
        session.close()

def get_log_channel() -> int | None:
    """Retorna o canal de logs configurado no banco de dados."""
    session = SessionLocal()
    try:
        logger.info("[GET] Buscando canal de logs configurado...")
        config = session.query(BotConfig).filter(BotConfig.config_key == "log_channel").first()
        if config:
            logger.info(f"[GET] Canal encontrado: {config.config_value}")
            return int(config.config_value)
        logger.info("[GET] Nenhum canal configurado")
        return None
    except Exception as e:
        logger.error(f"[GET] Erro ao buscar canal de logs: {e}", exc_info=True)
        raise
    finally:
        session.close()

def clear_log_channel():
    """Remove o canal de logs configurado no banco de dados."""
    session = SessionLocal()
    try:
        logger.info("[CLEAR] Removendo canal de logs...")
        config = session.query(BotConfig).filter(BotConfig.config_key == "log_channel").first()
        if config:
            logger.info(f"[CLEAR] Canal removido: {config.config_value}")
            session.delete(config)
            session.commit()
        else:
            logger.info("[CLEAR] Nenhum canal para remover")
    except Exception as e:
        logger.error(f"[CLEAR] Erro ao remover canal de logs: {e}", exc_info=True)
        raise
    finally:
        session.close()
