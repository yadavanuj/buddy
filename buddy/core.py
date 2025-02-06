from data import store
from enum import Enum

class ChangePlanner(Enum):
    DIRECT = 1
    WITH_SEARCH = 2
    
def direct_from_gemini(model, call_graph, feature_request):
    """Generate AI-driven change plan based on JavaScript code analysis."""
    prompt = f"""
    Given the following JavaScript call graph:

    {call_graph.edges}

    Suggest a structured change plan to implement: {feature_request}
    """

    response = model.generate_content(prompt)
    
    return response.text
    
def gemini_with_filtered_call_graph(model, call_graph, feature_request):
    """Generate AI-driven change plan based on JavaScript code analysis."""
    prompt = f"""
    Given the following JavaScript call graph search results of code base stored earlier. 
    The call graph will be minimal. Thus, try to assume or ask possibility of having some component already in place or one need to be added from scratch:

    {call_graph.edges}

    Suggest a structured change plan to implement: {feature_request}
    """

    response = model.generate_content(prompt)
    
    return response.text


