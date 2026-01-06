# 📊 GitHub Metrics Dashboard

Welcome to my **GitHub Metrics Dashboard**!  
This repository automatically generates, visualizes, and updates detailed metrics about my GitHub activity, repositories, commits, pull requests, issues, contributions, and more — all fully self-hosted with GitHub Actions.  

Metrics are organized into **8 categories**, each updated daily automatically.

---

## ⚡ Commit-Level Metrics

Visualizing my coding activity, commit patterns, and productivity trends.

| Metric | Visualization |
|--------|---------------|
| **Commits per Repo** | ![Commits per Repo](metrics/commits/commits_per_repo.svg) |
| **Average Commit Length** | ![Commit Length](metrics/commits/avg_commit_length.png) |
| **Commit Message Sentiment** | ![Commit Sentiment](metrics/commits/commit_sentiment.png) |
| **Commits per Repo Topic** | ![Commits by Topic](metrics/commits/commits_per_topic.png) |
| **Commits by Branch** | ![Commits by Branch](metrics/commits/commits_by_branch.png) |
| **Most Frequently Edited Files** | ![Top Files](metrics/commits/top_files.png) |
| **Commit Distribution by Weekday** | ![Weekday Heatmap](metrics/commits/commit_weekday.png) |
| **Commit Distribution by Hour** | ![Hour Heatmap](metrics/commits/commit_hours.png) |

---

## 🔀 Pull Request & Issue Metrics

Track my PR and issue activity, engagement, and review efficiency.

| Metric | Visualization |
|--------|---------------|
| **PR Open → Merge Time** | ![PR Merge Time](metrics/prs_issues/pr_merge_time.png) |
| **PR Size** | ![PR Size](metrics/prs_issues/pr_size.png) |
| **PR Comments Received/Given** | ![PR Comments](metrics/prs_issues/pr_comments.png) |
| **PR Approval Rate** | ![PR Approval Rate](metrics/prs_issues/pr_approval_rate.png) |
| **Issue Age Distribution** | ![Issue Age](metrics/prs_issues/issue_age.png) |
| **Closed vs Open Issues by Repo** | ![Closed vs Open](metrics/prs_issues/closed_vs_open.png) |
| **Top Issue Labels Used** | ![Issue Labels](metrics/prs_issues/top_labels.png) |
| **PR Review Latency** | ![PR Review Latency](metrics/prs_issues/pr_review_latency.png) |
| **PR Merge Method Distribution** | ![PR Merge Method](metrics/prs_issues/pr_merge_method.png) |

---

## 🗂 Repository Metrics

Get an overview of my repositories, growth, languages, and contribution trends.

| Metric | Visualization |
|--------|---------------|
| **Repo Activity Score** | ![Repo Activity](metrics/repos/repo_activity.png) |
| **Repo Growth Rate** | ![Repo Growth](metrics/repos/repo_growth.png) |
| **Repo Size Distribution** | ![Repo Sizes](metrics/repos/repo_sizes.png) |
| **Repo Language Complexity** | ![Language Complexity](metrics/repos/language_complexity.png) |
| **Repo Star / Fork / Watch Trends** | ![Stars/Forks](metrics/repos/stars_forks.png) |
| **Repos Contributed To** | ![Repos Contributed](metrics/repos/contributed_to.png) |
| **Pinned Repos Stats** | ![Pinned Repos](metrics/repos/pinned_repos.png) |

---

## 🖥 Language & Tech Metrics

Analyze my coding languages, LOC, and trends over time.

| Metric | Visualization |
|--------|---------------|
| **Languages by Contribution Volume** | ![Languages by Commits](metrics/languages/languages_commits.png) |
| **Languages by LOC** | ![Languages LOC](metrics/languages/languages_loc.png) |
| **New Languages Over Time** | ![New Languages](metrics/languages/new_languages.png) |
| **Language Popularity Trend** | ![Language Trend](metrics/languages/language_trend.png) |
| **Language vs Repo Size** | ![Language vs Repo](metrics/languages/language_repo.png) |

---

## 🌐 Social Metrics

Track my GitHub social activity and collaboration.

