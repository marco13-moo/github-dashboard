import os
import requests
from pathlib import Path
import matplotlib.pyplot as plt

USERNAME = "your-username"
TOKEN = os.environ.get("GH_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}

OUTPUT_DIR = Path("../metrics/social")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

user = requests.get(f"https://api.github.com/users/{USERNAME}", headers=HEADERS).json()
followers = user["followers"]
following = user["following"]

plt.bar(["Followers", "Following"], [followers, following])
plt.title("Social Metrics")
plt.savefig(OUTPUT_DIR / "followers_following.png")
plt.close()
