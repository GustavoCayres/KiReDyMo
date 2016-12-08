#!/usr/bin/python3
import sys
import os
import subprocess

from source.database_management.database_insert import *
from source.models.base_model import BaseModel
BaseModel.set_database("tests/test_db/test_db.sqlite")
from source.database_management.database import *

# prepare test database
drop_tables()
create_tables()
insert_chromosome("c1", 20, 2, 5, "test1")
insert_replication_origin(position=0, start_probability=1, chromosome="c1")
insert_replication_origin(position=5, start_probability=1, chromosome="c1")
insert_replication_origin(position=7, start_probability=1, chromosome="c1")
insert_transcription_region(3, 6, 1, 7, "c1")
insert_transcription_region(13, 16, 1, 7, "c1")

# run tests ignoring program's output
output = open(os.devnull, 'w')
subprocess.run("python3 -m unittest", shell=True, stdout=sys.stderr)

# clean test environment
drop_tables()
