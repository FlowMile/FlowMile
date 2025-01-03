from langchain_core.messages import AIMessage
from langchain_core.tools import tool

from langgraph.prebuilt import ToolNode

@tool
def get_weather(location: str):
    """Call to get the current weather."""
    if location.lower() in ["sf", "san francisco"]:
        return "It's 60 degrees and foggy."
    else:
        return "It's 90 degrees and sunny."


@tool
def get_coolest_cities():
    """Get a list of coolest cities"""
    return "nyc, sf"

from PIL import Image
from os import listdir
from os.path import splitext



@tool
def image_file_converter(target_directory: str, source_format: str,  target_format: str):
    """Call to convert the files in a directory from source to target format."""
    print('invoking tool image_file_converter')
    for file in listdir(target_directory):
        filename, extension = splitext(file)
        try:
            if extension in [source_format]:
                im = Image.open(filename + extension)
                im.save(filename + target_format)
        except OSError:
            raise('Cannot convert %s' % file)

tools = [image_file_converter]
tool_node = ToolNode(tools)


message_with_single_tool_call = AIMessage(
    content="",
    tool_calls=[
        {
            "name": "image_file_converter",
            "args": {"target_directory": '', "source_format": '', "target_format": ''},
            "id": "tool_call_id",
            "type": "tool_call",
        }
    ],
)
print(message_with_single_tool_call)
res = tool_node.invoke({"messages": [message_with_single_tool_call]})
print(res)