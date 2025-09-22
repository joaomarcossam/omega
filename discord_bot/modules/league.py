from discord.ext import commands
from services.riot_service import RiotService

class League(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.service = RiotService()

    @commands.command(name="elo")
    async def elo(self, ctx, *, summoner_name: str):
        data = await self.service.get_player_info(summoner_name)
        if not data:
            await ctx.send("❌ Jogador não encontrado!")
            return

        msg = f"🔹 Invocador: **{data['name']}** (Level {data['level']})\n"
        for entry in data["ranks"]:
            msg += (
                f"{entry['queueType']}: {entry['tier']} {entry['rank']} "
                f"- {entry['leaguePoints']} PDL ({entry['wins']}W/{entry['losses']}L)\n"
            )

        await ctx.send(msg)
