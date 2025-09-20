from discord.ext import commands
import logging

logger = logging.getLogger("discord_logs")

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        logging.info("Hello command called by %s", ctx.author)
        await ctx.send("Hello! 👋")
