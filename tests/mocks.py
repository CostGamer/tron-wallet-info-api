from unittest.mock import AsyncMock, MagicMock

from src.services.tron_service import TronService


def mock_tron_service() -> TronService:
    mock = MagicMock(spec=TronService)
    mock.check_wallet_format = AsyncMock(return_value=True)
    mock.get_wallet_info = AsyncMock(
        return_value={
            "balance": 1000,
            "bandwidth": 500,
            "energy": 200,
        }
    )
    return mock
