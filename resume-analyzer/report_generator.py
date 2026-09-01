"""
Report Generator - Create professional HTML reports
"""

from datetime import datetime
from typing import Dict, List, Optional
from models import AnalysisReport, ResumeAnalysis


class HTMLReportGenerator:
    def __init__(self):
        self.template_path = None

    def generate_report(self, analysis_report: AnalysisReport) -> str:
        """Generate HTML report"""
        analysis = analysis_report.analysis

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Analysis Report - {analysis.resume_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}

        .header p {{
            font-size: 14px;
            opacity: 0.9;
        }}

        .content {{
            padding: 40px;
        }}

        .section {{
            margin-bottom: 40px;
        }}

        .section h2 {{
            font-size: 20px;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}

        .score-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}

        .score-item {{
            text-align: center;
        }}

        .score-value {{
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .score-label {{
            font-size: 14px;
            opacity: 0.9;
        }}

        .match-indicator {{
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-weight: bold;
            text-align: center;
        }}

        .match-yes {{
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}

        .match-no {{
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }}

        .metric-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}

        .metric-name {{
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 8px;
            color: #333;
        }}

        .metric-score {{
            font-size: 24px;
            color: #667eea;
            font-weight: bold;
        }}

        .progress-bar {{
            width: 100%;
            height: 8px;
            background-color: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 8px;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
        }}

        .list-section {{
            margin-bottom: 20px;
        }}

        .list-section h3 {{
            font-size: 16px;
            color: #333;
            margin-bottom: 12px;
            font-weight: 600;
        }}

        .list-item {{
            background: #f8f9fa;
            padding: 12px 15px;
            margin-bottom: 8px;
            border-radius: 6px;
            border-left: 3px solid #667eea;
            font-size: 14px;
        }}

        .strength {{
            border-left-color: #28a745;
            background-color: #f0f9f5;
        }}

        .gap {{
            border-left-color: #dc3545;
            background-color: #fdf5f6;
        }}

        .recommendation {{
            border-left-color: #ffc107;
            background-color: #fffbf0;
        }}

        .interview-section {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}

        .interview-section h3 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 16px;
        }}

        .transcript {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            font-size: 14px;
            line-height: 1.6;
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #e9ecef;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #666;
            border-top: 1px solid #e9ecef;
        }}

        .badge {{
            display: inline-block;
            padding: 5px 12px;
            background-color: #667eea;
            color: white;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 5px;
            margin-bottom: 5px;
        }}

        .summary-box {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }}

        .summary-box p {{
            line-height: 1.6;
            margin-bottom: 10px;
        }}

        @media print {{
            body {{
                background: white;
            }}
            .container {{
                box-shadow: none;
                max-width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Resume Analysis Report</h1>
            <p>Sales & Business Development Profile Assessment</p>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
        </div>

        <div class="content">
            <!-- Candidate Information -->
            <div class="section">
                <h2>Candidate Information</h2>
                <div class="summary-box">
                    <p><strong>Name:</strong> {analysis_report.candidate_name}</p>
                    <p><strong>Resume:</strong> {analysis.resume_name}</p>
                    <p><strong>Assessment Type:</strong> Sales & Business Development Role</p>
                </div>
            </div>

            <!-- Overall Score -->
            <div class="section">
                <h2>Overall Assessment</h2>
                <div class="score-card">
                    <div class="score-item">
                        <div class="score-value">{analysis.overall_score:.1f}%</div>
                        <div class="score-label">Overall Score</div>
                    </div>
                    <div class="score-item">
                        <div class="score-value">{analysis.match_percentage:.1f}%</div>
                        <div class="score-label">Match Percentage</div>
                    </div>
                </div>

                <div class="match-indicator {'match-yes' if analysis.matched else 'match-no'}">
                    {'✓ MEETS 80% THRESHOLD - Ready for Advanced Screening' if analysis.matched else '✗ BELOW 80% THRESHOLD - Requires Development'}
                </div>

                <div class="summary-box">
                    <p><strong>Industry Alignment:</strong> <span class="badge">{analysis.industry_alignment}</span></p>
                    <p><strong>Job Readiness:</strong> {analysis.job_readiness}</p>
                </div>
            </div>

            <!-- Metric Scores -->
            <div class="section">
                <h2>Detailed Metric Scores</h2>
                <div class="metrics-grid">
{self._generate_metrics_html(analysis.metric_scores)}
                </div>
            </div>

            <!-- Strengths -->
            <div class="section">
                <h2>Key Strengths</h2>
                <div class="list-section">
{self._generate_list_items(analysis.strengths, 'strength')}
                </div>
            </div>

            <!-- Gaps & Development Areas -->
            <div class="section">
                <h2>Development Areas</h2>
                <div class="list-section">
{self._generate_list_items(analysis.gaps, 'gap')}
                </div>
            </div>

            <!-- Recommendations -->
            <div class="section">
                <h2>Recommendations for Development</h2>
                <div class="list-section">
{self._generate_list_items(analysis.recommendations, 'recommendation')}
                </div>
            </div>

{self._generate_interview_section(analysis_report)}

            <!-- Interview Response Summary -->
{self._generate_combined_assessment(analysis_report)}

        </div>

        <div class="footer">
            <p>This report is confidential and intended for authorized use only.</p>
            <p>For questions, contact the HR Department.</p>
            <p>© 2024 Sales & Business Development Talent Assessment</p>
        </div>
    </div>
</body>
</html>
"""
        return html

    def _generate_metrics_html(self, metric_scores: Dict[str, float]) -> str:
        """Generate HTML for metric scores"""
        html = ""
        for metric_name, score in metric_scores.items():
            # Format metric name
            formatted_name = metric_name.replace("_", " ").title()
            progress_width = score

            html += f"""
                <div class="metric-item">
                    <div class="metric-name">{formatted_name}</div>
                    <div class="metric-score">{score:.0f}%</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {progress_width}%"></div>
                    </div>
                </div>
"""
        return html

    def _generate_list_items(self, items: List[str], item_class: str) -> str:
        """Generate HTML for list items"""
        html = ""
        for item in items:
            html += f'<div class="list-item {item_class}">{item}</div>\n'
        return html

    def _generate_interview_section(self, report: AnalysisReport) -> str:
        """Generate interview section if data exists"""
        if not report.interview_transcript and not report.interview_notes:
            return ""

        html = """
            <!-- Interview Data -->
            <div class="section">
                <h2>Interview Information</h2>
"""

        if report.interview_transcript:
            html += f"""
                <div class="interview-section">
                    <h3>Interview Transcript</h3>
                    <div class="transcript">{report.interview_transcript}</div>
                </div>
"""

        if report.interview_notes:
            html += f"""
                <div class="interview-section">
                    <h3>Interview Notes</h3>
                    <div class="transcript">{report.interview_notes}</div>
                </div>
"""

        html += """
            </div>
"""
        return html

    def _generate_combined_assessment(self, report: AnalysisReport) -> str:
        """Generate combined assessment section"""
        if not report.query_responses and not report.combined_assessment:
            return ""

        html = """
            <!-- Combined Assessment -->
            <div class="section">
                <h2>Integrated Assessment</h2>
"""

        if report.query_responses:
            html += """
                <div class="interview-section">
                    <h3>Response Analysis</h3>
"""
            for question, response in report.query_responses.items():
                html += f"""
                    <div style="margin-bottom: 15px;">
                        <strong>{question}</strong>
                        <p style="margin-top: 5px; font-size: 14px;">{response}</p>
                    </div>
"""
            html += """
                </div>
"""

        if report.combined_assessment:
            html += f"""
                <div class="summary-box">
                    <h3 style="margin-bottom: 10px;">Overall Combined Assessment</h3>
                    <p>{report.combined_assessment}</p>
                </div>
"""

        html += """
            </div>
"""
        return html

    def save_report(self, html_content: str, output_path: str) -> bool:
        """Save HTML report to file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return True
        except Exception as e:
            print(f"Error saving report: {e}")
            return False
