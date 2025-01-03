from core.flows.abstract_flow import AbstractFlow
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage
from core.ai_models.provider import get_model
from core.utils import util
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from langgraph.prebuilt import ToolNode

@tool
def get_weather(location: str):
    """Call to get the current weather."""
    if location.lower() in ["sf", "san francisco"]:
        return "It's 60 degrees and foggy."
    else:
        return "It's 90 degrees and sunny."


@tool
def get_coolest_cities():
    """Get a list of coolest cities"""
    return "nyc, sf"

tools = [get_weather, get_coolest_cities]
tool_node = ToolNode(tools)

model_with_tools = ChatGroq(
        model = "llama-3.2-90b-vision-preview",
        temperature =1.0,
        max_tokens = 3000,
        timeout = None,
        max_retries = 2
        # other params...
    ).bind_tools(tools)


def call_model(state: MessagesState):
    print(state)
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END


class Flow6(AbstractFlow):
    
    def __init__(self):
        super().__init__()
        self.workflow  = StateGraph(MessagesState)
        self.build_graph()
                
    
    def build_graph(self):
        self.workflow.add_node("agent", call_model)
        self.workflow.add_node("tools", tool_node)
        
        self.workflow.add_edge(START, "agent")
        self.workflow.add_conditional_edges("agent", should_continue, ["tools", END])
        self.workflow.add_edge("tools", "agent")
        
    def run_graph(self):
        app = self.workflow.compile()
        
        inputs =  {"messages": [("human", "what's the weather in sf?")], "input":{}}
        result = app.invoke(inputs)
        print(' end of run ')
        print(result['messages'])   
    