from fastapi import APIRouter, Depends, Query

from src.api.dependencies import get_wallet_service, get_wallets_requests
from src.api.responses import post_wallet_responses
from src.core.pydantic_schemas import GetWallet, GetWalletRequest, PostWallet
from src.services.wallet_service import GetWalletsRequestsService, PostWaletService

wallet_router = APIRouter()


@wallet_router.post(
    "/post_wallet",
    response_model=GetWallet,
    responses=post_wallet_responses,
    description="Post wallet address to DB and get wallet parametres back",
)
async def post_wallet(
    wallet_address: PostWallet,
    wallet_service: PostWaletService = Depends(get_wallet_service),
) -> GetWallet:
    return await wallet_service(wallet_address)


@wallet_router.get(
    "/get_wallets_requests_list",
    response_model=list[GetWalletRequest],
    description="This endpoint allows you to get a list of \
    requests for wallets with pagination support. \
    You can specify the page number and the number of elements \
    per page to control what data is returned that is parsed.",
)
async def get_wallets_requests_list(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    get_wallets_requests: GetWalletsRequestsService = Depends(get_wallets_requests),
) -> list[GetWalletRequest]:
    return await get_wallets_requests(page, size)
