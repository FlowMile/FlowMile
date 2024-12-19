from typing import Dict, TypedDict, Optional, Annotated, Any
import operator
from langgraph.graph import StateGraph
from pydantic import BaseModel

class GraphState(TypedDict):
    input: Optional[Dict] = None
    prompt: Optional[str] = None
    response: Optional[Dict] = None
    output: Any
    
class AbstractFlow():
    
    
    def create_graph(self):
        workflow = StateGraph(GraphState)
        return workflow

