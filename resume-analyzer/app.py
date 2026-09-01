"""
Resume Analysis App - Streamlit Web Interface
Main application for uploading and analyzing resumes
"""

import streamlit as st
import os
from pathlib import Path
from resume_parser import ResumeParser
from analyzer import ResumeAnalyzer
from report_generator import HTMLReportGenerator
from models import AnalysisReport
from datetime import datetime


# Page config
st.set_page_config(
    page_title="Resume Analysis - S&BD",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 0;
    }
    .css-1d391kg {
        padding-top: 2rem;
    }
    h1 {
        color: #667eea;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 4px solid #667eea;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'parsed_resume' not in st.session_state:
        st.session_state.parsed_resume = None
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'report' not in st.session_state:
        st.session_state.report = None


def main():
    initialize_session_state()

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🎯 Sales & Business Development Resume Analyzer")
    with col2:
        st.caption("Powered by AI Analysis")

    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("📋 Analysis Settings")

        analysis_mode = st.radio(
            "Select Analysis Mode:",
            ["Resume Only", "Resume + Interview", "Resume + Query Responses", "Complete Assessment"]
        )

        st.markdown("---")
        st.subheader("Threshold Settings")
        match_threshold = st.slider(
            "Match Threshold (%)",
            min_value=50,
            max_value=100,
            value=80,
            step=5,
            help="Minimum score for candidate to be considered as matched"
        )

        st.markdown("---")
        st.subheader("About This Tool")
        st.info("""
        **Features:**
        - Parse resumes (PDF, DOCX, TXT)
        - Score against S&BD metrics
        - Generate detailed HTML reports
        - Integrate interview data
        - Assess job readiness

        **Metrics Evaluated:**
        - Sales Revenue Generation
        - Business Development
        - Account Management
        - Leadership Experience
        - Industry Expertise
        - Technical Knowledge
        - Communication Skills
        - Negotiation Skills
        - Certifications
        - Analytics & Data-Driven
        """)

    # Main content area
    tabs = st.tabs(["📤 Upload & Parse", "📊 Analysis Results", "📋 Interview Data", "📄 Generate Report"])

    # Tab 1: Upload and Parse
    with tabs[0]:
        st.header("Step 1: Upload Resume")

        col1, col2 = st.columns([2, 1])

        with col1:
            uploaded_file = st.file_uploader(
                "Choose a resume file",
                type=['pdf', 'docx', 'doc', 'txt'],
                help="Supported formats: PDF, DOCX, TXT"
            )

        with col2:
            parse_button = st.button("🔍 Parse Resume", use_container_width=True)

        if parse_button and uploaded_file:
            with st.spinner("Parsing resume..."):
                # Save uploaded file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())

                # Parse resume
                parser = ResumeParser()
                resume_data = parser.parse_file(temp_path)

                if resume_data:
                    st.session_state.parsed_resume = resume_data
                    st.success("✅ Resume parsed successfully!")

                    # Display parsed information
                    st.subheader("📋 Parsed Information")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Name", resume_data.name)
                    with col2:
                        st.metric("Email", resume_data.email)
                    with col3:
                        st.metric("Phone", resume_data.phone or "Not found")

                    # Professional Summary
                    with st.expander("Professional Summary", expanded=True):
                        st.write(resume_data.professional_summary)

                    # Experience
                    with st.expander("Work Experience", expanded=True):
                        for i, exp in enumerate(resume_data.experiences, 1):
                            st.write(f"**{i}. {exp.position} at {exp.company}**")
                            st.caption(f"Duration: {exp.duration_years} years")
                            if exp.key_achievements:
                                st.write("Key Achievements:")
                                for achievement in exp.key_achievements[:3]:
                                    st.write(f"- {achievement}")

                    # Education
                    with st.expander("Education", expanded=False):
                        for edu in resume_data.education:
                            st.write(f"**{edu.degree} in {edu.field}**")
                            st.caption(edu.institution)

                    # Skills
                    if resume_data.skills:
                        with st.expander("Skills", expanded=False):
                            cols = st.columns(3)
                            for i, skill in enumerate(resume_data.skills):
                                with cols[i % 3]:
                                    st.write(f"• {skill}")

                    # Certifications
                    if resume_data.certifications:
                        with st.expander("Certifications", expanded=False):
                            for cert in resume_data.certifications:
                                st.write(f"✓ {cert}")

                # Clean up temp file
                os.remove(temp_path)
                else:
                    st.error("❌ Error parsing resume. Please check the file format.")

        # Display stored resume if available
        if st.session_state.parsed_resume and not parse_button:
            st.info(f"Resume loaded: {st.session_state.parsed_resume.name}")

    # Tab 2: Analysis Results
    with tabs[1]:
        st.header("Step 2: Resume Analysis")

        if st.session_state.parsed_resume:
            analyze_button = st.button("🔬 Analyze Resume", use_container_width=True)

            if analyze_button:
                with st.spinner("Analyzing resume against S&BD metrics..."):
                    analyzer = ResumeAnalyzer()
                    analysis = analyzer.analyze(st.session_state.parsed_resume)
                    st.session_state.analysis_result = analysis

                    st.success("✅ Analysis complete!")

            if st.session_state.analysis_result:
                analysis = st.session_state.analysis_result

                # Overall Score
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Overall Score", f"{analysis.overall_score:.1f}%")

                with col2:
                    st.metric("Match Score", f"{analysis.match_percentage:.1f}%")

                with col3:
                    threshold_status = "✅ PASS" if analysis.matched else "❌ FAIL"
                    st.metric("80% Threshold", threshold_status)

                with col4:
                    st.metric("Industry Alignment", analysis.industry_alignment)

                st.markdown("---")

                # Match Decision Box
                if analysis.matched:
                    st.success(f"🎯 **QUALIFIED** - Score of {analysis.overall_score:.1f}% meets the 80% threshold")
                else:
                    st.warning(f"⚠️ **BELOW THRESHOLD** - Score of {analysis.overall_score:.1f}% is below 80% requirement")

                # Job Readiness
                st.info(f"**Job Readiness:** {analysis.job_readiness}")

                st.markdown("---")

                # Detailed Metrics
                st.subheader("📊 Detailed Metric Scores")

                cols = st.columns(2)
                for idx, (metric_name, score) in enumerate(analysis.metric_scores.items()):
                    with cols[idx % 2]:
                        formatted_name = metric_name.replace("_", " ").title()
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.progress(score / 100)
                            st.caption(formatted_name)
                        with col_b:
                            st.metric("Score", f"{score:.0f}%")

                st.markdown("---")

                # Strengths
                st.subheader("💪 Key Strengths")
                for strength in analysis.strengths:
                    st.success(strength)

                st.markdown("---")

                # Development Areas
                st.subheader("🎯 Development Areas")
                for gap in analysis.gaps:
                    st.warning(gap)

                st.markdown("---")

                # Recommendations
                st.subheader("💡 Recommendations")
                for i, rec in enumerate(analysis.recommendations, 1):
                    st.info(f"{i}. {rec}")

        else:
            st.warning("⚠️ Please upload and parse a resume first (Step 1)")

    # Tab 3: Interview Data
    with tabs[2]:
        st.header("Step 3: Add Interview Data (Optional)")

        col_toggle1, col_toggle2, col_toggle3 = st.columns(3)

        include_transcript = col_toggle1.checkbox("Include Interview Transcript", False)
        include_notes = col_toggle2.checkbox("Include Interview Notes", False)
        include_responses = col_toggle3.checkbox("Include Query Responses", False)

        interview_transcript = None
        interview_notes = None
        query_responses = None

        if include_transcript:
            st.subheader("Interview Transcript")
            interview_transcript = st.text_area(
                "Paste interview transcript:",
                height=200,
                label_visibility="collapsed"
            )

        if include_notes:
            st.subheader("Interview Notes")
            interview_notes = st.text_area(
                "Paste interview notes:",
                height=200,
                label_visibility="collapsed"
            )

        if include_responses:
            st.subheader("Query Responses")
            num_questions = st.slider("Number of questions:", 1, 10, 3)

            query_responses = {}
            for i in range(num_questions):
                question = st.text_input(f"Question {i+1}:")
                response = st.text_area(f"Response {i+1}:", height=100, key=f"response_{i}")
                if question and response:
                    query_responses[question] = response

        # Store in session
        st.session_state.interview_data = {
            'transcript': interview_transcript,
            'notes': interview_notes,
            'responses': query_responses
        }

        st.info("📌 Interview data will be included in the final report if provided.")

    # Tab 4: Generate Report
    with tabs[3]:
        st.header("Step 4: Generate Report")

        if st.session_state.analysis_result:
            col1, col2 = st.columns([2, 1])

            with col1:
                candidate_name = st.text_input(
                    "Candidate Name (for report):",
                    value=st.session_state.parsed_resume.name if st.session_state.parsed_resume else ""
                )

            with col2:
                st.write("")  # Spacing

            generate_report_button = st.button("📄 Generate HTML Report", use_container_width=True)

            if generate_report_button:
                with st.spinner("Generating report..."):
                    # Create analysis report
                    interview_data = st.session_state.get('interview_data', {})

                    report = AnalysisReport(
                        resume_name=st.session_state.parsed_resume.name,
                        candidate_name=candidate_name,
                        analysis=st.session_state.analysis_result,
                        interview_transcript=interview_data.get('transcript'),
                        interview_notes=interview_data.get('notes'),
                        query_responses=interview_data.get('responses')
                    )

                    # Generate HTML
                    generator = HTMLReportGenerator()
                    html_content = generator.generate_report(report)

                    # Create output directory
                    output_dir = "reports"
                    os.makedirs(output_dir, exist_ok=True)

                    # Save report
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = f"{output_dir}/resume_analysis_{candidate_name.replace(' ', '_')}_{timestamp}.html"

                    if generator.save_report(html_content, output_path):
                        st.success(f"✅ Report generated successfully!")
                        st.info(f"📁 Saved to: `{output_path}`")

                        # Provide download button
                        st.download_button(
                            label="⬇️ Download HTML Report",
                            data=html_content,
                            file_name=f"resume_analysis_{candidate_name.replace(' ', '_')}.html",
                            mime="text/html"
                        )

                        # Display report preview
                        st.subheader("📋 Report Preview")
                        st.components.v1.html(html_content, height=1200, scrolling=True)

                    else:
                        st.error("❌ Error generating report.")

        else:
            st.warning("⚠️ Please complete analysis first (Step 2)")

    st.markdown("---")
    st.caption("Sales & Business Development Resume Analyzer v1.0")


if __name__ == "__main__":
    main()
