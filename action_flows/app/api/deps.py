from app.core.database import engine
from sqlmodel import Session
from collections.abc import Generator
from typing import Annotated
from fastapi import Depends, HTTPException, status

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_db)]

     
    
