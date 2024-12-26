from src.core.custom_exceptions import WalletFormatIsIncorrect
from src.core.pydantic_schemas import GetWallet, PostWallet
from src.core.settings import FAILURE, SUCCESS
from src.repositories.wallet_repo import WalletRepo
from src.services.tron_service import TronService


class WaletService:
    def __init__(self, wallet_repo: WalletRepo) -> None:
        self._wallet_repo = wallet_repo

    async def __call__(
        self, tron_service: TronService, wallet: PostWallet
    ) -> GetWallet:
        check_wallet_format = tron_service.check_wallet_format(wallet.address)
        if not check_wallet_format:
            raise WalletFormatIsIncorrect

        try:
            get_wallet_info = await tron_service.get_wallet_info(wallet.address)
        except Exception as e:
            await self._wallet_repo.post_wallet_request_data(
                wallet=wallet, status=FAILURE
            )
            print(f"Unexpected error {e}")
            raise

        await self._wallet_repo.post_wallet_request_data(wallet=wallet, status=SUCCESS)
        return GetWallet.model_validate(get_wallet_info)
