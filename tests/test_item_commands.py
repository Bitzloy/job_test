import pytest
from dataclasses import asdict

from checklists.commands.item import CreateItemCommand, UpdateItemCommand, UpdateItemRequestDTO
from checklists.entities.checklist_item import ChecklistItem
from checklists.entities.checklist import CheckList


def test_create_item(orm_checklist_repo, item_repository, create_items):
    
    checklist = CheckList.create(title="dsds", description="dsawwe")
    orm_checklist_repo.add(checklist)
    
    item = create_items(title="Я дело", is_done=False, checklist_uuid=checklist.uuid)
    assert item[0].title == "Я дело"
    assert item[0].checklist_uuid == str(checklist.uuid)
    assert item[0].is_done == False
        
    orm_checklist_repo.remove(uuid=checklist.uuid)

    
    
    
    
def test_update_item(orm_checklist_repo, item_repository, create_items):
    
    checklist = CheckList.create(title="dsds", description="dsawwe")
    orm_checklist_repo.add(checklist)
    # data = {"title": "Я дело", "is_done": False, "checklist_id": checklist.uuid}
    # created_item = CreateItemCommand(
    #     item_repo=item_repository,
    #     checklist_repo=orm_checklist_repo,
    #     checklist_item=ChecklistItem
    # ).execute(data=data)
    
    item = create_items(title="Я дело", is_done=False, checklist_uuid=checklist.uuid)
    
    another_data = {"title": "Я другое дело", "is_done": True, "checklist_uuid": checklist.uuid, "id": item[0].id}
    updated_item = UpdateItemCommand(
        item_repo=item_repository,
        checklist_repo=orm_checklist_repo
    ).execute(data=UpdateItemRequestDTO(
        id=another_data["id"],
        title=another_data["title"],
        is_done=another_data["is_done"],
        checklist_uuid=another_data["checklist_uuid"]
    )
    )
    
    assert updated_item.title == "Я другое дело"
    assert updated_item.is_done == True
    assert updated_item.checklist_uuid == checklist.uuid
    assert updated_item.id == item[0].id   
    
    orm_checklist_repo.remove(uuid=checklist.uuid)
    # item_repository.remove(id=item[0].id)