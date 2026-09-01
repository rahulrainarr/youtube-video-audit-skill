# YouTube Audit Skills Setup Guide

**For portable use across Windows machines and GitHub integration**

---

## Overview

This repo now includes **4 reusable YouTube audit skills**:

1. **youtube-audit.md** — Core: Analyze individual videos (10 dimensions, business-focused)
2. **youtube-audit-dashboard.md** — Visualize: Compare multiple audits via interactive dashboards
3. **youtube-audit-recurring.md** — Automate: Run weekly audits with `/loop`
4. **youtube-audit-monthly-review.md** — Strategic: Monthly planning + team recommendations

All skills are **portable, platform-agnostic, and ready to use immediately**.

---

## Quick Start (60 seconds)

### On Any Machine

**Step 1: Clone or download the repo**
```bash
git clone https://github.com/rahulrainarr/youtube-video-audit-skill.git
cd youtube-video-audit-skill
```

**Step 2: Copy skills to Claude Code**
```
Copy these files from .claude/skills/ to your local Claude Code setup:
  C:\Users\[YourUsername]\.claude\skills\
```

**Step 3: Use in Claude Code**
```
In any Claude Code session, reference the skill:
/audit [video URL]
/audit-dashboard [your audit results]
/loop 7d [your recurring audit prompt]
```

---

## Installation by Machine Type

### Windows — Local Setup

**Automatic (Recommended):**
```powershell
# Run from PowerShell
$source = ".\\.claude\\skills\\"
$dest = "$env:USERPROFILE\\.claude\\skills\\"
Copy-Item $source -Destination $dest -Recurse -Force
```

**Manual:**
1. Open File Explorer
2. Navigate to `.claude\skills\` in this repo
3. Copy all `.md` files
4. Paste into `C:\Users\[YourUsername]\.claude\skills\`
5. Restart Claude Code
6. Skills are now available

### Windows — Using from GitHub (No Copy)

If you want to use directly from GitHub without copying:
1. Clone the repo: `git clone https://github.com/rahulrainarr/youtube-video-audit-skill.git`
2. Note the full path
3. In Claude Code, reference: `Read the skill from [repo-path]\.claude\skills\youtube-audit.md`

---

## Importing to Your GitHub Account

### Option 1: Fork This Repo (Recommended)

**On GitHub.com:**
1. Go to https://github.com/rahulrainarr/youtube-video-audit-skill
2. Click **Fork** (top right)
3. Choose your account
4. Done — you now have a copy in your GitHub

**On your machine:**
```bash
git clone https://github.com/[YOUR-USERNAME]/youtube-video-audit-skill.git
cd youtube-video-audit-skill
```

### Option 2: Create New Repo from These Skills

**Create new GitHub repo:**
1. Go to GitHub.com → New Repository
2. Name it `youtube-audit-skills` (or similar)
3. Click Create

**On your machine:**
```bash
cd youtube-video-audit-skill
git remote set-url origin https://github.com/[YOUR-USERNAME]/youtube-audit-skills.git
git push origin main
```

### Option 3: Add Skills to Existing Repo

If you have an existing GitHub repo:
```bash
# Copy .claude/skills/ folder into your repo
cp -r .claude/ [your-repo]/.claude/

# Commit and push
cd [your-repo]
git add .claude/skills/
git commit -m "Add YouTube audit skills"
git push origin main
```

---

## Using Skills Across Machines

### Scenario: Laptop → Desktop → Other

**Once:**
- Clone or fork the repo to your GitHub account
- Copy `.claude/skills/` files to each machine's Claude Code

**Then:**
- All machines have access to the same skills
- Sync skill improvements: `git pull` to get latest versions
- Push updates: `git commit && git push` when you improve a skill

### Keeping Skills Updated

**After updating a skill locally:**
```bash
git add .claude/skills/youtube-audit*.md
git commit -m "Update [skill name] with improvements"
git push origin main
```

**On another machine to get updates:**
```bash
git pull origin main
# Skills automatically updated
```

---

## Skills at a Glance

