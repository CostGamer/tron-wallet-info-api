from typing import Sequence

from sqlalchemy import desc, insert, select
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.pydantic_schemas import PostWallet
from src.DB.models import WalletsRequest


class PostWalletRepo:
    def __init__(self, con: AsyncSession) -> None:
        self._con = con

    async def post_wallet_request_data(self, wallet: PostWallet, status: str) -> None:
        query = insert(WalletsRequest).values(
            wallet_address=wallet.address, status=status
        )
        await self._con.execute(query)


class GetWalletsRequestsRepo:
    def __init__(self, con: AsyncSession) -> None:
        self._con = con

    async def get_latest_wallets(
        self,
        page: int,
        size: int,
    ) -> Sequence[Row]:
        offset = (page - 1) * size
        query = (
            select(
                WalletsRequest.wallet_address,
                WalletsRequest.request_time,
                WalletsRequest.status,
            )
            .order_by(desc(WalletsRequest.request_time))
            .limit(size)
            .offset(offset)
        )
        query_res = await self._con.execute(query)
        res = query_res.all()
        return res
