"""
Generate Pull Request & Issue Metrics for GitHub Dashboard
All outputs are PNG files in metrics/prs_issues/
"""

import os
import requests
from pathlib import Path
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# -------------------------------
# Config
# -------------------------------
repo_env = os.environ.get("GITHUB_REPOSITORY")
if not repo_env:
    raise RuntimeError("GITHUB_REPOSITORY environment variable not set")
USERNAME = repo_env.split("/")[0]

TOKEN = os.environ.get("GH_TOKEN")
if not TOKEN:
    raise RuntimeError("GH_TOKEN environment variable not set")
HEADERS = {"Authorization": f"token {TOKEN}"}

OUTPUT_DIR = Path("metrics/prs_issues")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos", headers=HEADERS).json()[:5]

# -------------------------------
# 1️⃣ PR Merge Time
# -------------------------------
pr_merge_times = []
for repo in repos:
    pulls = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/pulls?state=closed", headers=HEADERS).json()
    for pr in pulls:
        if pr.get("merged_at"):
            created = datetime.fromisoformat(pr["created_at"].replace("Z","+00:00"))
            merged = datetime.fromisoformat(pr["merged_at"].replace("Z","+00:00"))
            delta = (merged - created).total_seconds()/3600
            pr_merge_times.append(delta)

plt.figure(figsize=(8,4))
plt.hist(pr_merge_times, bins=20, color="skyblue")
plt.title("PR Open → Merge Time (hours)")
plt.xlabel("Hours")
plt.ylabel("PR Count")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "pr_merge_time.png")
plt.close()

# -------------------------------
# 2️⃣ PR Size (Lines Added + Deleted)
# -------------------------------
pr_sizes = []
for repo in repos:
    pulls = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/pulls?state=closed", headers=HEADERS).json()
    for pr in pulls:
        if pr.get("merged_at"):
            sha = pr["merge_commit_sha"]
            if sha:
                commit = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits/{sha}", headers=HEADERS).json()
                stats = commit.get("stats", {})
                pr_sizes.append(stats.get("additions",0) + stats.get("deletions",0))

plt.figure(figsize=(8,4))
plt.hist(pr_sizes, bins=20, color="orange")
plt.title("PR Size (Lines Changed)")
plt.xlabel("Lines Changed")
plt.ylabel("PR Count")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "pr_size.png")
plt.close()

# -------------------------------
# 3️⃣ PR Comments Received/Given
# -------------------------------
pr_comments = []
for repo in repos:
    pulls = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/pulls?state=all", headers=HEADERS).json()
    for pr in pulls:
        pr_comments.append(pr.get("comments",0) + pr.get("review_comments",0))

plt.figure(figsize=(8,4))
plt.hist(pr_comments, bins=20, color="green")
plt.title("PR Comments Received/Given")
plt.xlabel("Number of Comments")
plt.ylabel("PR Count")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "pr_comments.png")
plt.close()

# -------------------------------
# 4️⃣ PR Approval Rate
# -------------------------------
approvals = 0
total_reviews = 0
for repo in repos:
    pulls = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/pulls?state=all", headers=HEADERS).json()
    for pr in pulls:
        reviews = requests.get(pr["url"] + "/reviews", headers=HEADERS).json()
        for review in reviews:
            if review["user"]["login"].lower() == USERNAME.lower():
                total_reviews += 1
                if review["state"].lower() == "approved":
                    approvals += 1

approval_rate = (approvals / total_reviews*100) if total_reviews else 0
plt.figure(figsize=(4,4))
plt.bar(["Approval Rate"], [approval_rate], color="purple")
plt.ylim(0,100)
plt.ylabel("% Approved")
plt.title("PR Approval Rate")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "pr_approval_rate.png")
plt.close()

