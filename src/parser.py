import os
import networkx as nx
import tree_sitter_javascript as tsJavaScript
from tree_sitter import Language, Parser

JS_LANGUAGE = Language(tsJavaScript.language())
parser = Parser(JS_LANGUAGE)

# Graph to store function dependencies
call_graph = nx.DiGraph()

def parse_code(file_path):
    """Parse code and extract function definitions & calls."""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    tree = parser.parse(bytes(code, "utf8"))
    root = tree.root_node

    functions = []
    calls = []
    function_stack = []  # Keep track of current function/method context

    def extract_methods(node, class_name=None):
        """Recursively extract class methods and function calls."""
        nonlocal function_stack

        for child in node.children:
            if child.type == "class_declaration":
                class_name = child.child_by_field_name("name").text.decode()
                extract_methods(child, class_name)

            elif child.type == "method_definition":
                method_name = child.child_by_field_name("name").text.decode()
                full_method_name = f"{class_name}.{method_name}" if class_name else method_name
                
                # Add function to list and push to stack
                functions.append(full_method_name)
                function_stack.append(full_method_name)

                extract_methods(child, class_name)

                # Remove from stack after processing
                function_stack.pop()

            elif child.type == "call_expression":
                if function_stack:  # Ensure we are inside a function context
                    caller = function_stack[-1]  # Current function
                    callee = child.child_by_field_name("function").text.decode()
                    calls.append((caller, callee))

            extract_methods(child, class_name)

    extract_methods(root)
    return functions, calls

def analyze_project(directory):
    """Analyze the project and build call graph."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".js")):
                file_path = os.path.join(root, file)
                functions, calls = parse_code(file_path)

                for func in functions:
                    call_graph.add_node(func, file_path=file_path)

                for caller, callee in calls:
                    call_graph.add_edge(caller, callee)
    return call_graph
