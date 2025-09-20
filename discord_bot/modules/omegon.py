import discord
from discord.ext import commands
from utils.module import Module
from logging import getLogger

logger = getLogger("discord_logs")  # mesmo nome que já está configurado no projeto

class Omegon(commands.Cog, Module):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("♪ Omegon module loaded!")  # vai pro console + Discord se handler estiver ativo

    @commands.command(name="stop")
    async def stop(self, ctx):
        await ctx.send("Bot is stopping...")
        logger.warning("Stopping Program...")
        Module.stop_all_modules()
