from fastapi import FastAPI, HTTPException
from starlette.responses import Response

from app.api import api

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Fast API in Python"}


@app.get("/health")
def read_user():
    return api.health()


