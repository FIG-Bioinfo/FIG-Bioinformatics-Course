import os
import sys
import subprocess
from pathlib import Path

def check_p3_cp_available():
    """Check if p3-cp is available in PATH."""
    from shutil import which
    if which("p3-cp") is None:
        print("Error: 'p3-cp' command not found. Please run this script in the BV-BRC.app environment.", file=sys.stderr)
        sys.exit(1)

def ensure_target_directory(subdir_path):
    """Ensure the local target subdirectory exists."""
    Path(subdir_path).mkdir(parents=True, exist_ok=True)

def fetch_fastq(base_path, target_path, sra_id):
    """Attempt to download paired-end FASTQ files for the given SRA ID."""
    subdir_path = os.path.join(target_path, sra_id)
    ensure_target_directory(subdir_path)

    for pair in ["1", "2"]:
        filename = f"{sra_id}_{pair}_ptrim.fq.gz"
        local_file_path = os.path.join(subdir_path, filename)

        if os.path.exists(local_file_path):
            print(f"File exists, skipping: {local_file_path}", file=sys.stderr)
            continue

        remote_path = f"ws:{base_path}/.{sra_id}/{filename}"
        print(f"Fetching data for SRA-ID: {sra_id}, pair {pair}", file=sys.stderr)
        try:
            subprocess.run(["p3-cp", remote_path, subdir_path], check=True)
        except subprocess.CalledProcessError:
            print(f"Warning: Failed to fetch file for {sra_id}, pair {pair}", file=sys.stderr)

def main():
    if len(sys.argv) != 3:
        print("Usage: python fetch_job_fastq_from_BVBRC.py <base_path> <target_path>", file=sys.stderr)
        sys.exit(1)

    base_path = sys.argv[1]
    target_path = sys.argv[2]

    check_p3_cp_available()
    ensure_target_directory(target_path)

    print("Reading SRA IDs from STDIN...", file=sys.stderr)
    for line in sys.stdin:
        sra_id = line.strip()
        if not sra_id:
            continue
        fetch_fastq(base_path, target_path, sra_id)

if __name__ == "__main__":
    main()
