"""
core/hasher.py
Cryptographic hashing engine supporting chunk-based SHA-256 extraction.
"""

import hashlib
from pathlib import Path


class FileHasher:
    # Using a 64KB buffer to avoid memory overflow with large files
    BUFFER_SIZE = 65536

    @classmethod
    def calculate_sha256(cls, filepath: Path) -> str:
        """Calculates SHA-256 digest of a file using buffered reading."""
        sha256 = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                while chunk := f.read(cls.BUFFER_SIZE):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except (PermissionError, FileNotFoundError):
            return ""