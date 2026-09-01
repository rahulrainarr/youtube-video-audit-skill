from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    # Application
    app_name: str = "Meeting Intelligence Assistant"
    app_env: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    # Database
    database_url: str = "sqlite:///./data/mia.db"
    database_echo: bool = False

    # Transcription
    transcription_provider: str = "faster_whisper"  # faster_whisper, openai
    transcription_model: str = "base"
    transcription_language: str = "en"
    transcription_device: str = "auto"  # auto, cpu, gpu, cuda, mps
    transcription_compute_type: str = "default"  # default, float16, int8
    enable_diarization: bool = True
    diarization_min_speakers: int = 1
    diarization_max_speakers: int = 10

    # Local Transcription (faster-whisper)
    whisper_model_cache: str = "./data/models"
    whisper_enable_quantization: bool = False

    # Cloud Transcription (OpenAI)
    openai_api_key: Optional[str] = None
    openai_api_base: str = "https://api.openai.com/v1"
    openai_whisper_model: str = "whisper-1"

    # LLM Provider
    llm_provider: str = "claude"  # claude, openai, openai_compatible
    llm_model: str = "claude-3-5-sonnet-20241022"

    # Claude API
    anthropic_api_key: Optional[str] = None
    anthropic_api_base: str = "https://api.anthropic.com"

    # OpenAI Compatible LLM
    openai_llm_api_key: Optional[str] = None
    openai_llm_api_base: str = "http://localhost:8000/v1"
    openai_llm_model: str = "gpt-3.5-turbo"

    # Microsoft Teams
    teams_enabled: bool = False
    teams_client_id: Optional[str] = None
    teams_client_secret: Optional[str] = None
    teams_tenant_id: Optional[str] = None
    teams_redirect_uri: str = "http://localhost:8501/callback"

    # File Upload
    max_upload_size_mb: int = 5000
    allowed_audio_formats: str = "wav,mp3,m4a,aac,flac,ogg"
    allowed_video_formats: str = "mp4,mov,mkv,webm,avi,flv"
    allowed_transcript_formats: str = "vtt,srt,txt,docx"
    temp_dir: str = "./data/temp"

    # Data Retention
    data_retention_days: int = 90
    enable_soft_delete: bool = True
    auto_cleanup_enabled: bool = True

    # API Settings
    api_port: int = 8000
    api_host: str = "0.0.0.0"
    cors_origins: str = "http://localhost:8501,http://localhost:3000"

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    encrypt_sensitive_data: bool = True
    audit_logging_enabled: bool = True

    # Processing
    max_concurrent_jobs: int = 2
    chunk_size_minutes: int = 15
    chunk_overlap_seconds: int = 10
    token_limit_per_chunk: int = 6000

    # Feature Flags
    feature_teams_graph_integration: bool = False
    feature_microphone_recording: bool = False
    feature_local_only_mode: bool = True

    # Logging
    log_file: str = "./logs/mia.log"
    log_file_size_mb: int = 100
    log_backup_count: int = 5

    # Performance
    enable_caching: bool = True
    cache_ttl_hours: int = 24
    use_gpu_if_available: bool = True

    # Reporting
    default_report_format: str = "docx"
    enable_pdf_export: bool = True
    enable_email_summary: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def get_allowed_audio_formats(self) -> List[str]:
        return self.allowed_audio_formats.split(",")

    @property
    def get_allowed_video_formats(self) -> List[str]:
        return self.allowed_video_formats.split(",")

    @property
    def get_allowed_transcript_formats(self) -> List[str]:
        return self.allowed_transcript_formats.split(",")

    @property
    def get_cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()
