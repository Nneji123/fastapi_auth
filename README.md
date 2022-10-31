# FastAPI Authentication

[![codecov](https://codecov.io/github/mrtolkien/fastapi_simple_security/branch/master/graph/badge.svg?token=8VIKJ9J3XF)](https://codecov.io/github/mrtolkien/fastapi_simple_security)
[![Python Tests](https://github.com/mrtolkien/fastapi_simple_security/actions/workflows/pr_python_tests.yml/badge.svg)](https://github.com/mrtolkien/fastapi_simple_security/actions/workflows/pr_python_tests.yml)
[![Linting](https://github.com/mrtolkien/fastapi_simple_security/actions/workflows/push_sanity_check.yml/badge.svg)](https://github.com/mrtolkien/fastapi_simple_security/actions/workflows/push_sanity_check.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![docs](https://github.com/Nneji123/fastapi_auth/actions/workflows/publish-docs.yml/badge.svg)](https://github.com/Nneji123/fastapi_auth/actions/workflows/publish-docs.yml)

[![publish-pypi](https://github.com/Nneji123/fastapi_auth/actions/workflows/publish-pypi.yml/badge.svg)](https://github.com/Nneji123/fastapi_auth/actions/workflows/publish-pypi.yml)

API key based Authentication package for FastAPI, focused on simplicity and ease of use:

- Full functionality out of the box, no configuration required
- API key security with local `sqlite` or `postgres` database backend, working with both header and query parameters
- Default 15 days deprecation for generated API keys
- Key creation, revocation, renewing, and usage logs handled through administrator endpoints
- Username, Email address and password(hashing + salting) verification features.
- Lightweight, minimal dependencies required.

This package can be used for development(sqlite3 database) and production(postgres database) environments.


## Installation

`pip install fastapi_auth2`

## Usage

### Creating an application

```python
from fastapi import Depends, FastAPI
from fastapi_auth import api_key_router, api_key_security


app = FastAPI(
    description="FastAPI Auth is a package that provides authentication based API security with FastAPI and Postgres Database or Sqlite3 Database.",
    title="FastAPI Auth Example",  
    version=1.0,
)


app.include_router(api_key_router, prefix="/auth", tags=["_auth"])

@app.get("/unsecure")
async def unsecure_endpoint():
    return {"message": "This is a unsecure endpoint"}

@app.get("/secure", dependencies=[Depends(api_key_security)])
async def secure_endpoint():
    return {"message": "This is a secure endpoint"}
```

Resulting app is:

![app](images/auth_endpoints.png)

### API key creation through docs

Start your API and check the logs for the automatically generated secret key if you did not provide one through
environment variables.

![secret](images/secret.png)

Go to `/docs` on your API and inform this secret key in the `Authorize/Secret header` box.
All the administrator endpoints only support header security to make sure the secret key is not inadvertently
shared when sharing an URL.

![secret_header](images/secret_header.png)

Then, you can use `/auth/new` to generate a new API key.

![api key](images/new_api_key.png)

And finally, you can use this API key to access the secure endpoint.

![secure endpoint](images/secure_endpoint.png)

### API key creation in python

You can of course automate API key acquisition through python with `requests` and directly querying the endpoints.

If you do so, you can hide the endpoints from your API documentation with the environment variable
`FASTAPI_AUTH_HIDE_DOCS`.

## Configuration

Environment variables:

- `FASTAPI_AUTH_SECRET`: Secret administrator key

    - Generated automatically on server startup if not provided
    - Allows generation of new API keys, revoking of existing ones, and API key usage view
    - It being compromised compromises the security of the API

- `FASTAPI_AUTH_HIDE_DOCS`: Whether or not to hide the API key related endpoints from the documentation
- `FASTAPI_AUTH_DB_LOCATION`: Location of the local sqlite database file
    - `sqlite.db` in the running directory by default
    - When running the app inside Docker, use a bind mount for persistence
- `FASTAPI_AUTH_AUTOMATIC_EXPIRATION`: Duration, in days, until an API key is deemed expired
    - 15 days by default
- `DEV_MODE`: If set to `True`, the app will run in development mode, using an in-memory sqlite database
    - Useful for testing and development
    - Not recommended for production
    - If set to `False`, the app will run in production mode, using a postgres database.
- `URI`: Location of the postgres database
    - `postgresql://postgres:postgres@localhost:5432/postgres` by default
    - Only used if `DEV_MODE` is set to `False`

## Contributing
See `CONTIBUTING.md` for more information.
### Setting up python environment

```bash
poetry install
poetry shell
```

### Setting up pre-commit hooks

```bash
pre-commit install
```

### Running tests

```bash
pytest
```

### Running the dev environment

The attached docker image runs a test app on `localhost:8080` with secret key `TEST_SECRET`. Run it with:

```bash
docker-compose build && docker-compose up
```

## TODO
- Add more tests
- Add more database backends
- Add more authentication methods
