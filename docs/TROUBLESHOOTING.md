# YouTube Video Audit Skill - Troubleshooting Guide

## Common Issues & Solutions

---

## Installation Issues

### Issue 1: "Skill not found" or "File not found"

**Symptoms:**
- Claude doesn't recognize the skill
- Error message: "youtube-audit skill not located"
- Skill doesn't appear in available skills list

**Diagnosis Steps:**
1. Check file exists:
   ```bash
   ls -la ".claude/skills/youtube-audit.md"
   ```
2. Check file size (should be 1000+ lines):
   ```bash
   wc -l ".claude/skills/youtube-audit.md"
   ```
3. Check file isn't empty:
   ```bash
   head -20 ".claude/skills/youtube-audit.md"
   # Should show markdown content
   ```

**Solutions (in order):**

1. **Create .claude/skills directory if missing:**
   ```bash
   mkdir -p ".claude/skills"
   ```

2. **Verify skill file location:**
   - Should be: `.claude/skills/youtube-audit.md`
   - NOT: `.claude/youtube-audit.md`
   - NOT: `youtube-audit.md` (no .claude folder)

3. **Ensure file copied completely:**
   ```bash
   # Check it's not truncated (should be 1000+ lines)
   tail -20 ".claude/skills/youtube-audit.md"
   # Should show end of file content, not error
   ```

4. **Reload Claude Code:**
   - Quit Claude Code completely
   - Wait 3-5 seconds
   - Restart Claude Code
   - Try again

5. **Clear Claude cache:**
   ```bash
   # On Windows:
   Remove-Item "$env:APPDATA\Claude\.claude" -Recurse -Force
   
   # On Mac:
   rm -rf ~/.claude/.cache
   
   # On Linux:
   rm -rf ~/.claude/.cache
   ```

6. **Verify file encoding:**
   ```bash
   file ".claude/skills/youtube-audit.md"
   # Should say "UTF-8 Unicode"
   ```

**If still not found:**
- Check CLAUDE.md to confirm you're using the skill correctly
- Verify Claude Code version is up to date
- Contact support with file location

---

### Issue 2: "Permission denied" when accessing skill

**Symptoms:**
- Error: "Permission denied"
- Cannot read skill file
- File shows as locked or inaccessible

**Diagnosis:**
```bash
# Check file permissions
ls -l ".claude/skills/youtube-audit.md"
# Should show: -rw-r--r--
```

**Solutions:**

1. **Fix file permissions:**
   ```bash
   # Make file readable
   chmod 644 ".claude/skills/youtube-audit.md"
   
   # Make directory readable/executable
   chmod 755 ".claude/skills"
   ```

2. **Move file to new location:**
   ```bash
   # If permissions issue persists
   cp ".claude/skills/youtube-audit.md" "youtube-audit-backup.md"
   rm ".claude/skills/youtube-audit.md"
   cp "youtube-audit-backup.md" ".claude/skills/youtube-audit.md"
   chmod 644 ".claude/skills/youtube-audit.md"
   ```

3. **Check if file is in use:**
   - Another application may have locked it
   - Close all text editors with the file open
   - Restart Claude Code

---

### Issue 3: Skill file corrupted or incomplete

**Symptoms:**
- File exists but Claude gives errors
- Skill "half works" but incomplete
- Random error messages when using skill

**Diagnosis:**
```bash
# Check key sections exist
grep "Overall Audit Score" ".claude/skills/youtube-audit.md"
grep "Scoring Framework" ".claude/skills/youtube-audit.md"
grep "Quick Wins" ".claude/skills/youtube-audit.md"

# All should return results
```

**Solutions:**

1. **Re-download skill file:**
   - Get fresh copy from source
   - Delete old file: `rm ".claude/skills/youtube-audit.md"`
   - Copy new file to location

2. **Check for truncation:**
   ```bash
   # Look at last 20 lines
   tail -20 ".claude/skills/youtube-audit.md"
   # Should see full content, not incomplete section
   ```

