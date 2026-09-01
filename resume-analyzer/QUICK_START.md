# ⚡ Quick Start (5 Minutes)

## Prerequisites
- Python 3.8+ installed
- 500MB free disk space

## Option A: Windows (Easiest)

1. **Open PowerShell** in the project folder
2. Run:
```powershell
.\run.ps1
```
3. Browser opens automatically at `http://localhost:8501`
4. Skip to "Using the App" below

## Option B: macOS/Linux

1. **Open Terminal** in the project folder
2. Run:
```bash
bash run.sh
```
3. Open browser at `http://localhost:8501`
4. Skip to "Using the App" below

## Option C: Manual Setup

1. **Create virtual environment:**
```bash
python -m venv venv
```

2. **Activate it:**
```bash
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install packages:**
```bash
pip install -r requirements.txt
```

4. **Run app:**
```bash
streamlit run app.py
```

---

## Using the App (Step by Step)

### Step 1️⃣ Upload Resume
- Click **"Upload & Parse"** tab
- Upload a resume (PDF, DOCX, or TXT)
- Click **"🔍 Parse Resume"**
- Review the parsed information

**Test:** Use included `sample_resume.txt`

### Step 2️⃣ Analyze
- Click **"Analysis Results"** tab
- Click **"🔬 Analyze Resume"**
- View scores and check if meets 80% threshold

### Step 3️⃣ (Optional) Interview Data
- Click **"Interview Data"** tab
- Toggle interview transcript, notes, or Q&A
- Add your data

### Step 4️⃣ Generate Report
- Click **"Generate Report"** tab
- Enter candidate name
- Click **"📄 Generate HTML Report"**
- Download or view in browser

---

## 📊 What Gets Scored

**10 Metrics evaluated:**
1. Sales Revenue Generation
2. Business Development
3. Account Management
4. Leadership Experience
5. Industry Expertise
6. Product & Technical Knowledge
7. Communication Skills
8. Negotiation & Deal Closing
9. Certifications
10. Analytics & Data-Driven

**Scoring:**
- **80%+**: ✅ Qualified
- **70-79%**: ⚠️ Developing
- **60-69%**: ⚠️ Significant Gaps
- **<60%**: ❌ Needs Work

---

## 🎯 Key Features

✅ Upload resumes in multiple formats (PDF, DOCX, TXT)
✅ AI-powered analysis against industry metrics
✅ Automatic 80% threshold evaluation
✅ Beautiful HTML reports (printable & downloadable)
✅ Interview data integration
✅ Job readiness assessment
✅ Strengths & gaps identification
✅ Development recommendations

---

## 📁 Generated Files

Reports saved in: `resume-analyzer/reports/`

Filename format: `resume_analysis_[name]_[timestamp].html`

---

## 🆘 Common Issues

**Issue: "ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**Issue: Port 8501 already in use**
```bash
streamlit run app.py --server.port 8502
```

**Issue: PDF won't parse**
- Try DOCX or TXT format instead
- Check PDF isn't corrupted

---

## 💡 Tips

- **First time?** Use `sample_resume.txt` to test
- **Multiple resumes?** Repeat steps 1-4 for each
- **Custom metrics?** Edit `metrics.py`
- **Change threshold?** Use sidebar slider in app

---

## 📖 Full Documentation

- **Setup**: See `SETUP_GUIDE.md`
- **Details**: See `README.md`
- **Metrics**: See `metrics.py`

---

**That's it! You're ready to analyze resumes! 🚀**

Need help? Check SETUP_GUIDE.md for troubleshooting.
