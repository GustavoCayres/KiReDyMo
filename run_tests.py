import os
from source.models.base_model import BaseModel
BaseModel.set_database("tests/test_db/test_db.sqlite")
from source.db_modules.database_wrapper import *


connect()
create_tables()
insert_chromosome("c1", 20, 2, 5, "test1")
insert_replication_origin(5, "c1")
insert_replication_origin(7, "c1")
insert_transcription_region(13, 16, 1, 7, "c1")
os.system("python3 -m unittest tests/test_models/test_transcriptionRegion.py")
drop_tables()
close()
