"""Tests for file utilities."""

import pytest
import os
from pathlib import Path
from app.utils.file_utils import (
    sanitize_filename,
    validate_file_extension,
    validate_file_path,
    get_safe_path,
    calculate_file_hash,
)


class TestSanitizeFilename:
    def test_removes_invalid_characters(self):
        assert sanitize_filename("file<>name.txt") == "filename.txt"
        assert sanitize_filename("file|name*.txt") == "filename.txt"

    def test_prevents_path_traversal(self):
        result = sanitize_filename("../../etc/passwd")
        assert not result.startswith(".")
        assert "/" not in result

    def test_limits_length(self):
        long_name = "a" * 300 + ".txt"
        result = sanitize_filename(long_name)
        assert len(result) <= 255

    def test_preserves_extension(self):
        result = sanitize_filename("my_file.pdf")
        assert result.endswith(".pdf")


class TestValidateFileExtension:
    def test_valid_extension(self):
        assert validate_file_extension("file.mp3", ["mp3", "wav"])
        assert validate_file_extension("file.MP3", ["mp3", "wav"])

    def test_invalid_extension(self):
        assert not validate_file_extension("file.exe", ["mp3", "wav"])
        assert not validate_file_extension("file.txt", ["mp3", "wav"])

    def test_no_extension(self):
        assert not validate_file_extension("file", ["mp3", "wav"])


class TestValidateFilePath:
    def test_valid_path(self, tmp_path):
        file_path = tmp_path / "file.txt"
        assert validate_file_path(str(file_path), str(tmp_path))

    def test_path_traversal_protection(self, tmp_path):
        base_dir = tmp_path / "uploads"
        base_dir.mkdir()

        # Try to escape the directory
        malicious_path = str(base_dir / ".." / ".." / "etc" / "passwd")
        assert not validate_file_path(malicious_path, str(base_dir))

    def test_different_directory(self, tmp_path):
        dir1 = tmp_path / "dir1"
        dir2 = tmp_path / "dir2"
        dir1.mkdir()
        dir2.mkdir()

        file_path = dir2 / "file.txt"
        assert not validate_file_path(str(file_path), str(dir1))


class TestGetSafePath:
    def test_creates_safe_path(self, tmp_path):
        base_dir = str(tmp_path)
        filename = "normal_file.txt"

        safe_path = get_safe_path(base_dir, filename)
        assert safe_path.startswith(base_dir)
        assert filename in safe_path

    def test_rejects_path_traversal(self, tmp_path):
        base_dir = str(tmp_path)
        filename = "../../etc/passwd"

        with pytest.raises(ValueError):
            get_safe_path(base_dir, filename)


class TestCalculateFileHash:
    def test_hash_consistency(self, tmp_path):
        # Create a test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        # Calculate hash twice
        hash1 = calculate_file_hash(str(test_file))
        hash2 = calculate_file_hash(str(test_file))

        assert hash1 == hash2

    def test_different_content_different_hash(self, tmp_path):
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("content1")
        file2.write_text("content2")

        hash1 = calculate_file_hash(str(file1))
        hash2 = calculate_file_hash(str(file2))

        assert hash1 != hash2

    def test_hash_format(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        hash_result = calculate_file_hash(str(test_file))

        # SHA256 produces 64 character hex string
        assert len(hash_result) == 64
        assert all(c in "0123456789abcdef" for c in hash_result)
