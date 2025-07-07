import pandas as pd
import sqlite3

from checklists.common import DATABASE
print(DATABASE)

a = pd.read_sql(DATABASE, sqlite3.connect(DATABASE))

# from checklists.storages.checklist_storage import Checklist_model
# from checklists.storages.checklist_item_storage import Checklist_item_model