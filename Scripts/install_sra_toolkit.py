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
    bin_dir = Path(top_dir)
        
    sra_toolkit_dir = bin_dir / "sratoolkit"
    fastq_dump_path = sra_toolkit_dir / "bin" / "fastq-dump"
    edirect_dir = bin_dir / "edirect"
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
            subprocess.run(["powershell", "-Command", f"cd {bin_dir} ; Invoke-WebRequest -Uri https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/edirect.zip -OutFile edirect.zip ; Expand-Archive -Path edirect.zip -DestinationPath {bin_dir} ; Remove-Item edirect.zip"], check=True)
        else:
            subprocess.run(["sh", "-c", f"mkdir -p {bin_dir} && cd {bin_dir} && curl -O https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/edirect.zip && unzip -o edirect.zip && rm edirect.zip"], check=True)
        
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
    with urlopen(url) as response:
        with taropen(fileobj=BytesIO(response.read()), mode="r:gz") as tar_ref:
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
    # Review path provided by user.
    # If no path provided, revert to a predefined subdirectory name with full path based on the OS.
    if len(arguments) > 1:
        bin_dir = Path(arguments[1])
        if not bin_dir.is_dir():
            # The follow method of presenting the message to the user is to keep the 
            # formatting in the terminal clean and left justified. Python methods such 
            # as triple quotes (f""" """) causes multiple lines to be indented based
            # on the indentation in the python code. 
            msg_line1 = f"Directory '{bin_dir}' does not exist."
            msg_line2 = f"If you would like the program to use a default path"
            msg_line3 = f"and subdirectory, run the program with no arguments."
            print(f"{msg_line1}\n\n{msg_line2}\n{msg_line3}", file=sys.stderr)
            exit(1)
        else:
            full_path = bin_dir
    else:
        bin_dir = "SRA"
        msg_line1 = f"No path provided."
        msg_line2 = f"Default directory name of {bin_dir} will be used."
        print(f"{msg_line1}\n{msg_line2}")
        
        try:
            # Determine the base path based on the operating system
            if sys.platform.startswith("win"):
                base_path = os.environ.get("LOCALAPPDATA") + "\\Programs"
            elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
                base_path = os.path.expanduser('~')
            else:
                raise EnvironmentError("Unsupported operating system.")

            # Construct the full path to the new subdirectory
            full_path = os.path.join(base_path, bin_dir)

        except Exception as e:
            print(f"An error occurred with directory path: {e}", file=sys.stderr)

    return full_path

def main():
    full_path = process_path(sys.argv)
    install_sra_toolkit_user(full_path)

if __name__ == "__main__":
    main()
