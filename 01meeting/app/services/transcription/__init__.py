"""Transcription service module."""

from .base import TranscriptionProvider, TranscriptSegment, TranscriptionResult
from .faster_whisper_provider import FastWhisperProvider

__all__ = [
    "TranscriptionProvider",
    "TranscriptSegment",
    "TranscriptionResult",
    "FastWhisperProvider",
]
