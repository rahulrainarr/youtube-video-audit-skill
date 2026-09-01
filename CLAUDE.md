# Claude Code Project: YouTube Video Audit Skill

## Overview
A portable, reusable skill for comprehensive YouTube video auditing and strategic content recommendations. Designed to be transferred across systems and used independently.

## Project Structure

```
.
├── .claude/
│   ├── skills/
│   │   └── youtube-audit.md          # Main skill definition
│   ├── settings.json                 # Configuration
│   └── launch.json                   # Demo server config (optional)
├── examples/
│   ├── sample_audit_request.md       # Example request format
│   ├── sample_transcript.txt         # Sample transcript data
│   └── sample_results.md             # Example output
├── docs/
│   ├── IMPROVEMENTS.md               # Documentation improvements made
│   ├── IMPLEMENTATION_GUIDE.md       # How to implement in your environment
│   └── TROUBLESHOOTING.md            # Common issues and solutions
├── CLAUDE.md                         # This file
└── README.md                         # Quick start guide

```

## What This Skill Does

The YouTube Video Audit skill analyzes videos across 10 critical dimensions:
1. Content Clarity
2. Hook Strength
3. SEO Optimization
4. Thumbnail Effectiveness
5. Audience Retention
6. Engagement Potential
7. Brand Alignment
8. Technical Quality
9. CTA Effectiveness
10. Business Impact

**Output:** Comprehensive reports (3,000-5,000 words) with:
- 10-dimension scorecard (1-10 scale each)
- Overall audit score (0-100)
- 3-5 key strengths with examples
- 3-5 key gaps with severity
- Quick wins, medium-term, and strategic recommendations
- Optimized metadata (titles, descriptions, keywords, hashtags)
- Engagement strategy recommendations
- Thumbnail improvement concept
- Prioritized action plan with effort/impact/timeline

## How to Use This Skill

### Option 1: Via Claude Code (Recommended)
```bash
# The skill is available in Claude Code
# Simply reference it in your prompt:
"Please audit this YouTube video: [URL/details]"
```

### Option 2: Standalone Usage
This skill can be used independently across systems:
1. Copy the `.claude/skills/youtube-audit.md` file
2. Share with team members or use on another machine
3. Reference in prompts to Claude

### Option 3: Integrate with Your Workflow
```yaml
# In your Claude Code workflow, reference:
- Use the YouTube Audit skill
- Input: video details, transcript, analytics
- Output: comprehensive audit report
```

## Quick Start

### Minimal Request
```
Please audit this YouTube video: https://www.youtube.com/watch?v=XXXXX
Target audience: Marketing managers
Business goal: Lead generation
```

### Comprehensive Request
```
URL: https://www.youtube.com/watch?v=XXXXX
Title: [if different from URL]
Transcript: [paste full transcript]
Duration: 12:34
Channel: Enterprise Tech Insights
Target Audience: CTOs, enterprise architects
Business Objective: Drive consulting leads
Analytics:
  - Views: 2,400
  - Watch Time: 4.2 min average
  - CTR: 8%
  - Comments: 45
Competitors: [link to competitor 1] [link to competitor 2]
Known Issues: Low subscriber retention
Focus: Optimize for lead generation
```

### Manual Input (No URL Access)
```
Title: "5 Ways AI Transforms Enterprises"
Description: [full description]
Transcript: [full transcript]
Target: Enterprise architects, $50k+ budget
Goal: Drive consulting leads and demos
```

## Key Features

✓ **Comprehensive Analysis** — 10 dimensions, not generic feedback  
✓ **Business-Focused** — Recommendations tied to your specific objective  
✓ **Actionable** — Concrete "how-to" guidance, not just critique  
✓ **Prioritized** — Quick wins first, then medium/strategic improvements  
✓ **Portable** — No dependencies; works across systems  
✓ **Flexible** — Works with or without complete video access  
✓ **Scalable** — Audit 1 video or compare multiple videos  
✓ **Professional** — Suitable for marketing teams and leadership  

## Required Information

### Minimum (Will work with this)
- Video title or URL
- Description (even partial)
- Target audience
- Business objective

### Recommended (Better analysis)
- Full transcript or captions
- Video duration
- Channel name
- Any available analytics
- Thumbnail image or description

### Optional (Enhanced insights)
- Competitor video URLs
- Known pain points
- Production quality notes
- Prior performance data

## Output Examples

### Executive Summary
```
Overall Assessment:
[2-3 sentence assessment]

Key Strengths (Top 3):
1. [Strength with specific example]
2. [Strength with specific example]
3. [Strength with specific example]

Key Gaps (Top 3):
1. [Gap with business impact]
2. [Gap with business impact]
3. [Gap with business impact]

Overall Audit Score: 72/100
```

