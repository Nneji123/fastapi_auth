"""Main dependency for other endpoints.
"""

import os
from re import L

from dotenv import load_dotenv
from fastapi import Security
from fastapi.security import APIKeyHeader, APIKeyQuery
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from fastapi_auth._mysql_access import mysql_access
from fastapi_auth._postgres_access import postgres_access
from fastapi_auth._sqlite_access import sqlite_access

load_dotenv()
API_KEY_NAME = "api-key"

api_key_query = APIKeyQuery(
    name=API_KEY_NAME, scheme_name="API key query", auto_error=False
)
api_key_header = APIKeyHeader(
    name=API_KEY_NAME, scheme_name="API key header", auto_error=False
)


try:
    DATABASE_MODE = os.getenv("DATABASE_MODE")
    if DATABASE_MODE == "postgres":
        dev = postgres_access
    elif DATABASE_MODE == "mysql":
        dev = mysql_access
    else:
        dev = sqlite_access
except KeyError as e:
    print("DATABASE_MODE not set. Default=SQLite3 Database")
    dev = sqlite_access


async def api_key_security(
    query_param: str = Security(api_key_query),
    header_param: str = Security(api_key_header),
):
    """
    The api_key_security function is a custom type that checks for the presence of an API key in the query string and header.
    If no API key is present, it raises an HTTPException with status code 403.
    If an invalid or revoked API key is found, it also raises an HTTPException with status code 403.

    Args:
        query_param:str=Security(api_key_query): Pass the api_key as a query parameter
        header_param:str=Security(api_key_header): Pass the api key in the header
        : Check if the api key is in the query string or not

    Returns:
        The api key if it is passed in the query string or header
    """
    if not query_param and not header_param:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="An API key must be passed as query or header",
        )

    elif query_param and dev.check_key(query_param):
        return query_param

    elif header_param and dev.check_key(header_param):
        return header_param

    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Wrong, revoked, or expired API key."
        )