3. **Validate file structure:**
   ```bash
   # Count major sections
   grep -c "^##" ".claude/skills/youtube-audit.md"
   # Should be 15+
   ```

4. **If all else fails:**
   - Delete file
   - Restart Claude Code
   - Re-add file fresh
   - Test with minimal request first

---

## Usage Issues

### Issue 4: "I don't know how to use this skill"

**Symptoms:**
- Not sure how to format requests
- Don't understand what to provide
- Results don't match expectations

**Solutions:**

1. **Start with minimal request:**
   ```
   Please audit this YouTube video: [paste any YouTube URL]
   Target audience: [1-2 sentences about who should watch]
   Business goal: [what you want to achieve]
   ```

2. **Refer to examples:**
   - See `examples/sample_audit_request.md` for 7 format options
   - See `examples/sample_results.md` for expected output
   - Pick the format that matches your situation

3. **Review CLAUDE.md:**
   - Section: "Quick Start"
   - Section: "How to Use This Skill"
   - Shows exact request structure

4. **Ask Claude directly:**
   ```
   I'm trying to use the YouTube Video Audit skill. 
   Can you explain how to format a request and what I'll get?
   ```

---

### Issue 5: "Results are too generic"

**Symptoms:**
- Feedback seems boilerplate
- Not specific to my video
- Doesn't address my unique situation

**Diagnosis:**
- Usually caused by insufficient input detail

**Solutions (in order of impact):**

1. **Provide video transcript (HIGHEST IMPACT):**
   - Best source: YouTube auto-generated captions
   - Copy full transcript into request
   - Enables detailed content analysis
   - Typically +50% improvement in specificity

2. **Include specific target audience:**
   ✗ Generic: "marketing professionals"
   ✓ Specific: "SaaS CTOs, 250-500M revenue companies, manufacturing focus"

3. **Define business objective precisely:**
   ✗ Generic: "improve engagement"
   ✓ Specific: "drive qualified leads to free trial signup"

4. **Add available analytics:**
   ```
   Views: 2,400
   Watch Time: 4.2 min average (out of 8:42)
   CTR: 8%
   Comments: 45
   Subscribers gained: 23
   ```

5. **Mention known issues:**
   "We know the middle section loses engagement. Please focus on retention and pacing."

6. **Specify focus areas:**
   "Please prioritize SEO optimization and lead generation conversion strategy."

**Expected improvement:**
- Minimal input: Generic feedback (40% match to your situation)
- Standard input: Good feedback (70% match)
- Comprehensive input: Expert-level recommendations (95%+ match)

---

### Issue 6: "I want to focus on specific dimensions"

**Symptoms:**
- Only care about SEO, not all dimensions
- Want deep-dive on engagement only
- Different business goal than general audit

**Solutions:**

1. **Specify focus in request:**
   ```
   I want a focused audit on these dimensions:
   - SEO Optimization
   - Thumbnail Effectiveness
   - Business Impact
   
   [Video details]
   ```

2. **Request after initial audit:**
   ```
   Based on the initial audit, I want to deep-dive on:
   - Why audience retention drops at minute 3?
   - Specific CTA optimization for lead generation?
   ```

3. **Use focus-area examples:**
   From `examples/sample_audit_request.md`:
   - Format 5: "Focus on Specific Issues"
   - Shows exact syntax for dimension focus

4. **Ask clarifying questions:**
   ```
   Which dimension should I focus on first?
   - SEO (for discoverability)
   - Engagement (for community growth)
   - Retention (for watch time)
   - Lead generation (for conversions)
   ```

---

### Issue 7: "I need to audit multiple videos"

**Symptoms:**
- Want to compare videos
- Auditing entire channel
- Need competitive benchmarking

**Solutions:**

1. **Request one audit at a time:**
   - Run complete audit on Video 1
   - Run complete audit on Video 2
   - Request comparison in separate session

