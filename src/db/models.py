import uuid
from datetime import datetime
from typing import Literal, get_args

from sqlalchemy import Enum, String, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

WalletRequestStatus = Literal["success", "failure"]


class Base(DeclarativeBase):
    pass


class WalletsRequest(Base):
    __tablename__ = "wallets_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    wallet_address: Mapped[str] = mapped_column(String(34), nullable=False)
    request_time: Mapped[datetime] = mapped_column(default=func.now())
    status: Mapped[WalletRequestStatus] = mapped_column(
        Enum(
            *get_args(WalletRequestStatus),
            name="wallet_request_status",
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
    )
