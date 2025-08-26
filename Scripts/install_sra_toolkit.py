import subprocess
import sys
import os
import shutil
from pathlib import Path
from urllib.request import urlopen
from io import BytesIO

if sys.platform == "win32":
    from zipfile import ZipFile
    import winreg as reg
else:
    from tarfile import open as taropen

def install_sra_toolkit_user(top_dir):
    """Install the SRA Toolkit and EDirect in user mode if they are not already installed."""
    #install_dir = Path(top_dir)
    install_dir = Path(top_dir)
        
    sra_toolkit_dir = install_dir / "sratoolkit"
    fastq_dump_path = sra_toolkit_dir / "bin" / "fastq-dump"
    edirect_dir = install_dir / "edirect"
    esearch_path = edirect_dir / "esearch"

    if fastq_dump_path.exists():
        print("SRA Toolkit is already installed.")
    else:
        print("Installing SRA Toolkit in user mode...")
        if sys.platform.startswith("linux"):
            sra_toolkit_url = "https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/current/sratoolkit.current-ubuntu64.tar.gz"
            download_and_extract_tar(sra_toolkit_url, sra_toolkit_dir)
        elif sys.platform == "darwin":
            sra_toolkit_url = "https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/current/sratoolkit.current-mac64.tar.gz"
            download_and_extract_tar(sra_toolkit_url, sra_toolkit_dir)
        elif sys.platform == "win32":
            sra_toolkit_url = "https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/current/sratoolkit.current-win64.zip"
            download_and_extract_zip(sra_toolkit_url, sra_toolkit_dir)

        print("SRA Toolkit installation completed.")
        add_to_path(sra_toolkit_dir / "bin")

    if esearch_path.exists():
        print("EDirect tools are already installed.")
    else:
        print("Installing EDirect tools in user mode...")
        if sys.platform == "win32":
            subprocess.run(["powershell", "-Command", f"cd {install_dir} ; Invoke-WebRequest -Uri https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/edirect.zip -OutFile edirect.zip ; Expand-Archive -Path edirect.zip -DestinationPath {install_dir} ; Remove-Item edirect.zip"], check=True)
        else:
            subprocess.run(["sh", "-c", f"mkdir -p {install_dir} && cd {install_dir} && curl -O https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/edirect.zip && unzip -o edirect.zip && rm edirect.zip"], check=True)
        
        print("EDirect tools installed successfully.")

def download_and_extract_zip(url, extract_to):
    """Download and extract a zip file from a URL."""
    with urlopen(url) as response:
        with ZipFile(BytesIO(response.read())) as zip_ref:
            # Get the top-level directory name inside the ZIP archive
            top_level_dir = zip_ref.namelist()[0].split('/')[0]
            
            for member in zip_ref.namelist():
                # Strip the top-level directory name from the member path
                member_path = os.path.relpath(member, start=top_level_dir)
                if member_path == '.':
                    continue
                
                target_path = os.path.join(extract_to, member_path)
                target_dir = os.path.dirname(target_path)
                
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                
                if not member.endswith('/'):  # Skip directories
                    with zip_ref.open(member) as source, open(target_path, "wb") as target:
                        shutil.copyfileobj(source, target)

                # Log extraction process (optional for debugging)
                print(f"Extracted: {target_path}")

def download_and_extract_tar(url, extract_to):
    """Download and extract a tar file from a URL."""
    import tarfile
    with urlopen(url) as response:
        with tarfile.open(fileobj=BytesIO(response.read()), mode="r:gz") as tar_ref:
            tar_ref.extractall(path=extract_to)

def add_to_path(new_path):
    """Add a directory to the user-level system PATH if it's not already present."""
    new_path_str = str(new_path)

    if sys.platform.startswith == "win":
        # Open the registry key for the user's environment variables
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, "Environment", 0, reg.KEY_ALL_ACCESS)
        try:
            # Read the current user-level PATH variable
            user_path, _ = reg.QueryValueEx(reg_key, "PATH")
        except FileNotFoundError:
            # If the PATH variable does not exist, create it
            user_path = ""
            
        # Check if the new path is already in the user-level PATH
        if new_path_str not in user_path.split(os.pathsep):
            # Add the new path to the user-level PATH
            new_user_path = user_path + os.pathsep + new_path_str if user_path else new_path_str
            reg.SetValueEx(reg_key, "PATH", 0, reg.REG_EXPAND_SZ, new_user_path)
        reg.CloseKey(reg_key)
    else:
        # For Unix-like systems, update the PATH in .profile or .bash_profile
        profile_path = Path.home() / ".profile"
        with open(profile_path, "a") as profile:
            profile.write(f'\nexport PATH="{new_path_str}:$PATH"\n')

def process_path(arguments):
    # If a path is provided, use it; otherwise, install in the NCBI directory under the course root directory.
    if len(arguments) > 1:
        bin_dir = Path(arguments[1])
        if not bin_dir.is_dir():
            msg_line1 = f"Directory '{bin_dir}' does not exist."
            msg_line2 = f"If you would like the program to use the script's directory,"
            msg_line3 = f"run the program with no arguments."
            print(f"{msg_line1}\n\n{msg_line2}\n{msg_line3}", file=sys.stderr)
            exit(1)
        else:
            full_path = bin_dir
    else:
        # Install in <course_root>/NCBI.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ncbi_dir = os.path.abspath(os.path.join(script_dir, '..', 'NCBI'))
        msg_line1 = f"No path provided."
        msg_line2 = f"Defaulting to the NCBI directory: {ncbi_dir}"
        print(f"{msg_line1}\n{msg_line2}")
        full_path = ncbi_dir

    return full_path

def main():
    full_path = process_path(sys.argv)
    install_sra_toolkit_user(full_path)

if __name__ == "__main__":
    main()
