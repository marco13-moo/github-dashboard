import os
import requests
from pathlib import Path
import matplotlib.pyplot as plt
from collections import Counter

#USERNAME = "your-username"

repo = os.environ.get("GITHUB_REPOSITORY")

if not repo:
    raise RuntimeError("GITHUB_REPOSITORY environment variable not set")

USERNAME = repo.split("/")[0]

TOKEN = os.environ.get("GH_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}

#OUTPUT_DIR = Path("../metrics/languages")
#OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR = Path("metrics/languages")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos", headers=HEADERS).json()

lang_counter = Counter()
for repo in repos[:10]:
    langs = requests.get(repo["languages_url"], headers=HEADERS).json()
    for lang, loc in langs.items():
        lang_counter[lang] += loc

plt.bar(lang_counter.keys(), lang_counter.values())
plt.title("Languages by LOC")
plt.xticks(rotation=45)
plt.savefig(OUTPUT_DIR / "languages_loc.png")
plt.close()
