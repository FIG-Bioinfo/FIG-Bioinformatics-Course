import sys
import os
import subprocess

def fetch_samples(base_path, target_dir):
    """
    Reads SRA-IDs from STDIN and fetches data using p3-cp commands.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)  # Create directory if it does not exist
    
    for line in sys.stdin:
        sra_id = line.strip()
        if not sra_id:
            continue
        
        print(f"Fetching job metadata for SRA-ID: {sra_id}", file=sys.stderr)
        
        # Example: /Vparrello@patricbrc.org/FIGCoreProjects/ParkinsonsProject/ParkinsonsControls/Trimming/.SRR10572161/SRR10572161_meta.txt
        
        file_path = f"ws:{base_path}/.{sra_id}/{sra_id}_meta.txt"
        
        try:
            #cmd = ["p3-cp", "-f", file_path, target_dir]
            #print(cmd, file=sys.stderr)
            subprocess.run(["p3-cp", "-f", file_path, target_dir], check=True)
            #exit()
        except subprocess.CalledProcessError:
            print(f"Warning: Failed to fetch {file_path}", file=sys.stderr)
        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fetch_samples.py <base_path> <target_dir>")
        sys.exit(1)
    
    base_path = sys.argv[1]
    target_dir = sys.argv[2]
    fetch_samples(base_path, target_dir)
