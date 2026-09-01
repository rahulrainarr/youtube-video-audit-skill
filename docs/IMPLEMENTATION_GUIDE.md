# YouTube Video Audit Skill - Implementation Guide

## Quick Setup (5 minutes)

### Step 1: Verify Skill Location
The skill file should be at:
```
.claude/skills/youtube-audit.md
```

Check if it exists:
```bash
ls -la ".claude/skills/youtube-audit.md"
```

### Step 2: Use in Claude Code
Simply reference the skill in your prompt:
```
Please audit this YouTube video: [URL]
Target audience: [describe]
Business goal: [describe]
```

**Done!** The skill is immediately available.

---

## Detailed Setup

### For Individual Use (Personal Laptop)

#### 1. Locate Your .claude Directory
```bash
# On Windows
cd "$env:APPDATA\Claude" -or-
cd "C:\Users\[YourUsername]\.claude"

# On Mac
cd "~/.claude"

# On Linux
cd "~/.claude"
```

#### 2. Create Skills Directory (if not exists)
```bash
mkdir -p ".claude/skills"
```

#### 3. Copy Skill File
Copy `youtube-audit.md` to `.claude/skills/youtube-audit.md`

#### 4. Verify Installation
```bash
# Check file exists
ls -la ".claude/skills/youtube-audit.md"

# Should output: (file details)
```

#### 5. Test in Claude Code
In Claude Code, try:
```
Please audit this YouTube video: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Target audience: Music lovers
Business goal: Increase engagement
```

**Expected:** Claude references the skill and provides audit structure.

---

### For Team Use (Shared Repository)

#### 1. Create Project Structure
```
project-root/
├── .claude/
│   ├── skills/
│   │   └── youtube-audit.md
│   └── settings.json
├── CLAUDE.md
├── examples/
│   ├── sample_audit_request.md
│   ├── sample_results.md
│   └── sample_transcript.txt
├── docs/
│   ├── IMPROVEMENTS.md
│   ├── IMPLEMENTATION_GUIDE.md
│   └── TROUBLESHOOTING.md
└── README.md
```

#### 2. Initialize Git (if using version control)
```bash
git init
git add .claude/skills/youtube-audit.md
git add CLAUDE.md examples/ docs/
git commit -m "Add YouTube Video Audit skill"
```

#### 3. Share with Team
```bash
# Clone or share the repository
git clone [repo-url] [local-path]

# Team members verify installation
ls -la .claude/skills/youtube-audit.md
```

#### 4. Validate Installation
Team members run:
```
I want to test the YouTube Video Audit skill. 
Here's a test video: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Target: Music lovers
Goal: Engagement
```

---

### For Enterprise/Organizational Use

#### 1. Create Shared Skills Library
```
org-claude-skills/
├── skills/
│   ├── youtube-audit.md
│   ├── [other-skills]/
│   └── README.md
├── templates/
│   ├── audit-request-template.md
│   └── audit-results-template.md
├── examples/
│   ├── youtube/
│   │   ├── sample_request.md
│   │   └── sample_results.md
│   └── [other-content-types]/
├── docs/
│   ├── SETUP.md
│   ├── BEST_PRACTICES.md
│   └── FAQ.md
└── README.md
```

#### 2. Set Up Central Repository
```bash
# Create shared repository
git init --bare youtube-audit-skill.git

# Team members clone
git clone file:///path/to/youtube-audit-skill.git
```

#### 3. Configure Access Control
- Share via internal repository (GitHub Enterprise, GitLab, Bitbucket)
- Include `.claude/settings.json` with team-specific configurations
- Document approval process for skill updates

#### 4. Train Team
- Share `CLAUDE.md` overview
- Have team complete one sample audit (examples/sample_audit_request.md)
- Review sample results (examples/sample_results.md)
- Assign one team member as "Skill Champion" for support

---

## Configuration Options

### Create `.claude/settings.json`

#### Minimal Configuration
```json
{
  "skills": {
    "youtube-audit": {
      "enabled": true,
      "path": ".claude/skills/youtube-audit.md"
    }
  }
}
```

