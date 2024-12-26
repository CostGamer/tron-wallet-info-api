from logging import getLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = getLogger(__name__)


def init_routers(app: FastAPI) -> None: ...


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


def setup_app() -> FastAPI:
    app = FastAPI(
        title="Tron Wallet API",
        description="A microservice that provides information about a Tron wallet address, \
        including its bandwidth, energy, and TRX balance. \
        This API accepts a wallet address as input and returns the corresponding data from the Tron network",
        version="0.1.0",
    )
    init_routers(app)
    init_middlewares(app)
    logger.info("App created", extra={"app_version": app.version})
    return app
