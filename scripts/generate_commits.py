"""
Generate Commit-Level Metrics for GitHub Dashboard
All outputs are PNG files in metrics/commits/
"""

import os
import requests
from pathlib import Path
from collections import Counter
import matplotlib
matplotlib.use("Agg")  # headless mode for GitHub Actions
import matplotlib.pyplot as plt
from textblob import TextBlob

# -------------------------------
# Configuration
# -------------------------------
repo_env = os.environ.get("GITHUB_REPOSITORY")
if not repo_env:
    raise RuntimeError("GITHUB_REPOSITORY environment variable not set")

USERNAME = repo_env.split("/")[0]
TOKEN = os.environ.get("GH_TOKEN")
if not TOKEN:
    raise RuntimeError("GH_TOKEN environment variable not set")

HEADERS = {"Authorization": f"token {TOKEN}"}

OUTPUT_DIR = Path("metrics/commits")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Fetch all repos (top 5 for performance)
repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos", headers=HEADERS).json()[:5]

# -------------------------------
# 1️⃣ Commits per Repo + Avg Commit Length
# -------------------------------
commit_lengths = []
commit_counts = {}

for repo in repos:
    name = repo["name"]
    commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{name}/commits", headers=HEADERS).json()
    count = len(commits)
    commit_counts[name] = count

    # collect commit lengths
    for c in commits:
        msg = c["commit"]["message"]
        commit_lengths.append(len(msg))

# Save commits per repo as text image
plt.figure(figsize=(8,4))
if commit_counts:
    y_pos = range(len(commit_counts))
    plt.barh(list(commit_counts.keys()), list(commit_counts.values()), color="skyblue")
    plt.xlabel("Number of Commits")
    plt.title("Commits per Repo")
else:
    plt.text(0.5,0.5,"No commits available", ha="center", va="center", fontsize=14)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "commits_per_repo.png")
plt.close()

# Average commit length
avg_length = sum(commit_lengths)/len(commit_lengths) if commit_lengths else 0
plt.figure(figsize=(4,4))
plt.bar(["Average Commit Length"], [avg_length], color="orange")
plt.ylabel("Chars")
plt.title("Average Commit Length")
plt.savefig(OUTPUT_DIR / "avg_commit_length.png")
plt.close()

# -------------------------------
# 2️⃣ Commit Message Sentiment
# -------------------------------
sentiments = {"positive":0, "negative":0, "neutral":0}
all_messages = []

for repo in repos:
    commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits", headers=HEADERS).json()
    for c in commits:
        all_messages.append(c["commit"]["message"])

for msg in all_messages:
    polarity = TextBlob(msg).sentiment.polarity
    if polarity > 0.1:
        sentiments["positive"] += 1
    elif polarity < -0.1:
        sentiments["negative"] += 1
    else:
        sentiments["neutral"] += 1

plt.figure(figsize=(6,4))
plt.bar(sentiments.keys(), sentiments.values(), color=["green","red","gray"])
plt.title("Commit Message Sentiment")
plt.savefig(OUTPUT_DIR / "commit_sentiment.png")
plt.close()

# -------------------------------
# 3️⃣ Commits per Repo Topic
# -------------------------------
topic_counter = Counter()
for repo in repos:
    topics_url = repo.get("topics_url") or f"https://api.github.com/repos/{USERNAME}/{repo['name']}/topics"
    topics_resp = requests.get(topics_url, headers={**HEADERS, "Accept":"application/vnd.github.mercy-preview+json"}).json()
    topics = topics_resp.get("names", [])
    commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits", headers=HEADERS).json()
    for t in topics:
        topic_counter[t] += len(commits)

plt.figure(figsize=(8,4))
if topic_counter:
    plt.bar(topic_counter.keys(), topic_counter.values())
    plt.xticks(rotation=45)
else:
    plt.text(0.5,0.5,"No topics available", ha="center", va="center", fontsize=14)
plt.title("Commits per Repo Topic")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "commits_per_topic.png")
plt.close()

# -------------------------------
# 4️⃣ Commits by Branch
# -------------------------------
branch_counter = Counter()
for repo in repos:
    branches = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/branches", headers=HEADERS).json()
    for branch in branches:
        branch_name = branch["name"]
        commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits?sha={branch_name}", headers=HEADERS).json()
        branch_counter[branch_name] += len(commits)

plt.figure(figsize=(8,4))
if branch_counter:
    plt.bar(branch_counter.keys(), branch_counter.values())
    plt.xticks(rotation=45)
else:
    plt.text(0.5,0.5,"No branches found", ha="center", va="center", fontsize=14)
plt.title("Commits by Branch")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "commits_by_branch.png")
plt.close()

# -------------------------------
# 5️⃣ Most Frequently Edited Files
# -------------------------------
file_counter = Counter()
for repo in repos[:3]:
    commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits", headers=HEADERS).json()
    for c in commits:
        sha = c["sha"]
        commit_details = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits/{sha}", headers=HEADERS).json()
        for f in commit_details.get("files", []):
            file_counter[f["filename"]] += 1

top_files = dict(file_counter.most_common(10))
plt.figure(figsize=(8,4))
if top_files:
    plt.barh(list(top_files.keys()), list(top_files.values()), color="orange")
else:
    plt.text(0.5,0.5,"No files found", ha="center", va="center", fontsize=14)
plt.title("Top 10 Most Frequently Edited Files")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "top_files.png")
plt.close()

print("✅ Commit-level metrics generated successfully!")
