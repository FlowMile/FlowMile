from app.flow_core.abstract_flow import AbstractFlow
from typing import TypedDict, Literal, Callable, Dict

from langgraph.graph import StateGraph, END
from app.flow_core.abstract_flow import AgentState, GraphState
from app.flow_core.tools.tools import image_file_converter


def call_model(state):
    print('calling model')


def tool_node(state):
    print('calling tool')


def should_continue(state):
    pass


# END constant to represent the end of the graph
END = "__end__"

# General function registry to map function names to actual function references
function_registry = {
    "call_model": call_model,
    "tool_node": tool_node,
    "should_continue": should_continue,
    "image_file_converter": image_file_converter
}


# Function to retrieve a function reference from the registry
def get_function_reference(name: str) -> Callable:
    return function_registry.get(name, lambda: None)

# Generalized adapter function to reconstruct the imperative input
def build_graph_from_json(flow_json: Dict) -> Callable:
    # Step 1: Initialize the graph with config
    workflow = StateGraph(GraphState)

    # Step 2: Add all nodes to the workflow based on the flow JSON
    for node in flow_json["nodes"]:
        node_id = node["id"]

        # Skip special start and end nodes in this step
        if node_id in ["__start__", "__end__"]:
            continue

        # Retrieve the function for this node
        function_name = node["data"].get("function")
        function_ref = get_function_reference(function_name)

        # Add the node with the associated function
        workflow.add_node(node_id, function_ref)

    # Step 3: Set the entry point if there's an edge from "__start__"
    for edge in flow_json["edges"]:
        if edge["source"] == "__start__":
            workflow.set_entry_point(edge["target"])
            break

    # Step 4: Add edges to the workflow
    for edge in flow_json["edges"]:
        source = edge["source"]
        target = edge["target"]

        # Skip "__start__" and "__end__" here, as they have special handling
        if source == "__start__" or target == "__end__":
            continue

        # Determine if the edge is conditional
        conditional = edge.get("conditional", "False") == "True"

        if conditional:
            # Retrieve the conditional function
            function_name = edge.get("function")
            condition_function = get_function_reference(function_name)

            # Define the mapping for conditional edges
            # TODO: THERE CAN BE MULTIPLE CONDITIONS
            mapping = {
                edge["data"]: target,
                "end": END,
            }

            # Add the conditional edge to the workflow
            workflow.add_conditional_edges(source, condition_function, mapping)
        else:
            # Add a normal edge if it's not conditional
            workflow.add_edge(source, target)

    # Step 5: Compile the workflow
    graph = workflow.compile()

    return graph

