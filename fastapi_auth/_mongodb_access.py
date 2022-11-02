import os
import threading
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Tuple


from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi_auth.endpoints import DATABASE_MODE

import pymongo
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


load_dotenv()

try:
    if DATABASE_MODE == "mongodb":
        MONGODB_URL = os.getenv("MONGODB_URL")
    else:
        pass
except KeyError as e:
    print("DATABASE_MODE not set. Default=SQLite3 Database")
    pass

#myclient = pymongo.MongoClient(MONGODB_URL)

# mydb = myclient["mydatabase"]
# mydb = myclient["mydatabase"]
# mycol = mydb["user_database"]
# #mydict = {"username":, "email":,"password":}
# print(myclient.list_database_names())
# print("done")

class MongodbAccess:
    """Class handling Remote Mongodb connection and writes. Change MONGODB_URI, if migrating database to a new location."""
    def __init__(self):
        try:
             # Connect to an existing database
            connection = pymongo.MongoClient(MONGODB_URL)
            mydb = connection["mydatabase"]
            mytable = mydb["user_database"]
            # Print PostgreSQL details
            print(mydb.list_database_names())
            print("You are connected to - ", mytable.list_database_names(), "\n")
        except Exception as e:
            print("Error while connecting to mongodb database!", e)
            
        def init_db(self):
        """
        The init_db function creates a new database if one does not exist.
        It also migrates the old user_database to the new format, and adds columns for email, password, and username.

        Args:
            self: Access variables that belong to the class

        Returns:
            The connection to the database
        """
        try:

            host = os.getenv("MYSQL_HOST_NAME")
            database = os.getenv("MYSQL_DATABASE")
            user = os.getenv("MYSQL_USER")
            password = os.getenv("MYSQL_PASSWORD")
            connection = pymysql.connect(
                host=host, database=database, user=user, password=password
            )
            c = connection.cursor()
            # Create database
            c.execute(
                """
            CREATE TABLE IF NOT EXISTS user_database (
                api_key TEXT PRIMARY KEY,
                is_active INTEGER,
                never_expire INTEGER,
                expiration_date TEXT,
                latest_query_date TEXT,
                total_queries INTEGER)
            """
            )
            connection.commit()
            # Migration: Add api key username
            try:
                c.execute(
                    "ALTER TABLE user_database ADD COLUMN IF NOT EXISTS username TEXT"
                )
                c.execute(
                    "ALTER TABLE user_database ADD COLUMN IF NOT EXISTS email TEXT"
                )
                c.execute(
                    "ALTER TABLE user_database ADD COLUMN IF NOT EXISTS password TEXT"
                )
                connection.commit()
            except pymysql.err.OperationalError as e:
                pass
        except (pymysql.err.OperationalError, KeyError) as e:
            print("Error while connecting to MySQL:", e)
            # pass  # Column already exist
            

mongodb_access = MongodbAccess()