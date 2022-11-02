import os

import pymongo
from dotenv import load_dotenv
# from fastapi_auth._mongodb_access import MONGODB_URL

load_dotenv()

# function names

MONGODB_URL = os.getenv("MONGODB_URL")
connection = pymongo.MongoClient(MONGODB_URL)
db = connection["test"]
mycol = db["users"]
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
# mycol.insert_one(mydict)
# print("done")

data = list()
for x in mycol.find():
    data.append(x)
    print(data)

email = "emal"
username= "username"


if email in mycol.find_one({'email': email}):
    print("This username exists!")
else:
    except Exception as e:
        
    print("done")


# value = data[0]["email"]
# print(value)

# import pymongo

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]

# myquery = { "address": "Park Lane 38" }

# if myquery in mycol.find(myquery):
# 	print("This data exists")
# else:
#     print("this data does not exist")