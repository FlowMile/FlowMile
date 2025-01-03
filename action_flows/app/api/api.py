import json
from fastapi import APIRouter
from app.api.routes import flows

api_router = APIRouter()
api_router.include_router(flows.router)