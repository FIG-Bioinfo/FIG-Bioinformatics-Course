Assuming that the SRA Toolkit is installed and available in the user's system PATH, write a Python script named `sra_download_with_prefetch.py` that automates the process of downloading and processing SRA entries. The script should support the following command-line arguments:

Mandatory arguments:
- `-i` or `--id-file`: A file containing a list of SRA IDs (one per line).
- `-d` or `--download-directory`: The directory where the processed FASTQ files should be stored.

Optional argument:
- `-c` or `--sra-cache`: An optional directory to be used as a cache location for `prefetch`.

### **Script Behavior**
1. **Read the SRA IDs** from the input file.
2. **Fetch each SRA entry using `prefetch`**:
   - If `--sra-cache` is provided, store the `.sra` file inside `<cache_dir>/<sra_id>/`.
   - Otherwise, store it in the default `~/.ncbi/public/sra/` location.
3. **Convert the SRA file into FASTQ format using `fasterq-dump`**:
   - Ensure that `fasterq-dump` reads from the correct `.sra` file location.
   - Store the resulting FASTQ files in the specified `--download-directory`, inside a subdirectory named after the SRA ID.
   - Use the `--split-files` option to handle paired-end reads.
4. **Check and analyze the downloaded files**:
   - Determine whether the dataset is single-end or paired-end based on the presence of `_1.fastq` and `_2.fastq` files.
   - Calculate and display file sizes.
5. **Print a final summary** of:
   - Total SRA IDs requested.
   - Number of successful downloads.
   - Breakdown of single-end vs paired-end datasets.

### **Implementation Notes**
- The script should use `subprocess.run()` to execute shell commands (`prefetch` and `fasterq-dump`).
- Ensure robust error handling:
  - If `prefetch` fails, print a warning and continue to the next SRA ID.
  - If the expected `.sra` file is not found in the cache directory, print an error message.
  - If `fasterq-dump` fails, print a warning.
  - If no `.fastq` files are found after conversion, print a warning.
- The script should log all actions to STDERR for debugging.
- Use `os.makedirs()` to ensure output directories exist before downloading.

The output should include:
- Informational messages for each step.
- Warnings in case of failures.
- A final summary of download statistics.

Write the full, functional Python script that implements this behavior.
