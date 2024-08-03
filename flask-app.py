# ngrok http 5002

from flask import Flask, request, jsonify # type: ignore
import hmac
import hashlib
import shutil
from git import Repo, GitCommandError # type: ignore
import os
from dotenv import load_dotenv # type: ignore
import re

from graph_node import GraphNode
from graph_traversal import create_traversal_list_from_nodes

load_dotenv()

app = Flask(__name__)

GITHUB_SECRET = os.getenv("GITHUB_SECRET")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def verify_github_signature(request):
    signature = request.headers.get('X-Hub-Signature')
    if not signature:
        return False
    sha_name, signature = signature.split('=')
    if sha_name != 'sha1':
        return False
    mac = hmac.new(bytes(GITHUB_SECRET, 'utf-8'), msg=request.data, digestmod=hashlib.sha1)
    return hmac.compare_digest(str(mac.hexdigest()), str(signature))

@app.route('/webhook', methods=['POST'])
def webhook():
    if not verify_github_signature(request):
        return jsonify({'message': 'Invalid signature'}), 400

    event = request.headers.get('X-GitHub-Event')
    if event == 'pull_request':
        payload = request.json
        action = payload.get('action')
        if action in ['opened', 'synchronize']:
            pr = payload.get('pull_request')
            repo_name = payload['repository']['full_name']
            pr_number = pr['number']
            head_ref = pr['head']['ref']
            base_ref = pr['base']['ref']
            process_pull_request(repo_name, pr_number, head_ref, base_ref)
            return jsonify({'message': 'PR processed'}), 200

    return jsonify({'message': 'Event not handled'}), 200

def parse_diff_for_filenames_and_functions(diff_output, repo_path):
    # Regular expression to match the diff header line that contains the file name and path
    diff_header_regex = re.compile(r'^diff --git a/(.+?) b/\1$')
    # Regular expression to match function definitions in Node.js, ignoring lines with "if"
    function_regex = re.compile(r'''
        (?!.*\bif\b)                  # Ignore lines containing "if"
        (?:static\s+)?                # Optional 'static' keyword
        (?:async\s+)?                 # Optional 'async' keyword
        (?:\*?\s*)?                   # Optional '*' for generator functions
        (\w+)\s*\([^)]*\)\s*\{        # Function name with parameters
        |                             # OR
        (?!.*\bif\b)                  # Ignore lines containing "if"
        (\w+)\s*=\s*\([^)]*\)\s*=>\s*\{ # Arrow function expression
    ''', re.VERBOSE)

    # Split the diff output into lines
    lines = diff_output.split('\n')

    # Initialize a dictionary to store file paths and their respective edited functions
    file_functions = {}

    current_file = None
    current_changes = []

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
        elif current_file and line.startswith('@@'):
            # Extract line numbers from diff hunk header
            hunk_header = line
            start_line = int(re.search(r'\+(\d+)', hunk_header).group(1))
            current_changes.append(start_line)
        elif current_file and line.startswith('+') and not line.startswith('+++'):
            # Collect the actual line changes
            current_changes[-1] += 1

    node_list = []

    # Process the last collected changes
    if current_file:
        functions = find_functions_in_file(current_file, current_changes, repo_path, function_regex)
        file_functions[current_file] = functions

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

        for line_num in changed_lines:
            function_name = None
            function_start_line_num = None
            function_end_line_num = None
            # Look backwards from the changed line to find the wrapping function
            for i in range(line_num - 1, -1, -1):
                line = file_contents[i].strip()
                if not re.search(r'\bif\b', line) and '{' in line:
                    function_match = function_regex.search(line)
                    if function_match:
                        function_name = function_match.group(1) or function_match.group(2)
                        function_start_line_num = i + 1
                        break

            if function_name:
                # Find the end line number for the function
                open_braces = 0
                for j in range(function_start_line_num - 1, len(file_contents)):
                    line = file_contents[j]
                    open_braces += line.count('{')
                    open_braces -= line.count('}')
                    if open_braces == 0:
                        function_end_line_num = j + 1
                        break

                functions.append((function_name, function_start_line_num, function_end_line_num))

    return functions

def process_pull_request(repo_name, pr_number, head_ref, base_ref):
    try:
        print(f"Processing PR #{pr_number} from repo {repo_name}")
        # Clone the repo or fetch the latest changes
        repo_path = f'/tmp/{repo_name}'
        repo_url = f'https://{GITHUB_TOKEN}@github.com/{repo_name}.git'
        
        try:
            if os.path.exists(repo_path):
                repo = Repo(repo_path)
                origin = repo.remotes.origin
                print("Attempting to pull latest changes...")
                pull_info = origin.pull()
                print(f"Pull result: {pull_info}")
            else:
                print("Cloning the repository...")
                repo = Repo.clone_from(repo_url, repo_path)
                origin = repo.remotes.origin
        except GitCommandError as e:
            print(f"Error processing PR: {e}")
            print(f"stderr output: {e.stderr}")
            return

        # Fetch the PR branch
        try:
            print(f"Fetching the PR branch {head_ref}...")
            origin.fetch(f'pull/{pr_number}/head:{head_ref}')
            repo.git.checkout(head_ref)
        except GitCommandError as e:
            print(f"Error fetching PR: {e}")
            return

        # Get all changed files between the base branch and the PR branch
        try:
            merge_base = repo.git.merge_base(base_ref, head_ref).strip()
            print(f"Merge base: {merge_base}")
            changed_files = repo.git.diff('--name-only', merge_base, head_ref).split('\n')
        except GitCommandError as e:
            print(f"Error getting changed files: {e}")
            return

        print(f"Changed files: {changed_files}")

        all_changed_nodes = []

        for file in changed_files:
            if file:
                diff = repo.git.diff(merge_base, head_ref, file)
                parsed_diff = parse_diff_for_filenames_and_functions(diff, repo_path)
                for node in parsed_diff:
                    print(f"{node.toString()}")
                all_changed_nodes.extend(parsed_diff)

        # Create a graph from the changed nodes
        node_list = create_traversal_list_from_nodes(repo_path, all_changed_nodes)

        clean_up_local_repo(repo_path)
    except (GitCommandError, Exception) as e:
        print(f"Error processing PR: {e}")
        
        clean_up_local_repo(repo_path)
    # Example change: Append a comment to a file
    # TODO change logic
    # example_file_path = os.path.join(repo_path, 'example_file.txt')
    # with open(example_file_path, 'a') as file:
    #     file.write("\n# This is an automated comment added by the webhook")

    # # Push changes to the PR branch
    # push_changes_to_pr(repo, example_file_path, head_ref)

def push_changes_to_pr(repo, file_path, branch_name):
    repo.index.add([file_path])
    repo.index.commit('Automated commit from webhook') # TODO Replace with a more descriptive commit message
    origin = repo.remotes.origin
    origin.push(refspec=f'{branch_name}:{branch_name}')
    print(f"Changes pushed to branch {branch_name}")

def clean_up_local_repo(repo_path):
    try:
        print(f"Cleaning up local repository at {repo_path}...")
        shutil.rmtree(repo_path)
        print("Clean up successful.")
    except Exception as e:
        print(f"Error cleaning up local repository: {e}")

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=5002)