from data import store

def search_function(feature_request):
    return store.search_function_in_chroma(feature_request)

def generate_js_change_plan(model, call_graph, feature_request):
    """Generate AI-driven change plan based on JavaScript code analysis."""
    prompt = f"""
    Given the following JavaScript call graph search results of code base stored earlier. The call graph will be minimal. Thus, try to assume or ask possibility of having some component already in place or one need to be added from scratch:

    {call_graph.edges}

    Suggest a structured change plan to implement: {feature_request}
    """

    response = model.generate_content(prompt)
    
    return response.text