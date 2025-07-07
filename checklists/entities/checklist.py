import uuid
import datetime
from dataclasses import dataclass, asdict

from checklists.exceptions import (
    CheckListNotFoundApiError,
    ChecklistValidationApiError,
)


@dataclass
class CheckList:
    UPDATABLE_FIELDS = ["title", "description", "is_done"]
    title: str
    uuid: uuid
    created_at: datetime.datetime
    updated_at: datetime.datetime
    description: str
    is_done: bool

    def change_title(self, title: str):
        self.title = title

    @classmethod
    def create(cls, title: str, description: str) -> "CheckList":
        # if len(title) < 50 and len(title) > 3:
            return cls(
                title=title,
                uuid=uuid.uuid4(),
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
                description=description,
                is_done=False,
            )
        # else:
        #     raise ChecklistValidationApiError()


    def update(self, title: str, description: str, is_done: bool) -> None:
        is_updated = False
        un_updated_fields = (self.title, self.description, self.is_done)
        self.title = title
        self.description = description
        self.is_done = is_done
        updated_fields = (self.title, self.description, self.is_done)
        
        if un_updated_fields != updated_fields:
            is_updated = True
        
        if is_updated:
            self.updated_at = datetime.datetime.now()
            
            
            

    # def update(self, data: dict) -> None:
    #     is_updated = False
    #     for key in self.UPDATABLE_FIELDS:
    #         if data.get(key) and getattr(self, key) != data.get(key):
    #             # if data[key] == "title" and len(data[key]) < 50 or len(data[key]) > 3:
    #             if (
    #                 data.get("title")
    #                 and len(data["title"]) < 50
    #                 and len(data["title"]) > 3
    #             ):
    #                 setattr(self, key, data[key])
    #                 is_updated = True
    #             else:
    #                 raise ChecklistValidationApiError()
    #     if is_updated:
    #         self.updated_at = datetime.datetime.now()
