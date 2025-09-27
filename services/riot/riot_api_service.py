from .base import RiotBaseService


class RiotAPIService(RiotBaseService):
    """Camada de baixo nível: chamadas diretas à Riot API (1:1 endpoints)."""

    async def get_account_by_riot_id(self, game_name: str, tag_line: str):
        """Busca conta pelo Riot ID (gameName#tagLine)."""
        return await self.api.get_account_by_riot_id(game_name, tag_line)

    async def get_summoner_by_puuid(self, puuid: str, platform: str = "br1"):
        """Busca informações do invocador pelo PUUID."""
        return await self.api.get_summoner_by_puuid(puuid, platform)

    async def get_league_entries_by_puuid(self, puuid: str, platform: str = "br1"):
        """Busca informações ranqueadas do invocador pelo PUUID."""
        return await self.api.get_league_entries_by_puuid(puuid, platform)

    async def get_champion_mastery_by_puuid(self, puuid: str, platform: str = "br1"):
        """Busca maestrias de campeão pelo PUUID."""
        return await self.api.get_champion_mastery_by_puuid(puuid, platform)

