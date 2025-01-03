from core.flows.abstract_flow import AbstractFlow
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from core.ai_models.provider import get_model
from core.utils import util
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

def process_text(state):
    prompt = state.get('prompt')
    file_data = state.get('output')['file_data']
    message_template = ChatPromptTemplate.from_messages([
       
        HumanMessagePromptTemplate.from_template(
            '''Given the following context, answer the question:
            CONTEXT:{file_data}
            
            QUESTION: {prompt}
            '''),
    ])
    messages = message_template.format(file_data = file_data, prompt = prompt)
    
    model = get_model('groq', "llama-3.2-90b-vision-preview")
    response = model.invoke([messages])
    print('response from model ')
    print(response.content)
    updated_data = {"response": response.content}
    return {"output": updated_data}
    
def read_text(state):
    #TODO read from file
    file_data = '''
    The World Health Organization (WHO)[1] is a specialized agency of the United Nations responsible for international public health.[2] The WHO Constitution states its main objective as 'the attainment by all peoples of the highest possible level of health'.[3] Headquartered in Geneva, Switzerland, it has six regional offices and 150 field offices worldwide. The WHO was established on 7 April 1948.[4][5] The first meeting of the World Health Assembly (WHA), the agency's governing body, took place on 24 July of that year. The WHO incorporated the assets, personnel, and duties of the League of Nations' Health Organization and the Office International d'Hygiène Publique, including the International Classification of Diseases (ICD).[6] Its work began in earnest in 1951 after a significant infusion of financial and technical resources.[7]
    '''
    updated_data = {"file_data": file_data}
    return {"output": updated_data}


class Flow5(AbstractFlow):
    
    def __init__(self):
        super().__init__()
        self.workflow  = self.create_graph()
        self.build_graph()
        
    
    def build_graph(self):
        self.workflow.add_node("read_text", read_text)
        self.workflow.add_node("process_text", process_text)
        
        self.workflow.set_entry_point("read_text")
        self.workflow.add_edge('read_text', "process_text")
        self.workflow.add_edge('process_text', END)
        
    def run_graph(self):
        app = self.workflow.compile()
        input = {"file_url":"resume.pdf"}
        inputs = {"prompt": "Extract the Named Entities from this text. Also extract dates.", "input":input}
        result = app.invoke(inputs)
        print(' end of run ')
        print(result['output'])   
    