import discord
from discord.ext import commands

from services import log_service


class LogChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name="logchannel", invoke_without_command=True)
    async def logchannel(self, ctx: commands.Context):
        """Gerencia o canal de logs."""
        await ctx.send("Use `?logchannel set <canal>` para definir o canal de logs.")

    @logchannel.command(name="set")
    async def set_logchannel(self, ctx: commands.Context, channel: discord.TextChannel):
        log_service.set_log_channel(channel.id)
        await ctx.send(f"Canal de logs definido como {channel.mention}")

    @logchannel.command(name="show")
    async def show_logchannel(self, ctx: commands.Context):
        channel_id = log_service.get_log_channel()
        if channel_id:
            channel = self.bot.get_channel(channel_id)
            await ctx.send(f"Canal de logs: {channel.mention}")
        else:
            await ctx.send("Canal de logs não definido.")

    @logchannel.command(name="clear")
    async def clear_logchannel(self, ctx: commands.Context):
        log_service.clear_log_channel()
        await ctx.send("Canal de logs removido.")