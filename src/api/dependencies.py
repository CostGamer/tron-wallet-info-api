from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import all_settings
from src.DB import get_session_instance
from src.repositories.wallet_repo import GetWalletsRequestsRepo, PostWalletRepo
from src.services.tron_service import TronService
from src.services.wallet_service import GetWalletsRequestsService, PostWaletService


def get_wallet_repo(db: AsyncSession = Depends(get_session_instance)) -> PostWalletRepo:
    return PostWalletRepo(db)


def get_latest_wallets(
    db: AsyncSession = Depends(get_session_instance),
) -> GetWalletsRequestsRepo:
    return GetWalletsRequestsRepo(db)


def get_tron_service() -> TronService:
    return TronService(all_settings.tron)


def get_wallet_service(
    wallet_repo: PostWalletRepo = Depends(get_wallet_repo),
    tron_service: TronService = Depends(get_tron_service),
) -> PostWaletService:
    return PostWaletService(wallet_repo, tron_service)


def get_wallets_requests(
    get_latest_wallets: GetWalletsRequestsRepo = Depends(get_latest_wallets),
) -> GetWalletsRequestsService:
    return GetWalletsRequestsService(get_latest_wallets)
