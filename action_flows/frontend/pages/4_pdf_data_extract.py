import streamlit as st
from app.flow_core import flow_executor 

def click_button():
    input = {}
    input['tool_name'] = "pdf_data_extract"
    input['target_file_path'] = target_file_path
    input['prompt'] = prompt
    input['source_directory'] = source_dir_path
    inputs = {"input": input}
    flow_executor.execute_flow(flow_id, inputs)

prompt = st.text_area(height=200, label='Input the prompt')
source_dir_path = st.text_input('Input the Source directory path')
target_file_path = st.text_input('Input the Target File path')
flow_id = "5"
st.button('Submit', on_click=click_button)

    