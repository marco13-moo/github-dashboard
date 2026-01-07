import os
import requests
from pathlib import Path
import matplotlib.pyplot as plt

#USERNAME = "your-username"

repo = os.environ.get("GITHUB_REPOSITORY")

if not repo:
    raise RuntimeError("GITHUB_REPOSITORY environment variable not set")

USERNAME = repo.split("/")[0]

TOKEN = os.environ.get("GH_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}
OUTPUT_DIR = Path("../metrics/ci_cd")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Get workflow runs (example for one repo)
repo = "example-repo"
runs = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo}/actions/runs", headers=HEADERS).json()
statuses = [run["conclusion"] for run in runs.get("workflow_runs", [])]

success_count = statuses.count("success")
failure_count = statuses.count("failure")

plt.bar(["Success", "Failure"], [success_count, failure_count])
plt.title(f"Workflow Success Rate - {repo}")
plt.savefig(OUTPUT_DIR / "workflow_success.png")
plt.close()
