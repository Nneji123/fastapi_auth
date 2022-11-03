The fastapi_auth package uses exported environment variables or reads environment variables from a `.env` file.

These are the environment variables that can be used:
# Database Settings
- DATABASE_MODE (default: sqlite)

# MySQL settings
**For now mysql is not supported.**
- MYSQL_USER
- MYSQL_PASSWORD
- MYSQL_HOST
- MYSQL_PORT 
- MYSQL_DATABASE
- MYSQL_URI



# Postgres settings
** Set `DATABASE_MODE` to postgres to use postgres.**

- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_HOST
- POSTGRES_PORT
- POSTGRES_DATABASE
- POSTGRES_URI
- POSTGRES_SSL ("require" #delete if not used.)

# MongoDB settings
** Set `DATABASE_MODE` to mongodb.**

- MONGODB_URL

# FastAPI_Auth settings
FASTAPI_AUTH_SECRET  `set your secret key here`
FASTAPI_AUTH_AUTOMATIC_EXPIRATION=15 `Default=15`
FASTAPI_AUTH_DB_LOCATION=sqlite.db # `change location of sqlite.db`
