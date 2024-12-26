import uuid
from datetime import datetime
from typing import Literal, get_args

from sqlalchemy import Enum, Float, ForeignKey, Integer, String, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

WalletRequestStatus = Literal["success", "failure", "processing"]


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )


class Wallet(Base):
    __tablename__ = "wallets"

    address: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    bandwidth: Mapped[int] = mapped_column(Integer, nullable=False)
    energy: Mapped[int] = mapped_column(Integer, nullable=False)
    balance: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    requests: Mapped[list["WalletRequest"]] = relationship(
        "WalletRequest",
        back_populates="wallet",
        uselist=True,
        cascade="all, delete-orphan",
    )


class WalletRequest(Base):
    __tablename__ = "wallet_requests"

    wallet_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("wallets.id"))
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

    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="requests")
