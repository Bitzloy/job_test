from flask import Flask, jsonify, g

import traceback
import inject
from inject import *

from checklists.storages.checklist_storage import (
    CheckListStorage,
    SqliteChecklistRepository,
    AbstractChecklistsRepository,
    OrmChecklistRepository,
)
from checklists.exceptions import ApiError, ValidationApiError
from checklists.views.checklists_handles import blueprint
from checklists.views.items_handles import item_blueprint
from checklists.database import db
from checklists.di_containers import di_configure


def validation_api_errors(error):
    response = jsonify({"message": error.message})
    response.status_code = error.status_code
    return response


def handle_api_errors(error):
    response = jsonify({"code": error.message, "details": error.details})
    response.status_code = error.status_code
    return response


def handle_other_errors(error):
    response = jsonify({"code": "INTERNAl", "details": "Ошибка кода"})
    response.status_code = 500
    traceback.print_exc()
    return response




def create_app():

    app = Flask(__name__)

    app.register_blueprint(blueprint=blueprint)
    app.register_blueprint(blueprint=item_blueprint)

    app.register_error_handler(ApiError, handle_api_errors)
    app.register_error_handler(Exception, handle_other_errors)
    app.register_error_handler(ValidationApiError, validation_api_errors)
    # app.run(host="0.0.0.0", port=5000)

    # app.teardown_appcontext(close_connection)
    return app
