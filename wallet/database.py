from peewee import * 

# db = PostgresqlDatabase(database="pgdb", user="lol", password="example", host="pgdb", port=5432)
db = SqliteDatabase("./database.db")