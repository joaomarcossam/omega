import logging
import discord
from discord.ext import commands

from utils.discord_log_handler import DiscordLogHandler
from services import log_service
from ..core.settings import Env
from utils.font import Font
from ..modules.hello import Hello
from ..modules.league import League
from ..modules.omegon import Omegon
from ..modules.logchannel import LogChannel


def create_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    return commands.Bot(command_prefix="?", intents=intents)


async def register_cogs(bot: commands.Bot):
    await bot.add_cog(Omegon(bot))
    await bot.add_cog(Hello(bot))
    await bot.add_cog(LogChannel(bot))
    await bot.add_cog(League(bot))


def setup_logging(bot):
    # cria logger exclusivo pro Discord
    discord_logger = logging.getLogger("discord_logs")
    discord_logger.setLevel(logging.INFO)

    handler = DiscordLogHandler(bot)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    discord_logger.addHandler(handler)

    return discord_logger


def run():
    Env.load()
    bot = create_bot()

    print(Font("Omegon is starting...").blink.cyan)

    import asyncio

    async def runner():
        await register_cogs(bot)
        setup_logging(bot)  # ativa handler
        await bot.start(Env.OMEGON_TOKEN)

    asyncio.run(runner())
