from typing import Dict, TypedDict, Optional, Annotated, Any
import operator
from langgraph.graph import StateGraph
from pydantic import BaseModel
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from typing import TypedDict, Annotated, Sequence

class GraphState(TypedDict):
    input: Optional[Dict] = None
    prompt: Optional[str] = None
    response: Optional[Dict] = None
    output: Any
    
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
class AbstractFlow():
    
    
    def create_graph(self):
        workflow = StateGraph(GraphState)
        return workflow

