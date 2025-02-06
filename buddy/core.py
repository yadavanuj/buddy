from parser import analyze_project
from storage import store
from enum import Enum
from ai_model import ai_model
from dotenv import load_dotenv
from pathlib import Path
    
def direct_from_gemini_prompt(model, call_graph, feature_request):
    """Generate AI-driven change plan based on JavaScript code analysis."""
    prompt = f"""
    Given the following JavaScript call graph:

    {call_graph.edges}

    Suggest a structured change plan to implement: {feature_request}
    """

    response = model.generate_content(prompt)
    
    return response.text
    
def gemini_with_filtered_call_graph_prompt(model, call_graph, feature_request):
    """Generate AI-driven change plan based on JavaScript code analysis."""
    prompt = f"""
    Given the following JavaScript call graph search results of code base stored earlier. 
    The call graph will be minimal. Thus, try to assume or ask possibility of having some component already in place or one need to be added from scratch:

    {call_graph.edges}

    Suggest a structured change plan to implement: {feature_request}
    """

    response = model.generate_content(prompt)
    
    return response.text


def direct_from_gemini(args):
    call_graph = analyze_project(Path(args.source_directory))
    print("\nCall Graph:")
    print(call_graph.edges)

    feature_request = args.task
    change_plan = direct_from_gemini_prompt(ai_model, call_graph, feature_request)
    print("\n[🔧 Change Plan for JavaScript]:\n", change_plan)

def search_function(feature_request):
    return store.search_function_in_chroma(feature_request)

def gemini_with_filtered_call_graph(args):
    call_graph = analyze_project(Path(args.source_directory))
    print("\nCall Graph:")
    print(call_graph.nodes)

    for function in call_graph.nodes:
        file_path = call_graph.nodes[function].get("path", None)
        call_relations = list(call_graph.successors(function))
        if file_path is not None:
            store.store_function_in_chroma(function, file_path, call_relations)

    feature_request = args.task
    result = search_function(feature_request)
    print("\n[🔧 Search result for feature request]:\n", result)
    change_plan = gemini_with_filtered_call_graph_prompt(ai_model, call_graph, feature_request)
    print("\n[🔧 Change Plan for JavaScript]:\n", change_plan)
