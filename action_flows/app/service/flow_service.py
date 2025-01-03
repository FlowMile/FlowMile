import uuid
from sqlalchemy.orm import Session
from app.models.flow import FlowModel
from app.schemas.flow import Flow
from app.api.deps import SessionDep

def create_flow(session: SessionDep, flow: Flow):
    db_flow = FlowModel(
        flow_id = flow.flow_id,
        name=flow.name,
        description=flow.description,
        definition=flow.definition,
    )
    session.add(db_flow)
    session.commit()
    session.refresh(db_flow)
    return db_flow

def get_flow_by_uid(session: SessionDep, uid: str):
    return session.query(Flow).filter(Flow.uid == uid).first()
