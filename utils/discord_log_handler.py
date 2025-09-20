import logging
import asyncio
import discord
from services import log_service


class DiscordLogHandler(logging.Handler):
    """Handler que envia logs do root logger para o canal configurado no Discord."""

    def __init__(self, bot: discord.Client):
        super().__init__()
        self.bot = bot

    def emit(self, record: logging.LogRecord):
        try:
            channel_id = log_service.get_log_channel()
            if not channel_id:
                return

            channel = self.bot.get_channel(channel_id)
            if not channel:
                return

            msg = self.format(record)

            # garante execução no loop do discord
            asyncio.run_coroutine_threadsafe(
                channel.send(f"```{msg}```"), self.bot.loop
            )
        except Exception:
            # nunca deixar o handler quebrar o logger
            self.handleError(record)
