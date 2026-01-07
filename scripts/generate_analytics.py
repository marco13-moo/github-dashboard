"""
Ultra-Niche / Analytical GitHub Metrics Generator
Author: Your Name
Description:
    This script generates advanced analytical metrics for a GitHub user:
    1. Churn Rate (lines added vs deleted)
    2. Repo Health Index (open issues ratio, PR merge ratio, last commit recency)
    3. Tech Stack Evolution (languages used over time)
    4. Commit Hot Times (productive hours/weeks heatmap)
    5. PR & Issue Topic Analysis (count by labels/topics)
    6. Average Contributor Count per Repo
    7. Open Source Impact Score (stars + forks + watchers)

Requirements:
    pip install requests matplotlib pandas seaborn
"""

import os
import requests
from pathlib import Path
from datetime import timezone
from utils.time import utc_now, parse_github_timestamp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import Counter

# -------------------------------
# 0️⃣ Configuration
# -------------------------------
#USERNAME = "your-username"  # Replace with your GitHub username

repo = os.environ.get("GITHUB_REPOSITORY")

if not repo:
    raise RuntimeError("GITHUB_REPOSITORY environment variable not set")

USERNAME = repo.split("/")[0]

TOKEN = os.environ.get("GH_TOKEN")  # GitHub token stored in Actions secrets
HEADERS = {"Authorization": f"token {TOKEN}"}

#OUTPUT_DIR = Path("../metrics/analytics")
#OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR = Path("metrics/analytics")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Fetch repositories (top 10 for performance)
repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos", headers=HEADERS).json()[:10]

# -------------------------------
# 1️⃣ Churn Rate (lines added vs deleted)
# -------------------------------
lines_added = 0
lines_deleted = 0

for repo in repos:
    commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits", headers=HEADERS).json()
    for c in commits:
        sha = c["sha"]
        commit_detail = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits/{sha}", headers=HEADERS).json()
        stats = commit_detail.get("stats", {})
        lines_added += stats.get("additions", 0)
        lines_deleted += stats.get("deletions", 0)

plt.figure(figsize=(6,4))
plt.bar(["Lines Added","Lines Deleted"], [lines_added, lines_deleted], color=["green","red"])
plt.title("Churn Rate")
plt.savefig(OUTPUT_DIR / "churn_rate.png")
plt.close()

# -------------------------------
# 2️⃣ Repo Health Index
# Metrics: open issues ratio, PR merge ratio, last commit recency
# -------------------------------
repo_health = {}
for repo in repos:
    repo_name = repo["name"]
    # Open Issues
    open_issues = repo.get("open_issues_count",0)
    # PRs
    prs = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo_name}/pulls?state=all", headers=HEADERS).json()
    merged = sum(1 for pr in prs if pr.get("merged_at"))
    total_prs = len(prs)
    merge_ratio = merged / total_prs if total_prs > 0 else 0
    # Last commit recency in days
    last_commit_date = parse_github_timestamp(repo["pushed_at"])
    days_since_last_commit = (utc_now() - last_commit_date).days


    repo_health[repo_name] = {
        "open_issues": open_issues,
        "merge_ratio": merge_ratio,
        "days_since_last_commit": days_since_last_commit
    }

# Convert to DataFrame for visualization
df_health = pd.DataFrame(repo_health).T
df_health.plot(kind="bar", subplots=True, layout=(1,3), figsize=(12,4), title=["Open Issues","PR Merge Ratio","Days Since Last Commit"])
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "repo_health_index.png")
plt.close()

# -------------------------------
# 3️⃣ Tech Stack Evolution
# Timeline of languages used per year (based on first commit year per repo)
# -------------------------------
lang_over_time = {}

for repo in repos:
    commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits", headers=HEADERS).json()
    if not commits:
        continue
    first_commit_date = parse_github_timestamp(commits[-1]["commit"]["author"]["date"])
    year = first_commit_date.year
    langs = requests.get(repo["languages_url"], headers=HEADERS).json()
    for lang in langs.keys():
        if year not in lang_over_time:
            lang_over_time[year] = Counter()
        lang_over_time[year][lang] += langs[lang]

# Convert to DataFrame
df_lang = pd.DataFrame(lang_over_time).fillna(0).T
df_lang.plot(kind="bar", stacked=True, figsize=(10,5))
plt.title("Tech Stack Evolution Over Years")
plt.xlabel("Year")
plt.ylabel("Lines of Code")
plt.xticks(rotation=45)
plt.savefig(OUTPUT_DIR / "tech_stack_evolution.png")
plt.close()

# -------------------------------
# 4️⃣ Commit Hot Times (heatmap of productive hours)
# -------------------------------
hours = []
weekdays = []

for repo in repos:
    commits = requests.get(
        f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits",
        headers=HEADERS
    ).json()

    for commit in commits:
        ts = commit["commit"]["author"]["date"]
        dt = parse_github_timestamp(ts)

        hours.append(dt.hour)
        weekdays.append(dt.weekday())


# Create heatmap dataframe
df_heat = pd.DataFrame({"Hour": hours, "Weekday": weekdays})
heatmap_data = pd.crosstab(df_heat["Weekday"], df_heat["Hour"])
plt.figure(figsize=(12,6))
sns.heatmap(heatmap_data, cmap="YlGnBu")
plt.title("Commit Hot Times (Hours vs Weekday)")
plt.savefig(OUTPUT_DIR / "commit_hot_times.png")
plt.close()

# -------------------------------
# 5️⃣ PR & Issue Topic Analysis (count by labels)
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
    prs = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/pulls?state=all", headers=HEADERS).json()
    for pr in prs:
        for label in pr.get("labels", []):
            label_counter[label["name"]] += 1

top_labels = dict(label_counter.most_common(10))
plt.figure(figsize=(8,4))
plt.bar(top_labels.keys(), top_labels.values(), color="skyblue")
plt.xticks(rotation=45)
plt.title("PR & Issue Topic Analysis (Top Labels)")
plt.savefig(OUTPUT_DIR / "pr_issue_topics.png")
plt.close()

# -------------------------------
# 6️⃣ Average Contributor Count per Repo
# -------------------------------
contributors = {}
for repo in repos:
    contrs = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/contributors", headers=HEADERS).json()
    contributors[repo["name"]] = len(contrs)

plt.figure(figsize=(8,4))
plt.bar(contributors.keys(), contributors.values(), color="purple")
plt.xticks(rotation=45)
plt.title("Average Contributor Count per Repo")
plt.savefig(OUTPUT_DIR / "avg_contributors.png")
plt.close()

# -------------------------------
# 7️⃣ Open Source Impact Score (stars + forks + watchers)
# -------------------------------
impact_score = {}
for repo in repos:
    impact_score[repo["name"]] = repo.get("stargazers_count",0) + repo.get("forks_count",0) + repo.get("watchers_count",0)

plt.figure(figsize=(8,4))
plt.bar(impact_score.keys(), impact_score.values(), color="gold")
plt.xticks(rotation=45)
plt.title("Open Source Impact Score")
plt.savefig(OUTPUT_DIR / "open_source_impact.png")
plt.close()

print("✅ Ultra-Niche / Analytical metrics generated successfully in metrics/analytics/")
