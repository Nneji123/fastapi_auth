#


## SQLiteAccess
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_sqlite_access.py/#L19)
```python 

```


---
Class handling SQLite connection and writes


**Methods:**


### .revoke_key
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_sqlite_access.py/#L213)
```python
.revoke_key(
   api_key: str
)
```

---
Revokes an API key


**Args**

* **api_key**  : the API key to revoke


### .check_key
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_sqlite_access.py/#L234)
```python
.check_key(
   api_key: str
)
```

---
Checks if an API key is valid


**Args**

* **api_key**  : the API key to validate


### ._update_usage
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_sqlite_access.py/#L283)
```python
._update_usage(
   api_key: str, usage_count: int
)
```

---
The _update_usage function is called by the @use_api_key decorator.
It takes an API key and a usage count as arguments, and updates the database to reflect that.
The usage count is passed in from the @use_api_key decorator, which increments it every time it’s called.


**Args**

* **self**  : Access the class attributes
* **str**  : Identify the row in the database
* **int**  : Increment the usage count of the api key


**Returns**

The number of queries that were performed

### .create_key
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_sqlite_access.py/#L72)
```python
.create_key(
   name, email, password, never_expire
)
```

---
The create_key function creates a new API key for the user.


**Args**

* **self**  : Access attributes of the class
* **name**  : Identify the user
* **email**  : Validate the email address
* **password**  : Store the hashed password
* **never_expire**  : Set the expiration date to none


**Returns**

A string

### .get_usage_stats
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_sqlite_access.py/#L317)
```python
.get_usage_stats()
```

---
The get_usage_stats function returns a list of tuples with values being api_key, is_active, expiration_date, latest_query_date, and total_queries.



**Args**

* **self**  : Access variables that belongs to the class


**Returns**

A list of tuples with values being api_key, is_active, expiration_date,                 latest_query_date, and total_queries


### .renew_key
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_sqlite_access.py/#L130)
```python
.renew_key(
   api_key: str, new_expiration_date: str
)
```

---
The renew_key function takes an API key and a new expiration date.
If the API key is not found, it returns a 404 error.
If the API key has already expired, it will be reactivated and return &quot;This API key was revoked and has been reactivated.&quot;
Otherwise, if no new expiration date is given or if the provided one cannot be parsed as ISO 8601 (see https://en.wikipedia.org/wiki/ISO_8601#Time),
the function will set its expiration date to 7 days from now by default.


**Args**

* **self**  : Access the class attributes
* **str**  : Check if the api key exists in the database
* **str**  : Set a new expiration date for the api key


**Returns**

A string with a message about the api key's new expiration date

### .init_db
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_sqlite_access.py/#L37)
```python
.init_db()
```

---
The init_db function creates a new database file if one does not already exist.
It also adds the necessary columns to the table for storing API keys.


**Args**

* **self**  : Access variables that belongs to the class


**Returns**

Nothing
