from peewee import *
from checklists.common import DATABASE

db = SqliteDatabase(DATABASE)


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = "created_at"


class Checklist_model(BaseModel):
    title = CharField()
    description = CharField()
    created_at = CharField()
    updated_at = CharField()
    uuid = CharField()
    is_done = BooleanField()

    class Meta:
        db_table = "checklists"


# a = Checklist_model.select()
# for i in a:
#     print(i.description)

# Checklist_model.create(title="sdsd", description="123")