### 1. Core Audit Skill — `youtube-audit.md`
**What it does:** Analyze any single video across 10 dimensions  
**When to use:** Ad-hoc video reviews, competitive analysis, new upload screening  
**Input:** Video URL or (title + description + transcript)  
**Output:** 10-dimension scorecard (1-10 each), overall score (0-100), 3-5 strengths, 3-5 gaps, prioritized recommendations

**Quick usage:**
```
/audit [YouTube URL]
or
/audit
Title: "Video Title"
Description: [...]
Transcript: [...]
Target audience: [description]
Business objective: [goal]
```

---

### 2. Dashboard Skill — `youtube-audit-dashboard.md`
**What it does:** Visualize multiple audits with interactive charts  
**When to use:** After 3+ audits, monthly reviews, reporting to leadership  
**Input:** Multiple audit results (scores + metadata)  
**Output:** Radar charts, trend lines, performance grids, pattern analysis

**Quick usage:**
```
/audit-dashboard
Videos: [Video 1 scores] [Video 2 scores] [Video 3 scores]
Period: Monthly review
Focus: [dimension or business goal]
```

---

### 3. Recurring Audit Skill — `youtube-audit-recurring.md`
**What it does:** Automatically audit new uploads weekly  
**When to use:** Continuous channel monitoring, weekly team reports  
**Setup:** One-time command via `/loop`  
**Output:** Weekly audit results + updated dashboard

**Quick usage:**
```
/loop 7d Audit new YouTube videos and generate dashboard
```

**To stop:**
```
/stop-loop
```

---

### 4. Monthly Review Skill — `youtube-audit-monthly-review.md`
**What it does:** Synthesize 4 weeks of audits into strategic plan  
**When to use:** Monthly strategy meetings, team training planning  
**Input:** All audits from the month + business context  
**Output:** Executive summary, action plan (quick wins + medium-term + strategic), team training recommendations

**Quick usage:**
```
YouTube Audit Monthly Review — September 2026

Videos analyzed: [paste all audit results]

Business objective: Lead generation
Compare to: Last month's results
```

**Or:** Automatically on the 1st of each month (pre-scheduled)

---

## File Organization

```
youtube-video-audit-skill/
├── .claude/
│   ├── settings.json
│   └── skills/
│       ├── youtube-audit.md                    ← Core skill
│       ├── youtube-audit-dashboard.md          ← Visualization
│       ├── youtube-audit-recurring.md          ← Weekly automation
│       └── youtube-audit-monthly-review.md     ← Strategic planning
├── examples/
│   ├── sample_audit_request.md
│   ├── sample_transcript.txt
│   └── sample_results.md
├── docs/
│   ├── IMPROVEMENTS.md
│   ├── IMPLEMENTATION_GUIDE.md
│   └── TROUBLESHOOTING.md
├── CLAUDE.md                          ← Project overview
├── SKILL-SETUP-GUIDE.md              ← This file
└── README.md                          ← Quick start
```

---

## Workflow Examples

### Workflow 1: Individual Video Audit (One-Time)
```
Session 1: Audit video
├─ Run: /audit [URL]
└─ Get: Scores + recommendations

Done — share results or use for strategy
```

### Workflow 2: Weekly Monitoring (Recurring)
```
Week 1: Set up automation
├─ Run: /loop 7d Audit new YouTube videos...
└─ Get: Weekly audit + dashboard updates

Week 2+: Automated
├─ Every Monday: New audits run automatically
├─ Dashboard updates with new data
└─ You review results and act on recommendations

Month-end: Strategic review
├─ Run: Monthly review skill
├─ Analyze: 4-week trends
└─ Plan: Next month strategy
```

### Workflow 3: Team Collaboration
```
Person A (Leader):
├─ Sets up /loop for weekly audits
└─ Reviews monthly strategy reports

Person B (Creator):
├─ Gets weekly dashboard
├─ Implements quick wins
└─ Applies training recommendations

Person C (Analyst):
├─ Maintains audit history
├─ Runs competitive benchmarking
└─ Prepares executive summaries
```

---

## Troubleshooting

### "Skill not found" error
**Solution:**
1. Check `.claude/skills/` directory exists locally
2. File names must match exactly: `youtube-audit-dashboard.md` (lowercase, hyphens)
3. Restart Claude Code after adding files

