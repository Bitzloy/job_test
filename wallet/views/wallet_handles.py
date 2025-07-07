from flask import Blueprint


wallet_blueprint = Blueprint(
    name="wallet", import_name=__name__, url_prefix="/api/v1/wallets/"
)


@wallet_blueprint.post('/')
def add_wallet():
    return "Hello world"

# @wallet_blueprint.post('/<WALLET_UUID:uuid>/withdraw')
