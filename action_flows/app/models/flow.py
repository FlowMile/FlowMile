from sqlalchemy import Column, Integer, String, JSON
from sqlmodel import Field, Session, SQLModel, create_engine, select

class FlowModel(SQLModel, table=True):
    __tablename__ = "flows"

    flow_id: str = Field(primary_key=True, index=True)
    name: str = Field( nullable=False)
    description: str = Field(nullable=True)
    definition: str = Field(sa_column=Column(JSON))