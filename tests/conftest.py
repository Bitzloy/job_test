import pytest
import sqlite3
from flask import Flask
import inject
from inject import Binder
import uuid


from checklists.database import DATABASE, db
from checklists.storages.checklist_storage import (
    SqliteChecklistRepository,
    OrmChecklistRepository,
    Checklist_model,
    AbstractChecklistsRepository,
)
from checklists.entities.checklist import CheckList
from checklists.storages.checklist_item_storage import OrmItemRepository
from checklists.entities.checklist_item import ChecklistItem

from checklists.di_containers import di_configure


from checklists.__init__ import create_app


# di_configure(binder=Binder)
# inject.configure(di_configure)


@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True})

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def make_dicts(cursor, row):
    return dict(
        (cursor.description[idx][0], value) for idx, value in enumerate(row)
    )


@pytest.fixture
def connect(app):
    db = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db


@pytest.fixture
def checklist_repository(connect):
    return inject.instance(AbstractChecklistsRepository)


@pytest.fixture
def create_checklist(
    checklist_repository,
    title: str = "Checklist",
    description: str = "Это чеклист",
):
    entities = []

    def create(title=title, description=description):

        checklist = CheckList.create(title=title, description=description)
        checklist_repository.add(checklist=checklist)

        checklist = checklist_repository.get_by_id(checklist.uuid)
        entities.append(checklist)

        return checklist

    yield create

    for checklist in entities:
        checklist_repository.remove(uuid=checklist.uuid)


@pytest.fixture
def orm_checklist_repo():
    return inject.instance(AbstractChecklistsRepository)


@pytest.fixture
def create_orm_checklists(
    title: str = "Checklist", description: str = "Это чеклист"
):
    orm_checklist_repo = inject.instance(AbstractChecklistsRepository)
    entities = []

    def create(title=title, description=description):

        checklist = CheckList.create(title=title, description=description)
        orm_checklist_repo.add(checklist)

        checklist = orm_checklist_repo.get_by_id(checklist.uuid)
        entities.append(checklist)

        return entities

    yield create

    for checklist in entities:
        orm_checklist_repo.remove(checklist.uuid)


@pytest.fixture
def item_repository():
    return OrmItemRepository(db)


@pytest.fixture
def create_items(
    title: str = "Дело", is_done: bool = False, checklist_uuid: uuid = None
):
    item_repository = OrmItemRepository(db)
    entities = []

    def create(title=title, is_done=is_done, checklist_uuid=checklist_uuid):

        item = ChecklistItem.create(
            title=title, is_done=is_done, checklist_uuid=checklist_uuid
        )
        query = item_repository.add(item)

        new_item = item_repository.get_by_id(query.id)
        entities.append(new_item)

        return entities

    yield create

    for item in entities:
        item_repository.remove(item.id)
