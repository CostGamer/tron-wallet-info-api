from src.core.custom_exceptions import WalletFormatIsIncorrect
from src.core.pydantic_schemas import GetWallet, GetWalletRequest, PostWallet
from src.core.settings import FAILURE, SUCCESS
from src.repositories.wallet_repo import GetWalletsRequestsRepo, PostWalletRepo
from src.services.tron_service import TronService


class PostWaletService:
    def __init__(
        self,
        wallet_repo: PostWalletRepo,
        tron_service: TronService,
    ) -> None:
        self._wallet_repo = wallet_repo
        self._tron_service = tron_service

    async def __call__(
        self,
        wallet: PostWallet,
    ) -> GetWallet:
        check_wallet_format = self._tron_service.check_wallet_format(wallet.address)
        if not check_wallet_format:
            raise WalletFormatIsIncorrect

        try:
            get_wallet_info = await self._tron_service.get_wallet_info(wallet.address)
        except Exception as e:
            await self._wallet_repo.post_wallet_request_data(
                wallet=wallet, status=FAILURE
            )
            print(f"Unexpected error {e}")
            raise

        await self._wallet_repo.post_wallet_request_data(wallet=wallet, status=SUCCESS)
        return GetWallet.model_validate(get_wallet_info)


class GetWalletsRequestsService:
    def __init__(self, get_wallet_repo: GetWalletsRequestsRepo) -> None:
        self._get_wallet_repo = get_wallet_repo

    async def __call__(self, page: int, size: int) -> list[GetWalletRequest]:
        wallets_requests = await self._get_wallet_repo.get_latest_wallets(page, size)

        formatted_requests = []
        for wallet in wallets_requests:
            formatted_request = {
                "wallet_address": wallet[0],
                "request_time": wallet[1].strftime("%Y-%m-%d %H:%M:%S"),
                "status": wallet[2],
            }
            formatted_requests.append(
                GetWalletRequest.model_validate(formatted_request)
            )

        return formatted_requests
