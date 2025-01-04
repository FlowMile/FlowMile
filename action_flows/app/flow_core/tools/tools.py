from PIL import Image
from os import listdir
from os.path import splitext
from langchain_core.tools import tool
import os
from app.flow_core.utils import util
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from app.flow_core.ai_models.provider import get_model
import shutil
import xml.etree.ElementTree as ET
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage, HumanMessage
import traceback
#from markitdown import MarkItDown
import pymupdf4llm
import csv
import json


@tool
def image_file_converter(target_directory: str, source_format: str,  target_format: str):
    """Call to convert the files in a directory from source to target format."""
    print('invoking tool image_file_converter')
    for file in listdir(target_directory):
        
        filename, extension = splitext(file)
        try:
            if extension[1:] == source_format:
                source_path = os.path.join(target_directory, filename + extension)
                im = Image.open(source_path)
                target_path = os.path.join(target_directory, filename + "." +target_format)
                im.save(target_path)
        except OSError as e:
            raise('Cannot convert %s' % file)
        
   
@tool  
def resume_shortlist(prompt: str, source_directory: str, target_directory: str):
    """Call to shortlist the resumes found in source_directory according to the rules specified in the prompt and then move them
    to the target_directory"""
    print("in resume_shortlist tool call")
    print(source_directory)
    for file in listdir(source_directory):
        filename, extension = splitext(file)
        if extension[1:] == 'pdf':
            print(file)
            source_path = os.path.join(source_directory, file)
            file_data  = util.read_pdf_text(source_path)
            
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
            xml_response = response.content
            root = ET.fromstring(xml_response)
            if root.text == 'shortlisted':
                dst_path = os.path.join(target_directory, file)
                shutil.move(source_path, dst_path)
        
@tool
def invoice_data_extract(prompt: str, source_directory: str):
    """Call to extract information from images found in source_directory according to the rules specified in the prompt and then return in JSON format"""
    print("in invoice_data_extract tool call")
    for file in listdir(source_directory):
        filename, extension = splitext(file)
        if extension[1:] == 'png':
            print(file)
            source_path = os.path.join(source_directory, file)
            image_data  = util.read_image_from_path(source_path)
            
            message = HumanMessage(
                    content=[
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_data}"},
                        },
                    ],
                )
            
            model = get_model('groq', "llama-3.2-90b-vision-preview")
            response = None
            try:
                response = model.invoke([message])
            except Exception as e:
                print(e)
                print(traceback.format_exc())
            print('response from model ')
            print(response.content)
            xml_response = response.content
            root = ET.fromstring(xml_response)
            result = []
            for child in root:
                result_value = {}
                if child.tag == 'entity':
                    entity = child.text 
                    result_value['entity'] = entity
                if child.tag == 'date':
                    date = child.text 
                    result_value['date'] = date
                if child.tag == 'amount':
                    amount = child.text 
                    result_value['amount'] = amount
                result.append(result_value)
                    
            return result
        

@tool
def pdf_data_extract(prompt: str, source_directory: str):
    """Call to extract information from pdf found in source_directory according to the rules specified in the prompt and then return in JSON format"""
    print("in pdf_data_extract tool call")
    try:
        md_text = pymupdf4llm.to_markdown(source_directory + '/'+ 'tables.pdf', 
            page_chunks=True, 
            write_images=True,
            image_path=source_directory,
            image_format="png")
        #print(md_text)
        model = get_model('groq', "llama-3.2-90b-vision-preview")
        response = None
        message_template = ChatPromptTemplate.from_messages([
            
                HumanMessagePromptTemplate.from_template(
                    '''Given the following context, answer the question:
                    CONTEXT:{text}
                    
                    QUESTION: {prompt}
                    '''),
            ])
        messages = message_template.format(text = md_text, prompt = prompt)
        try:
            response = model.invoke(messages)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        print('response from model ')
        print(response.content)
        return response.content
        
        
        '''md = MarkItDown()
        result = md.convert(source_directory + '/'+ 'tables.pdf')
        print(result.text_content)'''
    except Exception as e:
            print(e)
            print(traceback.format_exc()) 
            
            
@tool
def json_to_csv(json_data: str, target_file_path: str):
    """Call to write JSON data to a csv file """
    print("in json_to_csv_func tool call")  
    try: 
        json_obj = json.loads(json_data)
        columns = json_obj[0]["columns"]
        rows = json_obj[0]["rows"]
        print(target_file_path)

        # Write to CSV
        with open(target_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(columns)  # Write header
            writer.writerows(rows)   # Write rows
    except Exception as e:
            print(e)
            print(traceback.format_exc())    
    
    
'''functions for tools'''
def invoice_data_extract_func(state):
    
    tool_name = 'invoice_data_extract'
    prompt = state.get('input')['prompt']
    source_directory = state.get('input')['source_directory']
    print("in invoice_data_extract_func call")
    tools = [registry.get(tool_name)]
    tool_node = ToolNode(tools)
    message_with_single_tool_call = AIMessage(
        content="",
        tool_calls=[
            {
                "name": tool_name,
                "args": {"prompt": prompt,  "source_directory": source_directory},
                "id": "tool_call_id",
                "type": "tool_call",
            }
        ],
    )
    tool_node.invoke({"messages": [message_with_single_tool_call]})
    
    
def pdf_data_extract_func(state):
    tool_name = 'pdf_data_extract'
    prompt = state.get('input')['prompt']
    source_directory = state.get('input')['source_directory']
    print("in pdf_data_extract_func call")
    tools = [registry.get(tool_name)]
    tool_node = ToolNode(tools)
    message_with_single_tool_call = AIMessage(
        content="",
        tool_calls=[
            {
                "name": tool_name,
                "args": {"prompt": prompt,  "source_directory": source_directory},
                "id": "tool_call_id",
                "type": "tool_call",
            }
        ],
    )
    tool_output_msg = tool_node.invoke({"messages": [message_with_single_tool_call]})
    tool_output = tool_output_msg.get('messages')[0].content
    print('tool output')
    print(tool_output)
    updated_data = {"tool_output": tool_output}
    return {"output": updated_data}
    

def json_to_csv_func(state):
    print('state')
    print(state)
    tool_name = 'json_to_csv'
    prompt = state.get('input')['prompt']
    source_directory = state.get('input')['source_directory']
    target_file_path = state.get('input')['target_file_path']
    pdf_data = state.get('output')['tool_output']
    print("in json_to_csv_func call")
    tools = [registry.get(tool_name)]
    tool_node = ToolNode(tools)
    message_with_single_tool_call = AIMessage(
        content="",
        tool_calls=[
            {
                "name": tool_name,
                "args": {"prompt": prompt,  "source_directory": source_directory, "target_file_path": target_file_path, "json_data": pdf_data},
                "id": "tool_call_id",
                "type": "tool_call",
            }
        ],
    )
    tool_node.invoke({"messages": [message_with_single_tool_call]})
    


registry = {
    "image_file_converter": image_file_converter,
    "resume_shortlist": resume_shortlist,
    "invoice_data_extract": invoice_data_extract,
    "pdf_data_extract": pdf_data_extract,
    "json_to_csv": json_to_csv
}