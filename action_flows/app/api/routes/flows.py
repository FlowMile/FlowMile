import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends

from app.schemas.flow import Flow
from app.service.flow_service import create_flow
from app.api.deps import SessionDep

router = APIRouter(prefix="/flows", tags=["flows"])


@router.post("/", response_model = Flow)
def create_flow(flow: Flow, session: SessionDep)  -> Any :
    try:
        db_flow = create_flow(session, flow)
        return db_flow
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    
@router.get("/", response_model = Flow)
def get_flows(session: SessionDep)  -> Any :
    try:
        print('in get flows')
        return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")