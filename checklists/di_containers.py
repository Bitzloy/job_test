from checklists.storages.checklist_storage import (
    OrmChecklistRepository,
    SqliteChecklistRepository,
    AbstractChecklistsRepository,
)

from checklists.database import db, SqliteDB
import inject
from inject import *

from flask import current_app


def di_configure(binder: Binder):
    binder.bind(AbstractChecklistsRepository, OrmChecklistRepository(db))
    # binder.bind(AbstractChecklistsRepository, SqliteChecklistRepository(SqliteDB())) # Подключение через sql


inject.configure(di_configure)
# checklist_repo = inject.instance(AbstractChecklistsRepository)
