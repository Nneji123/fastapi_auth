import os
from fastapi_auth.endpoints import DATABASE_MODE

import pymongo

from dotenv import load_dotenv

load_dotenv()

try:
    if DATABASE_MODE == "mongodb":
        MONGODB_URL = os.getenv("MONGODB_URL")
    else:
        pass
except KeyError as e:
    print("DATABASE_MODE not set. Default=SQLite3 Database")
    pass

myclient = pymongo.MongoClient(MONGODB_URL)

mydb = myclient["mydatabase"]
print(myclient.list_database_names())
print("done")