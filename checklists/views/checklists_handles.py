from flask import request, jsonify, Blueprint, current_app
from dataclasses import asdict
import sqlite3
import inject
from datetime import datetime

from checklists.entities.checklist import CheckList
from checklists.database import db
from checklists.storages.checklist_storage import (
    SqliteChecklistRepository,
    OrmChecklistRepository,
    AbstractChecklistsRepository,
)
from checklists.commands.checklist import CreateChecklistCommand, UpdateChecklistCommand, CreateChecklistRequestDTO, UpdateChecklistRequestDTO

# from checklists.di_containers import checklist_repo


blueprint = Blueprint(
    name="checklists", import_name=__name__, url_prefix="/api/checklists"
)


@blueprint.post("/")
@inject.params(checklist_repo=AbstractChecklistsRepository)
def create_checklist(checklist_repo=None):

    body = request.get_json()
    checklist = CreateChecklistCommand(
        checklist=CheckList,
        checklist_repo=checklist_repo
    ).execute(
        CreateChecklistRequestDTO(
            title=body["title"],
            description=body["description"]
        )
    )
    return jsonify(checklist)


@blueprint.get("/")
@inject.params(checklist_repo=AbstractChecklistsRepository)
def get_checklists(checklist_repo=None):
    return jsonify(checklist_repo.get_all())



@blueprint.get("/<uuid:uuid>")
@inject.params(checklist_repo=AbstractChecklistsRepository)
def get_checklist_by_id(uuid, checklist_repo=None):
    return jsonify(checklist_repo.get_by_id(uuid))



@blueprint.put("/<uuid:uuid>")
@inject.params(checklist_repo=AbstractChecklistsRepository)
def change_checklist(uuid, checklist_repo=None):
    body = request.get_json()
    updated_checklist = UpdateChecklistCommand(checklist_repo=checklist_repo).execute(
        uuid=uuid, 
        data=UpdateChecklistRequestDTO(
            title=body["title"],
            description=body["description"],
            is_done=body["is_done"]
        )
        # data=UpdateChecklistRequestDTO(
        #     title=body["title"],
        #     description=body["description"],
        #     is_done=body["is_done"]
        # )
    )
    return jsonify(updated_checklist)



@blueprint.delete("/<uuid:uuid>")
@inject.params(checklist_repo=AbstractChecklistsRepository)
def delete_checklist(uuid, checklist_repo=None):
    return jsonify(checklist_repo.remove(uuid))

