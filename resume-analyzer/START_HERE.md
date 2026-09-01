# 🎯 START HERE - Resume Analyzer Setup

Welcome! This guide will get you up and running in **5 minutes**.

---

## ✅ What You Have

A complete, production-ready **Sales & Business Development Resume Analyzer** with:
- ✅ AI-powered resume parsing (PDF, DOCX, TXT)
- ✅ 10 industry-standard evaluation metrics
- ✅ Automatic 80% match threshold
- ✅ Beautiful HTML report generation
- ✅ Interview data integration
- ✅ Professional web interface

---

## 🚀 Launch in 5 Minutes

### Option 1: Windows (Recommended)
```powershell
# Open PowerShell in this folder and run:
.\run.ps1
```

### Option 2: macOS/Linux
```bash
# Open Terminal in this folder and run:
bash run.sh
```

### Option 3: Manual (Any OS)
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows CMD)
venv\Scripts\activate
# OR (Windows PowerShell)
venv\Scripts\Activate.ps1
# OR (macOS/Linux)
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Run app
streamlit run app.py
```

### Browser Opens
App runs at: **http://localhost:8501**

---

## 📖 Documentation Files

### 👈 If You Want...

**To get started immediately**
→ You're reading it! Just run above ✓

**A 5-minute quick start**
→ See `QUICK_START.md`

**Complete setup help & troubleshooting**
→ See `SETUP_GUIDE.md`

**Full feature documentation**
→ See `README.md`

**Metric scoring details**
→ See `METRICS_REFERENCE.md`

**Project overview**
→ See `PROJECT_SUMMARY.md`

---

## 🎯 Using the App (Simple!)

### Step 1: Upload Resume
- Click "📤 Upload & Parse" tab
- Upload a resume (PDF/DOCX/TXT)
- Click "🔍 Parse Resume"
- Review parsed data

**First Time?** Use `sample_resume.txt` in this folder

### Step 2: Analyze
- Click "📊 Analysis Results" tab
- Click "🔬 Analyze Resume"
- View scores (80%+ = qualified)

### Step 3: (Optional) Add Interview Data
- Click "📋 Interview Data" tab
- Toggle what you want to include
- Paste interview transcript, notes, or Q&A

### Step 4: Generate Report
- Click "📄 Generate Report" tab
- Enter candidate name
- Click "📄 Generate HTML Report"
- Download or view in browser

---

## 📊 What Gets Evaluated

**10 Metrics** aligned with Sales & Business Development industry standards:

| Metric | Weight |
|--------|--------|
| Sales Revenue Generation | 15% |
| Business Development | 12% |
| Account Management | 12% |
| Leadership Experience | 10% |
| Industry Expertise | 10% |
| Technical Knowledge | 8% |
| Communication Skills | 8% |
| Negotiation & Deal Closing | 10% |
| Certifications | 7% |
| Analytics & Data-Driven | 8% |

**Scoring:** 80-100% ✅ Qualified | 70-79% ⚠️ Developing | <70% ❌ Needs Work

---

## 🗂️ What's Included

```
resume-analyzer/
├── 📄 Core Python Files (don't need to edit)
│   ├── app.py              → Web interface
│   ├── models.py           → Data structures
│   ├── resume_parser.py    → Resume parsing
│   ├── analyzer.py         → Scoring engine
│   ├── metrics.py          → Metric definitions
│   └── report_generator.py → Report creation
│
├── 📖 Documentation (read these!)
│   ├── START_HERE.md           → You're here
│   ├── QUICK_START.md          → 5-min guide
│   ├── SETUP_GUIDE.md          → Detailed setup
│   ├── README.md               → Features
│   ├── METRICS_REFERENCE.md    → Scoring details
│   └── PROJECT_SUMMARY.md      → Overview
│
├── 🚀 Startup Scripts
│   ├── run.ps1  → Windows launcher
│   └── run.sh   → macOS/Linux launcher
│
├── 📋 Test Data
│   └── sample_resume.txt   → Test resume
│
├── 📦 Dependencies
│   └── requirements.txt     → Python packages
│
└── 📁 reports/  → Generated reports (auto-created)
```

---

## ❓ Common Questions

**Q: How do I start?**
A: Run `.\run.ps1` (Windows) or `bash run.sh` (macOS/Linux)

**Q: Do I need to install anything else?**
A: No. Python 3.8+ is all you need. Everything else auto-installs.

**Q: Can I test with a sample?**
A: Yes! Use `sample_resume.txt` in first run.

**Q: Where do reports save?**
A: In `reports/` folder (auto-created)

**Q: Can I customize the metrics?**
A: Yes! Edit `metrics.py` to adjust weights.

**Q: Is my data safe?**
A: Yes! Everything processes locally. No cloud uploads.

---

## 🔧 Troubleshooting

### Python Not Found?
- Install from https://www.python.org
- Make sure to check "Add to PATH"

### Module Error?
```bash
pip install -r requirements.txt
```

### PDF Won't Parse?
Try DOCX or TXT format instead

### Port Already in Use?
```bash
streamlit run app.py --server.port 8502
```

**More help?** See `SETUP_GUIDE.md` → Troubleshooting section

---

## 📞 Need Help?

| Question | See File |
|----------|----------|
| How do I set it up? | SETUP_GUIDE.md |
| What features does it have? | README.md |
| How are metrics scored? | METRICS_REFERENCE.md |
| What's in this project? | PROJECT_SUMMARY.md |
| Quick start guide? | QUICK_START.md |

---

## 🎯 You're Ready!

### Run the app now:

**Windows:**
```powershell
.\run.ps1
```

**macOS/Linux:**
```bash
bash run.sh
```

Then open: **http://localhost:8501**

---

## 💡 Pro Tips

1. **Test first** - Use `sample_resume.txt` before uploading your own
2. **Read metrics** - Check `METRICS_REFERENCE.md` to understand scoring
3. **Customize** - Edit `metrics.py` to adjust for your organization
4. **Share reports** - Download HTML files and send to team

---

## 📋 Checklist

- [ ] Extracted resume-analyzer folder
- [ ] Read this file (START_HERE.md)
- [ ] Ran `.\run.ps1` or `bash run.sh`
- [ ] Opened http://localhost:8501 in browser
- [ ] Tested with `sample_resume.txt`
- [ ] Understood the 10 metrics
- [ ] Generated a report
- [ ] Read `README.md` for full features

---

## 🎓 Next Steps

**Beginner:**
1. Run the app
2. Test with sample_resume.txt
3. Generate a report
4. Review output

**Intermediate:**
1. Analyze your actual resumes
2. Adjust match threshold
3. Add interview data
4. Share reports with team

**Advanced:**
1. Customize metrics in metrics.py
2. Modify scoring logic in analyzer.py
3. Change report styling in report_generator.py
4. Integrate with your HR system

---

## 🎉 That's It!

Everything is ready to use. No additional setup needed.

**Start now:** `.\run.ps1` (Windows) or `bash run.sh` (macOS/Linux)

---

*Sales & Business Development Resume Analyzer*
*v1.0 - Ready for Production*
