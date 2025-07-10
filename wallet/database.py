import psycopg2

from peewee import *

"""Инициализируем базу данных указывая уровень изоляции"""


def make_db():
    db = PostgresqlDatabase(
        database="pgdb", user="lol", password="example", host="pgdb", port=5432
    )
    db.init(
        "pgdb",
        isolation_level=psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
    )

    return db
