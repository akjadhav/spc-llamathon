# ngrok http 5000

from flask import Flask, request, jsonify
import hmac
import hashlib
from git import Repo, GitCommandError
import os

app = Flask(__name__)

# Replace with your GitHub webhook secret and personal access token
GITHUB_SECRET = 'your_secret_here'
GITHUB_TOKEN = 'your_personal_access_token_here'

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
            process_pull_request(repo_name, pr_number, head_ref)
            return jsonify({'message': 'PR processed'}), 200

    return jsonify({'message': 'Event not handled'}), 200

def process_pull_request(repo_name, pr_number, head_ref):
    # Clone the repo or fetch the latest changes
    repo_path = f'/tmp/{repo_name}'
    repo_url = f'https://{GITHUB_TOKEN}@github.com/{repo_name}.git'
    
    if os.path.exists(repo_path):
        repo = Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
    else:
        repo = Repo.clone_from(repo_url, repo_path)

    # Fetch the PR branch
    try:
        origin = repo.remotes.origin
        origin.fetch(f'pull/{pr_number}/head:{head_ref}')
        repo.git.checkout(head_ref)
    except GitCommandError as e:
        print(f"Error fetching PR: {e}")
        return

    # Get changed files
    changed_files = [item.a_path for item in repo.index.diff('HEAD~1')]
    for file in changed_files:
        diff = repo.git.diff('HEAD~1', file)
        # TODO logic to have changed tuple (path, function changed)
        print(f"Changes in {file}:\n{diff}\n")

    # Example change: Append a comment to a file
    # TODO change logic
    example_file_path = os.path.join(repo_path, 'example_file.txt')
    with open(example_file_path, 'a') as file:
        file.write("\n# This is an automated comment added by the webhook")

    # Push changes to the PR branch
    push_changes_to_pr(repo, example_file_path, head_ref)

def push_changes_to_pr(repo, file_path, branch_name):
    repo.index.add([file_path])
    repo.index.commit('Automated commit from webhook') # TODO Replace with a more descriptive commit message
    origin = repo.remotes.origin
    origin.push(refspec=f'{branch_name}:{branch_name}')
    print(f"Changes pushed to branch {branch_name}")

if __name__ == '__main__':
    app.run(debug=True, port=5000)