"""
Meeting Intelligence Assistant - Streamlit Frontend

Main entry point for the Streamlit UI.
"""

import streamlit as st
import os
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Meeting Intelligence Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling
st.markdown("""
<style>
    .main-title {
        color: #1E3A8A;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #64748B;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'api_url' not in st.session_state:
    st.session_state.api_url = 'http://localhost:8000'

# Sidebar Navigation
with st.sidebar:
    st.markdown("# Navigation")

    pages = {
        "🏠 Home": "home",
        "📤 Upload Meeting": "upload",
        "📋 Meeting History": "history",
        "📝 Transcript": "transcript",
        "📊 Analysis": "analysis",
        "📄 Reports": "reports",
        "⚙️ Settings": "settings",
    }

    for label, page in pages.items():
        if st.button(label, key=f"nav_{page}", use_container_width=True):
            st.session_state.page = page

    st.divider()

    # API Status
    st.markdown("### API Status")
    try:
        import requests
        response = requests.get(f"{st.session_state.api_url}/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ Backend Online")
        else:
            st.warning("⚠️ Backend Error")
    except:
        st.error("❌ Backend Offline")

    st.markdown("### About")
    st.markdown("""
    **Meeting Intelligence Assistant** v1.0.0

    Convert meetings into actionable intelligence.
    """)

# Main Content
if st.session_state.page == 'home':
    st.markdown('<div class="main-title">📊 Meeting Intelligence Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Convert meetings into actionable intelligence</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Meetings", "0", help="Meetings processed in the system")

    with col2:
        st.metric("Total Hours", "0.0", help="Total meeting duration processed")

    with col3:
        st.metric("Open Actions", "0", help="Active action items")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Quick Start")
        st.info("""
        1. **Upload** a Teams recording or transcript
        2. **Review** the transcript and correct speakers
        3. **Analyze** the meeting to extract intelligence
        4. **Export** a professional report
        """)

    with col2:
        st.markdown("### Supported Formats")
        st.info("""
        **Audio**: MP3, WAV, M4A, AAC, FLAC, OGG

        **Video**: MP4, MOV, MKV, WEBM, AVI

        **Transcripts**: VTT, SRT, TXT, DOCX
        """)

elif st.session_state.page == 'upload':
    st.markdown("## 📤 Upload Meeting")

    st.info("""
    Upload a meeting recording or transcript.
    Supported formats: MP3, WAV, MP4, MOV, VTT, DOCX
    """)

    tab1, tab2 = st.tabs(["Upload File", "Import from Teams"])

    with tab1:
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["mp3", "wav", "m4a", "aac", "flac", "ogg",
                  "mp4", "mov", "mkv", "webm", "avi", "flv",
                  "vtt", "srt", "txt", "docx"],
            help="Maximum 5 GB"
        )

        meeting_title = st.text_input("Meeting Title", placeholder="Q3 Planning Meeting")
        meeting_date = st.date_input("Meeting Date", help="When did the meeting occur?")
        is_confidential = st.checkbox("Mark as Confidential")

        if st.button("Upload & Process"):
            if uploaded_file and meeting_title:
                st.success("✅ File uploaded successfully!")
                st.info("Processing started. Check the Status page for progress.")
            else:
                st.error("Please provide a file and meeting title.")

    with tab2:
        st.markdown("### Connect Microsoft Teams")
        st.info("Teams integration coming in v1.1")
        if st.button("Setup Teams Integration"):
            st.info("See Settings for Teams configuration")

elif st.session_state.page == 'history':
    st.markdown("## 📋 Meeting History")

    # Placeholder for meeting list
    st.info("No meetings processed yet. Upload a meeting to get started.")

elif st.session_state.page == 'transcript':
    st.markdown("## 📝 Transcript Editor")

    st.info("Select a meeting from History to view and edit its transcript.")

elif st.session_state.page == 'analysis':
    st.markdown("## 📊 Meeting Analysis")

    st.info("Analysis results will appear here once a meeting is processed.")

elif st.session_state.page == 'reports':
    st.markdown("## 📄 Reports & Exports")

    st.info("Generated reports will be available for download here.")

elif st.session_state.page == 'settings':
    st.markdown("## ⚙️ Settings")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Transcription",
        "LLM Provider",
        "Teams",
        "Storage"
    ])

    with tab1:
        st.markdown("### Transcription Settings")
        provider = st.selectbox(
            "Transcription Provider",
            ["faster_whisper (Local)", "openai (Cloud)"]
        )

        if "Local" in provider:
            model = st.selectbox("Model Size", ["tiny", "base", "small", "medium", "large"])
            device = st.selectbox("Processing Device", ["auto", "cpu", "gpu"])

        enable_diarization = st.checkbox("Enable Speaker Diarization", value=True)

    with tab2:
        st.markdown("### LLM Provider Settings")
        llm_provider = st.selectbox(
            "LLM Provider",
            ["Claude (Anthropic)", "OpenAI", "OpenAI-compatible"]
        )

        if "Claude" in llm_provider:
            st.text_input("Claude API Key", type="password", help="Your Anthropic API key")
            st.selectbox("Model", ["claude-3-5-sonnet", "claude-3-haiku"])

    with tab3:
        st.markdown("### Microsoft Teams Integration")
        st.info("Teams integration coming in v1.1")
        teams_enabled = st.checkbox("Enable Teams Integration", value=False)

    with tab4:
        st.markdown("### Data Storage")
        retention_days = st.number_input(
            "Data Retention (days)",
            min_value=1,
            max_value=365,
            value=90
        )

        auto_cleanup = st.checkbox("Auto Cleanup Expired Data", value=True)

        if st.button("Save Settings"):
            st.success("✅ Settings saved")

# Footer
st.divider()
st.markdown("""
---
**Meeting Intelligence Assistant** | [Documentation](https://github.com) | [Report Issue](https://github.com/issues)

Built with FastAPI, SQLAlchemy, and Streamlit
""", unsafe_allow_html=True)
