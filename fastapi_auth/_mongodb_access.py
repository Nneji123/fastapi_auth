import os
import threading
from types import NoneType
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Tuple


from dotenv import load_dotenv
from fastapi import HTTPException


import pymongo
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

load_dotenv()

try:
    if (
        os.getenv("DATABASE_MODE") == "mongodb"
        and os.getenv("MONGODB_URL") is not None
    ):
        MONGODB_URL = os.getenv("MONGODB_URL")
    else:
        MONGODB_URL = None
except KeyError as e:
    print(e)


class MongodbAccess:
    """Class handling Remote Mongodb connection and writes. Change MONGODB_URI, if migrating database to a new location."""

    def __init__(self):
        try:
            # Connect to an existing database
            connection = pymongo.MongoClient(MONGODB_URL)
            mydb = connection["test"]
            mytable = mydb["user"]
            print("You are connected to - ", mytable.list_database_names, "\n")
        except Exception as e:
            print("Error while connecting to mongodb database!", e)

        try:
            self.expiration_limit = int(os.getenv("FASTAPI_AUTH_AUTOMATIC_EXPIRATION"))
        except KeyError:
            self.expiration_limit = 15

        self.init_db()

    def init_db(self):
        try:
            connection = pymongo.MongoClient(MONGODB_URL)
            db = connection["test"]
            mycol = db["user_database"]
            mydict = {
                "api_key": "api_key",
                "is_active": "is_active",
                "never_expire": "never_expire",
                "expiration_date": "expiration_date",
                "latest_query_date": "latest_query_date",
                "total_queries": "total_queries",
                "username": "username",
                "email": "email",
                "password": "password",
            }
            
            # Create database
            mycol.insert_one(mydict)
        except Exception as e:
            print("Error while using mongodb:", e)

    def create_key(self, username, email, password, never_expire) -> dict:
        api_key = str(uuid.uuid4())
        connection = pymongo.MongoClient(MONGODB_URL)
        db = connection["test"]
        mycol = db["user"]
        mydict = {
                "api_key": api_key,
                "is_active": 1,
                "never_expire": 1 if never_expire else 0,
                "expiration_date": (
                    datetime.utcnow() + timedelta(days=self.expiration_limit)
                ).isoformat(timespec="seconds"),
                "latest_query_date": None,
                "total_queries": 0,
                "username": username,
                "email": email,
                "password": password,
            }
        try:
            if email not in connection.db.mycol.find_one({"username": username}):
                mycol.insert_one(mydict)
                data = list()
                for x in mycol.find():
                    data.append(x)
                    print(data)
                return {"api-key": api_key}
            else:
                print("Error")
        except TypeError:
            # print()
            raise HTTPException(status_code=HTTP_403_FORBIDDEN,
                               detail = "This user already exists")
        # else:
        #     raise HTTPException(
        #         status_code=HTTP_403_FORBIDDEN,
        #         detail="This user already exists in the database",
        #     )
            

        


mongodb_access = MongodbAccess()
