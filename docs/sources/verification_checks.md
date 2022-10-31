#


### hash_password
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/endpoints.py/#L29)
```python
.hash_password(
   password: str
)
```

---
The hash_password function takes a string and returns the hashed version of that string.
If no password is entered, it will return an error message.


**Args**

* **str**  : Store the password that is entered by the user


**Returns**

The hashed password

----


### email_validate
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/endpoints.py/#L51)
```python
.email_validate(
   email_text: str
)
```

---
The email_validate function takes in an email address as a string and returns the normalized form of that email address.
If the inputted email is not valid, it raises an HTTPException with a status code of 403 Forbidden.


**Args**

* **str**  : Store the email address that is inputted by the user


**Returns**

The normalized form of the email address

----


### check_length_password
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/endpoints.py/#L76)
```python
.check_length_password(
   password: str
)
```

---
The check_length_password function checks if the password is longer than 8 characters, contains an uppercase letter and digit.
If it is not, then it will generate a new password for the user and return that instead.


**Args**

* **str**  : Check if the password is at least 8 characters long, has a digit and an uppercase letter


**Returns**

The password if it is longer than 8 characters, has at least one digit and uppercase letter
