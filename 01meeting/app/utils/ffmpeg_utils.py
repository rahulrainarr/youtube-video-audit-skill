"""FFmpeg utilities for media processing."""

import subprocess
import os
import logging
from pathlib import Path
from typing import Tuple, Optional
import json

logger = logging.getLogger(__name__)


def is_ffmpeg_available() -> bool:
    """Check if FFmpeg is installed and available."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_media_info(file_path: str) -> Optional[dict]:
    """Get media information using ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_format",
                "-show_streams",
                "-print_json",
                file_path,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return json.loads(result.stdout)
        return None
    except Exception as e:
        logger.error(f"Error getting media info: {e}")
        return None


def extract_audio(
    input_path: str,
    output_path: str,
    audio_format: str = "wav",
    sample_rate: int = 16000,
) -> Tuple[bool, str]:
    """
    Extract audio from video file.

    Args:
        input_path: Path to input video file
        output_path: Path to output audio file
        audio_format: Output format (wav, mp3, flac, etc.)
        sample_rate: Target sample rate in Hz

    Returns:
        (success, message)
    """
    try:
        # Validate input
        if not os.path.exists(input_path):
            return False, f"Input file not found: {input_path}"

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        # Build FFmpeg command
        # Use libmp3lame codec for MP3, flac for FLAC, pcm_s16le for WAV
        codec_map = {
            "mp3": "libmp3lame",
            "wav": "pcm_s16le",
            "flac": "flac",
            "aac": "aac",
            "ogg": "libvorbis",
        }

        codec = codec_map.get(audio_format, "pcm_s16le")

        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-vn",  # No video
            "-acodec", codec,
            "-ar", str(sample_rate),
            "-ac", "1",  # Mono
            "-y",  # Overwrite output
            output_path,
        ]

        logger.info(f"Extracting audio: {input_path} -> {output_path}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600,  # 1 hour timeout
        )

        if result.returncode == 0:
            logger.info(f"Audio extraction successful: {output_path}")
            return True, "Audio extracted successfully"
        else:
            error_msg = result.stderr
            logger.error(f"FFmpeg error: {error_msg}")
            return False, f"FFmpeg error: {error_msg[:200]}"

    except subprocess.TimeoutExpired:
        return False, "Audio extraction timeout (file too long)"
    except Exception as e:
        logger.error(f"Error extracting audio: {e}")
        return False, f"Error extracting audio: {str(e)}"


def convert_audio(
    input_path: str,
    output_path: str,
    output_format: str = "wav",
    sample_rate: int = 16000,
) -> Tuple[bool, str]:
    """Convert audio between formats."""
    return extract_audio(input_path, output_path, output_format, sample_rate)


def get_audio_duration(file_path: str) -> Optional[float]:
    """Get audio duration in seconds."""
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1:noescapes=1",
                file_path,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return float(result.stdout.strip())
        return None
    except Exception as e:
        logger.error(f"Error getting audio duration: {e}")
        return None


def validate_audio_file(file_path: str) -> Tuple[bool, str]:
    """Validate audio file integrity."""
    try:
        result = subprocess.run(
            [
                "ffmpeg",
                "-v", "error",
                "-i", file_path,
                "-f", "null",
                "-",
            ],
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode == 0:
            return True, "Audio file is valid"
        else:
            return False, f"Invalid audio file: {result.stderr[:200]}"
    except Exception as e:
        logger.error(f"Error validating audio: {e}")
        return False, f"Error validating audio: {str(e)}"


def split_audio(
    input_path: str,
    output_dir: str,
    segment_duration_seconds: int = 300,
) -> Tuple[bool, list, str]:
    """
    Split audio into segments.

    Args:
        input_path: Path to input audio file
        output_dir: Directory for output segments
        segment_duration_seconds: Duration of each segment

    Returns:
        (success, list_of_output_paths, message)
    """
    try:
        os.makedirs(output_dir, exist_ok=True)

        duration = get_audio_duration(input_path)
        if not duration:
            return False, [], "Could not determine audio duration"

        output_files = []
        segment_count = int(duration / segment_duration_seconds) + 1

        for i in range(segment_count):
            start_time = i * segment_duration_seconds
            output_file = os.path.join(output_dir, f"segment_{i:03d}.wav")

            cmd = [
                "ffmpeg",
                "-i", input_path,
                "-ss", str(start_time),
                "-t", str(segment_duration_seconds),
                "-acodec", "pcm_s16le",
                "-ar", "16000",
                "-ac", "1",
                "-y",
                output_file,
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600,
            )

            if result.returncode == 0:
                output_files.append(output_file)
            else:
                logger.error(f"Error splitting segment {i}: {result.stderr}")

        if output_files:
            return True, output_files, f"Audio split into {len(output_files)} segments"
        else:
            return False, [], "Failed to split audio"

    except Exception as e:
        logger.error(f"Error splitting audio: {e}")
        return False, [], f"Error splitting audio: {str(e)}"
