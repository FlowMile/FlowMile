from core.flows.abstract_flow import AbstractFlow
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from core.ai_models.provider import get_model
from core.utils import util

def process_image(state):
    prompt = state.get('prompt')
    image_data = state.get('output')['image_data']
    message = HumanMessage(
    content=[
        {"type": "text", "text": prompt},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
        },
        ],
    )
    model = get_model('groq', "llama-3.2-90b-vision-preview")
    response = model.invoke([message])
    print('response from model ')
    print(response.content)
    updated_data = {"response": response.content}
    return {"output": updated_data}
    
def read_image(state):
    image_url = state.get('input')['image_url']
    image_data  = util.read_image_from_url(image_url)
    updated_data = {"image_data": image_data}
    return {"output": updated_data}


class Flow4(AbstractFlow):
    
    def __init__(self):
        super().__init__()
        self.workflow  = self.create_graph()
        self.build_graph()
        
    
    def build_graph(self):
        self.workflow.add_node("read_image", read_image)
        self.workflow.add_node("process_image", process_image)
        
        self.workflow.set_entry_point("read_image")
        self.workflow.add_edge('read_image', "process_image")
        self.workflow.add_edge('process_image', END)
        
    def run_graph(self):
        app = self.workflow.compile()
        input = {"image_url":"https://cdn-jklip.nitrocdn.com/safSuIdqgDlBkQZOuiEFYetySutVuoYj/assets/images/optimized/rev-8d551bb/happay.com/blog/wp-content/uploads/sites/12/2024/02/Invoice-examples-and-templates.webp"}
        inputs = {"prompt": "What is the total amount mentioned in the bill", "input":input}
        result = app.invoke(inputs)
        print(' end of run ')
        print(result['output'])   
    