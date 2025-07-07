import uuid
from datetime import datetime
import abc
import sqlite3

from flask import jsonify
from dataclasses import dataclass, asdict

from peewee import *


from checklists.exceptions import (
    CheckListNotFoundApiError,
    ChecklistValidationApiError,
    ChecklistIsExistApiError,
)
from checklists.database import SqliteDB, db
from checklists.entities.checklist import CheckList
from checklists.common import DATABASE


class AbstractChecklistsRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, checklist: CheckList) -> None:
        pass

    @abc.abstractmethod
    def remove(self, id: uuid) -> CheckList:
        pass

    @abc.abstractmethod
    def get_all(self) -> list[CheckList]:
        pass

    @abc.abstractmethod
    def get_by_id(self, id: uuid.UUID) -> CheckList:
        pass

    @abc.abstractmethod
    def update(self, checklist: CheckList) -> CheckList:
        pass

    @abc.abstractmethod
    def from_query_to_checklist(self, query: "Checklist_model") -> CheckList:
        pass

    @abc.abstractmethod
    def get_by_id_or_none(self, uuid: uuid.UUID) -> CheckList:
        pass


class CheckListStorage(AbstractChecklistsRepository):
    def __init__(self):
        self.checklists: dict = {}

    def add(self, checklist: "CheckList") -> None:
        self.checklists[checklist.id] = checklist

    def remove(self, checklist: "CheckList") -> CheckList:
        return self.checklists.pop(checklist.id)

    def get_all(self) -> list[CheckList]:
        checklists = []
        for i in self.checklists:
            checklists.append(asdict(self.checklists[i]))
        return checklists

    def get_by_id(self, id) -> CheckList:
        for checklist in self.checklists:
            if checklist == id:
                return self.checklists[id]
        raise CheckListNotFoundApiError()

    def update(checklist):
        pass


class SqliteChecklistRepository(AbstractChecklistsRepository):
    def __init__(self, db: SqliteDB):
        # self.connect = get_db()
        self.db = db

    def add(self, checklist: CheckList) -> None:
        # cursor = self.db.connect.cursor()
        cursor = self.db.connect.cursor()
        if cursor.execute(
            f"""SELECT * FROM checklists WHERE uuid='{checklist.uuid}'"""
        ).fetchone():
            raise ChecklistIsExistApiError
        cursor.execute(
            f"""INSERT INTO checklists(title, description, created_at, updated_at, is_done, uuid) VALUES(
                '{checklist.title}', '{checklist.description}', '{checklist.created_at.strftime("%Y-%m-%d %H:%M:%S")}', 
                '{checklist.updated_at.strftime("%Y-%m-%d %H:%M:%S")}', {1 if checklist.is_done is True else 0}, '{checklist.uuid}');"""
        )
        self.db.connect.commit()

    def remove(self, uuid) -> None:
        cursor = self.db.connect.cursor()
        checklist_to_delete = cursor.execute(
            f"""SELECT title, description, created_at, updated_at, is_done,
                                         uuid FROM checklists WHERE uuid='{uuid}';"""
        ).fetchone()
        if checklist_to_delete:
            cursor.execute(f"""DELETE FROM checklists WHERE uuid='{uuid}';""")
            self.db.connect.commit()
            return checklist_to_delete
        else:
            raise CheckListNotFoundApiError()

    def get_all(self) -> list[CheckList]:
        checklists = []
        cursor = self.db.connect.cursor()
        query = cursor.execute(
            """SELECT title, description, created_at, updated_at, is_done, uuid FROM checklists ORDER BY created_at;"""
        ).fetchall()
        for elem in query:
            checklist = self.from_query_to_object(query=elem)
            checklists.append(checklist)
        return checklists
        # return query, checklists

    def get_by_id(self, uuid) -> CheckList:
        cursor = self.db.connect.cursor()
        query = cursor.execute(
            f"""SELECT title, description, created_at, updated_at, is_done, uuid FROM checklists WHERE uuid='{uuid}';"""
        ).fetchone()
        if query:
            checklist = self.from_query_to_object(query=query)
            return checklist
        else:
            raise CheckListNotFoundApiError
        # return query, checklist

    def update(self, checklist) -> CheckList:
        cursor = self.db.connect.cursor()
        cursor.execute(
            f"""UPDATE checklists SET title='{checklist.title}', description='{checklist.description}',
                        updated_at='{checklist.updated_at.strftime("%Y-%m-%d %H:%M:%S")}',
                        is_done='{checklist.is_done}' WHERE uuid='{checklist.uuid}';"""
        )
        self.db.connect.commit()
        return self.get_by_id(checklist.uuid)

    def from_query_to_object(self, query) -> CheckList:
        created_date_string = query["created_at"].split(".")[0]
        updated_date_string = query["updated_at"].split(".")[0]
        checklist = CheckList(
            title=query["title"],
            uuid=query["uuid"],
            created_at=datetime.strptime(
                created_date_string, "%Y-%m-%d %H:%M:%S"
            ),
            updated_at=datetime.strptime(
                updated_date_string, "%Y-%m-%d %H:%M:%S"
            ),
            description=query["description"],
            is_done=True if query["is_done"] == 1 else False,
        )
        return checklist


