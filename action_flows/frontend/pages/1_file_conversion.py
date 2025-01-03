import streamlit as st
from app.flow_core import flow_executor 

def click_button():
    input = {}
    input['tool_name'] = "image_file_converter"
    input['target_directory'] = dir_path
    input['source_format'] = source_format
    input['target_format'] = target_format
    inputs = {"input": input}
    flow_executor.execute_flow(flow_id, inputs)

dir_path = st.text_input('Input the directory path')
source_format = st.text_input('Input the Source File Format')
target_format = st.text_input('Input the Target File Format')
flow_id = "2"
st.button('Submit', on_click=click_button)

    