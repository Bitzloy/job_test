from checklists.config import Config
from peewee import SqliteDatabase

config = Config()

DATABASE = Config.get_abspath() + config.get_db_path()
# db = SqliteDatabase(DATABASE) # переместить в database
