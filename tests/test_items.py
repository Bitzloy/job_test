import pytest
import uuid


from checklists.storages.checklist_item_storage import OrmItemRepository
from checklists.storages.checklist_storage import OrmChecklistRepository
from checklists.entities.checklist_item import ChecklistItem
from checklists.exceptions import (
    ItemNotFoundApiError,
    CheckListNotFoundApiError,
)
from checklists.commands.item import UpdateItemCommand, UpdateItemRequestDTO, CreateItemCommand, CreateItemRequestDTO


def test_create_item(
    client, item_repository: OrmItemRepository, create_orm_checklists
):
    checklist = create_orm_checklists(
        title="checklist", description="ya checklist"
    )
    item = ChecklistItem.create(
        title="дело", is_done=False, checklist_uuid=checklist[0].uuid
    )

    item_repository.add(item)
    response = client.get(f"/api/checklists/{item.checklist_uuid}/items")
    json_response = response.json

    assert json_response[0]["checklist_uuid"] == checklist[0].uuid
    assert json_response[0]["title"] == "дело"
    assert json_response[0]["is_done"] == False

    item_repository.remove(json_response[0]["id"])


def test_get_all(create_orm_checklists, item_repository, create_items):
    checklist = create_orm_checklists(
        title="checklist", description="ya checklist"
    )
    items = [
        create_items(
            title="дело", is_done=False, checklist_uuid=checklist[0].uuid
        ),
        create_items(
            title="дело2", is_done=True, checklist_uuid=checklist[0].uuid
        ),
    ]

    expected_result = item_repository.get_all(checklist_uuid=checklist[0].uuid)
    assert isinstance(expected_result[0], ChecklistItem)
    assert isinstance(expected_result[1], ChecklistItem)
    assert len(expected_result) == 2
    assert expected_result[0].title == "дело"
    assert expected_result[1].title == "дело2"
    assert expected_result[0].is_done == False
    assert expected_result[1].is_done == True


def test_remove_item_by_id(create_orm_checklists, item_repository):
    checklist = create_orm_checklists(
        title="checklist", description="ya checklist"
    )
    item = ChecklistItem.create(
        title="дело", is_done=False, checklist_uuid=checklist[0].uuid
    )
    new_item = item_repository.add(item)

    item_repository.remove(new_item.id)
    expected_result = item_repository.get_all(checklist_uuid=checklist[0].uuid)

    assert expected_result == []


def test_get_by_id(create_orm_checklists, item_repository):
    checklist = create_orm_checklists(
        title="checklist", description="ya checklist"
    )
    item = ChecklistItem.create(
        title="дело", is_done=False, checklist_uuid=checklist[0].uuid
    )
    new_item = item_repository.add(item)

    expected_result = item_repository.get_by_id(item_id=new_item.id)

    assert expected_result.id == new_item.id

    item_repository.remove(new_item.id)


def test_update_item(item_repository, create_orm_checklists, orm_checklist_repo, create_items):
    checklist = create_orm_checklists(
        title="checklist", description="ya checklist"
    )
    item = create_items(title="Я дело", is_done=False, checklist_uuid=checklist[0].uuid)
    another_data = {"title": "я дело22", "is_done": True, "checklist_uuid": checklist[0].uuid}
    
    
    
    updated_item = UpdateItemCommand(
        item_repo=item_repository,
        checklist_repo=orm_checklist_repo
    ).execute(
        UpdateItemRequestDTO(
            id=item[0].id,
            title=another_data["title"],
            is_done=another_data["is_done"],
            checklist_uuid=another_data["checklist_uuid"]
        )
    )
    
    assert updated_item.title == another_data["title"]
    assert updated_item.is_done == another_data["is_done"]
    assert updated_item.checklist_uuid == uuid.UUID(another_data["checklist_uuid"] )
    

    


def test_delete_not_exists_item(item_repository):
    with pytest.raises(ItemNotFoundApiError):
        item_repository.remove(10)


def test_create_item_without_checklist(item_repository, orm_checklist_repo):
    with pytest.raises(CheckListNotFoundApiError):
        data = {"title": "я дело", "is_done": False, "checklist_uuid": uuid.uuid4()}
        item = CreateItemCommand(
            item_repo=item_repository,
            checklist_repo=orm_checklist_repo,
            checklist_item=ChecklistItem).execute(
            data=CreateItemRequestDTO(
                title=data["title"],
                is_done=data["is_done"],
                checklist_uuid=data["checklist_uuid"]
            )
        )


