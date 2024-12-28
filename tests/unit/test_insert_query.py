import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.pydantic_schemas import PostWallet
from src.DB.models import WalletsRequest
from src.repositories.wallet_repo import PostWalletRepo


@pytest.mark.asyncio
async def test_post_wallet_request_data(
    session: AsyncSession, async_client: AsyncClient
) -> None:
    repo = PostWalletRepo(session)

    wallet_data = PostWallet(address="test_wallet_address")
    status = "success"

    await repo.post_wallet_request_data(wallet_data, status)

    result = await session.execute(
        select(WalletsRequest).where(
            WalletsRequest.wallet_address == wallet_data.address
        )
    )
    wallet_request = result.scalars().first()

    assert wallet_request is not None
    assert wallet_request.wallet_address == wallet_data.address
    assert wallet_request.status == status
