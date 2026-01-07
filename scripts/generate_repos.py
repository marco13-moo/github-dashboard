import os
import requests
from pathlib import Path
from collections import Counter
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# -----------------------------
# Auth / Setup
# -----------------------------
repo = os.environ.get("GITHUB_REPOSITORY")
if not repo:
    raise RuntimeError("GITHUB_REPOSITORY environment variable not set")

USERNAME = repo.split("/")[0]

TOKEN = os.environ.get("GH_TOKEN")
if not TOKEN:
    raise RuntimeError("GH_TOKEN not set")

HEADERS = {"Authorization": f"token {TOKEN}"}

OUTPUT_DIR = Path("metrics/repos")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

repos = requests.get(
    f"https://api.github.com/users/{USERNAME}/repos?per_page=100",
    headers=HEADERS
).json()

# -----------------------------
# 1️⃣ Repo Activity (last push)
# -----------------------------
activity = {
    r["name"]: datetime.fromisoformat(r["pushed_at"].replace("Z", ""))
    for r in repos
}

plt.figure(figsize=(8,4))
plt.bar(activity.keys(), range(len(activity)))
plt.xticks(rotation=45)
plt.title("Repo Activity")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "repo_activity.png")
plt.close()

# -----------------------------
# 2️⃣ Repo Growth (creation year)
# -----------------------------
years = Counter(r["created_at"][:4] for r in repos)

plt.figure(figsize=(6,4))
plt.plot(sorted(years.keys()), [years[y] for y in sorted(years.keys())], marker="o")
plt.title("Repo Growth")
plt.xlabel("Year")
plt.ylabel("Repos Created")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "repo_growth.png")
plt.close()

# -----------------------------
# 3️⃣ Repo Sizes
# -----------------------------
sizes = {r["name"]: r["size"] for r in repos}

plt.figure(figsize=(8,4))
plt.bar(sizes.keys(), sizes.values())
plt.xticks(rotation=45)
plt.title("Repo Sizes (KB)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "repo_sizes.png")
plt.close()

# -----------------------------
# 4️⃣ Language Complexity
# -----------------------------
language_complexity = {}

for r in repos:
    langs = requests.get(r["languages_url"], headers=HEADERS).json()
    language_complexity[r["name"]] = len(langs)

plt.figure(figsize=(8,4))
plt.bar(language_complexity.keys(), language_complexity.values())
plt.xticks(rotation=45)
plt.title("Language Complexity per Repo")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "language_complexity.png")
plt.close()

# -----------------------------
# 5️⃣ Stars vs Forks
# -----------------------------
stars = sum(r["stargazers_count"] for r in repos)
forks = sum(r["forks_count"] for r in repos)

plt.figure(figsize=(5,4))
plt.bar(["Stars", "Forks"], [stars, forks])
plt.title("Stars vs Forks")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "stars_forks.png")
plt.close()

# -----------------------------
# 6️⃣ Contributed To (forked repos)
# -----------------------------
forked = sum(1 for r in repos if r["fork"])

plt.figure(figsize=(4,4))
plt.bar(["Forked", "Owned"], [forked, len(repos) - forked])
plt.title("Contributed To Repos")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "contributed_to.png")
plt.close()

# -----------------------------
# 7️⃣ Pinned Repos (top starred)
# -----------------------------
top = sorted(repos, key=lambda r: r["stargazers_count"], reverse=True)[:6]

plt.figure(figsize=(8,4))
plt.bar([r["name"] for r in top], [r["stargazers_count"] for r in top])
plt.xticks(rotation=45)
plt.title("Pinned Repos (Top Stars)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "pinned_repos.png")
plt.close()

print("✅ Repo metrics generated successfully")