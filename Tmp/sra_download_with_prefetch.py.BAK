########################################################################
#...Prompt that generated this program:
"""
Write a Python script named "sra_download_with_prefetch.py"
that automates the download of paired-end SRA data
and converts it directly into FASTA format without using
external tools like seqtk. The script should be fully functional
and ready to run on a system where the SRA Toolkit is installed.

The script must support the following command-line arguments:
- "-i" or "--id-file": A required argument specifying a file
   that contains a list of SRA IDs, one per line.
- "-d" or "--download-directory": A required argument specifying
   the directory where the processed FASTA files should be stored.
- "-c" or "--sra-cache": An optional argument specifying a directory
   to be used as a cache location for SRA downloads.

### Script Behavior:
1. Read the list of SRA IDs from the specified file.
2. Use the "prefetch" command to download the corresponding SRA files
   into the cache directory (or the default "~/.ncbi/public/sra/" location if no cache directory is provided).
3. Ensure that the downloaded ".sra" file exists in the expected location
   before proceeding.
4. Use "fastq-dump --fasta 0 --split-files" to convert the downloaded
   SRA file into a pair of FASTA files (for paired-end reads)
   or a single FASTA file (for single-end reads).
5. Store the resulting FASTA files in a subdirectory under the specified
   download directory, named after the corresponding SRA ID.
6. Perform error handling at every step:
   - If "prefetch" fails, print a warning and move to the next SRA ID.
   - If "fastq-dump" fails, print a warning and move to the next SRA ID.
   - If no FASTA files are created, print a warning.
7. After processing all SRA IDs, print a summary that includes:
   - The total number of SRA entries requested.
   - The number of successful conversions.
   - The count of single-end and paired-end datasets.

### Implementation Requirements:
- Use "subprocess.run()" to execute system commands.
- Ensure all output directories exist before writing files.
- Capture and log STDERR output for debugging.
- Use readable function names and modular code organization.
- Print all informational messages and warnings to STDERR.

Write the complete, functional Python script with no placeholders
or missing sections.
"""

########################################################################
#...Pseudocode for this program:
"""
FUNCTION run_command(command):
    TRY:
        EXECUTE command using system shell
        RETURN (command was successful, standard output, error output)
    CATCH exception AS e:
        RETURN (False, "", error message)

FUNCTION fetch_sra(sra_id, download_dir, cache_dir):
    PRINT "[INFO] Fetching SRA ID: " + sra_id TO STDERR

    SET prefetch_output_dir = cache_dir IF cache_dir IS NOT NULL ELSE HOME_DIRECTORY + "/.ncbi/public/sra"
    SET prefetch_sra_dir = prefetch_output_dir + "/" + sra_id
    SET prefetch_sra_path = prefetch_sra_dir + "/" + sra_id + ".sra"

    SET prefetch_cmd = "prefetch " + sra_id + " --output-directory " + prefetch_output_dir
    success, stdout, stderr = run_command(prefetch_cmd)

    IF NOT success:
        PRINT "[WARNING] Failed to fetch " + sra_id + ". Error: " + stderr TO STDERR
        RETURN NULL

    IF FILE NOT EXISTS prefetch_sra_path:
        PRINT "[ERROR] Prefetch did not place " + sra_id + ".sra in expected location: " + prefetch_sra_path TO STDERR
        RETURN NULL

    PRINT "[INFO] Prefetch saved SRA file at " + prefetch_sra_path TO STDERR

    SET output_path = download_dir + "/" + sra_id
    CREATE DIRECTORY output_path IF NOT EXISTS

    SET fastq_dump_cmd = "fastq-dump --fasta 0 --split-files " + prefetch_sra_path + " -O " + output_path
    PRINT "[INFO] Running fastq-dump: " + fastq_dump_cmd TO STDERR
    success, stdout, stderr = run_command(fastq_dump_cmd)

    IF NOT success:
        PRINT "[WARNING] Failed to convert " + sra_id + " to FASTA. Error: " + stderr TO STDERR
        RETURN NULL

    RETURN output_path

FUNCTION analyze_download(download_path):
    IF DIRECTORY NOT EXISTS download_path:
        PRINT "[WARNING] Download directory " + download_path + " does not exist." TO STDERR
        RETURN NULL, NULL

    SET files = LIST FILES IN download_path
    SET fasta_files = FILTER files WHERE file ENDS WITH ".fasta"

    IF fasta_files IS EMPTY:
        PRINT "[WARNING] No FASTA files found in " + download_path TO STDERR
        RETURN NULL, NULL

    SET file_sizes = EMPTY DICTIONARY
    FOR EACH file IN fasta_files:
        file_sizes[file] = GET FILE SIZE OF (download_path + "/" + file)

    SET paired = FALSE
    FOR EACH file IN fasta_files:
        IF "_1.fasta" IN file OR "_2.fasta" IN file:
            SET paired = TRUE
            BREAK

    RETURN (file_sizes, "paired-end" IF paired ELSE "single-end")

FUNCTION main():
    PARSE COMMAND LINE ARGUMENTS:
        - "-i" OR "--id-file" REQUIRED AS id_file
        - "-d" OR "--download-directory" REQUIRED AS download_directory
        - "-c" OR "--sra-cache" OPTIONAL AS sra_cache

    CREATE DIRECTORY download_directory IF NOT EXISTS
    IF sra_cache IS NOT NULL:
        CREATE DIRECTORY sra_cache IF NOT EXISTS

    READ id_file AND STORE FIRST COLUMN AS sra_ids

    SET total_count = LENGTH OF sra_ids
    SET success_count = 0
    SET single_count = 0
    SET paired_count = 0

    FOR EACH sra_id IN sra_ids:
        SET download_path = fetch_sra(sra_id, download_directory, sra_cache)
        IF download_path IS NULL:
            CONTINUE

        SET (file_sizes, read_type) = analyze_download(download_path)
        IF file_sizes IS NOT NULL:
            INCREMENT success_count
            IF read_type == "single-end":
                INCREMENT single_count
            ELSE:
                INCREMENT paired_count
            
            FOR EACH (file, size) IN file_sizes:
                PRINT "[INFO] Downloaded " + file + ": " + size + " bytes (" + read_type + ")" TO STDERR
        ELSE:
            PRINT "[WARNING] No valid files found for " + sra_id TO STDERR

    PRINT "[SUMMARY] Requested: " + total_count + ", Successful: " + success_count + 
          ", Single-end: " + single_count + ", Paired-end: " + paired_count TO STDERR

IF SCRIPT IS EXECUTED:
    CALL main()
"""

