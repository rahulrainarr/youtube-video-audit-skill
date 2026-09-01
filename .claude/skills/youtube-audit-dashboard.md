# YouTube Audit Dashboard — Multi-Video Comparison

## Overview
Compare multiple YouTube video audits visually across all 10 dimensions. Generates interactive dashboards showing performance trends, dimension scores, and actionable insights across your entire channel or content set.

**Perfect for:**
- Tracking audit improvements over time
- Comparing performance across multiple videos
- Identifying patterns in what works
- Executive reporting on content performance
- Identifying top gaps to address strategically

---

## When to Use

✓ After running 3+ video audits — visualize the patterns  
✓ Monthly/quarterly performance reviews  
✓ Competitive benchmarking dashboard  
✓ Executive presentations on content quality  
✓ Trend analysis across channel content  
✓ Identifying best practices from top performers  
✓ Tracking improvement over time  

---

## Input Requirements

### Essential
- **Video audit results** (the output from youtube-audit.md skill)
  - Requires: Overall score, 10-dimension scores, key strengths, key gaps
- **Minimum 1 video**, optimal 3+ for comparison

### Data Format (Paste Audit Results)
```
Video Title: [title]
Overall Score: [0-100]
Content Clarity: [1-10]
Hook Strength: [1-10]
SEO Optimization: [1-10]
Thumbnail Effectiveness: [1-10]
Audience Retention: [1-10]
Engagement Potential: [1-10]
Brand Alignment: [1-10]
Technical Quality: [1-10]
CTA Effectiveness: [1-10]
Business Impact: [1-10]
```

### Optional but Valuable
- **Publication date** (for trend analysis)
- **Video URL** or video metadata
- **View count / engagement metrics** (for correlation)
- **Channel analytics** (to contextualize performance)
- **Thumbnail images** (for visual comparison)
- **Date of audit** (to track changes over time)

---

## What You'll Get

### 1. Interactive Dashboard
- **Metric cards** showing: videos audited, average score, top dimension, gap area
- **10-dimension radar chart** comparing 2-3 videos side-by-side
- **Trend line** showing overall score progression across audits
- **Performance grid** with dimension scores, averages, and trends (↑↓)

### 2. Visual Analysis
- Color-coded performance (green=strong, amber=needs work)
- Trend arrows showing improvement/decline per dimension
- Comparative benchmarks across your videos
- Pattern identification across content

### 3. Actionable Insights
- Dimensions with consistent high/low performance
- Quick wins (high-impact, low-effort improvements)
- Strategic focus areas (patterns worth addressing)
- What's working well (replicate in future content)

---

## How to Request

### Basic Dashboard
```
Create a dashboard comparing these 3 video audits:
[Paste audit 1 scores]
[Paste audit 2 scores]
[Paste audit 3 scores]

Show: 10-dimension comparison, trend analysis, key patterns
```

### Comprehensive Review
```
Create a monthly audit dashboard for our channel.

Videos to analyze:
- [Video 1 title + scores]
- [Video 2 title + scores]
- [Video 3 title + scores]

Include:
1. Radar chart comparing all three across 10 dimensions
2. Trend visualization (how scores changed month-over-month)
3. Performance grid with dimension breakdown
4. Pattern analysis: what's consistently strong/weak
5. Recommendations for next month's content focus
```

### Competitive Benchmarking
```
Compare our videos against competitor benchmarks.

Our videos:
[Our audit results]

Competitor videos:
[Competitor audit results]

Dimensions to emphasize: SEO, Hook Strength, CTA Effectiveness
Business goal: Lead generation
```

---

## Output Format

### Dashboard Components

**1. Metric Cards (Summary)**
```
Videos audited: 12
Avg score: 68/100
Top dimension: Technical Quality (7.8)
Gap area: SEO Optimization (5.2)
```

**2. Radar Chart**
- Shows all 10 dimensions
- Compares 2-3 videos (or your avg vs. a target)
- Easy visual pattern spotting

**3. Trend Line**
- X-axis: Video sequence or dates
- Y-axis: Overall score (0-100)
- Shows improvement trajectory

**4. Performance Grid**
```
Dimension              Latest  Avg(12)  Trend
Content Clarity        7.2     6.8      ↑+0.4
Hook Strength          6.1     5.9      ↑+0.2
SEO Optimization       5.8     5.2      ↑+0.6
Thumbnail Effective.   7.8     7.4      ↑+0.4
CTA Effectiveness      5.4     5.1      ↑+0.3
Business Impact        6.8     6.3      ↑+0.5
```

**5. Key Patterns**
- Consistently high-performing dimensions
- Persistent gap areas
- Month-over-month improvements
- Correlation with audience/business metrics

---

## Pro Tips

### Spotting Patterns
- **Consistent strengths** (7+): Replicate in future content
- **Consistent gaps** (<6): Target for training/templates
- **Trending up** (↑): Keep doing what you're doing
- **Flat or down** (→/↓): Investigate what changed

### Using for Executive Reports
- Lead with overall score trend (shows progress)
- Highlight 2-3 biggest wins
- Name 1-2 focus areas for next period
- Tie recommendations to business objectives

### Building Momentum
1. Audit first 3 videos (establish baseline)
2. Review dashboard weekly (track improvements)
3. A/B test recommendations in new content
4. Re-audit and compare (validate improvements)

### Benchmarking Against Competitors
- Audit your top 3 + competitor top 3
- Identify dimension gaps vs. competitors
- Prioritize dimensions important to your audience
- Track competitive gap narrowing over time

---

## Integration with Other Skills

**Works with:**
- `youtube-audit.md` — audit individual videos first, then dashboard
- `youtube-audit-recurring.md` — feed recurring audits into dashboard
- `youtube-audit-monthly-review.md` — monthly review uses dashboard

**Typical workflow:**
```
1. Run youtube-audit.md on 3-5 videos
2. Collect audit results in spreadsheet/document
3. Use this skill to create comparison dashboard
4. Share dashboard with team/stakeholders
5. Plan content strategy based on patterns
```

---

## Success Criteria

✓ Dashboard loads cleanly and updates with new data  
✓ Trends are visible and easy to interpret  
✓ Patterns across videos are obvious at a glance  
✓ Actionable recommendations follow from the data  
✓ Can be shared with non-technical stakeholders  
✓ Guides next month's content strategy  

---

## Troubleshooting

**Issue:** "Dashboard looks cluttered"
- Solution: Reduce to 3-4 key videos; use multiple dashboards for large sets

**Issue:** "Can't see trends yet"
- Solution: Audit 4+ videos over 2-4 weeks; trends need time to emerge

**Issue:** "Don't have all dimension scores"
- Solution: Dashboard works with partial data; missing dimensions will be flagged

---

## Version & Portability

- **Portable:** Yes — works across machines/Windows
- **Dependencies:** Claude Code + dataviz capability
- **File location:** `.claude/skills/youtube-audit-dashboard.md`
- **No setup needed:** Use directly in any session

Copy this file to any machine's `.claude/skills/` folder and reference in prompts.
