from flask import Blueprint, request, jsonify
from flask_pydantic import validate
from pydantic import BaseModel
import uuid


from wallet.commands.command import UpdateWalletCommand, GetBalanceCommand, UpdateWalletRequestDTO
from wallet.entities.wallet import Wallet
from wallet.storages.wallet_storage import OrmWalletRepo, AbstractWalletRepository
from wallet.database import db


wallet_blueprint = Blueprint(
    name="wallet", import_name=__name__, url_prefix="/api/v1/wallets/"
)

""" 
Будет искать кошелек по uuid и в случае если он существует, выполнит ее 
---
Создаст новый кошелек в случае если его не существует и операция ПОПОЛНЕНИЕ
или выкинет ошибку если операция СНЯТИЕ
"""




# @wallet_blueprint.post("/<uuid:wallet_uuid>/operation")
# def update_wallet(wallet_uuid):
#     body = request.get_json()
#     body = UpdateWalletRequestDTO(amount=body["amount"], operation_type=body["operation_type"])
#     # wallet_uuid = uuid.UUID(wallet_uuid)
#     # body = request.get_json()
#     wallet = UpdateWalletCommand(wallet_repo=OrmWalletRepo(db)).execute(
#         body, wallet_uuid
#     )
#     #  UpdateWalletRequestDTO(
#     #         amount=body["amount"],
#     #         operation_type=body["operation_type"],
#     #         uuid=wallet_uuid
#     #     )
#     return jsonify(wallet)
    
#     # wallet = UpdateWalletCommand(
#     #     operation=body["operation_type"],
#     #     amount=body["amount"],
#     #     wallet=Wallet
#     # ).execute(uuid=wallet_uuid, wallet_repo=OrmWalletRepo())
    






@wallet_blueprint.post("/<wallet_uuid>/operation")
@validate()
def update_wallet(wallet_uuid: uuid.UUID, body: UpdateWalletRequestDTO):
    # body = request.get_json()
    wallet = UpdateWalletCommand(
        wallet_repo=OrmWalletRepo(db)
        ).execute(body, wallet_uuid)
    return jsonify(wallet)
    
    


@wallet_blueprint.get("/<uuid:wallet_uuid>/")
def get_wallet_balance(wallet_uuid):
    balance = GetBalanceCommand(wallet_repo=OrmWalletRepo(db)).execute(uuid=wallet_uuid)
    return jsonify(balance)