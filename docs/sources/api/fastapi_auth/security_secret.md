#


## GhostLoadedSecret
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_security_secret.py/#L13)
```python 

```


---
Ghost-loaded secret handler


**Methods:**


### .get_secret_value
[source](https://github.com/nneji123/fastapi_auth/blob/main/fastapi_auth/_security_secret.py/#L28)
```python
.get_secret_value()
```

---
The get_secret_value function is a helper function that returns the secret value for the session.
If no secret value has been set, it will generate a single-use secret key for this session.


**Args**

* **self**  : Access the class attributes and methods


**Returns**

A string
