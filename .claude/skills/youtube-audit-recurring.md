# YouTube Audit Recurring — Automated Weekly Checks

## Overview
Automatically audit new YouTube videos on a recurring schedule. Use with `/loop` to check for new uploads weekly, audit each one, and maintain an ongoing dashboard of video performance.

**Perfect for:**
- Continuous content quality monitoring
- Automatic new upload detection and analysis
- Weekly performance tracking
- Identifying trends as you publish
- Ensuring brand consistency across videos
- Proactive gap identification before videos underperform

---

## When to Use

✓ Running a content channel with regular uploads  
✓ Want to audit every new video automatically  
✓ Need ongoing performance baseline  
✓ Building a content quality culture  
✓ Identifying patterns in what works  
✓ Reducing manual audit workload  
✓ Weekly performance reports to leadership  

---

## Setup

### Prerequisites
- YouTube channel with regular uploads
- Access to video URLs, transcripts, or metadata
- Claude Code with loop capability
- Existing dashboard skill: `youtube-audit-dashboard.md`

### Starting a Recurring Audit Loop

**Weekly audits (recommended):**
```
/loop 7d Audit new YouTube videos and generate dashboard
```

**Bi-weekly audits:**
```
/loop 14d Audit new YouTube videos and generate dashboard
```

**Daily (for high-volume channels):**
```
/loop 1d Audit new YouTube videos and generate dashboard
```

---

## Input Requirements

### Essential
- **YouTube channel URL or channel name**
- **Access to new videos** (link, title + description, or transcript)
- **Business objective** for audits
- **Target audience** definition

### Recommended
- **API access or manual tracking** of recent uploads
- **Transcript data** or automatic caption access
- **Analytics from Google Analytics/YouTube Studio**
- **Previous audit results** for trend comparison

### Optional
- **Specific focus areas** (SEO, engagement, etc.)
- **Competitor videos** for benchmarking
- **Thumbnail images** for visual review
- **Production notes** for quality insights

---

## How It Works

### Week 1: Initial Setup
```
1. Scan channel for new uploads (last 7 days)
2. Run full audit on each using youtube-audit.md
3. Create comparison dashboard
4. Identify patterns and quick wins
5. Generate week 1 report
```

### Week 2+: Ongoing Monitoring
```
1. Check for new uploads (past week)
2. Audit each automatically
3. Add results to rolling dashboard
4. Track trends across all videos
5. Identify improving/declining dimensions
6. Generate weekly update report
```

---

## Sample Loop Prompts

### Basic Weekly Loop
```
/loop 7d Check for new videos on [Channel Name] uploaded in the last 7 days.
For each new video:
1. Run the full YouTube Audit (10 dimensions)
2. Note any videos that scored below 65/100
3. Add scores to running dashboard

Output:
- List of audited videos this week
- Overall trend (improving/stable/declining)
- Any videos flagged for immediate attention
```

### Comprehensive Weekly Loop with Dashboard
```
/loop 7d Audit new YouTube uploads and generate performance dashboard.

Process:
1. Identify all videos published in the past 7 days on [Channel Name]
2. For each video, run complete YouTube Audit (10 dimensions, 3-5 recommendations)
3. Collect scores: overall score + each dimension (1-10)

Dashboard should show:
- This week's audited videos (count + avg score)
- 10-dimension radar comparing this week's videos
- 12-week trend line of overall scores
- Performance grid (dimension, latest, avg, trend)
- Key patterns (what's improving, what needs attention)

Recommendations:
- Quick wins for lowest-scoring dimension
- Week-over-week improvement areas
- Dimensions to focus on next week
```

### Executive Report Loop
```
/loop 7d Audit new videos and prepare weekly executive summary.

For each new video published this week:
1. Run full YouTube Audit using youtube-audit.md skill
2. Highlight if score is above/below channel average
3. Flag any dimension scoring below 5/10

Weekly summary should include:
- Number of videos published this week
- Average score this week vs. 4-week average
- Videos exceeding channel standard (>75)
- Videos needing immediate attention (<60)
- Top 3 dimensions for the week
- Bottom 3 dimensions for the week
- One strategic recommendation for next week
```

---

## What Gets Tracked

### Per Video
- Overall score (0-100)
- All 10 dimension scores (1-10 each)
- Key strengths (top 3)
- Key gaps (top 3)
- Quick win recommendations
- Publication date
- Audit date

### Across Videos (Rolling)
- Average score by week
- Trend per dimension (improving/stable/declining)
- Most consistent strength
- Most consistent gap
- Publication velocity
- Performance vs. channel average

---

## Output Format

