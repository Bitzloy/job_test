from flask import Blueprint, request, jsonify

from wallet.commands.command import UpdateWalletCommand, GetBalanceCommand
from wallet.entities.wallet import Wallet
from wallet.storages.wallet_storage import OrmWalletRepo


wallet_blueprint = Blueprint(
    name="wallet", import_name=__name__, url_prefix="/api/v1/wallets/"
)

""" 
Будет искать кошелек по uuid и в случае если он существует, выполнит ее 
---
Создаст новый кошелек в случае если его не существует и операция ПОПОЛНЕНИЕ
или выкинет ошибку если операция СНЯТИЕ
"""

@wallet_blueprint.post("/<uuid:wallet_uuid>/operation")
def update_wallet(wallet_uuid):
    body = request.get_json()
    wallet = UpdateWalletCommand(
        operation=body["operation_type"],
        amount=body["amount"],
        wallet=Wallet
    ).execute(uuid=wallet_uuid, wallet_repo=OrmWalletRepo())
    return jsonify(wallet)


@wallet_blueprint.get("/<uuid:wallet_uuid>/")
def get_wallet_balance(wallet_uuid):
    balance = GetBalanceCommand().execute(uuid=wallet_uuid, wallet_repo=OrmWalletRepo())
    return jsonify(balance)