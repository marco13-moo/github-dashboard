# GitHub Metrics

Daily, self-hosted visual analytics for my code, repositories, collaboration, and delivery workflows.

## At a glance

<p align="center">
  <a href="metrics/commits/commits_per_repo.png"><img src="metrics/commits/commits_per_repo.png" width="49%" alt="Commits per repository"></a>
  <a href="metrics/languages/languages_loc.png"><img src="metrics/languages/languages_loc.png" width="49%" alt="Languages by lines of code"></a>
  <a href="metrics/analytics/commit_hot_times.png"><img src="metrics/analytics/commit_hot_times.png" width="49%" alt="Commit activity heatmap"></a>
  <a href="metrics/repos/repo_growth.png"><img src="metrics/repos/repo_growth.png" width="49%" alt="Repository growth"></a>
</p>

Select a chart to open it at full resolution. Every visualization is generated with Python and refreshed daily by GitHub Actions.

<details open>
<summary><strong>Commit activity</strong> — patterns, timing, sentiment, and frequently edited files</summary>
<br>
<p align="center">
  <a href="metrics/commits/avg_commit_length.png"><img src="metrics/commits/avg_commit_length.png" width="49%" alt="Average commit length"></a>
  <a href="metrics/commits/commit_sentiment.png"><img src="metrics/commits/commit_sentiment.png" width="49%" alt="Commit message sentiment"></a>
  <a href="metrics/commits/commits_per_topic.png"><img src="metrics/commits/commits_per_topic.png" width="49%" alt="Commits by topic"></a>
  <a href="metrics/commits/commits_by_branch.png"><img src="metrics/commits/commits_by_branch.png" width="49%" alt="Commits by branch"></a>
  <a href="metrics/commits/top_files.png"><img src="metrics/commits/top_files.png" width="49%" alt="Most frequently edited files"></a>
  <a href="metrics/commits/commit_weekday.png"><img src="metrics/commits/commit_weekday.png" width="49%" alt="Commits by weekday"></a>
  <a href="metrics/commits/commit_hours.png"><img src="metrics/commits/commit_hours.png" width="49%" alt="Commits by hour"></a>
</p>
</details>

<details>
<summary><strong>Pull requests & issues</strong> — throughput, review speed, size, and engagement</summary>
<br>
<p align="center">
  <a href="metrics/prs_issues/pr_merge_time.png"><img src="metrics/prs_issues/pr_merge_time.png" width="49%" alt="Pull request merge time"></a>
  <a href="metrics/prs_issues/pr_size.png"><img src="metrics/prs_issues/pr_size.png" width="49%" alt="Pull request size"></a>
  <a href="metrics/prs_issues/pr_comments.png"><img src="metrics/prs_issues/pr_comments.png" width="49%" alt="Pull request comments"></a>
  <a href="metrics/prs_issues/pr_approval_rate.png"><img src="metrics/prs_issues/pr_approval_rate.png" width="49%" alt="Pull request approval rate"></a>
  <a href="metrics/prs_issues/issue_age.png"><img src="metrics/prs_issues/issue_age.png" width="49%" alt="Issue age"></a>
  <a href="metrics/prs_issues/closed_vs_open.png"><img src="metrics/prs_issues/closed_vs_open.png" width="49%" alt="Closed and open issues"></a>
  <a href="metrics/prs_issues/top_labels.png"><img src="metrics/prs_issues/top_labels.png" width="49%" alt="Top issue labels"></a>
  <a href="metrics/prs_issues/pr_review_latency.png"><img src="metrics/prs_issues/pr_review_latency.png" width="49%" alt="Pull request review latency"></a>
  <a href="metrics/prs_issues/pr_merge_method.png"><img src="metrics/prs_issues/pr_merge_method.png" width="49%" alt="Pull request merge methods"></a>
</p>
</details>

<details>
<summary><strong>Repositories</strong> — activity, growth, size, reach, and complexity</summary>
<br>
<p align="center">
  <a href="metrics/repos/repo_activity.png"><img src="metrics/repos/repo_activity.png" width="49%" alt="Repository activity"></a>
  <a href="metrics/repos/repo_growth.png"><img src="metrics/repos/repo_growth.png" width="49%" alt="Repository growth"></a>
  <a href="metrics/repos/repo_sizes.png"><img src="metrics/repos/repo_sizes.png" width="49%" alt="Repository sizes"></a>
  <a href="metrics/repos/language_complexity.png"><img src="metrics/repos/language_complexity.png" width="49%" alt="Language complexity"></a>
  <a href="metrics/repos/stars_forks.png"><img src="metrics/repos/stars_forks.png" width="49%" alt="Stars and forks"></a>
  <a href="metrics/repos/contributed_to.png"><img src="metrics/repos/contributed_to.png" width="49%" alt="Repositories contributed to"></a>
  <a href="metrics/repos/pinned_repos.png"><img src="metrics/repos/pinned_repos.png" width="49%" alt="Pinned repository statistics"></a>
</p>
</details>

