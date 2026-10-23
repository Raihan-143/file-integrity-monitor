"""
main.py
CLI entry point for the Host-based File Integrity Monitor (FIM).
"""

import argparse
import sys
from core.monitor import IntegrityMonitor


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Host-based File Integrity Monitoring (FIM) Engine"
    )
    parser.add_argument(
        "-d", "--dir",
        dest="target_dir",
        required=True,
        help="Target directory path to monitor (e.g., C:\\test_dir or ./test_dir)"
    )
    parser.add_argument(
        "-b", "--baseline",
        dest="db_file",
        default="baseline.json",
        help="Baseline database file path (Default: baseline.json)"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--init",
        action="store_true",
        help="Generate a baseline cryptographic snapshot of the target directory"
    )
    group.add_argument(
        "--audit",
        action="store_true",
        help="Audit current target directory files against the established baseline"
    )

    args = parser.parse_args()

    monitor = IntegrityMonitor(target_dir=args.target_dir, db_file=args.db_file)

    if args.init:
        monitor.initialize_baseline()
    elif args.audit:
        results = monitor.audit_integrity()
        if results.get("modified") or results.get("deleted"):
            sys.exit(2)


if __name__ == "__main__":
    main()