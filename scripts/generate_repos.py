import os
import requests
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import chart_style  # noqa: F401 - applies the shared dashboard theme

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
recent_repos = sorted(repos, key=lambda r: r["pushed_at"], reverse=True)[:12]
activity = {
    r["name"]: max(
        0,
        (datetime.now(timezone.utc) - datetime.fromisoformat(r["pushed_at"].replace("Z", "+00:00"))).days,
    )
    for r in reversed(recent_repos)
}

plt.figure(figsize=(9,5))
plt.barh(activity.keys(), activity.values())
plt.xlabel("Days since last push · lower is better")
plt.title("Most Recently Active Repositories")
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
largest = sorted(repos, key=lambda r: r["size"], reverse=True)[:12]
sizes = {r["name"]: r["size"] for r in reversed(largest)}

plt.figure(figsize=(9,5))
plt.barh(sizes.keys(), sizes.values())
plt.xlabel("Repository size (KB)")
plt.title("Largest Repositories")
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

complex_repos = sorted(language_complexity.items(), key=lambda item: item[1], reverse=True)[:12]
complex_repos = dict(reversed(complex_repos))
plt.figure(figsize=(9,5))
plt.barh(complex_repos.keys(), complex_repos.values())
plt.xlabel("Languages detected")
plt.title("Most Polyglot Repositories")
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
plt.barh([r["name"] for r in reversed(top)], [r["stargazers_count"] for r in reversed(top)])
plt.xlabel("Stars")
plt.title("Most Starred Repositories")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "pinned_repos.png")
plt.close()

print("✅ Repo metrics generated successfully")
