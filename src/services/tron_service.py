import re

from tronpy import Tron


class TronService:
    def __init__(self, node_url: str = "https://api.trongrid.io"):
        self._client = Tron(full_node=node_url)

    async def get_wallet_info(self, address: str) -> dict:
        account = self._client.get_account(address)
        return {
            "balance": account.get("balance", 0) / 1_000_000,  # TRX
            "bandwidth": account.get("free_net_usage", 0),
            "energy": account.get("energy_usage", 0),
        }

    @staticmethod
    def check_wallet_format(address: str) -> bool:
        return bool(re.match(r"^T[a-zA-Z0-9]{33}$", address))
