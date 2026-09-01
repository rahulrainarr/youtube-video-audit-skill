# 🎯 Sales & Business Development Resume Analyzer

Professional resume analysis tool designed specifically for evaluating Sales and Business Development candidates against industry standard metrics.

## 📋 Features

### Core Functionality
- **Resume Parsing**: Upload and parse resumes in PDF, DOCX, or TXT formats
- **AI-Powered Analysis**: Score resumes against 10 industry-specific metrics
- **80% Match Threshold**: Automatic evaluation of candidate qualification
- **Professional HTML Reports**: Beautiful, printable analysis reports
- **Multi-Input Assessment**: Integrate interview transcripts, notes, and query responses

### Evaluation Metrics (S&BD Specific)
1. **Sales Revenue Generation** (15% weight)
   - Demonstrates ability to generate revenue or close deals
   - 5+ years: 100pts, 3-4 years: 80pts, 1-2 years: 60pts

2. **Business Development** (12% weight)
   - New market identification and client acquisition
   - Strategic account development, market expansion

3. **Account Management** (12% weight)
   - Management and retention of existing accounts
   - Enterprise accounts, client retention, relationship management

4. **Leadership Experience** (10% weight)
   - Leading and managing sales/BD teams
   - 10+ direct reports: 100pts, 5-9: 85pts, 1-4: 70pts

5. **Industry Expertise** (10% weight)
   - Deep knowledge of target industry
   - 5+ years same industry: 100pts

6. **Product & Technical Knowledge** (8% weight)
   - SaaS, CRM, Salesforce, technical concepts
   - Advanced: 100pts, Intermediate: 80pts

7. **Communication Skills** (8% weight)
   - Ability to communicate and persuade effectively
   - Executive presentations, public speaking

8. **Negotiation & Deal Closing** (10% weight)
   - Strong negotiation and closing capabilities
   - Demonstrated closing experience

9. **Relevant Certifications** (7% weight)
   - Industry-recognized credentials
   - Multiple certifications: 100pts, Salesforce: 90pts

10. **Analytics & Data-Driven** (8% weight)
    - Using data and analytics for decision making
    - Dashboard reporting, metrics-driven approach

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Navigate to project directory**
```bash
cd "c:\02 Claude\02 Code\resume-analyzer"
```

2. **Create virtual environment** (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 How to Use

### Step 1: Upload Resume
1. Click "Upload Resume" tab
2. Select a resume file (PDF, DOCX, or TXT)
3. Click "🔍 Parse Resume"
4. Review parsed information (name, email, experience, education, skills)

### Step 2: Analyze Resume
1. Click "Analysis Results" tab
2. Click "🔬 Analyze Resume"
3. Review metrics scores and assessment
4. Check if candidate meets 80% threshold

### Step 3: (Optional) Add Interview Data
1. Click "Interview Data" tab
2. Toggle options for:
   - Interview Transcript
   - Interview Notes
   - Query Responses (Q&A)
3. Paste or enter data

### Step 4: Generate Report
1. Click "Generate Report" tab
2. Enter candidate name
3. Click "📄 Generate HTML Report"
4. Download or view report in browser

## 📊 Report Output

Generated HTML reports include:
- **Overall Assessment**: Score, match status, industry alignment
- **Detailed Metrics**: Individual scores for all 10 metrics
- **Strengths**: Key competencies identified
- **Development Areas**: Areas needing improvement
- **Recommendations**: Actionable development suggestions
- **Interview Integration**: Transcript, notes, Q&A responses
- **Professional Formatting**: Ready to print or share

## 🎯 Scoring Explanation

### Overall Score Calculation
- Weighted average of all 10 metrics
- Each metric has specific weight (sum = 100%)
- Scores range from 0-100%

### Match Threshold
- **80%+**: Qualified - Ready for advanced screening
- **70-79%**: Developing - Requires targeted development
- **60-69%**: Developing - Significant gaps
- **<60%**: Needs Work - Substantial preparation required

## 📁 File Structure

```
resume-analyzer/
├── app.py                  # Main Streamlit application
├── models.py              # Pydantic data models
├── metrics.py             # S&BD metric definitions
├── resume_parser.py       # Resume file parsing
├── analyzer.py            # Analysis engine
├── report_generator.py    # HTML report generation
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── reports/              # Generated report outputs (auto-created)
```

## 🔧 Customization

### Adjust Metric Weights
Edit `metrics.py` - Update weight values in `SALES_BD_METRICS` dictionary:
```python
"sales_revenue_generation": {
    "weight": 0.15,  # Change this value
    ...
}
```

### Change Threshold
In Streamlit app, use sidebar slider to adjust match threshold (default: 80%)

### Add New Metrics
1. Add metric definition to `SALES_BD_METRICS` in `metrics.py`
2. Add scoring method in `analyzer.py`
3. Metric will automatically appear in reports

## 🐛 Troubleshooting

### "File format not supported"
- Ensure file is PDF, DOCX, or TXT
- Try converting the file to a supported format

### "Resume parsed but no experience found"
- Resume format may not follow standard structure
- Try reformatting resume with clear "Experience" section header

### Report not generating
- Ensure all required fields are filled
- Check that candidate name is not empty
- Verify "reports" folder has write permissions

## 📝 Examples

### Sample Analysis Scores
**High Performer (85% overall)**
- Sales Revenue: 95%
- Leadership: 90%
- Account Management: 85%
- Business Development: 80%
- Status: ✅ MEETS THRESHOLD

**Developing Candidate (65% overall)**
- Sales Revenue: 70%
- Business Development: 60%
- Leadership: 45%
- Technical Knowledge: 55%
- Status: ⚠️ BELOW THRESHOLD - Needs Development

## 📞 Support & Contribution

For issues or feature requests:
1. Check the README first
2. Verify all inputs are correct
3. Review generated HTML for detailed insights

## 📄 License

Internal Use Only - Sales & Business Development Assessment Tool

## 🎓 Industry Standards Reference

Metrics are aligned with:
- Salesforce Certified Sales Cloud Consultant standards
- LinkedIn Sales Navigator best practices
- Gartner Sales Excellence frameworks
- Common sales industry benchmarks

## ✨ Version History

**v1.0** (Current)
- Initial release
- 10 core S&BD metrics
- PDF/DOCX/TXT support
- Interview data integration
- HTML report generation

---

**Built for accuracy and efficiency in Sales & Business Development talent assessment**
