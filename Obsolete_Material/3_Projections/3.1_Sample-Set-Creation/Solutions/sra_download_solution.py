########################################################################
#...Prompt that generated this program:
"""
Write a Python script named "sra_download.py"
that automates the download of paired-end SRA data and converts it
directly into FASTA format without using external tools like seqtk.
The script should be fully functional and ready to run on a system
where the SRA Toolkit is installed.

The script must support the following command-line arguments:
- "-i" or "--id-file": A required argument specifying a file
   that contains a list of SRA IDs, one per line.

- "-d" or "--download-directory": A required argument specifying
   the directory where the processed FASTA files should be stored.

- "-c" or "--sra-cache": An optional argument specifying a directory
   to be used as a cache location for SRA downloads.

- "-D" or "--Debug": An optional flag to enable debug output.

### Script Behavior:
1. Read the list of SRA IDs from the specified file.
2. Use the "prefetch" command to download the corresponding SRA files
   into the cache directory (or the default "~/.ncbi/public/sra/" location
   if no cache directory is provided).
3. Ensure that the downloaded ".sra" file exists in the expected location
   before proceeding.
4. Use "fastq-dump --fasta 0 --split-files" to convert the downloaded
   SRA file into a pair of FASTA files (for paired-end reads)
   or a single FASTA file (for single-end reads).
5. Store the resulting FASTA files in a subdirectory under the specified
   download directory, named after the corresponding SRA ID.
6. Perform error handling at every step:
   - If "prefetch" fails, print a warning and move to the next SRA ID.
   - If "fastq-dump" succeeds, delete the cached .sra file;
     elseif "fastq-dump" fails, print a warning and move to the next SRA ID.
   - If no FASTA files are created, print a warning.
7. Ensure all informational messages (`[INFO]`) and debugging messages
   (`[DEBUG]`) are printed to STDERR.
8. Debug messages should only be printed if the script is invoked with the
   `-D` or `--Debug` flag.
9. After processing all SRA IDs, print a summary that includes:
   - The total number of SRA entries requested.
   - The number of successful conversions.
   - The count of single-end and paired-end datasets.

### Implementation Requirements:
- Use "subprocess.run()" to execute system commands;
   also send STDOUT and STDERR from the system commands
   to STDOUT and STDERR for the script.
- Ensure all output directories exist before writing files.
- Send all informative and progress messages to STDERR,
   and in "Debug" mode also print all system-commands to STDERR.
- Use readable function names and modular code organization.
- Print all informational messages and warnings to STDERR.
"""