class BaseModel(Model):
    id = AutoField()

    class Meta:
        database = db
        # order_by = 'created_at'


class Checklist_model(BaseModel):
    title = CharField(default="")
    description = CharField(default="")
    created_at = CharField(default="")
    updated_at = CharField(default="")
    uuid = CharField(default="")
    is_done = BooleanField(default=False)

    class Meta:
        table_name = "checklists"
        order_by = "created_at"


class OrmChecklistRepository(AbstractChecklistsRepository):
    db: Database

    def __init__(self, db: Database):
        self.db = db

    def add(self, checklist: CheckList) -> None:
        added_checklist = Checklist_model.create(
            title=checklist.title,
            description=checklist.description,
            created_at=str(checklist.created_at).split(".")[0],
            updated_at=str(checklist.updated_at).split(".")[0],
            uuid=checklist.uuid,
            is_done=checklist.is_done,
        )
        return self.from_query_to_checklist(added_checklist)



    def get_by_id(self, uuid: uuid.UUID) -> CheckList:
        try:
            checklist = self.from_query_to_checklist(
                Checklist_model.get(Checklist_model.uuid == uuid)
            )
            return checklist
        except DoesNotExist:
            raise CheckListNotFoundApiError()
    
    
    def get_by_id_or_none(self, uuid: uuid.UUID) -> CheckList | None:
        
        model = Checklist_model.get_or_none(Checklist_model.uuid == uuid)
        if not model:
            return None
        
        return self.from_query_to_checklist(model)
    

    def get_all(self) -> list[CheckList]:
        checklists = []
        query = Checklist_model.select()
        for checklist in query:
            checklists.append(self.from_query_to_checklist(checklist))
        return checklists

    def remove(self, uuid) -> CheckList:
        try:
            checklist = Checklist_model.get(Checklist_model.uuid == uuid)
            checklist.delete_instance()
            return self.from_query_to_checklist(checklist)
        except DoesNotExist:
            raise CheckListNotFoundApiError

    """Обновление чеклиста в ручке"""

    def update(self, checklist: CheckList) -> CheckList:

        # Checklist_model.update(**asdict(checklist)).where(Checklist_model.uuid == checklist.uuid).execute()
        Checklist_model.update(
            title=checklist.title,
            description=checklist.description,
            updated_at=checklist.updated_at,
            created_at=checklist.created_at,
            is_done=checklist.is_done,
        ).where(Checklist_model.uuid == checklist.uuid).execute()
        
        return checklist


    def from_query_to_checklist(self, query: Checklist_model) -> CheckList:
        checklist = CheckList(
            title=query.title,
            description=query.description,
            is_done=query.is_done,
            #   is_done= True if query.is_done ==False else False,
            created_at=str(query.created_at).split(".")[0],
            updated_at=str(query.updated_at).split(".")[0],
            uuid=query.uuid,
        )
        # print(query.is_done)
        # print(query.__dict__)
        # print(checklist)
        return checklist
