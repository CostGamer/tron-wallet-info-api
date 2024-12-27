import re

from tronpy import AsyncTron
from tronpy.providers import AsyncHTTPProvider

from src.core.settings import TronSettings


class TronService:
    def __init__(self, tron_configs: TronSettings) -> None:
        self._client = AsyncTron(
            provider=AsyncHTTPProvider(
                endpoint_uri=tron_configs.tron_provider,
                api_key=tron_configs.tron_api_key,
            )
        )

    async def get_wallet_info(self, address: str) -> dict:
        balance = await self._client.get_account_balance(address)
        bandwidth = await self._client.get_bandwidth(address)
        energy = await self._client.get_account(address)
        return {
            "balance": balance,
            "bandwidth": bandwidth,
            "energy": energy.get("energy_usage", 0),
        }

    @staticmethod
    def check_wallet_format(address: str) -> bool:
        return bool(re.match(r"^T[a-zA-Z0-9]{33}$", address)) and len(address) == 34
