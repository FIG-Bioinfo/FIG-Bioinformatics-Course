import os
import sys
import argparse
import subprocess


def log_message(message, debug=False, level="INFO"):
    """Logs messages to STDERR with optional debug flag."""
    if debug or level != "DEBUG":
        sys.stderr.write(f"[{level}] {message}\n")


def run_command(command, debug=False):
    """Runs a shell command and sends output to STDOUT and STDERR."""
    try:
        if debug:
            log_message(f"Executing: {command}", debug, "DEBUG")
        result = subprocess.run(command, shell=True)
        return result.returncode == 0
    except Exception as e:
        log_message(f"Error executing command '{command}': {str(e)}", True, "ERROR")
        return False


def process_sra_id(sra_id, download_dir, cache_dir, file_type, debug):
    """Downloads and converts an SRA file to FASTA or FASTQ format."""
    log_message(f"Processing SRA ID: {sra_id} (Type: {file_type})", debug)
    
    # Determine SRA file path
    sra_file_path = os.path.join(cache_dir, sra_id, f"{sra_id}.sra") if cache_dir else os.path.expanduser(f"~/.ncbi/public/sra/{sra_id}.sra")
    fasta_output_dir = os.path.join(download_dir, sra_id)
    os.makedirs(fasta_output_dir, exist_ok=True)
    
    # Step 1: Prefetch the SRA file
    prefetch_cmd = f"prefetch {sra_id}"
    if cache_dir:
        prefetch_cmd += f" --output-directory {cache_dir}"
    
    if not run_command(prefetch_cmd, debug):
        log_message(f"Failed to prefetch {sra_id}. Skipping...", debug, "WARNING")
        return False
    
    # Step 2: Check if SRA file exists
    if not os.path.exists(sra_file_path):
        log_message(f"SRA file {sra_file_path} not found. Skipping...", debug, "ERROR")
        return False
    
    # Step 3: Convert SRA to the requested format
    dump_cmd = f"fastq-dump --{file_type.lower()} 0 --split-files --outdir {fasta_output_dir} {sra_file_path}"
    log_message(f"Executing: {dump_cmd}", debug, "DEBUG")
    if not run_command(dump_cmd, debug):
        log_message(f"fastq-dump failed for {sra_id}. Skipping...", debug, "ERROR")
        return False
    
    # Step 4: Cleanup SRA file if output files were created
    if os.listdir(fasta_output_dir):
        os.remove(sra_file_path)
    else:
        log_message(f"No {file_type} files created for {sra_id}.", debug, "WARNING")
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Automate SRA downloads and conversion.")
    parser.add_argument("-i", "--id-file", required=True, help="File containing list of SRA IDs.")
    parser.add_argument("-d", "--download-directory", required=True, help="Directory to store output files.")
    parser.add_argument("-c", "--sra-cache", help="Cache directory for SRA files.")
    parser.add_argument("-t", "--type", choices=["FASTA", "FASTQ"], default="FASTA", help="Output format (FASTA or FASTQ). Default: FASTA.")
    parser.add_argument("-D", "--Debug", action="store_true", help="Enable debug output.")
    args = parser.parse_args()
    
    debug = args.Debug
    
    if not os.path.exists(args.download_directory):
        os.makedirs(args.download_directory)
    
    if args.sra_cache and not os.path.exists(args.sra_cache):
        os.makedirs(args.sra_cache)
    
    # Read SRA IDs
    try:
        with open(args.id_file, "r") as file:
            sra_ids = [line.strip() for line in file if line.strip()]
    except Exception as e:
        log_message(f"Error reading ID file: {str(e)}", debug, "ERROR")
        sys.exit(1)
    
    total_ids = len(sra_ids)
    successful = 0
    paired_count = 0
    single_count = 0
    
    for sra_id in sra_ids:
        if process_sra_id(sra_id, args.download_directory, args.sra_cache, args.type, debug):
            successful += 1
            output_files = os.listdir(os.path.join(args.download_directory, sra_id))
            if any("_2" in f for f in output_files):
                paired_count += 1
            else:
                single_count += 1
    
    # Summary
    log_message("""
Processing Summary:
-------------------
Total SRA IDs: {}
Successfully Converted: {}
Paired-End Datasets: {}
Single-End Datasets: {}
""".format(total_ids, successful, paired_count, single_count), debug)


if __name__ == "__main__":
    main()
