from flask import Flask, Blueprint


from wallet.views.wallet_handles import wallet_blueprint
from wallet.exceptions import handle_api_errors, ApiError, handle_other_errors


def create_app():

    app = Flask(__name__)

    app.register_blueprint(blueprint=wallet_blueprint)
    app.register_error_handler(ApiError, handle_api_errors)
    app.register_error_handler(Exception, handle_other_errors)
    
    return app