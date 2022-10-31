#


### api_key_security
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/security_api_key.py/#L28)
```python
.api_key_security(
   query_param: str = Security(api_key_query),
   header_param: str = Security(api_key_header)
)
```

---
The api_key_security function is a custom type that checks for the presence of an API key in the query string and header.
If no API key is present, it raises an HTTPException with status code 403.
If an invalid or revoked API key is found, it also raises an HTTPException with status code 403.


**Args**

* **Security** (api_key_query) : Pass the api_key as a query parameter
* **Security** (api_key_header) : Pass the api key in the header
* Check if the api key is in the query string or not


**Returns**

The api key if it is passed in the query string or header
