# ngrok http 5002

from flask import Flask, request, jsonify, abort # type: ignore
import hmac
import hashlib
import shutil
from git import Repo, GitCommandError # type: ignore
import os
from dotenv import load_dotenv # type: ignore
import re
from flask_cors import CORS
from datetime import datetime, timedelta

from graph_node import GraphNode
from graph_traversal import create_traversal_list_from_nodes
from test_ninja import run_test_ninja
from bot_status import BotStatus

import pdb

load_dotenv()

app = Flask(__name__)
cors = CORS(app)

GITHUB_SECRET = os.getenv("GITHUB_SECRET")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Global data list to store updates
data = []

repo_path = '/tmp/akjadhav/spc-llamathon-example'

test_hash = {}

bot = BotStatus()

def verify_github_signature(request):
    signature = request.headers.get('X-Hub-Signature')
    if not signature:
        return False
    sha_name, signature = signature.split('=')
    if sha_name != 'sha1':
        return False
    mac = hmac.new(bytes(GITHUB_SECRET, 'utf-8'), msg=request.data, digestmod=hashlib.sha1)
    return hmac.compare_digest(str(mac.hexdigest()), str(signature))

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()

    if not data:
        abort(400, description="No data received")

    if data.get('testFileName'):
        add_test_file_update(data['testFileName'], "Test generated for " + data['testFileName'], inProgress=False)

    if (data.get('failedLines') and data.get('testFileName') and data.get('testStatusMapping')):
        print(f"Failed lines received for {data['testFileName']}: {data['failedLines']}")
        print(f"Test status mapping for {data['testFileName']}: {data['testStatusMapping']}")

        add_text_update(f"Ran tests from {data['testFileName']}", inProgress=False)
        add_text_update(f"Identified failed lines in {data['testFileName']}", inProgress=False)

        test_hash[data['testFileName']] = {'failedLines': data['failedLines'], 
                                           'testStatusMapping': data['testStatusMapping']}

    return jsonify({"message": "Data received", "data": data}), 200

@app.route('/receive_test_ninja_update', methods=['POST'])
def receive_test_ninja_update():
    data = request.get_json()

    if not data:
        abort(400, description="No data received")

    if data:
        add_text_update(data['text'], inProgress=data['inProgress'], key=data['key'])

    return jsonify({"message": "Data received", "data": data}), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    if not verify_github_signature(request):
        return jsonify({'message': 'Invalid signature'}), 400

    event = request.headers.get('X-GitHub-Event')
    if event == 'pull_request':
        payload = request.json
        action = payload.get('action')
        if action in ['opened']:
            pr = payload.get('pull_request')
            repo_name = payload['repository']['full_name']
            pr_number = pr['number']
            head_ref = pr['head']['ref']
            base_ref = pr['base']['ref']
            print('\n\n')
            process_pull_request(repo_name, pr_number, head_ref, base_ref)
            return jsonify({'message': 'PR processed'}), 200

    return jsonify({'message': 'Event not handled'}), 200

@app.route('/api/status', methods=['GET'])
def bot_status():
    data = bot.get_current_status()
    response = jsonify(data)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/api/get_file', methods=['POST'])
def get_file_from_request():
    file_name = request.json.get('fileName')

    print(file_name)
    
    if not file_name:
        abort(400, description="File name is required")
    
    try:
        file_path = os.path.join(repo_path, file_name)
        print('File path:', file_path)
        
        if not os.path.exists(file_path):
            abort(404, description=f"File not found at path: {file_path}")
        
        with open(file_path, 'r') as file:
            file_contents = file.read()

        if file_name not in test_hash.keys():
            test_hash[file_name] = {'failedLines': [], 'testStatusMapping': {}}
        test_file_metadata = test_hash[file_name]
        
        data = {
            'type': 'test' if '.test.' in file_name else 'comment',
            'data': file_contents,
            'testStatus': test_file_metadata['testStatusMapping'],
            'failedLines': test_file_metadata['failedLines'],
            'fileName': file_name,
            'failed': len(test_file_metadata['failedLines']) > 0
        }
        
        return jsonify(data), 200
    
    except Exception as e:
        abort(500, description=f"Error processing request: {str(e)}")

