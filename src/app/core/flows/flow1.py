from core.flows.abstract_flow import AbstractFlow
from langgraph.graph import StateGraph, START, END

def classify_input_node(state):
    question = state.get('question', '').strip()
    classification = "hello"
    return {"classification": classification}


class Flow1(AbstractFlow):
    
    def __init__(self):
        super().__init__()
        self.workflow  = self.create_graph()
        self.build_graph()
        
    
    def build_graph(self):
        self.workflow.add_node("classify_input", classify_input_node)
        
        self.workflow.set_entry_point("classify_input")
        #self.workflow.add_edge('handle_greeting', END)
        self.workflow.add_edge('classify_input', END)
        
    def run_graph(self):
        app = self.workflow.compile()
        inputs = {"input": "Hello, how are you?"}
        result = app.invoke(inputs)
        print(result)   
    