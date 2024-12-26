import uuid
from datetime import datetime
from typing import Literal, get_args

from sqlalchemy import Enum, Float, ForeignKey, Integer, String, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

WalletRequestStatus = Literal["success", "failure", "processing"]


class Base(DeclarativeBase):
    pass


class Wallets(Base):
    __tablename__ = "wallets"

    address: Mapped[str] = mapped_column(
        String(34), unique=True, nullable=False, primary_key=True
    )
    bandwidth: Mapped[int] = mapped_column(Integer, nullable=False)
    energy: Mapped[int] = mapped_column(Integer, nullable=False)
    balance: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    requests: Mapped[list["WalletsRequest"]] = relationship(
        "WalletRequest",
        back_populates="wallet",
        uselist=True,
        cascade="all, delete-orphan",
    )


class WalletsRequest(Base):
    __tablename__ = "wallets_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    wallet_address: Mapped[str] = mapped_column(ForeignKey("wallets.address"))
    request_time: Mapped[datetime] = mapped_column(default=func.now())
    response_time: Mapped[datetime] = mapped_column(nullable=True)
    status: Mapped[WalletRequestStatus] = mapped_column(
        Enum(
            *get_args(WalletRequestStatus),
            name="wallet_request_status",
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
    )

    wallet: Mapped["Wallets"] = relationship("Wallet", back_populates="requests")
