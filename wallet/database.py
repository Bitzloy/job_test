import psycopg2

from peewee import *

# from psycopg2.extensions import ISOLATION_LEVEL_SERIALIZABLE

# db = PostgresqlDatabase(
#     database="pgdb", user="lol", password="example", host="pgdb", port=5432
# )
# # db = SqliteDatabase("./database.db")
# # db = PostgresqlDatabase()

# db.init('pgdb', isolation_level=psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)


def make_db():
    db = PostgresqlDatabase(
        database="pgdb", user="lol", password="example", host="pgdb", port=5432
    )
    db.init(
        "pgdb",
        isolation_level=psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
    )

    return db
