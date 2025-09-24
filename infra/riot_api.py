import aiohttp
import os

from discord_bot.core.settings import Env

BASE_URL = f"https://{Env.RIOT_REGION}.api.riotgames.com"

class RiotAPI:
    def __init__(self):
        self.headers = {"X-Riot-Token": Env.RIOT_API_KEY}

    async def get_summoner_by_name(self, name: str):
        url = f"{BASE_URL}/lol/summoner/v4/summoners/by-name/{name}"
        return await self._get(url)

    async def get_rank_by_puuid(self, puuid: str):
        url = f"{BASE_URL}/lol/league/v4/entries/by-puuid/{puuid}"
        return await self._get(url)

    async def _get(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.status != 200:
                    return None
                return await resp.json()
