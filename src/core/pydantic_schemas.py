from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from src.core.settings import FAILURE, SUCCESS


class WalletRequestStatus(str, Enum):
    success = SUCCESS
    failure = FAILURE


class PostWallet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    address: str = Field(..., description="wallet adress in Tron network")


class GetWallet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    bandwidth: int = Field(
        ..., description="The available bandwidth of the wallet, measured in bytes"
    )
    energy: int = Field(
        ...,
        description="The available energy of the wallet, used to execute smart contracts",
    )
    balance: float = Field(
        ..., description="The current balance of TRX (Tron) in the wallet"
    )


class GetWalletRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    wallet_address: str = Field(..., description="wallet adress in Tron network")
    request_time: str = Field(
        ..., description="The timestamp when the request was made"
    )
    status: WalletRequestStatus = Field(
        ..., description="The status of the request (success, failure, processing)"
    )
