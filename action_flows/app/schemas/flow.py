from pydantic import BaseModel, Field
from typing import Any
import uuid

# Schema for creating a flow
class Flow(BaseModel):
    flow_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: str | None = None
    definition: dict
