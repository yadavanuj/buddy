import os
import argparse
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from the .env file
load_dotenv()

from parser import analyze_project
from planner_plus import search_function, generate_js_change_plan
from data import store
from ai_model import ai_model

def plan(args):
    call_graph = analyze_project(Path(args.source_directory))
    print("\nCall Graph:")
    print(call_graph.nodes)
    
    for function in call_graph.nodes:
        file_path = call_graph.nodes[function].get("path", None)
        call_relations = list(call_graph.successors(function))
        if file_path is not None:
            store.store_function_in_chroma(function, file_path, call_relations)

    # feature_request = "Add caching to user verification"
    feature_request = args.task
    result = search_function(feature_request)
    print("\n[🔧 Search result for feature request]:\n", result);
    change_plan = generate_js_change_plan(ai_model, call_graph, feature_request)
    print("\n[🔧 Change Plan for JavaScript]:\n", change_plan)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code change planning CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create Plan
    plan_parser = subparsers.add_parser("plan", help="Plan a code change")
    plan_parser.add_argument("source_directory", type=str, help="Path to the source directory")
    plan_parser.add_argument("task", type=str, help="Change to be planned for")
    plan_parser.set_defaults(func=plan)

    # Parse arguments
    args = parser.parse_args()
    
    # Execute the appropriate command function
    args.func(args)