2. **For competitive benchmarking:**
   From `examples/sample_audit_request.md` Format 4:
   ```
   Please audit and compare three videos:
   
   OUR VIDEO:
   - URL: [our video URL]
   - Title: [title]
   - Views: [number]
   
   COMPETITOR 1:
   - URL: [competitor URL]
   - Title: [title]
   - Views: [number]
   
   [repeat for more competitors]
   ```

3. **For channel-wide audit:**
   - Recommend auditing top 5-10 videos (highest performing)
   - Use results to identify channel-wide patterns
   - Then audit newer videos for consistency

---

## Content & Data Issues

### Issue 8: "I don't have a transcript"

**Symptoms:**
- Video has no captions
- Can't access transcript
- YouTube didn't auto-generate captions

**Solutions (in order of effort):**

1. **Use YouTube auto-captions (if available):**
   - Open video on YouTube
   - Click CC (Captions) icon
   - Click settings (⚙️) → Show transcript
   - Copy transcript

2. **Use browser extension to extract:**
   - Install YouTube transcript tool
   - Download transcript as text
   - Paste into audit request

3. **Watch video and write summary:**
   - Take notes on key points
   - Summarize content structure
   - Include in audit request
   - Scope: "Transcript not available; based on title/description/summary"

4. **Use video title + description:**
   - Analysis will be limited
   - Will note limitation in results
   - Still valuable for SEO, structure, CTAs

5. **Request manual caption:**
   - Hire transcription service
   - Use for this audit + future reference
   - Best for important videos

**Note:** Audit proceeds with whatever you provide. Transcript enables best analysis, but not required.

---

### Issue 9: "Analytics data seems incomplete"

**Symptoms:**
- Missing some metrics from YouTube Studio
- Don't know what data to include
- Unsure if data is accurate

**Solutions:**

1. **Get complete analytics from YouTube Studio:**
   - Go to youtube.com/studio
   - Click "Analytics" → "Overview"
   - Metrics available:
     - Views, Watch time, Average duration
     - CTR, Clicks, Engagement rate
     - Subscribers gained, Likes, Comments, Shares
   - Copy relevant metrics

2. **What's most important:**
   - Views (total reach)
   - Watch time % (retention)
   - CTR (discovery effectiveness)
   - Engagement rate (audience interest)

3. **If metrics incomplete:**
   - Include what you have
   - Note what's missing
   - Skill will work with available data
   - Results will note limitations

4. **For new videos:**
   - Video may need 48 hours for analytics
   - Can audit with partial data
   - Re-audit after 1 week for comprehensive analysis

---

### Issue 10: "Data seems wrong or inconsistent"

**Symptoms:**
- YouTube metrics seem low/high
- Retention data doesn't match impressions
- Analytics look off

**Solutions:**

1. **Verify data source:**
   - Use official YouTube Studio (most reliable)
   - Don't use third-party tools (may have lag)
   - Check date range (last 28 days? Custom?)

2. **Check common issues:**
   - Is monetization enabled? (Affects some metrics)
   - Age restriction on video? (Affects discovery)
   - Is video listed/searchable? (Affects CTR)
   - Recently published? (Metrics update over time)

3. **Data interpretation:**
   - Low CTR (2-3%) is normal benchmark
   - 40-50% retention is good
   - 1-3% engagement rate is average
   - 0.5-2% subscriber gain rate is normal

4. **If still unsure:**
   - Include original YouTube metrics in audit request
   - Note any concerns
   - Skill will interpret data conservatively

---

## Performance Issues

### Issue 11: "Audit is taking very long"

**Symptoms:**
- Waiting 5+ minutes for results
- Claude appears stuck/processing
- Long processing time with no progress

**Solutions (in order):**

1. **Check internet connection:**
   ```bash
   ping google.com
   # Should respond within 50ms
   ```

2. **Start with simpler request:**
   ✗ Don't: 10,000-word transcript + 50 competitor videos
   ✓ Do: Title + description + target audience

3. **Clear Claude context:**
   - Close Claude Code
   - Restart it
   - Try again with fresh session

4. **Use quick-audit format:**
   From `examples/sample_audit_request.md` Format 7:
   ```
   QUICK AUDIT:
   URL: [video]
   Target: [audience]
   Goal: [objective]
   Questions: [3-5 specific questions]
   ```

