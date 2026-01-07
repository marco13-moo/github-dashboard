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

OUTPUT_DIR = Path("../metrics/repos")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos", headers=HEADERS).json()

# ---- Repo Star Trend ----
stars = [repo["stargazers_count"] for repo in repos[:10]]
names = [repo["name"] for repo in repos[:10]]
plt.bar(names, stars)
plt.title("Repo Stars")
plt.xticks(rotation=45)
plt.savefig(OUTPUT_DIR / "repo_stars.png")
plt.close()