### Weekly Report
```
Weekly YouTube Audit Summary — Week of [Date]

Videos Audited: 3
Average Score: 71/100
Week vs. 4-Week Avg: +3 points (improving trend ✓)

Audited Videos:
□ "Title 1" — 74/100 (✓ above average)
□ "Title 2" — 68/100 (~ on trend)
□ "Title 3" — 71/100 (~ on trend)

Dimension Performance This Week:
↑ Technical Quality: 7.8 (↑ +0.3 vs. last week)
↑ Brand Alignment: 7.5 (→ stable)
↓ SEO Optimization: 5.2 (↓ -0.4 vs. last week — investigate)

Quick Wins:
□ Rewrite titles for SEO keywords
□ Add chapters to all videos
□ Improve CTA messaging

Next Week Focus: SEO optimization + CTA testing
```

### Dashboard Integration
- Auto-updates each week with new video data
- Maintains 12-week rolling history
- Tracks trends by dimension
- Flags videos needing attention
- Compares to channel baseline

---

## Pro Tips

### Maximizing Value
1. **Consistency matters** — audit on the same day each week
2. **Build history** — results are more valuable after 4+ weeks
3. **Act on patterns** — if a dimension is consistently low, train the team
4. **Celebrate wins** — highlight improving dimensions to motivate creators
5. **Share weekly** — keep leadership and team informed

### Troubleshooting
- **"Can't find new videos"** → Manually provide video URLs or list titles
- **"Missing transcripts"** → Check YouTube auto-captions or request from creator
- **"Scores seem random"** → Audit is consistent; if wide variance, investigate process changes
- **"Dashboard not updating"** → Ensure previous week's data exists before comparing

### Integrating with Team
- Share weekly report in Slack/email
- Post dashboard publicly for creators
- Use scores in creator performance reviews
- Tie recommendations to content strategy

---

## Typical Weekly Workflow

**Monday 9:15 AM (Auto-triggered)**
```
System checks for new uploads → Audits them → Creates dashboard → Sends report
```

**Monday 10:00 AM**
```
You review report → Identify gaps → Plan content strategy
```

**Wednesday**
```
Share quick wins with video team
```

**Friday**
```
Debrief on what recommendations were implemented
```

---

## Integration with Other Skills

**Works with:**
- `youtube-audit.md` — provides the audit framework
- `youtube-audit-dashboard.md` — visualizes rolling data
- `youtube-audit-monthly-review.md` — synthesizes 4 weeks into strategic plan

**Typical workflow:**
```
1. Set up this skill with /loop (weekly)
2. Each week, audits run automatically
3. Dashboard updates with new data
4. Monthly skill generates strategic review
5. Team acts on recommendations
6. Cycle repeats
```

---

## Success Criteria

✓ Loop runs on schedule without manual intervention  
✓ New videos are detected and audited automatically  
✓ Dashboard updates weekly with new data  
✓ Trends emerge within 3-4 weeks  
✓ Team can see progress/decline by dimension  
✓ Quick wins are actionable (can be done in 1 week)  
✓ Reports are useful for decision-making  

---

## Advanced: Custom Focus Areas

If your business goal is specific, customize the loop:

**For Lead Generation:**
```
Emphasize: CTA Effectiveness, Hook Strength, Business Impact
Report: Highlight videos likely to convert leads
```

**For SEO/Discoverability:**
```
Emphasize: SEO Optimization, Thumbnail, Content Clarity
Report: Flag SEO gaps, recommend keyword opportunities
```

**For Brand Positioning:**
```
Emphasize: Brand Alignment, Content Clarity, Technical Quality
Report: Consistency across channel, brand adherence score
```

---

## Version & Portability

- **Portable:** Yes — works across machines/Windows
- **Dependencies:** Claude Code + loop capability
- **File location:** `.claude/skills/youtube-audit-recurring.md`
- **Setup time:** 2 minutes (run one command)

Copy this file to any machine's `.claude/skills/` and use `/loop` command.

### To Transfer to Another Machine:
1. Copy `.claude/skills/youtube-audit-recurring.md` to new machine
2. Copy `.claude/skills/youtube-audit.md` (core skill)
3. Copy `.claude/skills/youtube-audit-dashboard.md` (visualization)
4. Run same `/loop` command
5. Done — audits continue automatically

---

## Stopping/Pausing

**To pause audits temporarily:**
```
/stop-loop
```

**To resume:**
```
/loop 7d [your audit prompt]
```

**To adjust frequency:**
```
/stop-loop
/loop 14d [your audit prompt]  ← Changes to bi-weekly
```

---

## Support

For issues or customizations, reference the core `youtube-audit.md` skill or customize the loop prompt above.
