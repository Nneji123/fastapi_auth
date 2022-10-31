""""
Sqlite3 Database Connection Class. This class should be used in development. Set "DEV_MODE=True" as an environmental variable.
"""
import os
import sqlite3
import threading
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from fastapi import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


class SQLiteAccess:
    """Class handling SQLite connection and writes"""

    # TODO This should not be a class, a fully functional approach is better

    def __init__(self):
        try:
            self.db_location = os.environ["FASTAPI_AUTH_DB_LOCATION"]
        except KeyError:
            self.db_location = "sqlite.db"

        try:
            self.expiration_limit = int(os.environ["FASTAPI_AUTH_AUTOMATIC_EXPIRATION"])
        except KeyError:
            self.expiration_limit = 15

        self.init_db()

    def init_db(self):
        """
        The init_db function creates a new database file if one does not already exist.
        It also adds the necessary columns to the table for storing API keys.

        Args:
            self: Access variables that belongs to the class

        Returns:
            Nothing
        """
        with sqlite3.connect(self.db_location) as connection:
            c = connection.cursor()
            # Create database
            c.execute(
                """
        CREATE TABLE IF NOT EXISTS FASTAPI_AUTH (
            api_key TEXT PRIMARY KEY,
            is_active INTEGER,
            never_expire INTEGER,
            expiration_date TEXT,
            latest_query_date TEXT,
            total_queries INTEGER)
        """
            )
            connection.commit()
            # Migration: Add api key name
            try:
                c.execute("ALTER TABLE FASTAPI_AUTH ADD COLUMN name TEXT")
                c.execute("ALTER TABLE FASTAPI_AUTH ADD COLUMN email TEXT")
                c.execute("ALTER TABLE FASTAPI_AUTH ADD COLUMN password TEXT")
                connection.commit()
            except sqlite3.OperationalError:
                pass  # Column already exist

    def create_key(self, name, email, password, never_expire) -> str:
        """
        The create_key function creates a new API key for the user.

        Args:
            self: Access attributes of the class
            name: Identify the user
            email: Validate the email address
            password: Store the hashed password
            never_expire: Set the expiration date to none

        Returns:
            A string
        """
        api_key = str(uuid.uuid4())

        with sqlite3.connect(self.db_location) as connection:
            c = connection.cursor()
            c.execute(
                """SELECT name, email
                          FROM FASTAPI_AUTH
                          WHERE name=?
                              OR email=?""",
                (name, email),
            )
            result = c.fetchone()
            print(result)
            if result:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="This user already exists in the database. Please choose another username or password.",
                )
            else:
                c.execute(
                    """
                    INSERT INTO FASTAPI_AUTH
                    (api_key, is_active, never_expire, expiration_date, \
                        latest_query_date, total_queries, name, email, password)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        api_key,
                        1,
                        1 if never_expire else 0,
                        (
                            datetime.utcnow() + timedelta(days=self.expiration_limit)
                        ).isoformat(timespec="seconds"),
                        None,
                        0,
                        name,
                        email,
                        password,
                    ),
                )
                connection.commit()

        return api_key

    def renew_key(self, api_key: str, new_expiration_date: str) -> Optional[str]:
        """
        The renew_key function takes an API key and a new expiration date.
        If the API key is not found, it returns a 404 error.
        If the API key has already expired, it will be reactivated and return &quot;This API key was revoked and has been reactivated.&quot;
        Otherwise, if no new expiration date is given or if the provided one cannot be parsed as ISO 8601 (see https://en.wikipedia.org/wiki/ISO_8601#Time),
        the function will set its expiration date to 7 days from now by default.

        Args:
            self: Access the class attributes
            api_key:str: Check if the api key exists in the database
            new_expiration_date:str: Set a new expiration date for the api key

        Returns:
            A string with a message about the api key's new expiration date
        """
        with sqlite3.connect(self.db_location) as connection:
            c = connection.cursor()

            # We run the query like check_key but will use the response differently
            c.execute(
                """
            SELECT is_active, total_queries, expiration_date, never_expire
            FROM FASTAPI_AUTH
            WHERE api_key = ?""",
                (api_key,),
            )

            response = c.fetchone()

            # API key not found
            if not response:
                raise HTTPException(
                    status_code=HTTP_404_NOT_FOUND, detail="API key not found"
                )

            response_lines = []

            # Previously revoked key. Issue a text warning and reactivate it.
            if response[0] == 0:
                response_lines.append(
                    "This API key was revoked and has been reactivated."
                )

            # Without an expiration date, we set it here
            if not new_expiration_date:
                parsed_expiration_date = (
                    datetime.utcnow() + timedelta(days=self.expiration_limit)
                ).isoformat(timespec="seconds")

            else:
                try:
                    # We parse and re-write to the right timespec
                    parsed_expiration_date = datetime.fromisoformat(
                        new_expiration_date
                    ).isoformat(timespec="seconds")
                except ValueError as exc:
                    raise HTTPException(
                        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="The expiration date could not be parsed. \
                            Please use ISO 8601.",
                    ) from exc

            c.execute(
                """
            UPDATE FASTAPI_AUTH
            SET expiration_date = ?, is_active = 1
            WHERE api_key = ?
            """,
                (
                    parsed_expiration_date,
                    api_key,
                ),
            )

            connection.commit()

            response_lines.append(
                f"The new expiration date for the API key is {parsed_expiration_date}"
            )

            return " ".join(response_lines)

    def revoke_key(self, api_key: str):
        """
        Revokes an API key

        Args:
            api_key: the API key to revoke
        """
        with sqlite3.connect(self.db_location) as connection:
            c = connection.cursor()

            c.execute(
                """
            UPDATE FASTAPI_AUTH
            SET is_active = 0
            WHERE api_key = ?
            """,
                (api_key,),
            )

            connection.commit()

    def check_key(self, api_key: str) -> bool:
        """
        Checks if an API key is valid

        Args:
             api_key: the API key to validate
        """

        with sqlite3.connect(self.db_location) as connection:
            c = connection.cursor()

            c.execute(
                """
            SELECT is_active, total_queries, expiration_date, never_expire
            FROM FASTAPI_AUTH
            WHERE api_key = ?""",
                (api_key,),
            )

            response = c.fetchone()

            if (
                # Cannot fetch a row
                not response
                # Inactive
                or response[0] != 1
                # Expired key
                or (
                    (not response[3])
                    and (datetime.fromisoformat(response[2]) < datetime.utcnow())
                )
            ):
                # The key is not valid
                return False
            else:
                # The key is valid

                # We run the logging in a separate thread as writing takes some time
                threading.Thread(
                    target=self._update_usage,
                    args=(
                        api_key,
                        response[1],
                    ),
                ).start()

                # We return directly
                return True

    def _update_usage(self, api_key: str, usage_count: int):
        """
        The _update_usage function is called by the @use_api_key decorator.
        It takes an API key and a usage count as arguments, and updates the database to reflect that.
        The usage count is passed in from the @use_api_key decorator, which increments it every time it’s called.

        Args:
            self: Access the class attributes
            api_key:str: Identify the row in the database
            usage_count:int: Increment the usage count of the api key

        Returns:
            The number of queries that were performed
        """
        with sqlite3.connect(self.db_location) as connection:
            c = connection.cursor()

            # If we get there, this means it’s an active API key that’s in the database.\
            #   We update the table.
            c.execute(
                """
            UPDATE FASTAPI_AUTH
            SET total_queries = ?, latest_query_date = ?
            WHERE api_key = ?
            """,
                (
                    usage_count + 1,
                    datetime.utcnow().isoformat(timespec="seconds"),
                    api_key,
                ),
            )

            connection.commit()

    def get_usage_stats(self) -> List[Tuple[str, bool, bool, str, str, int]]:
        """
        The get_usage_stats function returns a list of tuples with values being api_key, is_active, expiration_date, latest_query_date, and total_queries.
        
        
        Args:
            self: Access variables that belongs to the class
        
        Returns:
            A list of tuples with values being api_key, is_active, expiration_date, \
                latest_query_date, and total_queries
            
        """
        with sqlite3.connect(self.db_location) as connection:
            c = connection.cursor()

            c.execute(
                """
            SELECT api_key, is_active, never_expire, expiration_date, \
                latest_query_date, total_queries, name
            FROM FASTAPI_AUTH
            ORDER BY latest_query_date DESC
            """,
            )

            response = c.fetchall()

        return response


sqlite_access = SQLiteAccess()
