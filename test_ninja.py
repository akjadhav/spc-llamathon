import os
import sys
from graph_traversal import create_traversal_list_from_nodes
from test_generator import Test_Generator
import pdb 
from graph_node import GraphNode
import subprocess
import requests
import json
from extract_test_data import extract_data

def send_data_to_flask(testFileName=None, test_status_mapping=None, failed_lines=None):
    url = 'http://localhost:5002/receive_data'

    data = {
        'testFileName': testFileName,
        'testStatusMapping': test_status_mapping,
        'failedLines': failed_lines
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json_data, headers=headers)

def get_relative_path(absolute_path, base_path):
    # Ensure both paths are absolute
    absolute_path = os.path.abspath(absolute_path)
    base_path = os.path.abspath(base_path)

    # Get the relative path
    relative_path = os.path.relpath(absolute_path, base_path)
    
    return relative_path

def run_test_ninja(repo_path, node_list):    
    test_generator = Test_Generator(repo_path=repo_path)
    
    print("node file names")
    print("--------------------")

    file_path_counts = {}
    # Iterate over each node in the node_list
    for node in node_list:
        file_path = os.path.join(repo_path, node.file_path).replace(".js", ".test.js")
        if file_path in file_path_counts: file_path_counts[file_path] += 1
        else: file_path_counts[file_path] = 1
    
    print("repo_path:", repo_path)
    print(file_path_counts)
    print("--------------------")
    try:
        context_functions = []
        test_file_paths = []
        for node in node_list:
            target_file_info = (os.path.join(repo_path, node.file_path), (node.func_name, node.line_start, node.line_end))
            test_code, main_test_file_path = test_generator.generate_and_test(target_file_info, context_functions)
            print("Main test file path:", main_test_file_path)
            test_file_paths.append(main_test_file_path)
            print("Generated test code:\n", test_code)
            # Add the current node's information to the context for the next function
            context_functions.append((node.func_name, test_generator.read_functions_from_file(os.path.join(repo_path, node.file_path), (node.func_name, node.line_start, node.line_end))))

            curr_test_file_counts = {}
            # Keep track of how often a main_test_file_path has been seen
            for test_file_path in test_file_paths:
                if test_file_path in curr_test_file_counts: curr_test_file_counts[test_file_path] += 1
                else: curr_test_file_counts[test_file_path] = 1

            if curr_test_file_counts[main_test_file_path] == file_path_counts[main_test_file_path]:
                # We have generated all the tests for this file
                # Run the code and get the output
                print("LOG: The final running of tests is occruing")
                print("LOG: The main test file path is:", main_test_file_path)
                result = subprocess.run(['npx', 'jest', main_test_file_path], 
                        capture_output=True, 
                        text=True, 
                        cwd=repo_path)
                print("LOG: The result of the test run is:", result)

                print("Running Niall's code")

                # write result.stderr
                with open("stderr.txt", "w") as f:
                    f.write(result.stderr)

                with open("stdout.txt", "w") as f:
                    f.write(result.stdout)


                test_status_mapping, failed_context, failed_lines = extract_data(
                    result.stderr, # NAHUM LOOK HERE
                    main_test_file_path
                )

                        
                print('About to send data')
                send_data_to_flask(get_relative_path(main_test_file_path, repo_path), test_status_mapping, failed_lines)

    except Exception as e:
        print("Failed to generate a passing test:", str(e))


if "__main__" == __name__:
    # TODO: give actual local repo path
    repo_path = "spc-llamathon-example/utils"
    path = "spc-llamathon-example/utils/math.js"
    node_list = [GraphNode("multiply", path, 9, 11), GraphNode("sumOfSquares", path, 18, 21)]
    run_test_ninja(repo_path, node_list)

