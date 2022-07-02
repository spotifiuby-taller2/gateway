from http.client import HTTPException
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from exceptions.auth_error import AuthorizationException
from exceptions.spotifiubi_error import SpotifiubiException
from sqlalchemy.exc import SQLAlchemyError
from services import apikey_auth
import logging
import uvicorn

from services.logging_service import logInfo

app = FastAPI(title="Spotifiubi - services",
              description="services for Spotifiubi",
              version="0.0.1")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    error = {"message": exc.detail}
    return JSONResponse(status_code=exc.status_code, content=error)


@app.exception_handler(AuthorizationException)
async def auth_exception_handler(request, exc):
    error = {"message": exc.detail}
    logging.error(f"status_code: {exc.status_code} message: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content=error)


@app.exception_handler(SQLAlchemyError)
async def sql_exception_handler(request, exc):
    error = {"message": str(exc.__dict__)}
    logging.critical(f"status_code: 500 message: {str(exc.__dict__)}")
    return JSONResponse(status_code=500, content=error)


app.include_router(apikey_auth.router)

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, workers=4)
