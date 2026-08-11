"use client";

import { useMemo, useState } from "react";

const activity = [18, 24, 20, 31, 29, 42, 36, 48, 44, 57, 53, 66, 61, 76, 72, 84, 79, 91, 86, 102, 96, 114, 108, 126];
const repos = [
  ["github-dashboard", 92, "TypeScript"],
  ["devsecops-vulnerability-automation", 78, "Python"],
  ["self-service-cicd-platform", 66, "HCL"],
  ["marco13-moo.github.io", 54, "JavaScript"],
  ["daily-dose-of-devops", 42, "Shell"],
] as const;
const languages = [
  ["Python", 38, "#a78bfa"],
  ["JavaScript", 27, "#facc15"],
  ["HTML / CSS", 18, "#38bdf8"],
  ["HCL", 11, "#f472b6"],
  ["Other", 6, "#64748b"],
] as const;
const heat = [1,2,8,1,2,4,6,2,1,1,2,3,5,3,1,2,1,4,2,1,1,2,3,1, 1,3,7,2,5,8,6,2,1,2,4,3,6,4,2,1,2,5,3,2,1,2,4,2, 2,4,6,1,4,7,5,3,2,1,3,4,7,5,2,2,1,4,3,2,2,3,5,2, 1,2,7,2,4,6,7,3,1,2,4,5,8,5,3,2,2,5,4,2,1,3,4,2, 2,3,8,1,5,7,6,3,2,3,5,6,7,4,2,2,3,6,5,3,2,4,5,2, 1,2,6,2,3,5,4,2,1,2,3,4,6,3,2,1,2,4,3,2,1,2,3,1, 1,1,4,1,2,3,2,1,1,1,2,2,3,2,1,1,1,2,2,1,1,1,2,1];

const Icon = ({ children }: { children: React.ReactNode }) => <span className="icon" aria-hidden="true">{children}</span>;

