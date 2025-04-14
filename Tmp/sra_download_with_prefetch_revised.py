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
4. Extract the contents of the .sra file, determine if they are FASTQ or FASTA,
   inform the user of the contents of the .sra file, and 
   - if FASTQ, store them in the subdirectory "FASTQ/sraID",
   under the specified download directory, with "sraID" replaced
   by the SRA-ID being downloaded;
   - elsif FASTA, store them in the a subdirectory "FASTA/sraID",
   under the specified download directory, where again "sraID"
   is replaced by the SRA-ID being downloaded;
5. Perform error handling at every step:
   - If "prefetch" fails, print a warning and move to the next SRA ID.
   - If the extraction of the contents of the .sra file succeeds,
   delete the cached .sra file;
   elseif "fastq-dump" fails, print a warning and move to the next SRA ID.
   - If no FASTQ or FASTA files are created, print a warning.
6. Ensure all informational messages (`[INFO]`) and debugging messages
   (`[DEBUG]`) are printed to STDERR.
7. Debug messages should only be printed if the script is invoked with the
   `-D` or `--Debug` flag.
8. After processing all SRA IDs, print a summary that includes:
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
DEFINE FUNCTION print_info(message)
    PRINT "[INFO] " + message TO STDERR

DEFINE FUNCTION print_debug(message, debug)
    IF debug IS TRUE
        PRINT "[DEBUG] " + message TO STDERR

DEFINE FUNCTION ensure_directory_exists(directory)
    IF directory DOES NOT EXIST
        CREATE directory

DEFINE FUNCTION run_command(command, debug)
    CALL print_debug("Executing command: " + command, debug)
    EXECUTE SYSTEM COMMAND(command) AND CAPTURE EXIT STATUS
    RETURN EXIT STATUS == 0

DEFINE FUNCTION locate_sra_file(sra_id, cache_dir)
    SET default_cache = EXPAND_PATH("~/.ncbi/public/sra/")
    SET cache_dir = cache_dir OR default_cache  // Use provided or default cache directory

    SET expected_sra_file = cache_dir + "/" + sra_id + ".sra"
    SET alt_sra_file = cache_dir + "/" + sra_id + "/" + sra_id + ".sra"

    IF expected_sra_file EXISTS
        RETURN expected_sra_file
    ELSE IF alt_sra_file EXISTS
        RETURN alt_sra_file
    ELSE
        RETURN NULL

DEFINE FUNCTION download_sra(sra_id, cache_dir, debug)
    IF cache_dir IS NOT EMPTY
        SET cache_option = "--output-directory " + cache_dir
    ELSE
        SET cache_option = ""

    SET command = "prefetch " + cache_option + " " + sra_id
    RETURN run_command(command, debug)

DEFINE FUNCTION extract_sra(sra_id, download_dir, cache_dir, debug)
    SET sra_file = locate_sra_file(sra_id, cache_dir)

    IF sra_file IS NULL
        PRINT "[WARNING] SRA file for " + sra_id + " not found in expected locations. Skipping." TO STDERR
        RETURN FALSE

    SET fastq_dir = download_dir + "/FASTQ/" + sra_id
    SET fasta_dir = download_dir + "/FASTA/" + sra_id

    CALL ensure_directory_exists(fastq_dir)
    CALL ensure_directory_exists(fasta_dir)

    SET fastq_dump_cmd = "fastq-dump --split-files --outdir " + fastq_dir + " " + sra_file
    SET fasta_dump_cmd = "fastq-dump --fasta 0 --outdir " + fasta_dir + " " + sra_file

    SET fastq_success = run_command(fastq_dump_cmd, debug)
    SET fasta_success = run_command(fasta_dump_cmd, debug)

    IF fastq_success
        CALL print_info("FASTQ files stored in " + fastq_dir)
    ELSE IF fasta_success
        CALL print_info("FASTA files stored in " + fasta_dir)
    ELSE
        PRINT "[WARNING] Extraction failed for " + sra_id TO STDERR
        RETURN FALSE

    DELETE FILE sra_file
    RETURN TRUE

