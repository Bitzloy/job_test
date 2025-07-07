import pytest
import uuid
from dataclasses import asdict

from checklists.commands.checklist import UpdateChecklistCommand, CreateChecklistCommand, CreateChecklistRequestDTO, UpdateChecklistRequestDTO
from checklists.entities.checklist import CheckList



def test_update_checklist(orm_checklist_repo, create_orm_checklists):
    
    checklist = create_orm_checklists(title="dsds", description="dsawwe")
    body = {"title": "я новый", "description": "самый новый", "is_done": True}
    
    updated_checklist = UpdateChecklistCommand(orm_checklist_repo).execute(checklist[0].uuid, 
                                                                           data=UpdateChecklistRequestDTO(
                                                                                title=body["title"],
                                                                                description=body["description"],
                                                                                is_done=body["is_done"]
))
    
    if isinstance(updated_checklist, CheckList):
        assert updated_checklist.title == "я новый"
        assert updated_checklist.description == "самый новый"
        assert updated_checklist.is_done == True
        
    else:
        assert updated_checklist["title"] == "я новый"
        assert updated_checklist["description"] == "самый новый"
        assert updated_checklist["is_done"] == True
        
        
        
def test_create_checklist(client, orm_checklist_repo):
    data = {"title": "YA checklist", "description": "Eto checklist", "is_done": False}
    created_checklist = CreateChecklistCommand(CheckList, orm_checklist_repo).execute(CreateChecklistRequestDTO(
        title=data["title"],
        description=data["description"],
    ))
    
    response = client.get(f"/api/checklists/{created_checklist.uuid}")
    json_response = response.json
    
    assert created_checklist.uuid == uuid.UUID(json_response["uuid"])
    assert created_checklist.title == json_response["title"]
    assert created_checklist.is_done == json_response["is_done"]
    
    orm_checklist_repo.remove(created_checklist.uuid)