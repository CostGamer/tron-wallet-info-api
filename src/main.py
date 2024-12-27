from logging import getLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx import HTTPStatusError
from tronpy.exceptions import BadAddress

from src.api.exceptions import bad_address, incorrect_wallet_format, unathorized
from src.api.routers.wallet_routes import wallet_router
from src.core import all_settings
from src.core.custom_exceptions import WalletFormatIsIncorrect
from src.core.logs import init_logger
from src.middleware.logger import LoggerMiddleware

logger = getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(WalletFormatIsIncorrect, incorrect_wallet_format)  # type: ignore
    app.add_exception_handler(BadAddress, bad_address)
    app.add_exception_handler(HTTPStatusError, unathorized)  # type: ignore


def init_routers(app: FastAPI) -> None:
    app.include_router(wallet_router, prefix="/wallet", tags=["wallet"])


def init_middlewares(app: FastAPI) -> None:
    origins = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggerMiddleware)


def setup_app() -> FastAPI:
    app = FastAPI(
        title="Tron Wallet API",
        description="A microservice that provides information about a Tron wallet address, \
        including its bandwidth, energy, and TRX balance. \
        This API accepts a wallet address as input and returns the corresponding data from the Tron network",
        version="0.1.0",
    )
    init_logger(all_settings.logging)
    init_routers(app)
    init_middlewares(app)
    register_exception_handlers(app)
    logger.info("App created", extra={"app_version": app.version})
    return app
