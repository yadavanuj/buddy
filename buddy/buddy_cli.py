import os
import argparse
from dotenv import load_dotenv
from core import direct_from_gemini, gemini_with_filtered_call_graph
from db import create_table
# Load environment variables from the .env file
load_dotenv()
create_table()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code change planning CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ask
    ask_parser = subparsers.add_parser("ask-gemini", help="Ask gemini for code change directly. For small code base.")
    ask_parser.add_argument("source_directory", type=str, help="Path to the source directory")
    ask_parser.add_argument("task", type=str, help="Change to be planned for")
    ask_parser.set_defaults(func=direct_from_gemini)

    # plan
    plan_parser = subparsers.add_parser("search-and-gemini", help="Stores code embeddings localy and search on them to filter call graph.")
    plan_parser.add_argument("source_directory", type=str, help="Path to the source directory")
    plan_parser.add_argument("task", type=str, help="Change to be planned for")
    plan_parser.set_defaults(func=gemini_with_filtered_call_graph)

    # Parse arguments
    args = parser.parse_args()
    
    # Execute the appropriate command function
    args.func(args)
