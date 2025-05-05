from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse

app = Flask(__name__)

@app.route("/repo-info", methods=["POST"])
def repo_info():
    data = request.get_json()
    repo_url = data.get("repo_url")

    try:
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip("/").split("/")
        owner, repo = path_parts[0], path_parts[1]

        headers = {"Accept": "application/vnd.github.v3+json"}
        repo_api = f"https://api.github.com/repos/{owner}/{repo}"
        contributors_api = f"{repo_api}/contributors"
        commits_api = f"{repo_api}/commits"

        repo_data = requests.get(repo_api, headers=headers).json()
        contributors = requests.get(contributors_api, headers=headers).json()
        commits = requests.get(commits_api, headers=headers).json()

        return jsonify({
            "name": repo_data.get("name"),
            "stars": repo_data.get("stargazers_count"),
            "forks": repo_data.get("forks_count"),
            "commits": len(commits),
            "contributors": len(contributors)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