#### Extended Configuration
```json
{
  "skills": {
    "youtube-audit": {
      "enabled": true,
      "path": ".claude/skills/youtube-audit.md",
      "default_focus": "SEO optimization",
      "competitor_benchmarking": true,
      "output_format": "markdown",
      "report_length": "comprehensive"
    }
  },
  "preferences": {
    "default_audience_context": "B2B SaaS",
    "currency": "USD",
    "timezone": "UTC"
  }
}
```

### Team-Specific Configuration
```json
{
  "skills": {
    "youtube-audit": {
      "enabled": true,
      "path": ".claude/skills/youtube-audit.md"
    }
  },
  "team": {
    "name": "Marketing Team",
    "email_domain": "company.com",
    "default_goals": [
      "Lead generation",
      "Brand awareness",
      "SEO optimization"
    ]
  }
}
```

---

## Validation Steps

### Step 1: File Integrity Check
```bash
# Verify skill file exists and contains key sections
grep -c "Overall Audit Score" .claude/skills/youtube-audit.md
# Should output: 1 (or more)

grep -c "Scoring Framework" .claude/skills/youtube-audit.md
# Should output: 1
```

### Step 2: Functionality Test
In Claude Code, run:
```
Test the YouTube Video Audit skill with this request:

Title: "5 AI Tools for Marketing"
Duration: 8:42
Target Audience: Marketing managers
Business Objective: Lead generation

Can you confirm the skill loads and acknowledges these inputs?
```

**Expected output:** Claude confirms it recognized the request and skill context.

### Step 3: Output Format Test
Request a minimal audit:
```
Audit: https://www.youtube.com/watch?v=dQw4w9WgXcQ
(minimal test)
```

**Expected output:** Claude provides audit structure, even if limited by video access.

### Step 4: Full Workflow Test
Complete the sample request from examples:
```
[Copy full example from examples/sample_audit_request.md]
```

**Expected output:** Comprehensive report matching samples/sample_results.md structure.

---

## Troubleshooting Installation

### Issue: "Skill not found"

**Diagnosis:**
```bash
# Check file exists
ls -la .claude/skills/youtube-audit.md
# Should show file details, not "No such file"
```

**Solutions:**
1. Verify `.claude/skills/` directory exists
   ```bash
   mkdir -p .claude/skills
   ```
2. Copy skill file to correct location
   ```bash
   cp youtube-audit.md .claude/skills/
   ```
3. Reload Claude Code (quit and restart)
4. Clear cache: Delete `.claude/cache` if it exists

### Issue: "Skill file is corrupted"

**Diagnosis:**
```bash
# Check file isn't empty
wc -l .claude/skills/youtube-audit.md
# Should be 800+ lines
```

**Solutions:**
1. Verify file copied completely
2. Check file encoding is UTF-8
   ```bash
   file .claude/skills/youtube-audit.md
   ```
3. Re-download skill file from source
4. Verify no truncation occurred during copy

### Issue: "Results are too generic"

**Diagnosis:** Skill works but recommendations lack specificity

**Solutions:**
1. Provide more detail in request:
   - Full transcript (not just title/description)
   - Specific audience demographics
   - Detailed business objective
   - Available analytics data
2. Use comprehensive request format (see SAMPLE_AUDIT_REQUEST.md Format 3)
3. Specify focus areas:
   ```
   Focus on: SEO optimization and lead generation
   ```

### Issue: "Takes too long to generate results"

**Diagnosis:** Complex requests with lots of data

**Solutions:**
1. Start with minimal request, iterate
2. Break large audits into multiple smaller audits
3. Use quick-audit format (SAMPLE_AUDIT_REQUEST.md Format 7)

---

## Optimization Tips

### For Faster Results
1. **Use minimal input format** — Enough for quick feedback
2. **Specify focus areas** — Narrows analysis scope
3. **Provide structured data** — Easier to process than narrative

### For Better Results
1. **Provide full transcript** — Enables content analysis
2. **Include analytics** — Shows what's working
3. **Specify exact audience** — More targeted recommendations
4. **Clarify business objective** — Better business-aligned advice

### For Team Efficiency
1. **Create template requests** — Standardize input format
2. **Share sample results** — Everyone knows what to expect
3. **Designate skill champion** — One person handles complex audits
4. **Build request library** — Reuse formats for similar videos

---

## Advanced Configuration

