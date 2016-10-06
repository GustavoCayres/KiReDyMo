from peewee import *


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase('db/simulation_db.sqlite')
