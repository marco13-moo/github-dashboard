import os
import requests
from pathlib import Path
from collections import Counter
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# -----------------------------
# Setup
# -----------------------------
repo_env = os.environ.get("GITHUB_REPOSITORY")
if not repo_env:
    raise RuntimeError("GITHUB_REPOSITORY not set")

USERNAME = repo_env.split("/")[0]

TOKEN = os.environ.get("GH_TOKEN")
if not TOKEN:
    raise RuntimeError("GH_TOKEN not set")

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

OUTPUT_DIR = Path("metrics/ci_cd")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

repos = requests.get(
    f"https://api.github.com/users/{USERNAME}/repos?per_page=20",
    headers=HEADERS
).json()

# -----------------------------
# Data collectors
# -----------------------------
workflow_counts = Counter()
trigger_counts = Counter()
failed_jobs = 0
auto_merge_enabled = 0
deployment_times = []

# -----------------------------
# Iterate repos
# -----------------------------
for r in repos:
    name = r["name"]

    runs_resp = requests.get(
        f"https://api.github.com/repos/{USERNAME}/{name}/actions/runs?per_page=30",
        headers=HEADERS
    ).json()

    for run in runs_resp.get("workflow_runs", []):
        workflow_counts[name] += 1

        trigger = run.get("event")
        if trigger:
            trigger_counts[trigger] += 1

        if run.get("conclusion") == "failure":
            failed_jobs += 1

        # deployment time
        if run.get("run_started_at") and run.get("updated_at"):
            start = datetime.fromisoformat(run["run_started_at"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(run["updated_at"].replace("Z", "+00:00"))
            deployment_times.append((end - start).total_seconds() / 60)

    # auto-merge (repo setting)
    if r.get("allow_auto_merge"):
        auto_merge_enabled += 1

# -----------------------------
# 1️⃣ Workflow Runs
# -----------------------------
plt.figure(figsize=(8,4))
plt.bar(workflow_counts.keys(), workflow_counts.values())
plt.xticks(rotation=45)
plt.title("Workflow Runs per Repo")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "workflow_runs.png")
plt.close()

# -----------------------------
# 2️⃣ Workflow Triggers
# -----------------------------
plt.figure(figsize=(6,4))
plt.bar(trigger_counts.keys(), trigger_counts.values())
plt.title("Workflow Triggers")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "workflow_triggers.png")
plt.close()

# -----------------------------
# 3️⃣ Auto-Merge
# -----------------------------
plt.figure(figsize=(4,4))
plt.bar(["Enabled", "Disabled"], [auto_merge_enabled, len(repos) - auto_merge_enabled])
plt.title("Auto-Merge Usage")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "auto_merge.png")
plt.close()

# -----------------------------
# 4️⃣ Deployment Time
# -----------------------------
plt.figure(figsize=(6,4))
if deployment_times:
    plt.hist(deployment_times, bins=15)
else:
    plt.text(0.5, 0.5, "No deployment data", ha="center", va="center")
plt.xlabel("Minutes")
plt.title("Deployment Time")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "deployment_time.png")
plt.close()

# -----------------------------
# 5️⃣ Failed Jobs
# -----------------------------
plt.figure(figsize=(4,4))
plt.bar(["Failed Jobs"], [failed_jobs], color="red")
plt.title("Failed CI Jobs")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "failed_jobs.png")
plt.close()

print("✅ CI/CD metrics generated successfully")
