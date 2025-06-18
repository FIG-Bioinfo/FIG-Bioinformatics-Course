#!/usr/bin/env python

import argparse
import os
import subprocess
import sys

def print_info(message):
    print(f"[INFO] {message}", file=sys.stderr)

def print_debug(message, debug):
    if debug:
        print(f"[DEBUG] {message}", file=sys.stderr)

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def run_command(command, debug):
    print_debug(f"Executing command: {command}", debug)
    result = subprocess.run(command, shell=True, stdout=sys.stdout, stderr=sys.stderr)
    return result.returncode == 0

def get_default_cache_dir():
    return os.path.join(os.environ.get("COURSE_HOME", os.path.expanduser("~")), "NCBI", "public", "sra")

def locate_sra_file(sra_id, cache_dir):
    cache_dir = cache_dir or get_default_cache_dir()

    expected_sra_file = os.path.join(cache_dir, f"{sra_id}.sra")
    alt_sra_file = os.path.join(cache_dir, sra_id, f"{sra_id}.sra")

    if os.path.exists(expected_sra_file):
        return expected_sra_file
    elif os.path.exists(alt_sra_file):
        return alt_sra_file
    else:
        return None

def download_sra(sra_id, cache_dir, debug):
    cache_dir = cache_dir or get_default_cache_dir()
    cache_option = f"--output-directory {cache_dir}"
    command = f"prefetch {cache_option} {sra_id}"
    return run_command(command, debug)

def extract_sra(sra_id, download_dir, cache_dir, debug):
    sra_file = locate_sra_file(sra_id, cache_dir)

    if not sra_file:
        print(f"[WARNING] SRA file for {sra_id} not found in expected locations. Skipping.", file=sys.stderr)
        return False

    fastq_dir = os.path.join(download_dir, "FASTQ", sra_id)
    fasta_dir = os.path.join(download_dir, "FASTA", sra_id)

    ensure_directory_exists(fastq_dir)
    ensure_directory_exists(fasta_dir)

    fastq_dump_cmd = f"fastq-dump --split-files --outdir {fastq_dir} {sra_file}"
    fasta_dump_cmd = f"fastq-dump --fasta 0 --outdir {fasta_dir} {sra_file}"

    fastq_success = run_command(fastq_dump_cmd, debug)
    fasta_success = run_command(fasta_dump_cmd, debug)

    if fastq_success:
        print_info(f"FASTQ files stored in {fastq_dir}")
    elif fasta_success:
        print_info(f"FASTA files stored in {fasta_dir}")
    else:
        print(f"[WARNING] Extraction failed for {sra_id}.", file=sys.stderr)
        return False

    os.remove(sra_file)
    return True

def process_sra_list(id_file, download_dir, cache_dir, debug):
    with open(id_file, "r") as file:
        sra_ids = [line.strip() for line in file if line.strip()]

    total = len(sra_ids)
    success_count = 0
    single_end_count = 0
    paired_end_count = 0

    for sra_id in sra_ids:
        print_info(f"Processing {sra_id}...")

        if not download_sra(sra_id, cache_dir, debug):
            print(f"[WARNING] Failed to download {sra_id}. Skipping.", file=sys.stderr)
            continue

        if extract_sra(sra_id, download_dir, cache_dir, debug):
            success_count += 1
            sra_fastq_path = os.path.join(download_dir, "FASTQ", sra_id)
            paired_end = any("_2.fastq" in file for file in os.listdir(sra_fastq_path) if os.path.isfile(os.path.join(sra_fastq_path, file)))

            if paired_end:
                paired_end_count += 1
            else:
                single_end_count += 1

    print_info(f"Summary: Total requested: {total}, Successful: {success_count}, Single-end: {single_end_count}, Paired-end: {paired_end_count}")

def main():
    parser = argparse.ArgumentParser(description="Download and extract SRA files into FASTA format.")
    parser.add_argument("-i", "--id-file", required=True, help="File containing list of SRA IDs.")
    parser.add_argument("-d", "--download-directory", required=True, help="Directory to store extracted FASTA files.")
    parser.add_argument("-c", "--sra-cache", help="Cache directory for SRA downloads.")
    parser.add_argument("-D", "--Debug", action="store_true", help="Enable debug output.")

    args = parser.parse_args()
    process_sra_list(args.id_file, args.download_directory, args.sra_cache, args.Debug)

if __name__ == "__main__":
    main()
