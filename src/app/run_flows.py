from core.flows.flow1 import Flow1
from core.flows.flow2 import Flow2
from core.flows.flow3 import Flow3

def one():
    f = Flow1()
    f.run_graph()
    
def two():
    image_url = "https://lovetravellingblog.com/wp-content/uploads/2024/04/new-york-header-2.jpg?w=1024"
    from langchain_core.messages import HumanMessage
    import os
    from langchain_groq import ChatGroq

    os.environ["GROQ_API_KEY"] = "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"
    model = ChatGroq(
        model="llama-3.2-90b-vision-preview",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )
    import base64

    import httpx

    image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")
    
    message = HumanMessage(
    content=[
        {"type": "text", "text": "describe this image"},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
        },
        ],
    )
    response = model.invoke([message])
    print(response.content)

def three():
    f = Flow2()
    f.run_graph()
    
def four():
    f = Flow3()
    f.run_graph()

four()