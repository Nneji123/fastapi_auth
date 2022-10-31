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
    return {"message": "This is an unsecure endpoint"}

@app.get("/secure", dependencies=[Depends(api_key_security)])
async def secure_endpoint():
    return {"message": "This is a secure endpoint"}


