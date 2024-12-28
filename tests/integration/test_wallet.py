import random
import string

import pytest
from httpx import AsyncClient

from src.core.pydantic_schemas import PostWallet


@pytest.fixture(scope="module")
async def fill_wallets_db(async_client: AsyncClient) -> None:
    for _ in range(18):
        random_address = "T" + "".join(
            random.choices(string.ascii_letters + string.digits, k=33)
        )
        wallet_data = PostWallet(address=random_address)

        post_query = await async_client.post(
            "/wallet/post_wallet", json=wallet_data.model_dump()
        )

        assert post_query.status_code == 200, (
            f"Unexpected status code: {post_query.status_code}. "
            f"Response: {post_query.text}"
        )


@pytest.mark.asyncio(loop_scope="module")
@pytest.mark.parametrize(
    "pagination_data, expected_wallet_count",
    [
        ({"page": 1, "size": 10}, 10),
        ({"page": 2, "size": 5}, 5),
        ({"page": 1, "size": 20}, 18),
    ],
)
async def test_get_wallet(
    fill_wallets_db: None,
    async_client: AsyncClient,
    pagination_data: dict,
    expected_wallet_count: int,
) -> None:
    get_query = await async_client.get(
        "/wallet/get_wallets_requests_list", params=pagination_data
    )

    assert get_query.status_code == 200, (
        f"Expected status code 200, got {get_query.status_code}. "
        f"Response: {get_query.text}"
    )

    response_data = get_query.json()
    assert len(response_data) == expected_wallet_count, (
        f"Expected {expected_wallet_count} wallets in response, got {len(response_data)}. "
        f"Response: {response_data}"
    )
