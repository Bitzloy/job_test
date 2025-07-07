from flask import Flask, Blueprint


from wallet.views.wallet_handles import wallet_blueprint


def create_app():

    app = Flask(__name__)

    app.register_blueprint(blueprint=wallet_blueprint)
  

    # app.register_error_handler(ApiError, handle_api_errors)
    # app.register_error_handler(Exception, handle_other_errors)
    # app.register_error_handler(ValidationApiError, validation_api_errors)
    # app.run(host="0.0.0.0", port=5000)

    # app.teardown_appcontext(close_connection)
    return app