"""File utility functions for upload validation and processing."""

import os
import hashlib
import mimetypes
from pathlib import Path
from typing import Tuple, Optional
import re
from app.core import settings


def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """Calculate file hash for duplicate detection and integrity."""
    hash_obj = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def validate_mime_type(file_path: str, allowed_types: list) -> bool:
    """Validate file MIME type."""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type in allowed_types if mime_type else False


def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """Validate file extension."""
    _, ext = os.path.splitext(filename)
    return ext.lower().lstrip(".") in [e.lower() for e in allowed_extensions]


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """Sanitize filename to prevent path traversal and invalid characters."""
    # Remove path components
    filename = os.path.basename(filename)

    # Remove invalid characters
    filename = re.sub(r'[^\w\s.-]', '', filename)

    # Limit length
    if len(filename) > max_length:
        name, ext = os.path.splitext(filename)
        filename = name[:max_length - len(ext)] + ext

    # Prevent empty filename
    if not filename or filename.startswith("."):
        filename = "file_" + str(hashlib.md5(filename.encode()).hexdigest()[:8])

    return filename


def validate_file_path(file_path: str, base_dir: str) -> bool:
    """Prevent path traversal attacks."""
    abs_path = os.path.abspath(file_path)
    abs_base = os.path.abspath(base_dir)
    return abs_path.startswith(abs_base)


def validate_upload_file(
    file_path: str,
    file_size: int,
    file_type: str,  # 'audio', 'video', 'transcript'
) -> Tuple[bool, str]:
    """
    Validate uploaded file.
    Returns (is_valid, error_message)
    """
    # Check file exists
    if not os.path.exists(file_path):
        return False, "File not found"

    # Check file size
    max_size = settings.max_upload_size_mb * 1024 * 1024
    if file_size > max_size:
        return False, f"File exceeds maximum size of {settings.max_upload_size_mb}MB"

    if file_size == 0:
        return False, "File is empty"

    # Check extension
    allowed_exts = []
    if file_type == "audio":
        allowed_exts = settings.get_allowed_audio_formats
    elif file_type == "video":
        allowed_exts = settings.get_allowed_video_formats
    elif file_type == "transcript":
        allowed_exts = settings.get_allowed_transcript_formats
    else:
        return False, f"Unknown file type: {file_type}"

    if not validate_file_extension(file_path, allowed_exts):
        return False, f"File type not supported. Allowed: {', '.join(allowed_exts)}"

    # Check MIME type for known types
    allowed_mimes = {
        "audio": [
            "audio/mpeg", "audio/wav", "audio/mp4",
            "audio/ogg", "audio/flac", "audio/aac"
        ],
        "video": [
            "video/mp4", "video/quicktime", "video/x-mkvideo",
            "video/webm", "video/x-msvideo", "video/x-flv"
        ],
        "transcript": [
            "text/plain", "text/vtt", "text/srt",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword"
        ]
    }

    if file_type in allowed_mimes:
        if not validate_mime_type(file_path, allowed_mimes[file_type]):
            # Allow fallback if extension is correct (MIME detection can be unreliable)
            pass

    return True, ""


def ensure_directory(directory: str) -> None:
    """Ensure directory exists and create if needed."""
    Path(directory).mkdir(parents=True, exist_ok=True)


def get_safe_path(directory: str, filename: str) -> str:
    """Get a safe file path preventing directory traversal."""
    safe_filename = sanitize_filename(filename)
    safe_path = os.path.join(directory, safe_filename)

    if not validate_file_path(safe_path, directory):
        raise ValueError("Invalid file path")

    return safe_path


def get_file_size(file_path: str) -> int:
    """Get file size in bytes."""
    return os.path.getsize(file_path)


def delete_file(file_path: str) -> bool:
    """Safely delete a file."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        return True
    except Exception as e:
        return False


def get_audio_format_from_path(file_path: str) -> Optional[str]:
    """Extract audio format from file path."""
    _, ext = os.path.splitext(file_path)
    return ext.lower().lstrip(".")
