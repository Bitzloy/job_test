import abc
from peewee import *
import uuid

from checklists.entities.checklist_item import ChecklistItem
from checklists.entities.checklist import CheckList
from checklists.database import db
from checklists.storages.checklist_storage import BaseModel, Checklist_model
from checklists.exceptions import (
    ItemNotFoundApiError,
    CheckListNotFoundApiError,
)


class AbstractChecklistItemRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, item: ChecklistItem) -> None:
        pass

    @abc.abstractmethod
    def update(self, item: ChecklistItem) -> ChecklistItem:
        pass

    @abc.abstractmethod
    def remove(self, item: ChecklistItem) -> str | None:
        pass

    @abc.abstractmethod
    def get_all(self, checklist_uuid: str) -> list[ChecklistItem]:
        pass

    @abc.abstractmethod
    def get_by_id(self, item_id: int) -> ChecklistItem:
        pass
    
    @abc.abstractmethod
    def from_query_to_object(self, query) -> ChecklistItem:
        pass


class Checklist_item_model(BaseModel):
    title = CharField()
    checklist_uuid = CharField()
    # checklist_id = ForeignKeyField(Checklist_model,  backref="item")
    # checklist_id = ForeignKeyField(Checklist_model, backref=Checklist_model.id)
    is_done = BooleanField()
    id = AutoField()

    class Meta:
        table_name = "checklist_item"
        order_by = "checklist_id"


class OrmItemRepository(AbstractChecklistItemRepository):
    def __init__(self, db: Database):
        self.db = db


    def add(self, item: ChecklistItem) -> None:
        created_item = Checklist_item_model.create(
            title=item.title,
            is_done=item.is_done,
            checklist_uuid=item.checklist_uuid,
        )
        return self.from_query_to_object(created_item)


    
    def update(self, item: ChecklistItem) -> ChecklistItem|None:
        Checklist_item_model.update(
            title=item.title, 
            is_done=item.is_done,
            checklist_uuid=item.checklist_uuid
        ).where(Checklist_item_model.id == item.id).execute()
        return item
            

    def remove(self, id: int) -> str | None:
        deleted_item = Checklist_item_model.delete_by_id(id)
        if deleted_item == 0:
            raise ItemNotFoundApiError()
        return "Deleted"


    def get_all(self, checklist_uuid) -> list[ChecklistItem]:

        items = []
        query = Checklist_item_model.select().where(
            Checklist_item_model.checklist_uuid == checklist_uuid
        )
        for item in query:
            items.append(self.from_query_to_object(query=item))
        return items

    def get_by_id(self, item_id) -> ChecklistItem:
        try:
            query = Checklist_item_model.get_by_id(pk=item_id)
            item = self.from_query_to_object(query)
            return item
        except DoesNotExist:
            raise ItemNotFoundApiError()

    def from_query_to_object(self, query) -> ChecklistItem:
        item = ChecklistItem(
            title=query.title,
            checklist_uuid=query.checklist_uuid,
            is_done=query.is_done,
            id=query.id,
        )
        return item
