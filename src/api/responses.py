from http import HTTPStatus
from typing import Any


def create_error_responses(
    error_responses: dict[int, dict[str, dict[str, Any]]]
) -> dict:
    responses = {}

    for status_code, examples in error_responses.items():
        description = HTTPStatus(status_code).phrase
        responses[status_code] = {
            "description": description,
            "content": {"application/json": {"examples": examples}},
        }

    return responses


post_wallet_exceptions = {
    400: {
        "wallet_format_error": {
            "summary": "WalletFormatIsIncorrect",
            "value": {"detail": "The wallet address format is incorrect"},
        },
        "bad_address": {
            "summary": "BadAddress",
            "value": {"detail": "The inserted adress is bad (TRONPY Exception)"},
        },
    },
    401: {
        "unathorized": {
            "summary": "Unauthorized",
            "value": {"detail": "The API key or provider uri is incorrect"},
        }
    },
    500: {
        "interanal_server_error": {
            "summary": "RuntimeError",
            "value": {"detail": "A runtime error occurred"},
        }
    },
}


post_wallet_responses = create_error_responses(post_wallet_exceptions)