5. **Break into multiple audits:**
   - First audit: Structure + SEO
   - Second audit: Engagement + retention
   - Faster iteration, same insight

6. **If still slow:**
   - Claude may be under load
   - Wait and try again in 15 minutes
   - Or use quick-audit format while waiting

---

### Issue 12: "Results are cut off or incomplete"

**Symptoms:**
- Report ends mid-sentence
- Missing sections (no "Action Plan")
- Output seems truncated

**Solutions:**

1. **Ask Claude to continue:**
   ```
   Please continue the audit report from where you left off.
   Complete the missing sections.
   ```

2. **Request shorter output:**
   ```
   I want a concise audit (2,000 words max) focusing on:
   - Executive summary
   - Top 5 strengths and gaps
   - Top 5 recommendations
   ```

3. **Request by section:**
   ```
   1. Complete the action plan section
   2. Add financial impact estimates
   3. Provide competitive analysis
   ```

4. **Use quick format:**
   - Request only specific sections you need
   - Build full report iteratively

---

## Results & Recommendations

### Issue 13: "I don't understand a recommendation"

**Symptoms:**
- Recommendation is unclear
- Don't know how to implement
- Technical jargon is confusing

**Solutions:**

1. **Ask for clarification:**
   ```
   In the audit, you recommended: [quote specific recommendation]
   
   Can you explain in simpler terms how to do this?
   ```

2. **Request step-by-step guide:**
   ```
   For the [recommendation name] improvement,
   can you provide exact steps to implement?
   ```

3. **Ask for timeline:**
   ```
   How long would it take to implement [recommendation]?
   What's the effort level?
   ```

4. **Request expected outcome:**
   ```
   If I implement [recommendation], what results should I expect?
   How do I measure success?
   ```

---

### Issue 14: "Recommendation doesn't apply to my video"

**Symptoms:**
- Suggestion seems wrong for your content
- Business model is different
- Audience/goal doesn't match recommendation

**Solutions:**

1. **Clarify your business model:**
   ```
   Re-audit with more detail:
   - Business model: [subscription/freemium/advertising]
   - Customer lifetime value: [LTV]
   - Current conversion rate: [number]
   - Strategic priority: [which goal is #1]
   ```

2. **Request customized recommendation:**
   ```
   For [recommendation], how would this apply to:
   - [Your business model]
   - [Your audience type]
   - [Your specific goal]
   ```

3. **Ask for alternatives:**
   ```
   Instead of [recommendation], what would work better for:
   - [Your situation]
   - [Your constraints]
   - [Your goals]
   ```

4. **Skip and move on:**
   - Not all recommendations apply to every video
   - Use what's relevant, ignore rest
   - Audit works best for majority of recommendations

---

### Issue 15: "I implemented the recommendation but didn't see improvement"

**Symptoms:**
- Made the change, metrics didn't improve
- CTR stayed same, retention dropped
- Video performed worse after change

**Solutions:**

1. **Verify implementation:**
   - Did you actually make the change?
   - Did change publish/go live?
   - Is there any evidence of the change in analytics?

2. **Allow time for results:**
   - YouTube algorithm takes time to update
   - Wait minimum 1 week for metrics to stabilize
   - Many changes show results after 2-3 weeks

3. **Check for other variables:**
   - Did you change anything else?
   - Did publishing time/day affect results?
   - Did another external factor change?

4. **A/B test properly:**
   - Implement change on one video (test)
   - Keep old version on similar video (control)
   - Compare after 2-3 weeks
   - This proves if recommendation works for YOUR audience

5. **Request refined recommendation:**
   ```
   I implemented: [specific change]
   Expected: [improvement]
   Actual: [what happened]
   
   Can you suggest alternatives?
   ```

6. **Consider audience difference:**
   - Your audience may be different from average
   - Recommendation may not apply to your segment
   - Request variation optimized for your specific audience

---

## Technical Issues

