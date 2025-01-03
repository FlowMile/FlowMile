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
from langgraph.prebuilt import create_react_agent
from langchain import hub
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

import sqlite3

import requests
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool


def get_engine_for_chinook_db():
    """Pull sql file, populate in-memory database, and create engine."""
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
    response = requests.get(url)
    sql_script = response.text

    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(sql_script)
    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    
    
    
def init_db():
    engine = get_engine_for_chinook_db()

    db = SQLDatabase(engine)  
    return db  


def call_model(state):
    db = init_db()
    
    prompt = state.get('prompt')
    llm = get_model('groq', "llama-3.2-90b-vision-preview")
    prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
    system_message = prompt_template.format(dialect="SQLite", top_k=5)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_react_agent(
        llm, toolkit.get_tools(), state_modifier=system_message
    )
    input_msg = {"messages": [("user", prompt)]}
    response = agent_executor.invoke(input_msg)
    return {"output": [response]}




class Flow7(AbstractFlow):
    
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
        prompt = "Which country's customers spent the most"
        input = {}
        inputs = {"prompt": prompt, "input":input}
        result = app.invoke(inputs)
        print(' end of run ')
        print(result['output'])   
    