########################################################################
#...Pseudocode for this program:
"""
DEFINE FUNCTION log_message(message, debug=False, level="INFO")
    IF debug OR level != "DEBUG"
        PRINT "[", level, "] ", message TO STDERR

DEFINE FUNCTION run_command(command, debug=False)
    TRY
        IF debug
            CALL log_message("Executing: " + command, debug, "DEBUG")
        EXECUTE command USING SYSTEM SHELL
        RETURN command_success
    CATCH EXCEPTION e
        CALL log_message("Error executing command '" + command + "': " + e.message, True, "ERROR")
        RETURN False

DEFINE FUNCTION process_sra_id(sra_id, download_dir, cache_dir, debug)
    CALL log_message("Processing SRA ID: " + sra_id, debug)

    # Determine the SRA file path
    IF cache_dir EXISTS
        SET sra_file_path = cache_dir + "/" + sra_id + "/" + sra_id + ".sra"
    ELSE
        SET sra_file_path = HOME_DIR + "/.ncbi/public/sra/" + sra_id + ".sra"

    SET fasta_output_dir = download_dir + "/" + sra_id
    CREATE DIRECTORY fasta_output_dir IF NOT EXISTS

    # Step 1: Prefetch the SRA file
    SET prefetch_cmd = "prefetch " + sra_id
    IF cache_dir EXISTS
        APPEND " --output-directory " + cache_dir TO prefetch_cmd

    IF NOT run_command(prefetch_cmd, debug)
        CALL log_message("Failed to prefetch " + sra_id + ". Skipping...", debug, "WARNING")
        RETURN False

    # Step 2: Verify SRA file existence
    IF NOT EXISTS sra_file_path
        CALL log_message("SRA file " + sra_file_path + " not found. Skipping...", debug, "ERROR")
        RETURN False

    # Step 3: Convert SRA to FASTA
    SET fastq_dump_cmd = "fastq-dump --fasta 0 --split-files --outdir " + fasta_output_dir + " " + sra_file_path
    CALL log_message("Executing: " + fastq_dump_cmd, debug, "DEBUG")

    IF NOT run_command(fastq_dump_cmd, debug)
        CALL log_message("fastq-dump failed for " + sra_id + ". Skipping...", debug, "ERROR")
        RETURN False

    # Step 4: Cleanup if conversion was successful
    IF fasta_output_dir CONTAINS FILES
        DELETE sra_file_path
    ELSE
        CALL log_message("No FASTA files created for " + sra_id, debug, "WARNING")
        RETURN False

    RETURN True

DEFINE FUNCTION main()
    PARSE COMMAND LINE ARGUMENTS:
        - REQUIRED: id-file (-i)
        - REQUIRED: download-directory (-d)
        - OPTIONAL: sra-cache (-c)
        - OPTIONAL FLAG: Debug (-D)

    SET debug = Debug FLAG

    CREATE download-directory IF NOT EXISTS
    IF sra-cache ARGUMENT EXISTS
        CREATE sra-cache DIRECTORY IF NOT EXISTS

    TRY
        OPEN id-file FOR READING
        READ LINES INTO sra_ids
    CATCH EXCEPTION e
        CALL log_message("Error reading ID file: " + e.message, debug, "ERROR")
        EXIT PROGRAM

    SET total_ids = COUNT(sra_ids)
    SET successful = 0
    SET paired_count = 0
    SET single_count = 0

    FOR EACH sra_id IN sra_ids
        IF process_sra_id(sra_id, download_directory, sra_cache, debug)
            INCREMENT successful
            SET fasta_files = LIST FILES IN (download_directory + "/" + sra_id)
            IF ANY FILE IN fasta_files CONTAINS "_2.fasta"
                INCREMENT paired_count
            ELSE
                INCREMENT single_count

    # Summary
    CALL log_message("
    Processing Summary:
    -------------------
    Total SRA IDs: " + total_ids + "
    Successfully Converted: " + successful + "
    Paired-End Datasets: " + paired_count + "
    Single-End Datasets: " + single_count, debug)

IF SCRIPT EXECUTED AS MAIN
    CALL main()
"""

########################################################################
#...Code generated by Grimoire:
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


def process_sra_id(sra_id, download_dir, cache_dir, debug):
    """Downloads and converts an SRA file to FASTA format."""
    log_message(f"Processing SRA ID: {sra_id}", debug)
    
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
    
    # Step 3: Convert SRA to FASTA
    fastq_dump_cmd = f"fastq-dump --fasta 0 --split-files --outdir {fasta_output_dir} {sra_file_path}"
    log_message(f"Executing: {fastq_dump_cmd}", debug, "DEBUG")
    if not run_command(fastq_dump_cmd, debug):
        log_message(f"fastq-dump failed for {sra_id}. Skipping...", debug, "ERROR")
        return False
    
    # Step 4: Cleanup SRA file if FASTA files were created
    if os.listdir(fasta_output_dir):
        os.remove(sra_file_path)
    else:
        log_message(f"No FASTA files created for {sra_id}.", debug, "WARNING")
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Automate SRA downloads and FASTA conversion.")
    parser.add_argument("-i", "--id-file", required=True, help="File containing list of SRA IDs.")
    parser.add_argument("-d", "--download-directory", required=True, help="Directory to store FASTA files.")
    parser.add_argument("-c", "--sra-cache", help="Cache directory for SRA files.")
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
        if process_sra_id(sra_id, args.download_directory, args.sra_cache, debug):
            successful += 1
            fasta_files = os.listdir(os.path.join(args.download_directory, sra_id))
            if any("_2.fasta" in f for f in fasta_files):
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