| Metric | Visualization |
|--------|---------------|
| **Follower / Following Growth** | ![Network Growth](metrics/social/followers_growth.png) |
| **Top Collaborators** | ![Top Collaborators](metrics/social/top_collaborators.png) |
| **Mentions in Issues / PRs** | ![Mentions](metrics/social/mentions.png) |
| **Organizations Contributed To** | ![Organizations](metrics/social/orgs.png) |
| **Stars Given vs Stars Received** | ![Stars Karma](metrics/social/stars_karma.png) |
| **Most Starred Repos You Contributed To** | ![Starred Repos](metrics/social/starred_repos.png) |

---

## ⚙ CI/CD & DevOps Metrics

Monitor my workflows, deployments, and automation efficiency.

| Metric | Visualization |
|--------|---------------|
| **Workflow Runs Per Repo** | ![Workflow Runs](metrics/ci_cd/workflow_runs.png) |
| **Workflow Success Rate** | ![Success Rate](metrics/ci_cd/workflow_success.png) |
| **Workflow Trigger Distribution** | ![Trigger Distribution](metrics/ci_cd/workflow_triggers.png) |
| **PR Auto-Merge Frequency** | ![Auto Merge](metrics/ci_cd/auto_merge.png) |
| **Average Deployment Time** | ![Deployment Time](metrics/ci_cd/deployment_time.png) |
| **Failed Jobs by Repo** | ![Failed Jobs](metrics/ci_cd/failed_jobs.png) |

---

## 🎮 Advanced / Fun / Gamified Metrics

Add gamified insights about my contributions.

| Metric | Visualization |
|--------|---------------|
| **Contribution Streaks** | ![Contribution Streaks](metrics/fun/contribution_streaks.png) |
| **Hot Repos** | ![Hot Repos](metrics/fun/hot_repos.png) |
| **Commit Word Cloud** | ![Word Cloud](metrics/fun/commit_wordcloud.png) |
| **Contributor Diversity** | ![Contributor Diversity](metrics/fun/contributor_diversity.png) |
| **Hackathon / Event Contributions** | ![Hackathon Contributions](metrics/fun/hackathon_contributions.png) |
| **Code Review Karma** | ![Code Review Karma](metrics/fun/code_review_karma.png) |
| **Activity Score per Day** | ![Activity Score](metrics/fun/activity_score_per_day.png) |

---

## 📊 Ultra-Niche / Analytical Metrics

In-depth analysis of my GitHub activity.

| Metric | Visualization |
|--------|---------------|
| **Churn Rate (Lines Added vs Deleted)** | ![Churn Rate](metrics/analytics/churn_rate.png) |
| **Repo Health Index** | ![Repo Health](metrics/analytics/repo_health_index.png) |
| **Tech Stack Evolution** | ![Tech Stack](metrics/analytics/tech_stack_evolution.png) |
| **Commit Hot Times (Heatmap)** | ![Commit Hot Times](metrics/analytics/commit_hot_times.png) |
| **PR & Issue Topic Analysis** | ![PR & Issue Topics](metrics/analytics/pr_issue_topics.png) |
| **Average Contributor Count per Repo** | ![Avg Contributors](metrics/analytics/avg_contributors.png) |
| **Open Source Impact Score** | ![Open Source Impact](metrics/analytics/open_source_impact.png) |

---

## ⚙ Workflow

All metrics are **automatically updated daily** via GitHub Actions.  
The workflow:

1. Pulls repo data via the **GitHub API** using a **personal access token** stored as `GH_TOKEN`.  
2. Runs all Python scripts in `scripts/` to generate updated charts and SVGs.  
3. Commits updated metrics to the `metrics/` folder.  
4. Skips CI on the auto-commit to avoid infinite loops.  

> You can trigger the workflow manually in the **Actions tab** if needed.

---

## 📌 Notes

- All metrics are **self-hosted**; no third-party services.  
- This dashboard is continuously updated to reflect real-time contributions.  
- Images/SVGs are auto-generated and referenced in this README.

---

**Enjoy exploring my GitHub stats! 🚀**
