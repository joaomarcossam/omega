import logging
import asyncio

from services import log_service


class DiscordLogHandler(logging.Handler):
    def __init__(self, bot):
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

            # manda pro Discord sem travar o loop
            asyncio.create_task(channel.send(f"```{msg}```"))

        except Exception:
            # nunca deixar o handler explodir
            self.handleError(record)
