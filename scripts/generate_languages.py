"""
Generate Language / Tech Metrics for GitHub Dashboard
All outputs are PNG files in metrics/languages/
"""

import os
import requests
from pathlib import Path
from collections import Counter
import matplotlib
matplotlib.use("Agg")  # headless mode for GitHub Actions
import matplotlib.pyplot as plt

# -------------------------------
# Configuration
# -------------------------------
repo_env = os.environ.get("GITHUB_REPOSITORY")
if not repo_env:
    raise RuntimeError("GITHUB_REPOSITORY environment variable not set")

USERNAME = repo_env.split("/")[0]
TOKEN = os.environ.get("GH_TOKEN")
if not TOKEN:
    raise RuntimeError("GH_TOKEN environment variable not set")

HEADERS = {"Authorization": f"token {TOKEN}"}

OUTPUT_DIR = Path("metrics/languages")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Fetch top 10 repos
repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos", headers=HEADERS).json()[:10]

# -------------------------------
# 1️⃣ Languages by LOC
# -------------------------------
lang_counter = Counter()
for repo in repos:
    langs = requests.get(repo["languages_url"], headers=HEADERS).json()
    for lang, loc in langs.items():
        lang_counter[lang] += loc

plt.figure(figsize=(8,4))
if lang_counter:
    plt.bar(lang_counter.keys(), lang_counter.values(), color="skyblue")
    plt.xticks(rotation=45)
else:
    plt.text(0.5,0.5,"No languages found", ha="center", va="center", fontsize=14)
plt.title("Languages by LOC")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "languages_loc.png")
plt.close()

# -------------------------------
# 2️⃣ Languages by Commits
# -------------------------------
lang_commit_counter = Counter()
for repo in repos:
    commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits", headers=HEADERS).json()
    langs = requests.get(repo["languages_url"], headers=HEADERS).json()
    repo_langs = list(langs.keys()) or ["Unknown"]
    for lang in repo_langs:
        lang_commit_counter[lang] += len(commits)

plt.figure(figsize=(8,4))
if lang_commit_counter:
    plt.bar(lang_commit_counter.keys(), lang_commit_counter.values(), color="orange")
    plt.xticks(rotation=45)
else:
    plt.text(0.5,0.5,"No commits found", ha="center", va="center", fontsize=14)
plt.title("Languages by Commits")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "languages_commits.png")
plt.close()

# -------------------------------
# 3️⃣ New Languages Over Time
# -------------------------------
# Use first commit date per repo to approximate year of language usage
lang_year_counter = {}
for repo in repos:
    commits = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits", headers=HEADERS).json()
    if not commits:
        continue
    first_commit = commits[-1]["commit"]["author"]["date"]  # oldest commit
    year = int(first_commit[:4])
    langs = requests.get(repo["languages_url"], headers=HEADERS).json()
    for lang in langs.keys():
        if year not in lang_year_counter:
            lang_year_counter[year] = Counter()
        lang_year_counter[year][lang] += 1

# Convert to stacked bar
years = sorted(lang_year_counter.keys())
all_langs = set(lang for c in lang_year_counter.values() for lang in c)
bottom = [0]*len(years)

plt.figure(figsize=(10,5))
for lang in all_langs:
    counts = [lang_year_counter[y].get(lang, 0) for y in years]
    plt.bar(years, counts, bottom=bottom, label=lang)
    bottom = [b + c for b, c in zip(bottom, counts)]

if all_langs:
    plt.legend(title="Languages")
plt.xlabel("Year")
plt.ylabel("New Language Contributions")
plt.title("New Languages Over Time")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "new_languages.png")
plt.close()

# -------------------------------
# 4️⃣ Language vs Repo Size (LOC)
# -------------------------------
# Approximate repo size in KB using GitHub API, assign to languages proportionally
repo_lang_sizes = {}
for repo in repos:
    langs = requests.get(repo["languages_url"], headers=HEADERS).json()
    if not langs:
        continue
    repo_size = repo.get("size", 0)  # in KB
    for lang, loc in langs.items():
        repo_lang_sizes.setdefault(lang, 0)
        repo_lang_sizes[lang] += repo_size

plt.figure(figsize=(8,4))
if repo_lang_sizes:
    plt.bar(repo_lang_sizes.keys(), repo_lang_sizes.values(), color="purple")
    plt.xticks(rotation=45)
else:
    plt.text(0.5,0.5,"No data available", ha="center", va="center", fontsize=14)
plt.title("Language vs Repo Size")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "language_repo.png")
plt.close()

print("✅ Language metrics generated successfully!")
