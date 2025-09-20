import asyncio
import logging
import discord
from discord.ext import commands

from utils.discord_log_handler import DiscordLogHandler
from ..core.settings import Env
from utils.font import Font
from ..modules.logchannel import LogChannel
from ..modules.omegon import Omegon
from ..modules.hello import Hello


def create_bot() -> commands.Bot:
    """Cria a instância do bot com intents configurados."""
    intents = discord.Intents.default()
    intents.message_content = True
    return commands.Bot(command_prefix="?", intents=intents)


def setup_logging(bot: commands.Bot) -> None:
    """Configura logging para também enviar pro canal do Discord."""
    root_logger = logging.getLogger()

    # evita duplicar handlers se já tiver configurado
    if any(isinstance(h, DiscordLogHandler) for h in root_logger.handlers):
        return

    discord_handler = DiscordLogHandler(bot)
    discord_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )

    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(discord_handler)


async def register_cogs(bot: commands.Bot) -> None:
    """Registra todos os Cogs do bot."""
    await bot.add_cog(Omegon(bot))
    await bot.add_cog(Hello(bot))
    await bot.add_cog(LogChannel(bot))


def run() -> None:
    """Ponto de entrada para rodar o bot."""
    Env.load()
    bot = create_bot()

    print(Font("Omegon is starting...").blink.cyan)

    async def runner():
        setup_logging(bot)  # ativa logs cedo
        await register_cogs(bot)
        await bot.start(Env.OMEGON_TOKEN)

    asyncio.run(runner())
