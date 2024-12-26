from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.pydantic_schemas import PostWallet
from src.DB.models import WalletsRequest


class WalletRepo:
    def __init__(self, con: AsyncSession) -> None:
        self._con = con

    async def post_wallet_request_data(self, wallet: PostWallet, status: str) -> None:
        query = insert(WalletsRequest).values(
            wallet_address=wallet.address, status=status
        )
        await self._con.execute(query)
