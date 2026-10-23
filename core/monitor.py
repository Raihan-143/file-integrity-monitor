"""
core/monitor.py
Core engine for baseline state management and file integrity auditing.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from core.hasher import FileHasher
from utils.logger import ConsoleLogger


class IntegrityMonitor:
    def __init__(self, target_dir: str, db_file: str = "baseline.json") -> None:
        self.target_dir = Path(target_dir).resolve()
        self.db_path = Path(db_file).resolve()

    def scan_directory(self) -> Dict[str, str]:
        """Recursively hashes all files in the target directory."""
        snapshot: Dict[str, str] = {}
        for path in self.target_dir.rglob("*"):
            if path.is_file() and path != self.db_path:
                digest = FileHasher.calculate_sha256(path)
                if digest:
                    snapshot[str(path)] = digest
        return snapshot

    def initialize_baseline(self) -> None:
        """Generates a cryptographic baseline and saves it to a persistent JSON record."""
        ConsoleLogger.header("FIM Baseline Generation")
        ConsoleLogger.info(f"Target Directory: {self.target_dir}")
        ConsoleLogger.info("Scanning directory and calculating SHA-256 digests...")

        snapshot = self.scan_directory()
        payload = {
            "target_directory": str(self.target_dir),
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "file_count": len(snapshot),
            "records": snapshot
        }

        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4)
            ConsoleLogger.success(f"Baseline established for {len(snapshot)} files.")
            ConsoleLogger.success(f"Baseline record written to: {self.db_path}")
        except OSError as err:
            ConsoleLogger.failure(f"Failed to record baseline: {err}")

    def audit_integrity(self) -> Dict[str, List[str]]:
        """Audits target against baseline and flags modifications, additions, and deletions."""
        ConsoleLogger.header("FIM Integrity Audit Engine")
        ConsoleLogger.info(f"Auditing Directory: {self.target_dir}")

        if not self.db_path.exists():
            ConsoleLogger.failure(f"Baseline file '{self.db_path}' not found. Run with --init first.")
            return {}

        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                baseline_data = json.load(f)
        except (json.JSONDecodeError, OSError) as err:
            ConsoleLogger.failure(f"Error reading baseline data: {err}")
            return {}

        baseline_records: Dict[str, str] = baseline_data.get("records", {})
        current_records = self.scan_directory()

        modified_files: List[str] = []
        new_files: List[str] = []
        deleted_files: List[str] = []

        # Compare against the baseline to identify modifications and new files relative to the current files.
        for filepath, current_hash in current_records.items():
            if filepath not in baseline_records:
                new_files.append(filepath)
            elif baseline_records[filepath] != current_hash:
                modified_files.append(filepath)

        # Identifying deleted files
        for filepath in baseline_records:
            if filepath not in current_records:
                deleted_files.append(filepath)

        # Print results
        ConsoleLogger.info(f"Total Current Files Scanned: {len(current_records)}\n")

        has_tampering = False

        if modified_files:
            has_tampering = True
            for file in modified_files:
                ConsoleLogger.failure(f"FILE MODIFIED (TAMPERING DETECTED): {file}")
                ConsoleLogger.warning(f"  Old SHA256: {baseline_records[file]}")
                ConsoleLogger.warning(f"  New SHA256: {current_records[file]}")

        if new_files:
            has_tampering = True
            for file in new_files:
                ConsoleLogger.warning(f"UNRECOGNIZED FILE CREATED: {file}")

        if deleted_files:
            has_tampering = True
            for file in deleted_files:
                ConsoleLogger.failure(f"MONITORED FILE DELETED: {file}")

        print()
        if not has_tampering:
            ConsoleLogger.success("Integrity Check Passed: Zero anomalies or file alterations detected.")
        else:
            ConsoleLogger.failure(
                f"Integrity Compromised: {len(modified_files)} modified, "
                f"{len(new_files)} created, {len(deleted_files)} deleted."
            )

        return {
            "modified": modified_files,
            "new": new_files,
            "deleted": deleted_files
        }