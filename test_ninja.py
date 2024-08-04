import os
import sys
from graph_traversal import create_traversal_list_from_nodes
from test_generator import Test_Generator
import pdb 
from graph_node import GraphNode

def run_test_ninja(repo_path, node_list):
    test_generator = Test_Generator()

    print((node.file_path, (node.func_name, node.line_start, node.line_end)) for node in node_list)
    print("--------------------")
    try:

        context_functions = []
        for node in node_list:
            target_file_info = (os.path.join(repo_path, node.file_path), (node.func_name, node.line_start, node.line_end))
            test_code = test_generator.generate_and_test(target_file_info, context_functions)
            print("Generated test code:\n", test_code)
            # Add the current node's information to the context for the next function
            context_functions.append((node.func_name, test_generator.read_functions_from_file(os.path.join(repo_path, node.file_path), (node.func_name, node.line_start, node.line_end))))
    except Exception as e:
        print("Failed to generate a passing test:", str(e))


if "__main__" == __name__:
    # TODO: give actual local repo path
    repo_path = "spc-llamathon-example/utils"
    path = "spc-llamathon-example/utils/math.js"
    node_list = [GraphNode("multiply", path, 9, 11), GraphNode("sumOfSquares", path, 18, 21)]
    run_test_ninja(repo_path, node_list)