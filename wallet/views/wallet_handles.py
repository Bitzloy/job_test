import uuid

from flask import (
    Blueprint,
    jsonify,
)
from flask_pydantic import validate

from wallet.commands.command import (
    GetBalanceCommand,
    UpdateWalletCommand,
    UpdateWalletRequestDTO,
)
from wallet.database import db
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


@wallet_blueprint.post("/<wallet_uuid>/operation")
@validate()
def update_wallet(wallet_uuid: uuid.UUID, body: UpdateWalletRequestDTO):
    wallet = UpdateWalletCommand(wallet_repo=OrmWalletRepo(db)).execute(
        body, wallet_uuid
    )
    return jsonify(wallet)


@wallet_blueprint.get("/<uuid:wallet_uuid>/")
def get_wallet_balance(wallet_uuid):
    balance = GetBalanceCommand(wallet_repo=OrmWalletRepo(db)).execute(
        uuid=wallet_uuid
    )
    return jsonify(balance)
