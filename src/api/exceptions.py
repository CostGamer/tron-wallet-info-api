from fastapi import Request
from fastapi.responses import JSONResponse
from httpx import HTTPStatusError
from tronpy.exceptions import BadAddress

from src.core.custom_exceptions import WalletFormatIsIncorrect


async def incorrect_wallet_format(
    request: Request, exc: WalletFormatIsIncorrect
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": "The wallet address format is incorrect"},
    )


async def bad_address(request: Request, exc: BadAddress) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": "The inserted adress is bad"},
    )


async def unathorized(request: Request, exc: HTTPStatusError) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": "The API key or provider uri is incorrect"},
    )
