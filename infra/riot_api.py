from logging import getLogger
import aiohttp
from discord_bot.core.settings import Env

logger = getLogger("discord_logs")

REGIONAL_BASE = f"https://{Env.RIOT_REGION}.api.riotgames.com"   # AMERICAS/EUROPE/ASIA/SEA
PLATFORM_BASE = f"https://{Env.RIOT_PLATFORM}.api.riotgames.com" # BR1/NA1/EUW1/etc.

DEFAULT_PLATFORM = Env.RIOT_PLATFORM


class RiotAPI:
    def __init__(self):
        self.headers = {"X-Riot-Token": Env.RIOT_API_KEY}

    async def get_account_by_riot_id(self, game_name: str, tag_line: str):
        # ACCOUNT-V1 → regional host
        url = f"{REGIONAL_BASE}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        return await self._get(url)

    async def get_summoner_by_puuid(self, puuid: str, platform: str = DEFAULT_PLATFORM):
        # SUMMONER-V4 → platform host
        url = f"https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
        return await self._get(url)

    async def get_league_entries_by_puuid(self, puuid: str, platform: str = DEFAULT_PLATFORM):
        # LEAGUE-V4 → platform host
        url = f"https://{platform}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
        return await self._get(url)

    async def get_league_entries_by_summoner_id(self, summoner_id: str, platform: str = DEFAULT_PLATFORM):
        # LEAGUE-V4 → platform host
        url = f"https://{platform}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
        return await self._get(url)

    async def _get(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, ssl=True) as resp:
                status = resp.status
                if status == 200:
                    try:
                        data = await resp.json(content_type=None)
                        logger.info(f"[GET] {url} - 200")
                        return data
                    except Exception:
                        text = await resp.text()
                        logger.error(f"[GET] {url} - 200 mas payload não-JSON: {text[:300]}")
                        return None

                text = await resp.text()
                if status == 404:
                    logger.warning(f"[GET] {url} - 404")
                    return None
                if status == 401:
                    logger.error(f"[GET] {url} - 401 - {text}")
                    return None
                if status == 429:
                    logger.error(f"[GET] {url} - 429 - headers={dict(resp.headers)}")
                    return None

                logger.error(f"[GET] {url} - {status} - {text[:300]}")
                return None
