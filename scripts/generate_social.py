import os
import requests
from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # required for GitHub Actions (headless)
import matplotlib.pyplot as plt

# -----------------------------
# Configuration
# -----------------------------
#USERNAME = "your-username"  # <-- REPLACE THIS

repo = os.environ.get("GITHUB_REPOSITORY")

if not repo:
    raise RuntimeError("GITHUB_REPOSITORY environment variable not set")

USERNAME = repo.split("/")[0]

TOKEN = os.environ.get("GH_TOKEN")

if not TOKEN:
    raise RuntimeError("GH_TOKEN environment variable is not set")

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

#OUTPUT_DIR = Path("../metrics/social")
#OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR = Path("metrics/social")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Fetch user data safely
# -----------------------------
response = requests.get(
    f"https://api.github.com/users/{USERNAME}",
    headers=HEADERS,
    timeout=30
)

user = response.json()

# 🔒 Defensive check (THIS prevents your crash)
if response.status_code != 200 or "followers" not in user:
    raise RuntimeError(
        f"GitHub API error fetching user data ({response.status_code}): {user}"
    )

followers = user["followers"]
following = user["following"]

# -----------------------------
# Generate chart
# -----------------------------
plt.figure(figsize=(6, 4))
plt.bar(["Followers", "Following"], [followers, following])
plt.title("GitHub Social Metrics")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "followers_following.png")
plt.close()

print("✅ Social metrics generated successfully")
