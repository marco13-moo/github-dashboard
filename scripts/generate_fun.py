"""
Advanced / Fun Metrics Generator
Author: Your Name
Description:
    This script generates advanced and gamified GitHub metrics such as:
    - Contribution streaks
    - Hot repos (spike in activity)
    - Commit word cloud
    - Contributor diversity
    - Hackathon / event contributions
    - Code review karma
    - Activity score per day

Requirements:
    pip install requests matplotlib pandas wordcloud
"""

import os
import requests
from pathlib import Path
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from wordcloud import WordCloud

# -------------------------------
# 0️⃣ Configuration
# -------------------------------
#USERNAME = "your-username"  # replace with your GitHub username

repo = os.environ.get("GITHUB_REPOSITORY")

if not repo:
    raise RuntimeError("GITHUB_REPOSITORY environment variable not set")

USERNAME = repo.split("/")[0]

TOKEN = os.environ.get("GH_TOKEN")  # GitHub token stored in Actions secrets
HEADERS = {"Authorization": f"token {TOKEN}"}

# Output folder for metric images
OUTPUT_DIR = Path("../metrics/fun")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Fetch repositories (top 10 for performance)
repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos", headers=HEADERS).json()[:10]

# -------------------------------
# 1️⃣ Contribution Streaks
# -------------------------------
# This calculates your daily commit streaks over the last year
commit_dates = []

for repo in repos:
    commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits", headers=HEADERS).json()
    for c in commits:
        date_str = c["commit"]["author"]["date"]
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
        commit_dates.append(date_obj)

# Convert to sorted unique dates
commit_dates = sorted(list(set(commit_dates)))

# Calculate streaks
longest_streak = 0
current_streak = 0
previous_day = None

for date in commit_dates:
    if previous_day:
        if (date - previous_day).days == 1:
            current_streak += 1
        else:
            current_streak = 1
    else:
        current_streak = 1
    previous_day = date
    if current_streak > longest_streak:
        longest_streak = current_streak

# Save streaks as a bar chart
plt.figure(figsize=(6,4))
plt.bar(["Longest Streak", "Current Streak"], [longest_streak, current_streak], color=["green","blue"])
plt.title("GitHub Contribution Streaks (days)")
plt.savefig(OUTPUT_DIR / "contribution_streaks.png")
plt.close()

# -------------------------------
# 2️⃣ Hot Repos (Recent Activity Spike)
# -------------------------------
# Count commits in last 7 days for each repo
recent_activity = {}
seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)


for repo in repos:
    commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits", headers=HEADERS).json()
    count = 0
    for c in commits:
        commit_date = datetime.fromisoformat(c["commit"]["author"]["date"].replace("Z","+00:00"))
        if commit_date > seven_days_ago:
            count += 1
    recent_activity[repo["name"]] = count

# Plot hot repos
plt.figure(figsize=(8,4))
plt.bar(recent_activity.keys(), recent_activity.values(), color="orange")
plt.xticks(rotation=45)
plt.title("Hot Repos (Commits in Last 7 Days)")
plt.savefig(OUTPUT_DIR / "hot_repos.png")
plt.close()

# -------------------------------
# 3️⃣ Commit Word Cloud
# -------------------------------
# Collect commit messages
commit_messages = []
for repo in repos:
    commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits", headers=HEADERS).json()
    for c in commits:
        commit_messages.append(c["commit"]["message"])

# Generate word cloud
text = " ".join(commit_messages)
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Commit Word Cloud")
plt.savefig(OUTPUT_DIR / "commit_wordcloud.png")
plt.close()

# -------------------------------
# 4️⃣ Contributor Diversity
# -------------------------------
# Count unique contributors per repo
unique_contributors = {}
for repo in repos:
    contributors = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/contributors", headers=HEADERS).json()
    unique_contributors[repo["name"]] = len(contributors)

plt.figure(figsize=(8,4))
plt.bar(unique_contributors.keys(), unique_contributors.values(), color="purple")
plt.xticks(rotation=45)
plt.title("Contributor Diversity per Repo")
plt.savefig(OUTPUT_DIR / "contributor_diversity.png")
plt.close()

# -------------------------------
# 5️⃣ Hackathon / Event Contributions
# -------------------------------
# Identify repos with specific topics (e.g., 'hackathon')
hackathon_repos = {}
for repo in repos:
    topics_url = repo.get("topics_url") or f"https://api.github.com/repos/{USERNAME}/{repo['name']}/topics"
    topics_resp = requests.get(topics_url, headers={**HEADERS, "Accept":"application/vnd.github.mercy-preview+json"}).json()
    topics = topics_resp.get("names", [])
    if "hackathon" in topics:
        commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits", headers=HEADERS).json()
        hackathon_repos[repo["name"]] = len(commits)

plt.figure(figsize=(6,4))
plt.bar(hackathon_repos.keys(), hackathon_repos.values(), color="red")
plt.xticks(rotation=45)
plt.title("Hackathon / Event Contributions")
plt.savefig(OUTPUT_DIR / "hackathon_contributions.png")
plt.close()

# -------------------------------
# 6️⃣ Code Review Karma
# -------------------------------
# Points: 2 for approving PR, 1 for commenting
karma = 0
for repo in repos:
    prs = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/pulls?state=closed", headers=HEADERS).json()
    for pr in prs:
        reviews_url = pr.get("url") + "/reviews"
        reviews = requests.get(reviews_url, headers=HEADERS).json()
        for r in reviews:
            if r["user"]["login"].lower() == USERNAME.lower():
                if r["state"].lower() == "approved":
                    karma += 2
                elif r["state"].lower() == "commented":
                    karma += 1

# Save karma as a bar
plt.figure(figsize=(4,4))
plt.bar(["Code Review Karma"], [karma], color="gold")
plt.title("Code Review Karma")
plt.savefig(OUTPUT_DIR / "code_review_karma.png")
plt.close()

# -------------------------------
# 7️⃣ Activity Score per Day
# -------------------------------
# Combine commits + PRs + issues per day
activity = {}

for repo in repos:
    # Commits
    commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits", headers=HEADERS).json()
    for c in commits:
        date = datetime.fromisoformat(c["commit"]["author"]["date"].replace("Z","+00:00")).date()
        activity[date] = activity.get(date, 0) + 1
    # PRs
    prs = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/pulls?state=all", headers=HEADERS).json()
    for pr in prs:
        date = datetime.fromisoformat(pr["created_at"].replace("Z","+00:00")).date()
        activity[date] = activity.get(date, 0) + 2  # PR weight
    # Issues
    issues = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/issues?state=all", headers=HEADERS).json()
    for issue in issues:
        if "pull_request" not in issue:  # skip PRs
            date = datetime.fromisoformat(issue["created_at"].replace("Z","+00:00")).date()
            activity[date] = activity.get(date, 0) + 1

# Convert to DataFrame for plotting
df = pd.DataFrame(list(activity.items()), columns=["Date","Activity"])
df.sort_values("Date", inplace=True)
plt.figure(figsize=(10,4))
plt.plot(df["Date"], df["Activity"], marker="o")
plt.title("Activity Score Per Day")
plt.xlabel("Date")
plt.ylabel("Activity Score")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "activity_score_per_day.png")
plt.close()

print("✅ Fun / Advanced metrics generated successfully in metrics/fun/")