### Issue 16: "Claude Code crashes or freezes"

**Symptoms:**
- Application stops responding
- Computer becomes slow
- Error messages appear

**Solutions:**

1. **Force quit and restart:**
   ```bash
   # Mac/Linux:
   pkill -9 claude-code
   
   # Windows:
   taskkill /F /IM claude-code.exe
   ```

2. **Clear cache and restart:**
   ```bash
   # Delete cache
   rm -rf ~/.claude/cache
   
   # Restart Claude Code
   ```

3. **Reduce request size:**
   - Don't paste 10,000-word transcripts at once
   - Send smaller requests
   - Build up complexity gradually

4. **Check system resources:**
   - Close other applications
   - Free up disk space
   - Restart your computer

5. **Update Claude Code:**
   - Check for latest version
   - Update if available
   - Many issues fixed in updates

---

### Issue 17: "Error message I don't understand"

**Symptoms:**
- Technical error message appears
- Doesn't match any issue above
- Don't know what to do

**Solutions:**

1. **Read the full error:**
   - Screenshot or copy the exact error message
   - Note what you were doing
   - Note your system (Windows/Mac/Linux)

2. **Try basic fixes:**
   - Restart Claude Code
   - Reload skill file
   - Try simpler request
   - Clear cache

3. **Search for error:**
   - Copy error message
   - Search Claude Code documentation
   - Check GitHub issues if public

4. **Ask for help:**
   ```
   I'm getting an error: [paste error]
   I was trying to: [describe action]
   System: [Windows/Mac/Linux]
   
   What should I do?
   ```

---

## Getting Help

### Before You Report an Issue

1. **Check this guide:**
   - Search for your symptom
   - Try suggested solutions
   - Note which steps you've tried

2. **Check CLAUDE.md:**
   - Quick Start section
   - How to Use section
   - Troubleshooting might be mentioned there

3. **Check examples:**
   - Review sample_audit_request.md for correct format
   - Check sample_results.md for expected output
   - Compare your results

4. **Try step by step:**
   - Use minimal request first
   - Add complexity gradually
   - Note where it breaks

### How to Report an Issue

Include:
1. **Exact error message** (screenshot helpful)
2. **Steps to reproduce** (what were you doing?)
3. **Expected outcome** (what should happen?)
4. **Actual outcome** (what actually happened?)
5. **Your system** (Windows/Mac/Linux, Claude Code version)
6. **What you've tried** (which troubleshooting steps worked/didn't work?)

---

## FAQ

**Q: Do I need the transcript to audit?**
A: No. Audit works with just title + description + target. Transcript enables deeper analysis.

**Q: How long does an audit take?**
A: Minimal input: 3-5 min. Standard: 10-15 min. Comprehensive: 20-30 min.

**Q: Can I audit videos without access to them?**
A: Yes. Provide title, description, and any info you have. Limitations noted in results.

**Q: Can I use this for non-YouTube videos?**
A: Skill is YouTube-specific. Could adapt for other platforms by modifying scoring criteria.

**Q: How accurate are the recommendations?**
A: Based on best practices and industry benchmarks. Accuracy improves with complete data input.

**Q: Can I share the audit report with stakeholders?**
A: Yes. Export to PDF or share markdown directly. Report is professional-ready.

**Q: How often should I audit a video?**
A: Initial audit when published. Re-audit after 4 weeks to measure improvement impact.

**Q: Can I compare my videos to competitors?**
A: Yes. Use Format 4 from sample_audit_request.md for competitive comparison.

**Q: Should I implement all recommendations?**
A: No. Prioritize by effort/impact. Start with Quick Wins.

---

## Still Having Issues?

1. Review relevant section above
2. Check CLAUDE.md, IMPLEMENTATION_GUIDE.md, IMPROVEMENTS.md
3. Review sample_audit_request.md and sample_results.md
4. Try step-by-step approach (minimal → complex)
5. Ask Claude directly: "I'm having trouble with [issue]. Can you help?"

**Most issues resolve within 5 minutes with these guides.**

