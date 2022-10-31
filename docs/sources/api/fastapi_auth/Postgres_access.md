#


## PostgresAccess
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_postgres_access.py/#L23)
```python 

```


---
Class handling Remote Postgres connection and writes. Change URI if migrating database to a new location.


**Methods:**


### .revoke_key
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_postgres_access.py/#L231)
```python
.revoke_key(
   api_key: str
)
```

---
The revoke_key function revokes an API key.


**Args**

* **self**  : Access the class attributes and methods
* **str**  : Specify the api key to revoke


**Returns**

None

### .check_key
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_postgres_access.py/#L257)
```python
.check_key(
   api_key: str
)
```

---
The check_key function checks if the API key is valid.
It returns True if it is, False otherwise.



**Args**

* **self**  : Access the class attributes
* **str**  : Fetch the api_key from the database


**Returns**

True if the api key is valid, false otherwise

### ._update_usage
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_postgres_access.py/#L311)
```python
._update_usage(
   api_key: str, usage_count: int
)
```


### .create_key
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_postgres_access.py/#L89)
```python
.create_key(
   username, email, password, never_expire
)
```

---
The create_key function creates a new API key for the user.
It takes in the username, email, password and never_expire as parameters.
If there is already an existing user with that username or email it will return an error message to the client.
Otherwise it will create a new API key for that user and insert them into the database.


**Args**

* **self**  : Access variables that belongs to the class
* **username**  : Check if the username is already in use
* **email**  : Check if the email is already in use
* **password**  : Store the password in the database
* **never_expire**  : Determine if the user has an expiration date or not


**Returns**

The api_key

### .get_usage_stats
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_postgres_access.py/#L332)
```python
.get_usage_stats()
```

---
The get_usage_stats function returns a list of tuples with values being api_key, is_active, expiration_date,         latest_query_date, and total_queries. The function will return the usage stats for all API keys in the database.


**Args**

* **self**  : Refer to the object of the class


**Returns**

A list of tuples with values being api_key, is_active, expiration_date, latest_query_date, and total

### .renew_key
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_postgres_access.py/#L148)
```python
.renew_key(
   api_key: str, new_expiration_date: str
)
```

---
The renew_key function takes an API key and a new expiration date.
If the API key is not found, it raises a 404 error.
Otherwise, it updates the expiration date of the API key to be that specified by new_expiration_date (or 15 days from now if no argument is given).
It returns a string containing information about what happened.


**Args**

* **self**  : Access the class attributes
* **str**  : Check if the api key is valid
* **str**  : Set the new expiration date


**Returns**

A string

### .init_db
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_postgres_access.py/#L52)
```python
.init_db()
```

---
The init_db function creates a new database if one does not exist.
It also migrates the old user_database to the new format, and adds columns for email, password, and username.


**Args**

* **self**  : Access variables that belong to the class


**Returns**

The connection to the database
