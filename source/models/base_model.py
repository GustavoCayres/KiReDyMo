from peewee import *

db = SqliteDatabase("db/simulation_db.sqlite")


class BaseModel(Model):
    @staticmethod
    def set_database(path):
        global db
        db = SqliteDatabase(path)

    class Meta:
        database = db
