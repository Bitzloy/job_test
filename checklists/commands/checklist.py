import abc
from flask import jsonify
import uuid
from pydantic import BaseModel, field_validator

from checklists.entities.checklist import CheckList
from checklists.storages.checklist_storage import AbstractChecklistsRepository
from checklists.exceptions import ChecklistIsExistApiError, CheckListNotFoundApiError, ChecklistValidationApiError
from checklists.exceptions import ValidationApiError



class CreateChecklistRequestDTO(BaseModel):
    title: str
    description: str
    
    @field_validator("title", mode="before")
    def check_title(cls, value):
        if len(value) > 50 or len(value) < 3:
            raise ChecklistValidationApiError()
        return value
    
    
class UpdateChecklistRequestDTO(CreateChecklistRequestDTO):
    is_done: bool



class AbstractChecklistCommand(abc.ABC):
    @abc.abstractmethod
    def execute(self):
        pass



class CreateChecklistCommand(AbstractChecklistCommand):
    def __init__(
        self, 
        checklist:CheckList,
        checklist_repo: AbstractChecklistsRepository
        ):
    
        self.checklist = checklist
        self.checklist_repo = checklist_repo
    
    def execute(self, data: CreateChecklistRequestDTO):
        checklist = self.checklist.create(
        title=data.title, 
        description=data.description
    )
        if self.checklist_repo.get_by_id_or_none(uuid=checklist.uuid):
            raise ChecklistIsExistApiError
        
        return self.checklist_repo.add(checklist)
    
 
 
class UpdateChecklistCommand(AbstractChecklistCommand):
    def __init__(self, checklist_repo: AbstractChecklistsRepository)-> None:
        self.checklist_repo = checklist_repo
    
    def execute(self, uuid: uuid.UUID, data: UpdateChecklistRequestDTO)-> CheckList:
        checklist_to_change = self.checklist_repo.get_by_id_or_none(uuid)
        if not checklist_to_change:
            raise CheckListNotFoundApiError()
        checklist_to_change.update(title=data.title, 
                                   is_done=data.is_done, 
                                   description=data.description)
        
        return self.checklist_repo.update(checklist_to_change)

 
 
 
 
 
 
 
 
# @dataclass
# class UpdateChecklistRequestDTO:
#     title: str
#     description: str
#     is_done: bool




""" Не видит что объект это инстанс датакласса"""
# class UpdateChecklistCommand(AbstractChecklistCommand):
#     def __init__(self, checklist_repo: AbstractChecklistsRepository)-> None:
#         self.checklist_repo = checklist_repo
    
#     def execute(self, uuid: uuid.UUID, data: UpdateChecklistRequestDTO)-> dict:
#         checklist_to_change = self.checklist_repo.get_by_id_or_none(uuid)
#         if not checklist_to_change:
#             raise CheckListNotFoundApiError()
#         # print(checklist_to_change)
#         # print(data)
#         data = asdict(data)
#         checklist_to_change.update(data)
#         # print(body)
#         # print(checklist_to_change)
#         updated_checklist = self.checklist_repo.update(checklist_to_change)
#         return asdict(updated_checklist)
        