### Detailed Scorecard
```
Content Clarity:        7/10
Hook Strength:          6/10
SEO Optimization:       5/10
Thumbnail:              8/10
Audience Retention:     7/10
Engagement Potential:   6/10
Brand Alignment:        8/10
Technical Quality:      8/10
CTA Effectiveness:      4/10
Business Impact:        6/10
────────────────────
OVERALL SCORE:         72/100
```

### Action Plan (Examples)
```
Quick Wins (0-7 days):
□ Rewrite title for SEO [Effort: Low | Impact: Medium]
□ Optimize description keywords [Effort: Low | Impact: Medium]
□ Add chapter markers [Effort: Low | Impact: Low]

Medium-Term (2-4 weeks):
□ Redesign thumbnail concept [Effort: Medium | Impact: High]
□ Recut for improved retention [Effort: High | Impact: Medium]

Strategic (1-3 months):
□ Develop series around topic [Effort: High | Impact: High]
```

## Portability & Transfer

### Moving to Another System
1. Copy `.claude/skills/youtube-audit.md`
2. Place in target system's `.claude/skills/` directory
3. Skill is immediately available in Claude Code
4. No installation, configuration, or dependencies needed

### Sharing with Team Members
1. Export the skill file
2. Include `examples/` directory for context
3. Share documentation from `docs/` folder
4. Team members can immediately start using it

### Integration with Other Tools
- Skill works independently
- Can be referenced in automation workflows
- Outputs are in standard markdown format
- Results can be stored and compared over time

## Customization

### For Your Business
Edit `.claude/skills/youtube-audit.md` to add:
- Company-specific scoring criteria
- Your brand guidelines/voice
- Target audience definitions
- Custom focus areas

### Focus Area Examples
- "Focus on lead generation"
- "Optimize for social sharing"
- "Improve executive positioning"
- "Maximize SEO for discoverability"
- "Enhance engagement metrics"

## Examples & Demo

See `examples/` directory for:
- Sample audit request formats
- Example transcript data
- Sample results and outputs
- Common use cases

## Troubleshooting

### Common Issues
**Issue:** "Skill not found"
- Solution: Ensure `.claude/skills/youtube-audit.md` exists in correct directory

**Issue:** "Need transcript but don't have one"
- Solution: You can still audit with title, description, and context. Analysis will note the limitation.

**Issue:** "Results too generic"
- Solution: Provide more specific target audience and business objective details

**Issue:** "Want to focus on specific dimension"
- Solution: Add "Focus on [dimension name]" to your request

See `docs/TROUBLESHOOTING.md` for detailed solutions.

## Best Practices

1. **Be Specific About Audience**
   - Instead of: "General business audience"
   - Use: "Enterprise CTOs, budget $50k+, manufacturing industry"

2. **Define Objective Clearly**
   - Instead of: "Get more views"
   - Use: "Drive qualified leads for consulting services"

3. **Provide Transcript When Possible**
   - Enables deeper content analysis
   - Identifies messaging gaps
   - Improves SEO recommendations

4. **Include Analytics If Available**
   - Views, watch time, CTR inform recommendations
   - Identifies what's working
   - Benchmarks performance

5. **Specify Focus Areas**
   - "Optimize for SEO"
   - "Improve engagement"
   - "Perfect for executive visibility"

## Documentation Files

- **CLAUDE.md** (this file) — Project overview and usage
- **skills/youtube-audit.md** — Detailed skill definition
- **examples/sample_audit_request.md** — How to format requests
- **examples/sample_results.md** — What outputs look like
- **docs/IMPROVEMENTS.md** — Enhancements made to original
- **docs/IMPLEMENTATION_GUIDE.md** — Step-by-step setup
- **docs/TROUBLESHOOTING.md** — Common issues and solutions

## Version Information

- **Skill Version:** 1.0
- **Last Updated:** 2026-09-01
- **Status:** Production Ready
- **Portable:** Yes
- **Dependencies:** None (Claude Code required)

## Getting Help

If you have questions about:
- **Using the skill:** See examples/ and this CLAUDE.md
- **Troubleshooting:** See docs/TROUBLESHOOTING.md
- **Customizing:** See docs/IMPLEMENTATION_GUIDE.md
- **Request format:** See examples/sample_audit_request.md

## Next Steps

1. **Try it now:** Use the minimal request format above
2. **Review examples:** Check examples/ directory
3. **Audit your first video:** Pick a video and run through the skill
4. **Customize:** Adapt focus areas for your business needs
5. **Share:** Transfer skill to team members using portability steps

---

**Ready to audit? Start with a simple request and gradually provide more detail for deeper analysis.**
