from peewee import * 
from playhouse.migrate import *


# from checklists.storages.checklist_storage import Checklist_model
# from checklists.storages.checklist_item_storage import Checklist_item_model



db = PostgresqlDatabase(database="pgdb", user="lol", password="example", host="localhost", port=5432)



class StartModel(Model):
    id = AutoField()
    class Meta:
        database = db
        
        
class ChecklistTable(StartModel):
    class Meta:
        table_name = "checklists"
        
    
class ItemTable(StartModel):
    class Meta:
        table_name = "checklist_item"



db.create_tables([ChecklistTable])
db.create_tables([ItemTable])  #создание таблицы с помощью модели


migrator = PostgresqlMigrator(db)



migrate(
    
    migrator.add_column(table="checklists", column_name="title", field=CharField(default="")),
    migrator.add_column(table="checklists", column_name="description", field=CharField(default="")),
    migrator.add_column(table="checklists", column_name="created_at", field=CharField(default="")),
    migrator.add_column(table="checklists", column_name="updated_at", field=CharField(default="")),
    migrator.add_column(table="checklists", column_name="uuid", field=CharField(default="")),
    migrator.add_column(table="checklists", column_name="is_done", field=BooleanField(default=False)),
    
    migrator.add_column(table="checklist_item", column_name="title", field=CharField(default="")),
    migrator.add_column(table="checklist_item", column_name="checklist_uuid", field=CharField(default="")),
    migrator.add_column(table="checklist_item", column_name="is_done", field=BooleanField(default=False))
)






















# database = SqliteDatabase('./checklists/database.db')

# # class UnknownField(object):
# #     def __init__(self, *_, **__): pass

# class BaseModel(Model):
#     class Meta:
#         database = database

# class Checklists(BaseModel):
#     created_at = TextField(null=True)
#     description = TextField(null=True)
#     is_done = IntegerField(null=True)
#     title = TextField(null=True)
#     updated_at = TextField(null=True)
#     uuid = TextField(null=True)

#     class Meta:
#         table_name = 'Checklists'

# # class ChecklistItem(BaseModel):
# #     checklist = ForeignKeyField(column_name='checklist_id', field='id', model=Checklists, null=True)
# #     is_done = IntegerField(null=True)
# #     title = TextField(null=True)

# #     class Meta:
# #         table_name = 'checklist_item'

# class ChecklistItm(BaseModel):
#     checklist_uuid = TextField(null=True)
#     is_done = IntegerField(null=True)
#     title = TextField(null=True)
#     # checklist_id = ForeignKeyField(Checklists)

#     class Meta:
#         table_name = 'checklist_itm'