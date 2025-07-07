from flask import Blueprint, request, jsonify

from wallet.commands.command import UpdateWalletCommand
from wallet.entities.wallet import Wallet
from wallet.storages.wallet_storage import OrmWalletRepo


wallet_blueprint = Blueprint(
    name="wallet", import_name=__name__, url_prefix="/api/v1/wallets/"
)


@wallet_blueprint.post('/<wallet_uuid:uuid>/operation')
def update_wallet(wallet_uuid):
    body = request.get_json()
    wallet = UpdateWalletCommand(
        operation=body["operation_type"],
        amount=body["amount"],
        wallet=Wallet
    ).execute(uuid=wallet_uuid, wallet_repo=OrmWalletRepo)
    return jsonify(wallet)

# @wallet_blueprint.post('/<WALLET_UUID:uuid>/withdraw')
