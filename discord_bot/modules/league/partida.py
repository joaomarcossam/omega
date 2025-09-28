import discord
from discord.ext import commands
from .utils import league_of_graphs_url

from discord_bot.modules.league.base import LeagueBase


class Partida(LeagueBase):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="partida")
    async def partida(self, ctx, riot_id: str, platform: str = "br1"):
        game_name, tag_line = self.split_riot_id(riot_id)
        if not game_name:
            await ctx.send("❌ Formato inválido. Use: `?partida Nome#TAG [plataforma]`")
            return

        data = await self.service.get_current_match(game_name, tag_line, platform)
        if not data:
            await ctx.send("❌ Nenhuma partida em andamento encontrada.")
            return

        embed = discord.Embed(
            title=f"🔴 Partida em andamento - ID {data['gameId']}",
            color=discord.Color.blurple()
        )

        blue_team = [p for p in data["participants"] if p["teamId"] == 100]
        red_team = [p for p in data["participants"] if p["teamId"] == 200]

        def format_player(p):
            streak = "🔥" if p["hotStreak"] else "❄️"
            riot_id = p["riotId"]  # ex: "CondessaJanna#top1"
            url = league_of_graphs_url(riot_id, "br")
            return f"[{riot_id}]({url}) ({p['championName']})\n{p['rank']} {streak}"

        embed.add_field(name="🔵 Time Azul", value="\n\n".join(format_player(p) for p in blue_team), inline=True)
        embed.add_field(name="🔴 Time Vermelho", value="\n\n".join(format_player(p) for p in red_team), inline=True)

        await ctx.send(embed=embed)
