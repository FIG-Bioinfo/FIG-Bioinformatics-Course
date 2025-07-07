import os
import sys
import argparse
import subprocess

def parse_arguments():
    parser = argparse.ArgumentParser(description="Download SRA files and process them.")
    parser.add_argument("-i", "--id-file", required=True, help="File containing a list of SRA IDs.")
    parser.add_argument("-o", "--output-directory", required=True, help="Directory to store downloaded files.")
    return parser.parse_args()

def download_sra(sra_id, output_dir):
    output_path = os.path.join(output_dir, f"{sra_id}.fastq")
    stderr_prefix = f"[SRA {sra_id}] "
    
    sys.stderr.write(f"{stderr_prefix}Fetching {sra_id}...\n")
    
    try:
        # Download the SRA file as FASTQ
        command = ["fastq-dump", "--split-files", "--gzip", "--outdir", output_dir, sra_id]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            sys.stderr.write(f"{stderr_prefix}WARNING: Failed to download {sra_id}\n")
            return None, None

        # Check if single-end or paired-end
        single_end = os.path.exists(os.path.join(output_dir, f"{sra_id}.fastq.gz"))
        paired_end = (os.path.exists(os.path.join(output_dir, f"{sra_id}_1.fastq.gz")) and
                      os.path.exists(os.path.join(output_dir, f"{sra_id}_2.fastq.gz")))
        
        # Get file sizes
        file_size = 0
        if single_end:
            file_path = os.path.join(output_dir, f"{sra_id}.fastq.gz")
            file_size = os.path.getsize(file_path)
        elif paired_end:
            file_path_1 = os.path.join(output_dir, f"{sra_id}_1.fastq.gz")
            file_path_2 = os.path.join(output_dir, f"{sra_id}_2.fastq.gz")
            file_size = os.path.getsize(file_path_1) + os.path.getsize(file_path_2)
        
        sys.stderr.write(f"{stderr_prefix}Downloaded {sra_id} ({'Single-end' if single_end else 'Paired-end'}), Size: {file_size / 1024:.2f} KB\n")
        
        return file_size, "Paired" if paired_end else "Single"
    
    except Exception as e:
        sys.stderr.write(f"{stderr_prefix}ERROR: {e}\n")
        return None, None

def main():
    args = parse_arguments()
    os.makedirs(args.output_directory, exist_ok=True)
    
    with open(args.id_file, 'r') as f:
        sra_ids = [line.strip().split()[0] for line in f if line.strip()]
    
    total_entries = len(sra_ids)
    success_count = 0
    single_count = 0
    paired_count = 0
    
    for sra_id in sra_ids:
        file_size, read_type = download_sra(sra_id, args.output_directory)
        if file_size:
            success_count += 1
            if read_type == "Paired":
                paired_count += 1
            else:
                single_count += 1
    
    sys.stderr.write(f"Summary: Requested {total_entries}, Downloaded {success_count}, Single-end {single_count}, Paired-end {paired_count}\n")

if __name__ == "__main__":
    main()
