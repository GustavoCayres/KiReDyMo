import os
import subprocess

from source.db_modules.database_insert import *
from source.models.base_model import BaseModel
BaseModel.set_database("tests/test_db/test_db.sqlite")
from source.db_modules.database_create import *

# prepare test database
create_tables()
insert_chromosome("c1", 20, 2, 5, "test1")
insert_replication_origin(5, "c1")
insert_replication_origin(7, "c1")
insert_transcription_region(3, 6, 1, 7, "c1")
insert_transcription_region(13, 16, 1, 7, "c1")

# run tests ignoring program's output
output = open(os.devnull, 'w')
subprocess.run("python3 -m unittest", shell=True, stdout=output)

# clean test environment
drop_tables()
