"""Faster-Whisper transcription provider."""

import logging
import os
from typing import List, Optional
import asyncio

from app.core import settings
from .base import TranscriptionProvider, TranscriptSegment, TranscriptionResult

logger = logging.getLogger(__name__)


class FastWhisperProvider(TranscriptionProvider):
    """Local transcription using faster-whisper."""

    SUPPORTED_FORMATS = ["wav", "mp3", "m4a", "aac", "flac", "ogg", "wma"]
    MODEL_SIZES = ["tiny", "base", "small", "medium", "large"]

    def __init__(self):
        """Initialize Faster-Whisper provider."""
        self.model = None
        self.model_size = settings.transcription_model
        self.language = settings.transcription_language
        self.device = self._get_device()
        self.compute_type = settings.transcription_compute_type
        self._initialize_model()

    def _get_device(self) -> str:
        """Detect and return appropriate device."""
        device = settings.transcription_device.lower()

        if device == "auto":
            # Try to auto-detect CUDA
            try:
                import torch
                return "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                return "cpu"

        valid_devices = ["cpu", "cuda", "gpu", "mps"]
        if device not in valid_devices:
            logger.warning(f"Unknown device {device}, using CPU")
            return "cpu"

        return device

    def _initialize_model(self):
        """Initialize the Whisper model."""
        try:
            from faster_whisper import WhisperModel

            logger.info(
                f"Loading Faster-Whisper model: {self.model_size} "
                f"(device: {self.device}, compute_type: {self.compute_type})"
            )

            # Ensure model cache directory exists
            model_cache = settings.whisper_model_cache
            os.makedirs(model_cache, exist_ok=True)

            # Load model
            self.model = WhisperModel(
                self.model_size,
                device=self.device if self.device != "gpu" else "cuda",
                compute_type=self.compute_type if self.compute_type != "default" else "default",
                download_root=model_cache,
            )

            logger.info("Faster-Whisper model loaded successfully")

        except ImportError:
            logger.error(
                "faster-whisper not installed. "
                "Install with: pip install faster-whisper"
            )
            self.model = None
        except Exception as e:
            logger.error(f"Error loading Faster-Whisper model: {e}")
            self.model = None

    async def transcribe(self, audio_path: str) -> TranscriptionResult:
        """
        Transcribe audio using Faster-Whisper.

        Args:
            audio_path: Path to audio file

        Returns:
            TranscriptionResult
        """
        if not self.is_available():
            return TranscriptionResult(
                segments=[],
                language="unknown",
                duration_seconds=0,
                success=False,
                error="Faster-Whisper model not available",
            )

        try:
            logger.info(f"Transcribing: {audio_path}")

            # Run transcription in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            segments, info = await loop.run_in_executor(
                None,
                self._transcribe_sync,
                audio_path,
            )

            # Convert segments
            transcript_segments = [
                TranscriptSegment(
                    index=i,
                    start_time=segment.start,
                    end_time=segment.end,
                    text=segment.text.strip(),
                    confidence=segment.confidence if hasattr(segment, "confidence") else None,
                    language=info.language,
                )
                for i, segment in enumerate(segments)
            ]

            logger.info(
                f"Transcription completed: {len(transcript_segments)} segments, "
                f"language: {info.language}"
            )

            return TranscriptionResult(
                segments=transcript_segments,
                language=info.language,
                duration_seconds=info.duration,
                success=True,
            )

        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return TranscriptionResult(
                segments=[],
                language="unknown",
                duration_seconds=0,
                success=False,
                error=str(e),
            )

    def _transcribe_sync(self, audio_path: str):
        """Synchronous transcription wrapper."""
        segments, info = self.model.transcribe(
            audio_path,
            language=self.language if self.language != "auto" else None,
            beam_size=5,
            best_of=5,
            patience=1.0,
            condition_on_previous_text=True,
            temperature=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            compression_ratio_threshold=2.4,
            no_speech_threshold=0.6,
            repetition_penalty=1.0,
            word_level=False,
        )

        # Convert generator to list
        return list(segments), info

    def get_supported_formats(self) -> List[str]:
        """Get supported audio formats."""
        return self.SUPPORTED_FORMATS

    def is_available(self) -> bool:
        """Check if provider is available."""
        return self.model is not None

    def get_name(self) -> str:
        """Get provider name."""
        return "faster_whisper"

    def get_language(self) -> str:
        """Get configured language."""
        return self.language

    def detect_language(self, audio_path: str) -> str:
        """Detect language from audio."""
        if not self.is_available():
            return "unknown"

        try:
            # Use Whisper's language detection
            segments, info = self._transcribe_sync(audio_path)
            return info.language
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return "unknown"

    def get_model_info(self) -> dict:
        """Get model information."""
        return {
            "provider": self.get_name(),
            "model_size": self.model_size,
            "device": self.device,
            "compute_type": self.compute_type,
            "language": self.language,
            "is_available": self.is_available(),
        }