<details>
<summary><strong>Languages & technology</strong> — contribution volume, codebase mix, and trends</summary>
<br>
<p align="center">
  <a href="metrics/languages/languages_commits.png"><img src="metrics/languages/languages_commits.png" width="49%" alt="Languages by commits"></a>
  <a href="metrics/languages/new_languages.png"><img src="metrics/languages/new_languages.png" width="49%" alt="New languages over time"></a>
  <a href="metrics/languages/language_trend.png"><img src="metrics/languages/language_trend.png" width="49%" alt="Language popularity trend"></a>
  <a href="metrics/languages/language_repo.png"><img src="metrics/languages/language_repo.png" width="49%" alt="Language by repository size"></a>
</p>
</details>

<details>
<summary><strong>Social & collaboration</strong> — network growth, collaborators, mentions, and stars</summary>
<br>
<p align="center">
  <a href="metrics/social/followers_growth.png"><img src="metrics/social/followers_growth.png" width="49%" alt="Follower growth"></a>
  <a href="metrics/social/top_collaborators.png"><img src="metrics/social/top_collaborators.png" width="49%" alt="Top collaborators"></a>
  <a href="metrics/social/mentions.png"><img src="metrics/social/mentions.png" width="49%" alt="Mentions in issues and pull requests"></a>
  <a href="metrics/social/orgs.png"><img src="metrics/social/orgs.png" width="49%" alt="Organizations contributed to"></a>
  <a href="metrics/social/stars_karma.png"><img src="metrics/social/stars_karma.png" width="49%" alt="Stars given and received"></a>
  <a href="metrics/social/starred_repos.png"><img src="metrics/social/starred_repos.png" width="49%" alt="Most starred contributed repositories"></a>
</p>
</details>

<details>
<summary><strong>CI/CD & DevOps</strong> — workflow reliability, triggers, deployment speed, and failures</summary>
<br>
<p align="center">
  <a href="metrics/ci_cd/workflow_runs.png"><img src="metrics/ci_cd/workflow_runs.png" width="49%" alt="Workflow runs"></a>
  <a href="metrics/ci_cd/workflow_triggers.png"><img src="metrics/ci_cd/workflow_triggers.png" width="49%" alt="Workflow triggers"></a>
  <a href="metrics/ci_cd/auto_merge.png"><img src="metrics/ci_cd/auto_merge.png" width="49%" alt="Automatic merge frequency"></a>
  <a href="metrics/ci_cd/deployment_time.png"><img src="metrics/ci_cd/deployment_time.png" width="49%" alt="Average deployment time"></a>
  <a href="metrics/ci_cd/failed_jobs.png"><img src="metrics/ci_cd/failed_jobs.png" width="49%" alt="Failed jobs by repository"></a>
</p>
</details>

<details>
<summary><strong>Fun & gamified</strong> — streaks, hot repositories, word clouds, and karma</summary>
<br>
<p align="center">
  <a href="metrics/fun/contribution_streaks.png"><img src="metrics/fun/contribution_streaks.png" width="49%" alt="Contribution streaks"></a>
  <a href="metrics/fun/hot_repos.png"><img src="metrics/fun/hot_repos.png" width="49%" alt="Hot repositories"></a>
  <a href="metrics/fun/commit_wordcloud.png"><img src="metrics/fun/commit_wordcloud.png" width="49%" alt="Commit word cloud"></a>
  <a href="metrics/fun/contributor_diversity.png"><img src="metrics/fun/contributor_diversity.png" width="49%" alt="Contributor diversity"></a>
  <a href="metrics/fun/hackathon_contributions.png"><img src="metrics/fun/hackathon_contributions.png" width="49%" alt="Hackathon contributions"></a>
  <a href="metrics/fun/code_review_karma.png"><img src="metrics/fun/code_review_karma.png" width="49%" alt="Code review karma"></a>
  <a href="metrics/fun/activity_score_per_day.png"><img src="metrics/fun/activity_score_per_day.png" width="49%" alt="Daily activity score"></a>
</p>
</details>

<details>
<summary><strong>Deep analytics</strong> — churn, health, stack evolution, topics, and impact</summary>
<br>
<p align="center">
  <a href="metrics/analytics/churn_rate.png"><img src="metrics/analytics/churn_rate.png" width="49%" alt="Code churn"></a>
  <a href="metrics/analytics/repo_health_index.png"><img src="metrics/analytics/repo_health_index.png" width="49%" alt="Repository health index"></a>
  <a href="metrics/analytics/tech_stack_evolution.png"><img src="metrics/analytics/tech_stack_evolution.png" width="49%" alt="Technology stack evolution"></a>
  <a href="metrics/analytics/pr_issue_topics.png"><img src="metrics/analytics/pr_issue_topics.png" width="49%" alt="Pull request and issue topics"></a>
  <a href="metrics/analytics/avg_contributors.png"><img src="metrics/analytics/avg_contributors.png" width="49%" alt="Average contributor count"></a>
  <a href="metrics/analytics/open_source_impact.png"><img src="metrics/analytics/open_source_impact.png" width="49%" alt="Open source impact"></a>
</p>
</details>

## How it works

The dashboard refreshes daily with GitHub Actions:

1. Repository data is collected through the GitHub API.
2. The Python generators in [`scripts/`](scripts) build every chart with a shared visual theme.
3. Updated images are written to [`metrics/`](metrics) and committed automatically.

The workflow can also be started manually from the repository's **Actions** tab.

---

<p align="center"><sub>Self-hosted metrics · No external chart service · Updated automatically</sub></p>
