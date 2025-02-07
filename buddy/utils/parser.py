import os
import networkx as nx
import tree_sitter_javascript as tsJavaScript
from tree_sitter import Language, Parser

JS_LANGUAGE = Language(tsJavaScript.language())
parser = Parser(JS_LANGUAGE)

# Graph to store function dependencies
call_graph = nx.DiGraph()

def parse_code(file_path):
    """Parse JavaScript code and extract function definitions & calls."""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    tree = parser.parse(bytes(code, "utf8"))
    root = tree.root_node

    functions = []
    calls = []
    function_stack = []  # Track the current function/method context

    def extract_methods(node, class_name=None):
        """Recursively extract class methods, function declarations, arrow functions, and calls."""
        nonlocal function_stack

        for child in node.children:
            if child.type == "class_declaration":
                class_name = child.child_by_field_name("name").text.decode()
                extract_methods(child, class_name)

            elif child.type == "function_declaration":
                # Regular function declaration
                function_name_node = child.child_by_field_name("name")
                if function_name_node:
                    function_name = function_name_node.text.decode()
                    functions.append(function_name)
                    function_stack.append(function_name)

                    extract_methods(child, class_name)
                    function_stack.pop()

            elif child.type == "variable_declaration":
                # Variable declarations (for arrow functions or function expressions)
                for declarator in child.children:
                    if declarator.type == "variable_declarator":
                        var_name_node = declarator.child_by_field_name("name")
                        if var_name_node:
                            var_name = var_name_node.text.decode()

                            # Check if the assigned value is a function (arrow function or function expression)
                            init_node = declarator.child_by_field_name("value")
                            if init_node and init_node.type in {"arrow_function", "function"}:
                                functions.append(var_name)
                                function_stack.append(var_name)

                                extract_methods(init_node, class_name)
                                function_stack.pop()

            elif child.type == "method_definition":
                # Class methods
                method_name = child.child_by_field_name("name").text.decode()
                full_method_name = f"{class_name}.{method_name}" if class_name else method_name

                functions.append(full_method_name)
                function_stack.append(full_method_name)

                extract_methods(child, class_name)
                function_stack.pop()

            elif child.type == "call_expression":
                # Function calls
                if function_stack:
                    caller = function_stack[-1]  # Current function
                    callee_node = child.child_by_field_name("function")
                    if callee_node:
                        callee = callee_node.text.decode()
                        calls.append((caller, callee))

            extract_methods(child, class_name)

    extract_methods(root)
    return functions, calls

def analyze_project(directory):
    """Analyze the project and build the call graph while skipping node_modules."""
    for root, _, files in os.walk(directory):
        if 'node_modules' in root:
            continue  # Skip the node_modules folder

        for file in files:
            if file.endswith(".js"):  # Process only JavaScript files
                file_path = os.path.join(root, file)
                functions, calls = parse_code(file_path)

                # Add functions and calls to the call graph
                for func in functions:
                    call_graph.add_node(func, path=file_path)

                for caller, callee in calls:
                    call_graph.add_edge(caller, callee)

    return call_graph
