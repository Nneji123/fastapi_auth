"""Endpoints defined by the dependency.
"""
import os
import re
from typing import List, Optional


import bcrypt
from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_auth._postgres_access import postgres_access
from fastapi_auth._security_secret import secret_based_security
from fastapi_auth._sqlite_access import sqlite_access
from passwordgenerator import pwgenerator
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN

api_key_router = APIRouter()

show_endpoints = "FASTAPI_AUTH_HIDE_DOCS" not in os.environ

DEV_MODE = os.environ["DEV_MODE"]
if DEV_MODE == True:
    dev = sqlite_access
else:
    dev = postgres_access


def hash_password(password: str) -> str:
    """
    The hash_password function takes a string and returns the hashed version of that string.
    If no password is entered, it will return an error message.

    Args:
        password:str: Store the password that is entered by the user

    Returns:
        The hashed password
    """
    if password is not None:
        try:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(str(password).encode("utf-8"), salt)
            return hashed.decode("utf-8")
        except Exception as e:
            print(e)
    else:
        return "Invalid Password entered"


def email_validate(email_text: str):
    """
    The email_validate function takes in an email address as a string and returns the normalized form of that email address.
    If the inputted email is not valid, it raises an HTTPException with a status code of 403 Forbidden.

    Args:
        email_text:str: Store the email address that is inputted by the user

    Returns:
        The normalized form of the email address
    """
    try:
        # validate and get info
        v = validate_email(email_text)
        # replace with normalized form
        email_text = v["email"]
        return email_text
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="This is not a valid email address. Please input a valid email address.",
        )


def check_length_password(password: str) -> str:
    """
    The check_length_password function checks if the password is longer than 8 characters, contains an uppercase letter and digit.
    If it is not, then it will generate a new password for the user and return that instead.

    Args:
        password:str: Check if the password is at least 8 characters long, has a digit and an uppercase letter

    Returns:
        The password if it is longer than 8 characters, has at least one digit and uppercase letter
    """
    new_password = str(pwgenerator.generate())
    spec_char = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
    if len(password) <= 8:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f"This is password is too short (less than 8 characters). You can use this generated password instead: {new_password} or choose another password longer than 8 characters.",
        )
    elif re.search("[0-9]", password) is None:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f"The password must have at least one digit in it. You can use this generated password instead: {new_password} or choose another password longer than 8 characters.",
        )
    elif re.search("[A-Z]", password) is None:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f"The password must have at least one uppercase letter. You can use this generated password instead: {new_password} or choose another password longer than 8 characters.",
        )
    elif spec_char.search(password) == None:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f"The password must have at least one special character. You can use this generated password instead: {new_password} or choose another password longer than 8 characters.",
        )
    else:
        return password


@api_key_router.get(
    "/new",
    dependencies=[Depends(secret_based_security)],
    include_in_schema=show_endpoints,
)
def get_new_api_key(
    username: str = Query(
        None,
        description="set API key username",
    ),
    email: str = Query(
        None,
        description="set API key email",
    ),
    password: str = Query(
        None,
        description="set API key password. Must contain at least one uppercase letter, a digit and a special character.",
    ),
    never_expires: bool = Query(
        False,
        description="if set, the created API key will never be considered expired",
    ),
) -> str:
    """
    Returns:
        api_key: a newly generated API key
    """
    if password is not None:
        password = check_length_password(password)
        password = hash_password(password)
    if email is not None:
        email = email_validate(email)
    return dev.create_key(username, email, password, never_expires)


@api_key_router.get(
    "/revoke",
    dependencies=[Depends(secret_based_security)],
    include_in_schema=show_endpoints,
)
def revoke_api_key(
    api_key: str = Query(..., alias="api-key", description="the api_key to revoke")
):
    """
    Revokes the usage of the given API key

    """
    return dev.revoke_key(api_key)


@api_key_router.get(
    "/renew",
    dependencies=[Depends(secret_based_security)],
    include_in_schema=show_endpoints,
)
def renew_api_key(
    api_key: str = Query(..., alias="api-key", description="the API key to renew"),
    expiration_date: str = Query(
        None,
        alias="expiration-date",
        description="the new expiration date in ISO format",
    ),
):
    """
    Renews the chosen API key, reactivating it if it was revoked.
    """
    return dev.renew_key(api_key, expiration_date)


class UsageLog(BaseModel):
    api_key: str
    username: Optional[str]
    is_active: bool
    never_expire: bool
    expiration_date: str
    latest_query_date: Optional[str]
    total_queries: int
    email: str


class UsageLogs(BaseModel):
    logs: List[UsageLog]


@api_key_router.get(
    "/logs",
    dependencies=[Depends(secret_based_security)],
    response_model=UsageLogs,
    include_in_schema=show_endpoints,
)
def get_api_key_usage_logs():
    """
    Returns usage information for all API keys
    """
    # TODO Add some sort of filtering on older keys/unused keys?

    return UsageLogs(
        logs=[
            UsageLog(
                api_key=row[0],
                is_active=row[1],
                never_expire=row[2],
                expiration_date=row[3],
                latest_query_date=row[4],
                total_queries=row[5],
                username=row[6],
                email=row[7],
            )
            for row in dev.get_usage_stats()
        ]
    )
