import sqlite3

from flask import g, Flask
from peewee import *
import datetime


from checklists.common import DATABASE

# db = SqliteDatabase(DATABASE)  # коннект к базе данных через peewee

db = PostgresqlDatabase(database="pgdb", user="lol", password="example", host="pgdb", port=5432)



def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class SqliteDB:
    _instance = None
    connect: sqlite3.Connection

    def __init__(self):
        self.connect = sqlite3.connect(DATABASE)
        self.connect.row_factory = self.make_dicts

    def __del__(self):
        self.connect.close()

    @staticmethod
    def make_dicts(cursor, row):
        return dict(
            (cursor.description[idx][0], value)
            for idx, value in enumerate(row)
        )

    # def __new__(cls, *args, **kwargs):
    #     if cls._instance is None:
    #         cls._instance = super().__new__(cls, *args, **kwargs)
    #     return cls._instance


# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#         # db.row_factory = sqlite3.Row
#         db.row_factory = make_dicts
#     return db


# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()
