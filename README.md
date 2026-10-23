# Host-Based File Integrity Monitor (FIM) Engine

A lightweight, modular host-defense utility engineered in Python to detect unauthorized modifications, additions, and deletions across critical directories using cryptographic hashing (SHA-256).

---

## Technical Overview

File Integrity Monitoring is a cornerstone of host-based intrusion detection systems (HIDS) and compliance frameworks (such as PCI-DSS requirement 11.5). 

This utility establishes an immutable baseline snapshot of targeted directories and performs delta evaluations to identify tamper events, unauthorized configuration adjustments, or malware droppers.

---

## Key Engineering Features

- **Chunk-Based Cryptographic Hashing:** Processes files using buffered 64KB chunks to optimize memory utilization and prevent memory exhaustion on large datasets.
- **Stateful Snapshot Baseline:** Serializes normalized filesystem paths and cryptographic digests into a structured JSON registry.
- **Delta Tamper Engine:** Detects three distinct security anomalies:
  - **Modified (`[-]`):** Digest mismatch on established files (tampering/payload insertion).
  - **New File (`[!]`):** Unrecognized objects absent from the established baseline.
  - **Deleted (`[-]`):** Monitored system assets removed from disk.
- **Enterprise Console Output:** Zero-emoji, ANSI-standard diagnostic telemetry.

---

## Installation & Setup

1. Clone repository:
   ```bash
   git clone https://github.com/Raihan-143/file-integrity-monitor.git
   cd file-integrity-monitor

1. Install dependencies:
   ```bash
   pip install -r requirements.txt

1. Establish Baseline Snapshot
   ```bash
   python main.py -d /path/to/directory --init

1. Run Integrity Audit:
   ```bash
   python main.py -d /path/to/directory --audit 


1. Custom baseline storage path:
   ```bash
   python main.py -d /path/to/directory -b custom_baseline.json --audit

## Author
- Md Raihan Hasan Rana - Cybersecurity Enthusiast 