########################################################################
#...Code generated by Grimoire:
import os
import sys
import argparse
import subprocess

def run_command(command):
    """Run a shell command and return success status and output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def fetch_sra(sra_id, download_dir, cache_dir):
    """Fetch SRA entry and ensure correct paths between prefetch and fastq-dump."""
    print(f"[INFO] Fetching SRA ID: {sra_id}", file=sys.stderr)

    # Define expected prefetch output path
    prefetch_output_dir = cache_dir or os.path.expanduser("~/.ncbi/public/sra")
    prefetch_sra_dir = os.path.join(prefetch_output_dir, sra_id)
    prefetch_sra_path = os.path.join(prefetch_sra_dir, f"{sra_id}.sra")

    # Run prefetch command
    prefetch_cmd = f"prefetch {sra_id} --output-directory {prefetch_output_dir}"
    success, stdout, stderr = run_command(prefetch_cmd)

    if not success:
        print(f"[WARNING] Failed to fetch {sra_id}. Error: {stderr}", file=sys.stderr)
        return None

    # Check if the expected .sra file exists
    if not os.path.exists(prefetch_sra_path):
        print(f"[ERROR] Prefetch did not place {sra_id}.sra in the expected location: {prefetch_sra_path}", file=sys.stderr)
        return None

    print(f"[INFO] Prefetch saved SRA file at {prefetch_sra_path}", file=sys.stderr)

    # Define correct output directory for FASTA conversion
    output_path = os.path.join(download_dir, sra_id)
    os.makedirs(output_path, exist_ok=True)

    # Convert SRA to FASTA format (splitting paired-end reads)
    fastq_dump_cmd = f"fastq-dump --fasta 0 --split-files \"{prefetch_sra_path}\" -O \"{output_path}\""
    print(f"[INFO] Running fastq-dump: {fastq_dump_cmd}", file=sys.stderr)
    success, stdout, stderr = run_command(fastq_dump_cmd)

    if not success:
        print(f"[WARNING] Failed to convert {sra_id} to FASTA. Error: {stderr}", file=sys.stderr)
        return None

    return output_path

def analyze_download(download_path):
    """Determine if the downloaded file is single-end or paired-end and return file sizes."""
    if not os.path.exists(download_path):
        print(f"[WARNING] Download directory {download_path} does not exist.", file=sys.stderr)
        return None, None

    files = os.listdir(download_path)
    fasta_files = [f for f in files if f.endswith(".fasta")]

    if not fasta_files:
        print(f"[WARNING] No FASTA files found in {download_path}.", file=sys.stderr)
        return None, None

    file_sizes = {f: os.path.getsize(os.path.join(download_path, f)) for f in fasta_files}

    # Check if the files are paired-end or single-end
    paired = any("_1.fasta" in f or "_2.fasta" in f for f in fasta_files)

    return file_sizes, "paired-end" if paired else "single-end"

def main():
    parser = argparse.ArgumentParser(description="Download and process SRA entries into FASTA format using the SRA Toolkit.")
    parser.add_argument("-i", "--id-file", required=True, help="File containing a list of SRA IDs.")
    parser.add_argument("-d", "--download-directory", required=True, help="Output directory for downloaded files.")
    parser.add_argument("-c", "--sra-cache", help="Optional cache directory for SRA Toolkit commands.")
    
    args = parser.parse_args()

    # Ensure directories exist
    os.makedirs(args.download_directory, exist_ok=True)
    if args.sra_cache:
        os.makedirs(args.sra_cache, exist_ok=True)

    # Read SRA IDs
    with open(args.id_file, 'r') as file:
        sra_ids = [line.strip().split()[0] for line in file if line.strip()]

    total_count = len(sra_ids)
    success_count = 0
    single_count = 0
    paired_count = 0

    for sra_id in sra_ids:
        download_path = fetch_sra(sra_id, args.download_directory, args.sra_cache)
        if not download_path:
            continue

        file_sizes, read_type = analyze_download(download_path)
        if file_sizes:
            success_count += 1
            if read_type == "single-end":
                single_count += 1
            else:
                paired_count += 1
            
            for file, size in file_sizes.items():
                print(f"[INFO] Downloaded {file}: {size} bytes ({read_type})", file=sys.stderr)
        else:
            print(f"[WARNING] No valid files found for {sra_id}.", file=sys.stderr)

    # Print summary statistics
    print(f"[SUMMARY] Requested: {total_count}, Successful: {success_count}, Single-end: {single_count}, Paired-end: {paired_count}", file=sys.stderr)

if __name__ == "__main__":
    main()
