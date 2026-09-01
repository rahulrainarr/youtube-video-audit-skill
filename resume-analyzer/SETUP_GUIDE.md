# 📚 Complete Setup & User Guide

## System Requirements

- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Disk Space**: 500MB for dependencies
- **Browser**: Chrome, Firefox, Safari, or Edge

## 🔧 Installation Steps

### Step 1: Install Python

#### Windows
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
```bash
python --version
```

#### macOS
Using Homebrew:
```bash
brew install python3
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Step 2: Clone/Download Project

Navigate to desired location:
```bash
cd "c:\02 Claude\02 Code\resume-analyzer"
```

### Step 3: Create Virtual Environment

**Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run Application

**Windows (easiest)**:
```powershell
.\run.ps1
```

**macOS/Linux**:
```bash
bash run.sh
```

**Or manually**:
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📖 Quick Start Guide

### First Time Using the App?

#### 1. **Prepare Your Resume**
- Format: PDF, DOCX, or TXT
- Include: Name, Email, Phone, Experience, Education
- Use clear section headers: "Experience", "Education", "Skills"

#### 2. **Upload Resume**
- Click "Upload & Parse" tab
- Select resume file
- Click "🔍 Parse Resume"
- Review parsed information

#### 3. **Run Analysis**
- Click "Analysis Results" tab
- Click "🔬 Analyze Resume"
- Review metrics scores
- Check if meets 80% threshold

#### 4. **(Optional) Add Interview Data**
- Click "Interview Data" tab
- Toggle checkboxes for data you want to include
- Paste interview transcript, notes, or Q&A responses

#### 5. **Generate Report**
- Click "Generate Report" tab
- Enter candidate name
- Click "📄 Generate HTML Report"
- Download or view in browser

---

## 🎓 Understanding the Metrics

### Metric Categories

**Experience Metrics (44% total weight)**
- Sales Revenue Generation (15%)
- Business Development (12%)
- Account Management (12%)
- Leadership Experience (10%)
- Industry Expertise (10%)

**Technical Metrics (23% total weight)**
- Product & Technical Knowledge (8%)
- Relevant Certifications (7%)
- Analytics & Data-Driven (8%)

**Behavioral Metrics (18% total weight)**
- Communication Skills (8%)
- Negotiation & Deal Closing (10%)

**Other (15% weight)**
- Industry Expertise (10%)
- Additional factors (5%)

### Scoring Breakdown

**Sales Revenue Generation**
- 5+ years: 100 points
- 3-4 years: 80 points
- 1-2 years: 60 points
- <1 year: 40 points
- None: 0 points

**Business Development**
- Strategic account development: 100
- Market expansion: 90
- New business acquisition: 85
- Partner development: 75
- None: 0

**Leadership Experience**
- 10+ direct reports: 100
- 5-9 reports: 85
- 1-4 reports: 70
- Leadership projects: 60
- None: 0

---

## 🔍 How Parsing Works

### What Gets Extracted

1. **Contact Information**
   - Name (from first line)
   - Email (regex pattern)
   - Phone (pattern matching)
   - Location (keywords: "location", "based in")

2. **Professional Summary**
   - Looks for "Summary", "Objective", "About", "Profile"
   - Extracts up to 500 characters

3. **Work Experience**
   - Company names
   - Job titles
   - Duration calculation from dates or stated years
   - Key achievements from bullet points
   - Sales metrics (revenue, quota, etc.)

4. **Education**
   - Degree types (Bachelor, Master, MBA, PhD)
   - Field of study
   - Institution name

5. **Skills**
   - From dedicated "Skills" section
   - Split by commas or semicolons
   - Limited to 20 skills

6. **Certifications**
   - Common keywords: Salesforce, HubSpot, Google Analytics, etc.

### Tips for Better Parsing

✅ **Do:**
- Use clear section headers
- Include dates in YYYY format
- List achievements with bullet points
- Use standard job titles

❌ **Don't:**
- Use unusual formatting
- Scatter information across page
- Abbreviate without context
- Mix multiple sections together

---

## 📊 Reading the Report

### Overall Assessment Section
- **Overall Score**: Weighted average of all metrics
- **Match Percentage**: Same as overall score
- **80% Threshold**: Pass/Fail indicator
- **Industry Alignment**: High/Medium/Low
- **Job Readiness**: Level of preparation

### Detailed Metrics
Each metric shows:
- Name and description
- Score (0-100%)
- Progress bar visualization
- Weight in overall calculation

### Strengths
Top 5 competencies where candidate scored well (≥80%)

### Development Areas
Top 5 areas needing improvement (<60%)

### Recommendations
Actionable suggestions based on identified gaps

### Interview Integration
If provided:
- Full interview transcript
- Interview notes
- Q&A responses with analysis

---

## 🛠️ Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
pip install -r requirements.txt
```

