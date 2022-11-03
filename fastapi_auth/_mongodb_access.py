import os
import threading
from types import NoneType
from urllib import response
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
        """
        The init_db function creates a new database in MongoDB.
        
        
        Args:
            self: Reference the class itself
        
        Returns:
            A dictionary of the inserted document
        """
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
        """
        The create_key function creates a new api key for the user. It takes in username, email, password and never_expire as parameters. 
        It returns an api-key which is a string of random characters.
        
        Args:
            self: Access variables that belongs to the class
            username: Store the username of the user
            email: Check if the user already exists in the database
            password: Store the password of the user in a hashed format
            never_expire: Determine if the api key will expire or not
        
        Returns:
            A dictionary containing the api key
        """
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
        # check if user already exists in the mongodb database and if not, create a new user
        if (mycol.find_one({"username": username}) is None and mycol.find_one({"email": email}) is None):
            mycol.insert_one(mydict)
            # data = list()
            # for x in mycol.find():
            #     data.append(x)
            #     print(data)
            return {"api-key": api_key}
        else:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN,
                detail = "This user already exists")
            
            
            
    def renew_key(self, api_key: str, new_expiration_date: str) -> Optional[str]:
        """
        This method has not been fully implemented yet. Will be worked on in future updates.
        """
        raise HTTPException(status = HTTP_422_UNPROCESSABLE_ENTITY, detail="This endpoint is tot implemented yet with Mongodb")  



        # connection = pymongo.MongoClient(MONGODB_URL)
        # db = connection["test"]
        # mycol = db["user"]
        # response = mycol.find_one({"api_key": api_key})
       
        # if response is None:
        #     raise HTTPException(
        #         status_code=HTTP_404_NOT_FOUND, detail="API key not found"
        #     )

        #     # Without an expiration date, we set it here
        # if not new_expiration_date:
        #     parsed_expiration_date = (
        #         datetime.utcnow() + timedelta(days=self.expiration_limit)
        #     ).isoformat(timespec="seconds")

        # else:
        #     try:
        #         # We parse and re-write to the right timespec
        #         parsed_expiration_date = datetime.fromisoformat(
        #             new_expiration_date
        #         ).isoformat(timespec="seconds")
        #     except ValueError as exc:
        #         raise HTTPException(
        #             status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        #             detail="The expiration date could not be parsed. \
        #                     Please use ISO 8601.",
        #         ) from exc
        # response_lines = []
        # myquery = {"api_key": api_key, "expiration_date": new_expiration_date}
        # if mycol.find_one(myquery) is not None:
        #     newvalues = {"$set": {"expiration_date": parsed_expiration_date}}
        #     mycol.update_one(myquery, newvalues)
        #     response_lines.append(f"The expiration date has been set to {parsed_expiration_date}.")
        #     return " ".join(response_lines)
        # else:
        #     print("error")
            
            
    def revoke_key(self, api_key: str):
        """
        The revoke_key function takes an API key as a parameter and sets the is_active field to false.
        If the API key does not exist, it raises a 404 error.
        
        Args:
            self: Access variables that belongs to the class
            api_key:str: Specify the api_key that is to be revoked
        
        Returns:
            this api key has been revoked
        
        Doc Author:
            Trelent
        """
        connection = pymongo.MongoClient(MONGODB_URL)
        db = connection["test"]
        mycol = db["user"]
        myquery = {"api_key": api_key}
        if mycol.find_one(myquery) is not None:
            newvalues = {"$set": {"is_active": 0}}
            mycol.update_one(myquery, newvalues)
            return "This API key has been revoked." 
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="API key not found")


    def check_key(self, api_key: str) -> Optional[str]:
        """
        The check_key function has not been fully implemented yet. Will be worked on in future updates.
        """
        raise HTTPException(status = HTTP_422_UNPROCESSABLE_ENTITY, detail="This endpoint is tot implemented yet with Mongodb")  
    
    def get_usage_stats(self) -> List[Tuple[str, bool, bool, str, str, int, str, str]]:
        """
        The get_usage_stats function has not been fully implemented yet. Will be worked on in future updates.
        """
        raise HTTPException(status = HTTP_422_UNPROCESSABLE_ENTITY, detail="This endpoint is tot implemented yet with Mongodb")  
        
mongodb_access = MongodbAccess()
