import discord
from discord.ext import commands
from .base import LeagueBase, TIER_COLORS


class Elo(LeagueBase):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="elo")
    async def elo(self, ctx, riot_id: str, platform: str = "br1"):
        try:
            self.logger.info("Elo command called by %s", ctx.author)

            game_name, tag_line = self.split_riot_id(riot_id)
            if not game_name:
                await ctx.send("❌ Formato inválido. Use: `?elo Nome#TAG [plataforma]`")
                return

            data = await self.service.get_player_info(game_name, tag_line, platform)

            if not data:
                self.logger.warning("Player not found for %s#%s", game_name, tag_line)
                await ctx.send("❌ Jogador não encontrado!")
                return

            ranks = data.get("ranks") or []
            tier_main = ranks[0].get("tier", "UNRANKED") if ranks else "UNRANKED"

            # --- Embed bonito ---
            embed = discord.Embed(
                title=f"🔹 Invocador: {data['name']}",
                description=f"Nível **{data['level']}**",
                color=TIER_COLORS.get(tier_main, discord.Color.default())
            )

            # Ícone de perfil do invocador
            if data.get("profileIconId"):
                embed.set_thumbnail(
                    url=f"http://ddragon.leagueoflegends.com/cdn/14.17.1/img/profileicon/{data['profileIconId']}.png"
                )

            if not ranks:
                embed.add_field(name="Elo", value="❌ Unranked", inline=False)
            else:
                for entry in ranks:
                    queue = entry.get("queueType", "QUEUE")
                    tier = entry.get("tier", "UNRANKED")
                    rank = entry.get("rank", "")
                    lp = entry.get("leaguePoints", 0)
                    wins = entry.get("wins", 0)
                    losses = entry.get("losses", 0)
                    hotstreak = entry.get("hotStreak", False)

                    fila = "🗡️ Solo/Duo" if queue == "RANKED_SOLO_5x5" else "🛡️ Flex"
                    value = f"**{tier} {rank}** - {lp} PDL\n📊 {wins}W / {losses}L"
                    embed.add_field(name=fila, value=value, inline=True)
                    embed.add_field(name="Hotstreak", value="✅" if hotstreak else "❌", inline=False)

            embed.set_footer(text="Dados fornecidos pela Riot API")

            await ctx.send(embed=embed)
            self.logger.info("Elo result sent for %s", ctx.author)

        except Exception as e:
            self.logger.exception(f"Erro ao buscar elo de {riot_id} e {platform}. Erro: {e}")
            await ctx.send("⚠️ Ocorreu um erro ao buscar os dados.")
