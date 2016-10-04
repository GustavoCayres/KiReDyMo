from peewee import *

from .base_model import BaseModel


class Organism(BaseModel):
    """ Class containing data on the organism. """

    name = CharField(max_length=30, primary_key=True)
