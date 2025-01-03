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
from langchain_community.tools import TavilySearchResults

tool = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=True,
    # include_domains=[...],
    # exclude_domains=[...],
    # name="...",            # overwrite default tool name
    # description="...",     # overwrite default tool description
    # args_schema=...,       # overwrite default args_schema: BaseModel
)

tools = [tool]
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


def call_model_pd_not_working(state):
    file_url = state.get('input')['file_url']
    prompt = state.get('prompt')
    model = get_model('groq', "llama-3.2-90b-vision-preview")
    
    df = pd.read_csv(
        file_url
    )
    agent = create_pandas_dataframe_agent(model, df, verbose=True, allow_dangerous_code=True)
    
    
    response = agent.run(prompt)
    return {"output": [response]}


class Flow7(AbstractFlow):
    
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
    