@app.route('/api/update', methods=['GET'])
def send_update():
    response = jsonify(data)
    response.headers['Content-Type'] = 'application/json'
    return response

def add_text_update(text, inProgress=False, key=None):
    current_time = datetime.now()
    
    global data
    # data = [item for item in data if current_time - item['timestamp'] < timedelta(seconds=15)]
    
    data.append({
        'key': key if key else text,
        'type': 'text',
        'pathFileName': 'N/A',
        'description': text,
        'inProgress': inProgress,
        'timestamp': current_time
    })

def add_test_file_update(pathFileName, text, inProgress=False, key=None):
    current_time = datetime.now()
    
    global data
    # data = [item for item in data if current_time - item['timestamp'] < timedelta(seconds=15)]
    
    data.append({
        'key': key if key else text,
        'type': 'test',
        'pathFileName': pathFileName,
        'description': text,
        'inProgress': inProgress,
        'timestamp': current_time
    })

def add_comment_update(pathFileName, text, inProgress=False, key=None):
    current_time = datetime.now()
    
    global data
    # data = [item for item in data if current_time - item['timestamp'] < timedelta(seconds=15)]
    
    data.append({
        'key': key if key else text,
        'type': 'comment',
        'pathFileName': pathFileName,
        'description': text,
        'inProgress': inProgress,
        'timestamp': current_time
    })

def add_generate_update(pathFileName, text, node, inProgress=False, key=None):
    current_time = datetime.now()
    
    global data
    # data = [item for item in data if current_time - item['timestamp'] < timedelta(seconds=15)]
    
    data.append({
        'key': key if key else text,
        'type': 'generate',
        'pathFileName': pathFileName,
        'description': text,
        'functionName': node,
        'inProgress': inProgress,
        'timestamp': current_time
    })

def add_edit_file_update(pathFileName, text, inProgress=False, key=None):
    current_time = datetime.now()
    
    global data
    # data = [item for item in data if current_time - item['timestamp'] < timedelta(seconds=15)]
    
    data.append({
        'key': key if key else text,
        'type': 'edit',
        'pathFileName': pathFileName,
        'description': text,
        'inProgress': inProgress,
        'timestamp': current_time
    })

# Example usage
# @app.route('/api/add_update/<update>', methods=['GET'])
# def add_update_route(update):
#     add_update(update)
#     return "Update added successfully", 200

