"""Base transcription provider interface."""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from pydantic import BaseModel
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class TranscriptSegment:
    """A segment of transcript with speaker and timestamp info."""

    index: int
    start_time: float
    end_time: float
    text: str
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    language: str = "en"


@dataclass
class TranscriptionResult:
    """Result of transcription."""

    segments: List[TranscriptSegment]
    language: str
    duration_seconds: float
    success: bool
    error: Optional[str] = None


class TranscriptionProvider(ABC):
    """Base class for transcription providers."""

    @abstractmethod
    async def transcribe(self, audio_path: str) -> TranscriptionResult:
        """
        Transcribe audio file.

        Args:
            audio_path: Path to audio file

        Returns:
            TranscriptionResult with segments and metadata
        """
        pass

    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Get list of supported audio formats."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available/configured."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get provider name."""
        pass

    @abstractmethod
    def get_language(self) -> str:
        """Get configured language."""
        pass

    @abstractmethod
    def detect_language(self, audio_path: str) -> str:
        """Detect language from audio."""
        pass

    def merge_segments(self, segments: List[TranscriptSegment]) -> TranscriptSegment:
        """Merge multiple segments into one."""
        if not segments:
            return None

        merged_text = " ".join(seg.text for seg in segments)
        merged_confidence = (
            sum(seg.confidence for seg in segments if seg.confidence) / len(segments)
            if any(seg.confidence for seg in segments)
            else None
        )

        return TranscriptSegment(
            index=segments[0].index,
            start_time=segments[0].start_time,
            end_time=segments[-1].end_time,
            text=merged_text,
            speaker=segments[0].speaker,
            confidence=merged_confidence,
            language=segments[0].language,
        )

    @staticmethod
    def format_timestamp(seconds: float) -> str:
        """Format timestamp in HH:MM:SS format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
