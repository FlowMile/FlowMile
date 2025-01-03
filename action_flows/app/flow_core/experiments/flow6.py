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
from langchain_experimental.agents import create_csv_agent

from langgraph.prebuilt import ToolNode
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd






def call_model(state):
    file_url = state.get('input')['file_url']
    prompt = state.get('prompt')
    model = get_model('groq', "llama-3.2-90b-vision-preview")
    agent = create_csv_agent(
            model, file_url, verbose=True,agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, allow_dangerous_code=True)
    
    response = agent.run(prompt)
    return {"output": [response]}




class Flow6(AbstractFlow):
    
    def __init__(self):
        super().__init__()
        self.workflow  = self.create_graph()
        self.build_graph()
                
    
    def build_graph(self):
        self.workflow.add_node("agent", call_model)
        
        self.workflow.add_edge(START, "agent")
        self.workflow.add_edge("agent", END)
        
    def run_graph(self):
        app = self.workflow.compile()
        # prompt = 'How many orders were there in the year 2003'
        prompt = 'Give me details of disputed order in 2005. Use the status column with value Disputed.'
        input = {"file_url":"resources/sales_data_sample.csv"}
        inputs = {"prompt": prompt, "input":input}
        result = app.invoke(inputs)
        print(' end of run ')
        print(result['output'])   
    