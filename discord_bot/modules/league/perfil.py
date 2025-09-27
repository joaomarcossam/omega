import discord
from discord.ext import commands
from .base import LeagueBase

class Perfil(LeagueBase):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="perfil")
    async def perfil(self, ctx, riot_id: str, platform: str = "br1"):
        try:
            self.logger.info("Perfil command called by %s", ctx.author)

            game_name, tag_line = self.split_riot_id(riot_id)
            if not game_name:
                await ctx.send("❌ Formato inválido. Use: `?perfil Nome#TAG [plataforma]`")
                return

            data = await self.service.get_player_profile(game_name, tag_line, platform)
            if not data:
                await ctx.send("❌ Jogador não encontrado!")
                return

            # Embed usando helper da base
            embed = self.make_embed(
                title=f"🔹 Invocador: {data['name']}",
                description=f"Nível **{data['level']}**",
                color=discord.Color.blue()
            )

            # Ícone do perfil
            if data.get("profileIconId"):
                embed.set_thumbnail(
                    url=f"http://ddragon.leagueoflegends.com/cdn/14.17.1/img/profileicon/{data['profileIconId']}.png"
                )

            # Elo principal
            if data["ranks"]:
                rank = data["ranks"][0]
                embed.add_field(
                    name="Elo principal",
                    value=f"{rank['tier']} {rank['rank']} - {rank['leaguePoints']} PDL",
                    inline=False
                )

            # Campeões favoritos (top 3)
            if data["top_champions"]:
                for champ in data["top_champions"]:
                    embed.add_field(
                        name=champ["name"],
                        value=f"{champ['points']} pontos",
                        inline=True
                    )

                # thumbnail do primeiro campeão (favorito absoluto)
                embed.set_thumbnail(url=data["top_champions"][0]["icon"])
            else:
                embed.add_field(name="Campeões favoritos", value="❌ Nenhum campeão encontrado", inline=False)

            # Pontos totais
            embed.add_field(
                name="Total de pontos de maestria",
                value=str(data["total_mastery_points"]),
                inline=False
            )

            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.exception(f"Erro ao buscar perfil de {riot_id} e {platform}. Erro: {e}")
            await ctx.send("⚠️ Ocorreu um erro ao buscar os dados.")
