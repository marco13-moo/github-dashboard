"""
Generate Social Metrics for GitHub Dashboard
All outputs are PNG files in metrics/social/
"""

import os
import requests
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import Counter

# -----------------------------
# Configuration
# -----------------------------
repo_env = os.environ.get("GITHUB_REPOSITORY")
if not repo_env:
    raise RuntimeError("GITHUB_REPOSITORY environment variable not set")
USERNAME = repo_env.split("/")[0]

TOKEN = os.environ.get("GH_TOKEN")
if not TOKEN:
    raise RuntimeError("GH_TOKEN environment variable not set")

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

OUTPUT_DIR = Path("metrics/social")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# 1️⃣ Follower / Following Growth
# -----------------------------
user = requests.get(f"https://api.github.com/users/{USERNAME}", headers=HEADERS).json()
followers = user.get("followers", 0)
following = user.get("following", 0)

plt.figure(figsize=(6,4))
plt.bar(["Followers", "Following"], [followers, following], color=["blue","green"])
plt.title("Follower / Following Growth")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "followers_growth.png")
plt.close()

# -----------------------------
# 2️⃣ Top Collaborators (PRs and commits)
# -----------------------------
collaborators_counter = Counter()
repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos", headers=HEADERS).json()[:5]

for repo in repos:
    pulls = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/pulls?state=closed", headers=HEADERS).json()
    for pr in pulls:
        user_login = pr.get("user", {}).get("login")
        if user_login and user_login != USERNAME:
            collaborators_counter[user_login] += 1

top_collaborators = dict(collaborators_counter.most_common(10))
plt.figure(figsize=(8,4))
if top_collaborators:
    plt.barh(list(top_collaborators.keys()), list(top_collaborators.values()), color="orange")
else:
    plt.text(0.5,0.5,"No collaborators", ha="center", va="center", fontsize=14)
plt.title("Top Collaborators")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "top_collaborators.png")
plt.close()

# -----------------------------
# 3️⃣ Mentions in Issues / PRs
# -----------------------------
mentions_counter = Counter()
for repo in repos:
    issues = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/issues?state=all", headers=HEADERS).json()
    for issue in issues:
        if "@" in issue.get("body",""):
            mentions_counter[repo['name']] += 1

plt.figure(figsize=(8,4))
if mentions_counter:
    plt.bar(mentions_counter.keys(), mentions_counter.values(), color="purple")
    plt.xticks(rotation=45)
else:
    plt.text(0.5,0.5,"No mentions found", ha="center", va="center", fontsize=14)
plt.title("Mentions in Issues / PRs")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "mentions.png")
plt.close()

# -----------------------------
# 4️⃣ Organizations Contributed To
# -----------------------------
orgs = requests.get(f"https://api.github.com/users/{USERNAME}/orgs", headers=HEADERS).json()
org_names = [o.get("login") for o in orgs]

plt.figure(figsize=(8,4))
if org_names:
    plt.bar(org_names, [1]*len(org_names), color="cyan")
    plt.xticks(rotation=45)
else:
    plt.text(0.5,0.5,"No orgs found", ha="center", va="center", fontsize=14)
plt.title("Organizations Contributed To")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "orgs.png")
plt.close()

# -----------------------------
# 5️⃣ Stars Given vs Stars Received
# -----------------------------
# Stars given: sum of all stars in repos where USERNAME contributed (simplified)
stars_given = 0
repos_starred = requests.get(f"https://api.github.com/users/{USERNAME}/starred", headers=HEADERS).json()
stars_given = len(repos_starred)

# Stars received: sum of stars in user's repos
stars_received = sum(r.get("stargazers_count",0) for r in repos)

plt.figure(figsize=(6,4))
plt.bar(["Stars Given","Stars Received"], [stars_given, stars_received], color=["red","green"])
plt.title("Stars Given vs Stars Received")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "stars_karma.png")
plt.close()

# -----------------------------
# 6️⃣ Most Starred Repos Contributed To
# -----------------------------
repo_star_counts = {r["name"]: r.get("stargazers_count",0) for r in repos}
top_starred = dict(sorted(repo_star_counts.items(), key=lambda x: x[1], reverse=True)[:10])

plt.figure(figsize=(8,4))
if top_starred:
    plt.barh(list(top_starred.keys()), list(top_starred.values()), color="gold")
else:
    plt.text(0.5,0.5,"No starred repos", ha="center", va="center", fontsize=14)
plt.title("Most Starred Repos You Contributed To")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "starred_repos.png")
plt.close()

print("✅ Social metrics generated successfully!")
