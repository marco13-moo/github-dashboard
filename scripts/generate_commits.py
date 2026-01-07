import os
import requests
from pathlib import Path
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
from textblob import TextBlob

#USERNAME = "your-username"

repo = os.environ.get("GITHUB_REPOSITORY")

if not repo:
    raise RuntimeError("GITHUB_REPOSITORY environment variable not set")

USERNAME = repo.split("/")[0]

TOKEN = os.environ.get("GH_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}

OUTPUT_DIR = Path("../metrics/commits")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Fetch all repos
repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos", headers=HEADERS).json()

# -------------------------------
# 1️⃣ Commits per Repo + Commit Length Stats
# -------------------------------
commit_lengths = []
svg_path = OUTPUT_DIR / "commits_per_repo.svg"
svg = '<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">'
x, y = 10, 20

for repo in repos[:5]:  # top 5 repos for performance
    name = repo["name"]
    commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{name}/commits", headers=HEADERS).json()
    count = len(commits)
    
    # Collect commit lengths
    for c in commits:
        msg = c["commit"]["message"]
        commit_lengths.append(len(msg))
    
    svg += f'<text x="{x}" y="{y}" font-size="14">{name}: {count} commits</text>'
    y += 20

avg_length = sum(commit_lengths)/len(commit_lengths) if commit_lengths else 0
svg += f'<text x="{x}" y="{y+20}" font-size="14">Avg commit length: {avg_length:.1f} chars</text>'
svg += "</svg>"
svg_path.write_text(svg)

# -------------------------------
# 2️⃣ Commit Message Sentiment
# -------------------------------
sentiments = {"positive":0, "negative":0, "neutral":0}

for msg_len, commit_msg in zip(commit_lengths, [c["commit"]["message"] for r in repos[:5] for c in requests.get(f"https://api.github.com/repos/{USERNAME}/{r['name']}/commits", headers=HEADERS).json()]):
    polarity = TextBlob(commit_msg).sentiment.polarity
    if polarity > 0.1:
        sentiments["positive"] += 1
    elif polarity < -0.1:
        sentiments["negative"] += 1
    else:
        sentiments["neutral"] += 1

plt.bar(sentiments.keys(), sentiments.values(), color=["green","red","gray"])
plt.title("Commit Message Sentiment")
plt.savefig(OUTPUT_DIR / "commit_sentiment.png")
plt.close()

# -------------------------------
# 3️⃣ Commits per Repo Topic
# -------------------------------
topic_counter = Counter()
for repo in repos[:5]:
    topics_url = repo.get("topics_url") or f"https://api.github.com/repos/{USERNAME}/{repo['name']}/topics"
    topics_resp = requests.get(topics_url, headers={**HEADERS, "Accept":"application/vnd.github.mercy-preview+json"}).json()
    topics = topics_resp.get("names", [])
    commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits", headers=HEADERS).json()
    for t in topics:
        topic_counter[t] += len(commits)

plt.bar(topic_counter.keys(), topic_counter.values())
plt.xticks(rotation=45)
plt.title("Commits per Repo Topic")
plt.savefig(OUTPUT_DIR / "commits_per_topic.png")
plt.close()

# -------------------------------
# 4️⃣ Commits by Branch
# -------------------------------
branch_counter = Counter()
for repo in repos[:5]:
    branches = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/branches", headers=HEADERS).json()
    for branch in branches:
        branch_name = branch["name"]
        commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits?sha={branch_name}", headers=HEADERS).json()
        branch_counter[branch_name] += len(commits)

plt.bar(branch_counter.keys(), branch_counter.values())
plt.xticks(rotation=45)
plt.title("Commits by Branch")
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
        files = commit_details.get("files", [])
        for f in files:
            filename = f["filename"]
            file_counter[filename] += 1

top_files = dict(file_counter.most_common(10))
plt.barh(list(top_files.keys()), list(top_files.values()), color="orange")
plt.title("Top 10 Most Frequently Edited Files")
plt.savefig(OUTPUT_DIR / "top_files.png")
plt.close()
