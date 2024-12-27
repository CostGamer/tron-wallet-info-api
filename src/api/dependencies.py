from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import all_settings
from src.DB import get_session_instance
from src.repositories.wallet_repo import WalletRepo
from src.services.tron_service import TronService
from src.services.wallet_service import WaletService


def get_wallet_repo(db: AsyncSession = Depends(get_session_instance)) -> WalletRepo:
    return WalletRepo(db)


def get_tron_service() -> TronService:
    return TronService(all_settings.tron)


def get_wallet_service(
    wallet_repo: WalletRepo = Depends(get_wallet_repo),
    tron_service: TronService = Depends(get_tron_service),
) -> WaletService:
    return WaletService(wallet_repo, tron_service)
