from app.flow_core.flow_builder import build_graph_from_json
from typing import TypedDict, Literal, Callable, Dict, Any
import json
import os
import importlib.resources


def get_flow(flow_id: str):
    file_path = os.path.join("flow_templates", f"{flow_id}.json")
    
    print(file_path)
    flow_text = importlib.resources.read_text("app.flow_core.flow_templates", f"{flow_id}.json")
    print(flow_text)
    
    return flow_text

def execute_flow(flow_id: str, input: Dict) -> Any:
    flow_json_str = get_flow(flow_id)
    flow_json = json.loads(flow_json_str)
    graph = build_graph_from_json(flow_json)
    response = graph.invoke(input)
    print(response)
    return response

