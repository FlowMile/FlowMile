from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage
from app.flow_core.tools.tools import registry

def generic_tool_func2(state):
    tool_name = state.get('input')['tool_name']
    target_directory = state.get('input')['target_directory']
    source_format = state.get('input')['source_format']
    target_format = state.get('input')['target_format']

    tools = [registry.get(tool_name)]
    tool_node = ToolNode(tools)
    message_with_single_tool_call = AIMessage(
        content="",
        tool_calls=[
            {
                "name": tool_name,
                "args": {"target_directory": target_directory, "source_format": source_format, "target_format": target_format},
                "id": "tool_call_id",
                "type": "tool_call",
            }
        ],
    )
    tool_node.invoke({"messages": [message_with_single_tool_call]})
    
    
def generic_tool_func(state):
    tool_name = state.get('input')['tool_name']
    prompt = state.get('input')['prompt']
    target_directory = state.get('input')['target_directory']
    source_directory = state.get('input')['source_directory']
    print("in generic tool call")
    tools = [registry.get(tool_name)]
    tool_node = ToolNode(tools)
    message_with_single_tool_call = AIMessage(
        content="",
        tool_calls=[
            {
                "name": tool_name,
                "args": {"prompt": prompt, "target_directory": target_directory, "source_directory": source_directory},
                "id": "tool_call_id",
                "type": "tool_call",
            }
        ],
    )
    tool_node.invoke({"messages": [message_with_single_tool_call]})