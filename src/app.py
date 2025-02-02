import os
import argparse
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from the .env file
load_dotenv()

from parser import analyze_project
from planner import generate_js_change_plan
from ai_model import ai_model

def plan(args):
    print('called')
    # Run analysis on a sample project
    # call_graph = analyze_project(Path("D:/js-code/basicservice/src"))
    call_graph = analyze_project(Path(args.source_directory))
    print("\nCall Graph:")
    print(call_graph.edges)

    

    # feature_request = "Add caching to user verification"
    feature_request = args.task
    # change_plan = generate_js_change_plan(ai_model, call_graph, feature_request)
    # print("\n[🔧 Change Plan for JavaScript]:\n", change_plan)


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