export default function Home() {
  const [range, setRange] = useState("30d");
  const [theme, setTheme] = useState<"dark" | "light">("dark");
  const rangeFactor = range === "7d" ? .72 : range === "90d" ? 1.18 : 1;
  const bars = useMemo(() => activity.map((value) => Math.round(value * rangeFactor)), [rangeFactor]);

  return (
    <main className={theme}>
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark">M</span><span>metrics<span className="brand-dot">.</span></span></div>
        <nav aria-label="Dashboard navigation">
          <a className="nav-active" href="#overview"><Icon>⌂</Icon>Overview</a>
          <a href="#activity"><Icon>⌁</Icon>Activity</a>
          <a href="#repositories"><Icon>◇</Icon>Repositories</a>
          <a href="#languages"><Icon>⌘</Icon>Languages</a>
          <a href="#delivery"><Icon>↗</Icon>Delivery</a>
        </nav>
        <div className="sidebar-foot">
          <span className="pulse" /> Updated 14 hours ago
          <a href="https://github.com/marco13-moo/github-dashboard">View on GitHub ↗</a>
        </div>
      </aside>

      <section className="workspace" id="overview">
        <header>
          <div>
            <p className="eyebrow">PERSONAL ENGINEERING INTELLIGENCE</p>
            <h1>Good morning, Marco.</h1>
            <p className="intro">Here’s what’s happening across your GitHub ecosystem.</p>
          </div>
          <div className="header-actions">
            <div className="range" aria-label="Date range">
              {["7d", "30d", "90d"].map((item) => <button className={range === item ? "selected" : ""} onClick={() => setRange(item)} key={item}>{item}</button>)}
            </div>
            <button className="theme-toggle" aria-label="Toggle color theme" onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>{theme === "dark" ? "☼" : "☾"}</button>
          </div>
        </header>

        <div className="kpis">
          <article><div className="kpi-top"><span>COMMITS</span><i className="violet">↗ 18.4%</i></div><strong>{Math.round(126 * rangeFactor)}</strong><p>Across 16 repositories</p><div className="spark violet-spark">▁▂▂▃▂▄▃▅▄▆▅▇</div></article>
          <article><div className="kpi-top"><span>PULL REQUESTS</span><i className="green">↗ 8.2%</i></div><strong>{Math.round(24 * rangeFactor)}</strong><p>21 merged · 3 open</p><div className="spark green-spark">▂▁▃▂▄▃▅▄▆▅▇▆</div></article>
          <article><div className="kpi-top"><span>ACTIVE REPOS</span><i className="muted">— 0.0%</i></div><strong>16</strong><p>5 with activity today</p><div className="spark blue-spark">▃▃▄▃▅▄▅▆▅▇▆▇</div></article>
          <article><div className="kpi-top"><span>CI SUCCESS</span><i className="green">↗ 2.1%</i></div><strong>94.8<span className="suffix">%</span></strong><p>73 of 77 runs passed</p><div className="spark amber-spark">▅▆▅▇▆▇▇▆▇▇▇█</div></article>
        </div>

        <div className="dashboard-grid">
          <article className="panel activity-panel" id="activity">
            <div className="panel-head"><div><span className="label">CONTRIBUTION VELOCITY</span><h2>Activity is trending up</h2></div><span className="legend"><i /> Commits</span></div>
            <div className="bar-chart" aria-label="Commit activity chart">
              {bars.map((value, index) => <div key={index} className="bar-wrap"><span className="tooltip">{value}</span><div className="bar" style={{ height: `${Math.max(12, value / 1.3)}%` }} /></div>)}
            </div>
            <div className="chart-axis"><span>Jul 13</span><span>Jul 19</span><span>Jul 25</span><span>Jul 31</span><span>Aug 6</span><span>Aug 11</span></div>
          </article>

          <article className="panel rhythm-panel">
            <div className="panel-head"><div><span className="label">CODING RHYTHM</span><h2>When you ship</h2></div><span className="timezone">UTC</span></div>
            <div className="heat-layout"><div className="days"><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span></div><div className="heatmap">{heat.map((value, index) => <i key={index} title={`${value * 2} contributions`} style={{ opacity: .1 + value / 10 }} />)}</div></div>
            <div className="heat-axis"><span>00:00</span><span>06:00</span><span>12:00</span><span>18:00</span><span>23:00</span></div>
            <p className="insight"><b>Peak window</b> Tuesday & Thursday, 08:00–10:00</p>
          </article>

          <article className="panel repos-panel" id="repositories">
            <div className="panel-head"><div><span className="label">REPOSITORY MOMENTUM</span><h2>Most active projects</h2></div><a href="https://github.com/marco13-moo?tab=repositories">View all ↗</a></div>
            <div className="repo-list">{repos.map(([name, score, language], index) => <div className="repo" key={name}><span className="rank">0{index + 1}</span><div className="repo-info"><b>{name}</b><small>{language}</small></div><div className="track"><i style={{ width: `${score}%` }} /></div><strong>{score}</strong></div>)}</div>
          </article>

          <article className="panel language-panel" id="languages">
            <div className="panel-head"><div><span className="label">STACK COMPOSITION</span><h2>Languages</h2></div><span className="muted-label">By code volume</span></div>
            <div className="donut-row">
              <div className="donut"><div><strong>9</strong><span>languages</span></div></div>
              <div className="language-list">{languages.map(([name, value, color]) => <div key={name}><span><i style={{ background: color }} />{name}</span><b>{value}%</b></div>)}</div>
            </div>
          </article>
        </div>

        <section className="delivery" id="delivery">
          <div><span className="status-dot" /><span><b>All systems healthy</b><small>Metrics pipeline completed successfully</small></span></div>
          <div className="delivery-meta"><span><small>LAST RUN</small>14h ago</span><span><small>DURATION</small>3m 42s</span><span><small>NEXT RUN</small>in 10h</span></div>
        </section>
        <footer>Built from your GitHub activity · Updated daily <span>marco13-moo / github-dashboard</span></footer>
      </section>
    </main>
  );
}
