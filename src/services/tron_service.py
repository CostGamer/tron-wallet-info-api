from tronpy import Tron


class TronService:
    def __init__(self, node_url: str = "https://api.trongrid.io"):
        self.client = Tron(full_node=node_url)

    def get_wallet_info(self, address: str) -> dict:
        account = self.client.get_account(address)
        return {
            "balance": account.get("balance", 0) / 1_000_000,  # TRX
            "bandwidth": account.get("free_net_usage", 0),
            "energy": account.get("energy_usage", 0),
        }
