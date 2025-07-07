from flask import Blueprint, request, jsonify


from checklists.storages.checklist_item_storage import OrmItemRepository
from checklists.entities.checklist_item import ChecklistItem
from checklists.storages.checklist_storage import OrmChecklistRepository
from checklists.database import db
from checklists.commands.item import UpdateItemCommand, UpdateItemRequestDTO, CreateItemCommand, CreateItemRequestDTO


# item_blueprint = Blueprint("checklist_item", import_name=__name__, url_prefix="/api/checklists/item")
item_blueprint = Blueprint(
    "checklist_item", import_name=__name__, url_prefix="/api"
)
item_repo = OrmItemRepository(db=db)


@item_blueprint.post("/items")
def create_item():
    body = request.get_json()
    item = CreateItemCommand(
        item_repo=OrmItemRepository(db),
        checklist_repo=OrmChecklistRepository(db),
        checklist_item=ChecklistItem).execute(
            CreateItemRequestDTO(
                title=body["title"],
                is_done=body["is_done"],
                checklist_uuid=body["checklist_uuid"]
            )
        )
    return jsonify(item)


@item_blueprint.get("/checklists/<uuid:uuid>/items")
def get_all_items(uuid):
    items = item_repo.get_all(uuid)
    return jsonify(items)


@item_blueprint.delete("/items/<id>")
def remove_item(id):
    item = item_repo.remove(id)
    return jsonify(item)


@item_blueprint.get("/items/<id>")
def get_by_id(id):
    item = item_repo.get_by_id(id)
    return jsonify(item)


@item_blueprint.put("/items/<id>")
def update_by_id(id):
    body = request.get_json()
    updated_item = UpdateItemCommand(
        checklist_repo=OrmChecklistRepository(db),
        item_repo=OrmItemRepository(db)
        ).execute(
            UpdateItemRequestDTO(
            id=id,
            title=body["title"],
            is_done=body["is_done"],
            checklist_uuid=body["checklist_uuid"]
        )
            )
    return jsonify(updated_item)
