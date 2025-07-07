import sqlite3

from checklists.common import config, Config


DATABASE = Config.get_abspath() + config.get_db_path()
# DATABASE = "/home/bitzloy/Vs/net/checklists/database.db"

connect = sqlite3.connect(DATABASE)


# connect.row_factory = sqlite3.Row
cursor = connect.cursor()
cursor.execute(
    """INSERT INTO checklists(title, description, created_at, updated_at, is_done) VALUES(
                'privet', 'poka', 'now', 'now', 0);"""
)
connect.commit()
connect.close()
