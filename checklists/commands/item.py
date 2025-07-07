import abc
from dataclasses import dataclass, asdict
import uuid
from pydantic import BaseModel, field_validator, Field

from checklists.storages.checklist_item_storage import OrmItemRepository, Checklist_item_model, AbstractChecklistItemRepository
from checklists.storages.checklist_storage import OrmChecklistRepository, Checklist_model, AbstractChecklistsRepository
from checklists.exceptions import CheckListNotFoundApiError, ValidationApiError
from checklists.entities.checklist_item import ChecklistItem



class CreateItemRequestDTO(BaseModel):
    title: str
    is_done: bool
    checklist_uuid: uuid.UUID
    
    @field_validator("title", mode="before")
    def check_title(cls, value):
        if len(value) > 50 or len(value) < 3:
            raise ValidationApiError("Не корректное название")
        return value


class UpdateItemRequestDTO(CreateItemRequestDTO):
    id: int

    

    

class AbstractCommand(abc.ABC):
    
    @abc.abstractmethod
    def execute(self):
        pass


class UpdateItemCommand(AbstractCommand):
    def __init__(self, 
                 item_repo: AbstractChecklistItemRepository,
                 checklist_repo: AbstractChecklistsRepository):
        
        self.item_repo = item_repo
        self.checklist_repo = checklist_repo
    
    
    def execute(self, data: UpdateItemRequestDTO):
        id = data.id
        item = self.item_repo.get_by_id(id)
        if item.checklist_uuid != data.checklist_uuid:
            if not self.checklist_repo.get_by_id_or_none(data.checklist_uuid):
                raise CheckListNotFoundApiError()
        item.update(
            title=data.title,
            is_done=data.is_done,
            checklist_uuid=data.checklist_uuid
        )
        return self.item_repo.update(item)
    
    

class CreateItemCommand(AbstractCommand):
    def __init__(self, 
                 item_repo: AbstractChecklistItemRepository,
                 checklist_repo: AbstractChecklistsRepository,
                 checklist_item : ChecklistItem):
    
        self.item_repo = item_repo
        self.checklist_repo = checklist_repo
        self.checklist_item = checklist_item
    
    
    def execute(self, data: CreateItemRequestDTO):
        if not self.checklist_repo.get_by_id_or_none(data.checklist_uuid):
            raise CheckListNotFoundApiError()
        
        item = self.checklist_item.create(
        title=data.title,
        is_done=data.is_done,
        checklist_uuid=data.checklist_uuid,
    )
        return self.item_repo.add(item)
       