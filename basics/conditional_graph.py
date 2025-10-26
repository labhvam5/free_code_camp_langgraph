#!/usr/bin/env python3
"""
LangGraph application with conditional routing for calculator operations.
"""

import os
from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure LangSmith if API key is provided
if os.getenv("LANGSMITH_API_KEY"):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "langgraph-conditional-calculator")
    print(f"🔍 LangSmith tracing enabled for project: {os.environ['LANGCHAIN_PROJECT']}")
else:
    print("ℹ️  LangSmith not configured. Set LANGSMITH_API_KEY and LANGSMITH_PROJECT to enable tracing.")


# Define AgentState as a TypedDict structure
class AgentState(TypedDict):
    number1: float
    number2: float
    operation: str
    final_number: float


def decide_next_node(state: AgentState) -> AgentState:
    """Decision node that prepares the state for routing"""
    
    print(f"Decision node: Operation is '{state['operation']}'")
    return state


def route_next_node(state: AgentState) -> str:
    """Router function that decides which calculation node to execute next"""
    
    if state['operation'] == '+':
        return "add_node"
    elif state['operation'] == '-':
        return "subtract_node"
    else:
        raise ValueError(f"Unsupported operation: {state['operation']}")


def add_node(state: AgentState) -> AgentState:
    """Node that performs addition of number1 + number2"""
    
    result = state['number1'] + state['number2']
    state['final_number'] = result
    
    print(f"Addition: {state['number1']} + {state['number2']} = {result}")
    
    return state


def subtract_node(state: AgentState) -> AgentState:
    """Node that performs subtraction of number1 - number2"""
    
    result = state['number1'] - state['number2']
    state['final_number'] = result
    
    print(f"Subtraction: {state['number1']} - {state['number2']} = {result}")
    
    return state


def create_graph():
    """Create and configure the conditional LangGraph"""
    
    # Initialize the StateGraph
    workflow = StateGraph(AgentState)
    
    # Add nodes to the workflow
    workflow.add_node("decide_next_node", decide_next_node)
    workflow.add_node("add_node", add_node)
    workflow.add_node("subtract_node", subtract_node)
    
    # Define the graph flow
    workflow.add_edge(START, "decide_next_node")
    
    # Add conditional edges based on the router function's return value
    workflow.add_conditional_edges(
        "decide_next_node",
        route_next_node,
        {
            "add_node": "add_node",
            "subtract_node": "subtract_node"
        }
    )
    
    # Connect calculation nodes to END
    workflow.add_edge("add_node", END)
    workflow.add_edge("subtract_node", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def main():
    """Main function to test the conditional graph"""
    
    # Create the graph
    app = create_graph()
    
    # Test case 1: Addition
    print("=" * 50)
    print("TEST CASE 1: Addition")
    print("=" * 50)
    
    addition_state = {
        "number1": 15.5,
        "number2": 24.3,
        "operation": "+",
        "final_number": 0.0
    }
    
    print("Initial state:", addition_state)
    
    # Run the graph for addition
    addition_result = app.invoke(addition_state)
    
    print("Final result:", addition_result)
    print()
    
    # Test case 2: Subtraction
    print("=" * 50)
    print("TEST CASE 2: Subtraction")
    print("=" * 50)
    
    subtraction_state = {
        "number1": 100.0,
        "number2": 37.5,
        "operation": "-",
        "final_number": 0.0
    }
    
    print("Initial state:", subtraction_state)
    
    # Run the graph for subtraction
    subtraction_result = app.invoke(subtraction_state)
    
    print("Final result:", subtraction_result)


if __name__ == "__main__":
    main()
