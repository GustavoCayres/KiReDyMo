from peewee import *


db = SqliteDatabase('db/simulation_db.sqlite')


class BaseModel(Model):
    class Meta:
        database = db
