from core.flows.abstract_flow import AbstractFlow
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage
from core.ai_models.provider import get_model
from core.utils import util
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import AIMessage
from langchain_core.tools import Tool
from langchain_groq import ChatGroq

from langgraph.prebuilt import ToolNode
from langchain_community.utilities import GoogleSerperAPIWrapper

search = GoogleSerperAPIWrapper()
tools = [
    Tool(
        name="Intermediate Answer",
        func=search.run,
        description="useful for when you need to ask with search",
    )
]

tool_node = ToolNode(tools)

model_with_tools = ChatGroq(
        model = "llama-3.2-90b-vision-preview",
        temperature =1.0,
        max_tokens = 3000,
        timeout = None,
        max_retries = 2
        # other params...
    ).bind_tools(tools)

# Alternative: llm_with_tools = llm.bind_tools([tool])


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


class Flow8(AbstractFlow):
    
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
        
        inputs =  {"messages": [("human", "Give me a list of flights from New Delhi to Bangalore on Dec 25 2024.")], "input":{}}
        result = app.invoke(inputs)
        print(' end of run ')
        print(result['messages'])   
    