DEFINE FUNCTION process_sra_list(id_file, download_dir, cache_dir, debug)
    OPEN id_file AND READ CONTENT INTO sra_ids_list
    REMOVE EMPTY LINES FROM sra_ids_list

    SET total = LENGTH OF sra_ids_list
    SET success_count = 0
    SET single_end_count = 0
    SET paired_end_count = 0

    FOR EACH sra_id IN sra_ids_list
        CALL print_info("Processing " + sra_id + "...")

        IF NOT download_sra(sra_id, cache_dir, debug)
            PRINT "[WARNING] Failed to download " + sra_id + ". Skipping." TO STDERR
            CONTINUE

        IF extract_sra(sra_id, download_dir, cache_dir, debug)
            INCREMENT success_count

            SET sra_fastq_path = download_dir + "/FASTQ/" + sra_id
            SET paired_end = FALSE

            FOR EACH file IN DIRECTORY sra_fastq_path
                IF file CONTAINS "_2.fastq"
                    SET paired_end = TRUE
                    BREAK LOOP

            IF paired_end
                INCREMENT paired_end_count
            ELSE
                INCREMENT single_end_count

    CALL print_info("Summary: Total requested: " + total + 
                    ", Successful: " + success_count + 
                    ", Single-end: " + single_end_count + 
                    ", Paired-end: " + paired_end_count)

DEFINE FUNCTION main()
    PARSE COMMAND-LINE ARGUMENTS:
        - "-i" or "--id-file" → id_file (REQUIRED)
        - "-d" or "--download-directory" → download_dir (REQUIRED)
        - "-c" or "--sra-cache" → cache_dir (OPTIONAL)
        - "-D" or "--Debug" → debug (BOOLEAN FLAG)

    CALL process_sra_list(id_file, download_dir, cache_dir, debug)

IF SCRIPT IS EXECUTED DIRECTLY
    CALL main()
"""

########################################################################
#...Code generated by Grimoire:
#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

def print_info(message):
    """Prints informational messages to STDERR."""
    print(f"[INFO] {message}", file=sys.stderr)

def print_debug(message, debug):
    """Prints debug messages to STDERR if debug mode is enabled."""
    if debug:
        print(f"[DEBUG] {message}", file=sys.stderr)

def ensure_directory_exists(directory):
    """Ensures the specified directory exists, creates it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def run_command(command, debug):
    """Runs a shell command and returns success status."""
    print_debug(f"Executing command: {command}", debug)
    result = subprocess.run(command, shell=True, stdout=sys.stdout, stderr=sys.stderr)
    return result.returncode == 0

def locate_sra_file(sra_id, cache_dir):
    """Finds the SRA file location, checking different possible paths."""
    default_cache = os.path.expanduser("~/.ncbi/public/sra/")
    cache_dir = cache_dir or default_cache  # Use provided or default cache directory

    # Expected file paths
    expected_sra_file = os.path.join(cache_dir, f"{sra_id}.sra")
    alt_sra_file = os.path.join(cache_dir, sra_id, f"{sra_id}.sra")  # Case where it's placed in a subdirectory

    # Check for existence
    if os.path.exists(expected_sra_file):
        return expected_sra_file
    elif os.path.exists(alt_sra_file):
        return alt_sra_file
    else:
        return None

def download_sra(sra_id, cache_dir, debug):
    """Downloads an SRA file using `prefetch`."""
    cache_option = f"--output-directory {cache_dir}" if cache_dir else ""
    command = f"prefetch {cache_option} {sra_id}"
    return run_command(command, debug)

def extract_sra(sra_id, download_dir, cache_dir, debug):
    """Extracts SRA file into FASTQ or FASTA format."""
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

    os.remove(sra_file)  # Remove .sra file after processing
    return True

def process_sra_list(id_file, download_dir, cache_dir, debug):
    """Processes a list of SRA IDs."""
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
            # Checking for paired-end by the presence of "_2.fastq" files
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
