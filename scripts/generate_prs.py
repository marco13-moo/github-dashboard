import os
import requests
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

USERNAME = "your-username"
TOKEN = os.environ.get("GH_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}

OUTPUT_DIR = Path("../metrics/prs_issues")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Fetch repos
repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos", headers=HEADERS).json()

pr_merge_times = []

for repo in repos[:5]:
    pulls = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/pulls?state=closed", headers=HEADERS).json()
    for pr in pulls:
        if pr.get("merged_at"):
            created = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
            merged = datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00"))
            delta = (merged - created).total_seconds() / 3600  # in hours
            pr_merge_times.append(delta)

# ---- PR Merge Time Histogram ----
plt.hist(pr_merge_times, bins=20)
plt.title("PR Open → Merge Time (hours)")
plt.xlabel("Hours")
plt.ylabel("PR Count")
plt.savefig(OUTPUT_DIR / "pr_merge_time.png")
plt.close()
