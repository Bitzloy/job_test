import traceback

from flask import jsonify


class ApiError(Exception):
    message = None
    status_code = None
    details = None


class WalletNotFoundApiError(ApiError):
    message = "WALLET_NOT_FOUND"
    status_code = 404
    details = {
        "status_code": status_code,
        "field": "UUID",
        "message": "Кошелек с таким UUID не найден/не существует!",
    }


class MoneyNotEnoughApiError(ApiError):
    message = "MONEY_NOT_ENOUGH"
    status_code = 403
    details = {
        "status_code": status_code,
        "field": "balance",
        "message": "Недостаточно средств!",
    }


def handle_api_errors(error):
    response = jsonify({"code": error.message, "details": error.details})
    response.status_code = error.status_code
    return response


def handle_other_errors(error):
    response = jsonify({"code": "INTERNAl", "details": "Ошибка кода"})
    response.status_code = 500
    traceback.print_exc()
    return response