def parse_diff_for_filenames_and_functions(diff_output, repo_path):
    # Regular expression to match the diff header line that contains the file name and path
    diff_header_regex = re.compile(r'^diff --git a/(.+?) b/\1$')
    # Regular expression to match function definitions in Node.js, ignoring lines with "if"
    function_regex = re.compile(r'''
        ^(?!.*\bif\b)                # Ignore lines containing "if" at the beginning
        \s*(?:                       # Optional whitespace at the start
            (?:async\s+)?            # Optional 'async' keyword
            (?:function\s+)?         # Optional 'function' keyword
            (\w+)                    # Function name (group 1)
            \s*\([^)]*\)             # Function parameters
            \s*{                     # Opening brace
        |                            # OR
            (?:const|let|var)\s+     # Variable declaration
            (\w+)                    # Function name (group 2)
            \s*=\s*                  # Assignment
            (?:async\s+)?            # Optional 'async' keyword
            (?:function\s*)?         # Optional 'function' keyword
            \([^)]*\)                # Function parameters
            \s*=>                    # Arrow function syntax
        |                            # OR
            (\w+)                    # Method name (group 3)
            \s*:\s*                  # Colon (for object method)
            (?:async\s+)?            # Optional 'async' keyword
            (?:function\s*)?         # Optional 'function' keyword
            \([^)]*\)                # Function parameters
            \s*{                     # Opening brace
        )
    ''', re.VERBOSE | re.MULTILINE)

    # Split the diff output into lines
    lines = diff_output.split('\n')

    # Initialize a dictionary to store file paths and their respective edited functions
    file_functions = {}

    current_file = None
    current_changes = []
    current_line = 0

    # Iterate over the lines to find all that match our regex
    for line in lines:
        match = diff_header_regex.match(line)
        if match:
            if current_file:
                # Process the previously collected changes for the current file
                functions = find_functions_in_file(current_file, current_changes, repo_path, function_regex)
                file_functions[current_file] = functions
            
            # Extract the new file name and path
            current_file = match.group(1)
            current_changes = []
            current_line = 0
        elif current_file and line.startswith('@@'):
            # Extract line numbers from diff hunk header
            hunk_header = line
            matches = re.search(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@', hunk_header)
            if matches:
                current_line = int(matches.group(1)) - 1
                line_count = int(matches.group(2)) if matches.group(2) else 1
        elif current_file and line.startswith('+') and not line.startswith('+++'):
            # Collect the actual line changes
            current_line += 1
            current_changes.append(current_line)
        elif current_file and not line.startswith('-'):
            # Increment line count for context lines
            current_line += 1

    # Process the last collected changes
    if current_file:
        functions = find_functions_in_file(current_file, current_changes, repo_path, function_regex)
        file_functions[current_file] = functions

    node_list = []

    for file, functions in file_functions.items():
        for function in functions:
            function_name, line_start, line_end = function
            node = GraphNode(func_name=function_name, file_path=file, line_start=line_start, line_end=line_end)
            node_list.append(node)

    return node_list

def find_functions_in_file(file_path, changed_lines, repo_path, function_regex):
    functions = []
    full_path = os.path.join(repo_path, file_path)

    if os.path.exists(full_path):
        with open(full_path, 'r') as f:
            file_contents = f.readlines()

        changed_lines_set = set(changed_lines)
        function_stack = []
        open_braces = 0

        for i, line in enumerate(file_contents, start=1):
            stripped_line = line.strip()

            # Count braces before checking for new functions
            open_braces += stripped_line.count('{') - stripped_line.count('}')

            # Check if we're entering a new function
            match = function_regex.search(line)
            if match:
                function_name = match.group(1) or match.group(2) or match.group(3)

                exclude_keywords = ['if', 'while', 'for', 'switch', 'catch']

                if function_name and not any(keyword in line.lower() for keyword in exclude_keywords):
                    function_stack.append((function_name, i, None))

            # Check if we're exiting a function
            while open_braces == 0 and function_stack:
                function_name, start_line, _ = function_stack.pop()
                current_function = (function_name, start_line, i)
                
                # Check if any changed lines fall within this function
                if any(start_line <= line_num <= i for line_num in changed_lines_set):
                    functions.append(current_function)

            # print(f"Line {i}: {line.strip()}")
            # print(f"Open braces: {open_braces}")
            # print(f"Function stack: {function_stack}")
            # print(f"Changed lines: {list(changed_lines_set)}")
            # print()

            # If we've processed all changed lines, we can stop
            if changed_lines and i > max(changed_lines):
                break

    return functions

def process_pull_request(repo_name, pr_number, head_ref, base_ref):
    try:
        bot.set_status('RUNNING')
        global data
        data = []
        add_text_update(f"Processing PR #{pr_number} from repo {repo_name}", inProgress=True, key='processing_start_update')
        print(f"Processing PR #{pr_number} from repo {repo_name}")
        # Clone the repo or fetch the latest changes
        global repo_path
        repo_path = f'/tmp/{repo_name}'
        repo_url = f'https://{GITHUB_TOKEN}@github.com/{repo_name}.git'

        clean_up_local_repo(repo_path)

        #raise Exception("Test error")
        
        try:
            if os.path.exists(repo_path):
                add_text_update("Pulling latest changes...", inProgress=True)
                repo = Repo(repo_path)
                origin = repo.remotes.origin
                print("Attempting to pull latest changes...")
                pull_info = origin.pull()
                print(f"Pull result: {pull_info}")
                add_text_update("Pulling latest changes...", inProgress=False)
            else:
                add_text_update("Cloning the repository...", inProgress=True)
                print("Cloning the repository...")
                repo = Repo.clone_from(repo_url, repo_path)
                origin = repo.remotes.origin
                add_text_update("Cloning the repository...", inProgress=False)
        except GitCommandError as e:
            bot.set_status('ERROR')
            print(f"Error processing PR: {e}")
            print(f"stderr output: {e.stderr}")
            add_text_update(f"Error processing PR: {e}", inProgress=False)
            return

        # Fetch the PR branch
        try:
            add_text_update(f"Fetching the PR branch {head_ref}", inProgress=True)
            print(f"Fetching the PR branch {head_ref}")
            origin.fetch(f'pull/{pr_number}/head:{head_ref}')
            repo.git.checkout(head_ref)
            add_text_update(f"Fetching the PR branch {head_ref}", inProgress=False)
        except GitCommandError as e:
            bot.set_status('ERROR')
            print(f"Error fetching PR: {e}")
            return

        # Get all changed files between the base branch and the PR branch
        try:
            merge_base = repo.git.merge_base(base_ref, head_ref).strip()
            add_text_update(f"Merge base identified: {merge_base}", inProgress=False)
            print(f"Merge base: {merge_base}")
            changed_files = repo.git.diff('--name-only', merge_base, head_ref).split('\n')
        except GitCommandError as e:
            bot.set_status('ERROR')
            print(f"Error getting changed files: {e}")
            return

        print(f"Changed files: {changed_files}")

        for file in changed_files:
            add_text_update(f"File was changed: {file}", inProgress=False)
            add_edit_file_update(file, file + " changed in PR", inProgress=False)

        all_changed_nodes = []

        for file in changed_files:
            if file:
                diff = repo.git.diff(merge_base, head_ref, file)
                parsed_diff = parse_diff_for_filenames_and_functions(diff, repo_path)
                print(parsed_diff)
                for node in parsed_diff:
                    add_generate_update(file, f"Generated function node from changed code: {node}", node.getFuncName(), inProgress=False)
                    print(f"{node.toString()}")
                all_changed_nodes.extend(parsed_diff)

        # Agent that generates tests for all changed nodes is actited and runs
        # here!
        node_list = create_traversal_list_from_nodes(repo_path, all_changed_nodes)
        # node_list = [GraphNode("multiply", "utils/math.js", 9, 22), GraphNode("sumOfSquares", "utils/math.js", 18, 21)]

        print("============ Node List ============")
        for node in node_list:
            print(node.toString())
        print("===================================")

        add_text_update(f"Running TestNinja", inProgress=True, key='running_test_ninja_update')
        try:
            run_test_ninja(repo_path, node_list)
        except Exception as e:
            bot.set_status('ERROR')
            print(f"Error processing PR when running test ninja: {e}")
            add_text_update(f"Error processing PR: {e}", inProgress=False) 
        add_text_update(f"Running TestNinja", inProgress=False, key='running_test_ninja_update')

        push_changes_to_pr(repo, head_ref)

        end_process(repo_path)
    except (GitCommandError, Exception) as e:
        print(f"Error processing PR: {e}")
        bot.set_status('ERROR')
        
def push_changes_to_pr(repo, branch_name):
    add_text_update(f"Pushing changes to git", inProgress=True)
    repo.git.add(A=True)
    repo.index.commit('Commit from TestNinja')
    origin = repo.remotes.origin
    origin.push(refspec=f'{branch_name}:{branch_name}')
    add_text_update(f"Pushing changes to git", inProgress=False)
    print(f"Changes pushed to branch {branch_name}")

def clean_up_local_repo(repo_path):
    try:
        # check if repo exists
        if os.path.exists(repo_path):
            print(f"Cleaning up local repository at {repo_path}")
            shutil.rmtree(repo_path)
            print("Clean up successful.")
    except Exception as e:
        bot.set_status('ERROR')
        print(f"Error cleaning up local repository: {e}")

def end_process(repo_path):
    bot.set_status('COMPLETE')
    add_text_update(f"Processing", inProgress=False, key='processing_start_update')
    add_text_update(f"Cleaning up local repository at {repo_path}", inProgress=False)
    add_text_update(f"Clean up successful.", inProgress=False)

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=5002)