# -------------------------------
# 5️⃣ Issue Age Distribution
# -------------------------------
issue_ages = []
for repo in repos:
    issues = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/issues?state=all", headers=HEADERS).json()
    for issue in issues:
        if "pull_request" not in issue:
            created = datetime.fromisoformat(issue["created_at"].replace("Z","+00:00"))
            closed = datetime.fromisoformat(issue["closed_at"].replace("Z","+00:00")) if issue.get("closed_at") else datetime.utcnow()
            delta = (closed - created).days
            issue_ages.append(delta)

plt.figure(figsize=(8,4))
plt.hist(issue_ages, bins=20, color="red")
plt.title("Issue Age Distribution (days)")
plt.xlabel("Days")
plt.ylabel("Issue Count")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "issue_age.png")
plt.close()

# -------------------------------
# 6️⃣ Closed vs Open Issues by Repo
# -------------------------------
closed_open = {}
for repo in repos:
    issues = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/issues?state=all", headers=HEADERS).json()
    closed_open[repo["name"]] = {"open":0,"closed":0}
    for issue in issues:
        if "pull_request" not in issue:
            if issue.get("state") == "open":
                closed_open[repo["name"]]["open"] += 1
            else:
                closed_open[repo["name"]]["closed"] += 1

plt.figure(figsize=(10,4))
repos_list = list(closed_open.keys())
open_counts = [closed_open[r]["open"] for r in repos_list]
closed_counts = [closed_open[r]["closed"] for r in repos_list]
plt.bar(repos_list, open_counts, label="Open", color="orange")
plt.bar(repos_list, closed_counts, bottom=open_counts, label="Closed", color="green")
plt.xticks(rotation=45)
plt.ylabel("Issue Count")
plt.title("Closed vs Open Issues by Repo")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "closed_vs_open.png")
plt.close()

# -------------------------------
# 7️⃣ Top Issue & PR Labels
# -------------------------------
label_counter = Counter()
for repo in repos:
    # Issues
    issues = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/issues?state=all", headers=HEADERS).json()
    for i in issues:
        if "pull_request" not in i:
            for label in i.get("labels", []):
                label_counter[label["name"]] += 1
    # PRs
    pulls = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/pulls?state=all", headers=HEADERS).json()
    for pr in pulls:
        for label in pr.get("labels", []):
            label_counter[label["name"]] += 1

top_labels = dict(label_counter.most_common(10))
plt.figure(figsize=(8,4))
plt.bar(top_labels.keys(), top_labels.values(), color="skyblue")
plt.xticks(rotation=45)
plt.title("Top Issue Labels Used")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "top_labels.png")
plt.close()

# -------------------------------
# 8️⃣ PR Review Latency (Time to First Review)
# -------------------------------
review_latencies = []
for repo in repos:
    pulls = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/pulls?state=all", headers=HEADERS).json()
    for pr in pulls:
        reviews = requests.get(pr["url"] + "/reviews", headers=HEADERS).json()
        if reviews:
            first_review = min(datetime.fromisoformat(r["submitted_at"].replace("Z","+00:00")) for r in reviews)
            created = datetime.fromisoformat(pr["created_at"].replace("Z","+00:00"))
            latency = (first_review - created).total_seconds()/3600
            review_latencies.append(latency)

plt.figure(figsize=(8,4))
plt.hist(review_latencies, bins=20, color="purple")
plt.title("PR Review Latency (hours)")
plt.xlabel("Hours")
plt.ylabel("PR Count")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "pr_review_latency.png")
plt.close()

# -------------------------------
# 9️⃣ PR Merge Method Distribution
# -------------------------------
merge_methods = Counter()
for repo in repos:
    pulls = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/pulls?state=all", headers=HEADERS).json()
    for pr in pulls:
        method = pr.get("mergeable_state","unknown")
        merge_methods[method] += 1

plt.figure(figsize=(8,4))
plt.bar(merge_methods.keys(), merge_methods.values(), color="orange")
plt.title("PR Merge Method Distribution")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "pr_merge_method.png")
plt.close()

print("✅ PR & Issue metrics generated successfully!")
