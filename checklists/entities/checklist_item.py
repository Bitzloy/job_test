from dataclasses import dataclass
import uuid


@dataclass
class ChecklistItem:
    UPDATABLE_FIELDS = ["title", "is_done", "checklist_uuid"]
    title: str
    checklist_uuid: uuid.UUID
    is_done: bool
    id: int

    # def change_title(self, title: str):
    #     self.title = title

    @classmethod
    def create(
        cls,
        title: str,
        is_done: bool,
        checklist_uuid: uuid = None,
        id: int = None,
    ) -> "ChecklistItem":
        return cls(
            title=title, is_done=is_done, checklist_uuid=checklist_uuid, id=id
        )

    # def update(self, data: dict) -> None:
    #     for key in self.UPDATABLE_FIELDS:
    #         if data.get(key) and getattr(self, key) != data.get(key):
    #             setattr(self, key, data[key])

    def update(
        self, 
        title: str, 
        is_done: bool, 
        checklist_uuid: uuid.UUID
    ) -> None:
        
        self.title = title
        self.is_done = is_done
        self.checklist_uuid = checklist_uuid
        

# if __name__ == "__main__":
#     a = ChecklistItem.create("dsds", False)
#     print(a.__dict__)