### "Skills not showing in autocomplete"
**Solution:**
1. Restart Claude Code completely
2. Clear Claude Code cache: `~/.claude/cache` (if it exists)
3. Re-add skills and restart

### "Different results on different machines"
**Solution:**
1. Ensure same skill files are used (git pull to sync)
2. Same Claude model? (Check via `/config`)
3. Slight variation is normal; major differences suggest file corruption

### "Can't push to GitHub"
**Solution:**
1. Check git remote: `git remote -v`
2. Authenticate: `git config --global user.name` / `git config --global user.email`
3. Use GitHub token or SSH key if needed
4. See: https://docs.github.com/en/get-started/getting-started-with-git/set-up-git

---

## Customization

### Adding Your Brand
Edit any `.md` file to add company-specific:
- Brand guidelines (fonts, colors, tone)
- Target audience definitions
- Business objectives
- Scoring weights
- Recommended templates

### Creating Variants
Example: Create `youtube-audit-seo-focus.md` for SEO-specific audits
```markdown
# YouTube Video Audit — SEO Focus

[Copy from youtube-audit.md, then modify:]
- Emphasize SEO dimension
- Add keyword research requirements
- Include SERP positioning analysis
```

Then commit and push to GitHub for team access.

---

## Team Distribution

### Share with Team
```bash
# 1. Ensure repo is on GitHub (public or private)
# 2. Send team the GitHub URL
# 3. Each person:

git clone https://github.com/[YOUR-USERNAME]/youtube-video-audit-skill.git
# Copy .claude/skills/ to their Claude Code setup
# Done — they can now use all skills
```

### Keep Everyone Updated
```bash
# When you improve a skill:
git add .claude/skills/youtube-audit*.md
git commit -m "Improve [skill name]"
git push origin main

# Team members pull updates:
git pull origin main
# They now have the latest version
```

---

## Version History

### Current Version: 1.0 (September 2026)
- ✅ Core audit skill (youtube-audit.md)
- ✅ Dashboard visualization (youtube-audit-dashboard.md)
- ✅ Recurring audits (youtube-audit-recurring.md)
- ✅ Monthly strategic review (youtube-audit-monthly-review.md)
- ✅ Portable across Windows machines
- ✅ GitHub-ready for team collaboration

### Future Enhancements
- [ ] Integration with YouTube API for auto-pulls
- [ ] SQLite database for audit history
- [ ] Real-time dashboard updates
- [ ] Slack notifications for audits
- [ ] Competitor tracking automation
- [ ] A/B test result integration

---

## Support & Feedback

### Reporting Issues
1. Check `docs/TROUBLESHOOTING.md` first
2. Create GitHub Issue with:
   - Skill name
   - What you tried
   - What went wrong
   - Your OS/setup

### Contributing Improvements
1. Fork the repo
2. Create feature branch: `git checkout -b improve-seo-skill`
3. Make changes, test locally
4. Commit: `git commit -m "Improve SEO dimension accuracy"`
5. Push: `git push origin improve-seo-skill`
6. Create Pull Request on GitHub

### Sharing Customizations
Created a variant that's awesome? Share it!
- Fork → customize → push your version
- Create an issue with link so others can find it

---

## Next Steps

1. **Now:** Copy `.claude/skills/` to your Claude Code
2. **First use:** Try `/audit [your-video-URL]`
3. **Weekly:** Set up `/loop 7d` for recurring audits
4. **Monthly:** Let monthly review run automatically
5. **Team:** Push to GitHub and share with colleagues

---

## Quick Reference

| Task | Command |
|------|---------|
| Audit one video | `/audit [URL]` |
| Create dashboard | `/audit-dashboard` |
| Start weekly audits | `/loop 7d [prompt]` |
| Stop weekly audits | `/stop-loop` |
| Manual monthly review | `[Trigger monthly review skill]` |
| Update skills on GitHub | `git push origin main` |
| Get latest skills | `git pull origin main` |

---

For detailed skill documentation, see:
- **Core audit:** `.claude/skills/youtube-audit.md`
- **Dashboard:** `.claude/skills/youtube-audit-dashboard.md`
- **Recurring:** `.claude/skills/youtube-audit-recurring.md`
- **Monthly:** `.claude/skills/youtube-audit-monthly-review.md`

Happy auditing! 🎬📊