### Custom Scoring Weights
If you want different weighting for your business:
```
Focus on these dimensions with higher weight:
- SEO Optimization (for discoverability-first videos)
- CTA Effectiveness (for lead-generation videos)
- Engagement Potential (for viral-growth videos)
- Technical Quality (for brand/professional videos)
```

### Integration with Analytics
Combine skill output with YouTube Analytics:
1. Export analytics from YouTube Studio
2. Include in audit request
3. Get performance-contextualized recommendations

### Competitive Benchmarking Database
Build over time:
1. Audit 10 competitor videos
2. Store results in spreadsheet
3. Reference in future audits for benchmarking
4. Identify performance patterns

---

## Maintenance

### Regular Checks (Weekly)
- [ ] Verify skill file still exists
- [ ] Run one sample audit to confirm functionality
- [ ] Check for any error messages

### Quarterly Reviews
- [ ] Review skill version (check for updates)
- [ ] Assess if scoring criteria need adjustment
- [ ] Update competitive benchmarks if available

### Annual Updates
- [ ] Review and update scoring framework if needed
- [ ] Add new examples based on team experience
- [ ] Refine recommendations based on results
- [ ] Document learnings in IMPROVEMENTS.md

---

## Sharing & Collaboration

### Email Transfer
```
Subject: YouTube Video Audit Skill for [Recipient Name]

Steps to install:
1. Download attached youtube-audit.md
2. Place in .claude/skills/ directory
3. Reload Claude Code
4. Use immediately

Example:
"Audit: [video-url] ..."

Questions? See CLAUDE.md for details.
```

### Repository Transfer
```bash
# Create shareable bundle
mkdir youtube-audit-skill
cp .claude/skills/youtube-audit.md youtube-audit-skill/
cp CLAUDE.md youtube-audit-skill/
cp -r examples/ youtube-audit-skill/
cp -r docs/ youtube-audit-skill/
zip -r youtube-audit-skill.zip youtube-audit-skill/
```

### Team Documentation
Share with team:
- `CLAUDE.md` — Overview
- `examples/sample_audit_request.md` — How to request
- `examples/sample_results.md` — What to expect
- `docs/TROUBLESHOOTING.md` — Common issues

---

## Success Criteria

### Installation Success
✓ Skill file exists at `.claude/skills/youtube-audit.md`
✓ File is not empty (800+ lines)
✓ Claude Code loads without errors
✓ Sample request returns structured response

### Functional Success
✓ Provides 10-dimension scorecard
✓ Includes executive summary
✓ Lists specific strengths and gaps
✓ Provides actionable recommendations
✓ Calculates overall audit score

### Business Success
✓ Team uses skill for video audits
✓ Recommendations drive measurable improvements
✓ Time to audit decreases with practice
✓ Recommendations align with business goals

---

## Getting Help

### If Installation Fails
1. Check TROUBLESHOOTING.md for your specific error
2. Verify file location and permissions
3. Reload Claude Code
4. Try again

### If Results Are Unexpected
1. Review sample_results.md for expected output
2. Provide more complete input (transcript, analytics)
3. Specify focus areas to narrow analysis
4. Check TROUBLESHOOTING.md "Results too generic" section

### If You Need Customization
1. Document your specific requirements
2. Review CONFIGURATION_OPTIONS section above
3. Update settings.json for your team
4. Test with sample audit

---

## Next Steps After Setup

1. **Try a test audit** (5 minutes)
   - Use examples/sample_audit_request.md Format 1
   - Confirm you get structured response

2. **Run a real audit** (15 minutes)
   - Pick a real video you want to optimize
   - Use Format 2 or 3 for comprehensive analysis

3. **Review results** (10 minutes)
   - Compare to examples/sample_results.md
   - Note any differences or customizations needed

4. **Share with team** (30 minutes)
   - Send them CLAUDE.md overview
   - Have them try a sample audit
   - Collect feedback

5. **Integrate into workflow** (1-2 hours)
   - Create audit templates for your content type
   - Build competitive benchmarking database
   - Document team-specific scoring preferences

---

## Support & Resources

- **Quick Start:** See CLAUDE.md
- **Examples:** See examples/ directory
- **Troubleshooting:** See docs/TROUBLESHOOTING.md
- **Improvements Overview:** See docs/IMPROVEMENTS.md
- **Sample Results:** See examples/sample_results.md

**You're all set! Start with a minimal audit and work up to comprehensive analysis.**