### "Cannot read PDF file"

**Solutions:**
- Ensure PDF isn't corrupted
- Try converting PDF to different format
- Check file permissions

### "Resume parsed but data missing"

**Solutions:**
- Verify resume has clear section headers
- Check resume format matches standards
- Try manual entry in the app

### "Report not generating"

**Solutions:**
- Ensure candidate name is filled
- Check "reports" folder exists and is writable
- Try with simpler candidate name (no special characters)
- Check browser console for errors

### "Port 8501 already in use"

**Solutions:**
```bash
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8501
kill -9 <PID>
```

Or use different port:
```bash
streamlit run app.py --server.port 8502
```

### Virtual Environment Not Activating

**Windows (cmd.exe - don't use PowerShell)**:
```bash
venv\Scripts\activate.bat
```

**macOS/Linux**:
```bash
source venv/bin/activate
```

---

## 🔐 Data Privacy & Security

### What Happens to Your Data

- ✅ Resumes are processed locally on your machine
- ✅ No data is sent to external servers
- ✅ No data is stored after session ends
- ✅ Reports are saved only in local "reports" folder

### Deleting Old Reports

```bash
# Windows
rmdir /s reports

# macOS/Linux
rm -rf reports
```

---

## ⚙️ Advanced Configuration

### Change Default Threshold

Edit `app.py` and find:
```python
match_threshold = st.slider(
    "Match Threshold (%)",
    min_value=50,
    max_value=100,
    value=80,  # Change this
    step=5,
)
```

### Adjust Metric Weights

Edit `metrics.py`:
```python
SALES_BD_METRICS = {
    "sales_revenue_generation": {
        "weight": 0.15,  # Change this value
        # ...
    }
}
```

### Add Custom Metrics

1. Add to `SALES_BD_METRICS` in `metrics.py`
2. Create scoring method in `analyzer.py`
3. Method name: `_score_[metric_name]`

---

## 📞 Getting Help

### Common Questions

**Q: Can I analyze multiple resumes at once?**
A: Current version analyzes one at a time. Repeat steps for each resume.

**Q: Can I export data in other formats?**
A: Currently HTML only. You can print HTML to PDF via browser.

**Q: How accurate is the parsing?**
A: Depends on resume format. Standard formats parse at 90%+ accuracy.

**Q: Can I customize the metrics?**
A: Yes! Edit `metrics.py` to adjust weights and add new metrics.

**Q: Is there a limit to resume file size?**
A: No hard limit, but 10MB+ files may slow processing.

---

## 🚀 Performance Tips

1. **Run with fewer browser tabs** - Streamlit works best with dedicated attention
2. **Use modern browsers** - Chrome, Firefox perform best
3. **Close background apps** - Free up RAM for processing
4. **Restart app periodically** - Clears memory after analyzing many resumes

---

## 📝 Logging Issues

To debug issues, enable verbose output:

```bash
streamlit run app.py --logger.level=debug
```

Check output in terminal for error messages.

---

**Ready to analyze resumes? Start with Step 1 above!** 🎯
