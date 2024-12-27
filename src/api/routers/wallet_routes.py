from fastapi import APIRouter, Depends

from src.api.dependencies import get_wallet_service
from src.api.responses import post_wallet_responses
from src.core.pydantic_schemas import GetWallet, PostWallet
from src.services.wallet_service import WaletService

wallet_router = APIRouter()


@wallet_router.post(
    "/post_wallet",
    response_model=GetWallet,
    responses=post_wallet_responses,
    description="Post wallet address to DB and get wallet parametres back",
)
async def post_wallet(
    wallet_address: PostWallet,
    wallet_service: WaletService = Depends(get_wallet_service),
) -> GetWallet:
    return await wallet_service(wallet_address)
