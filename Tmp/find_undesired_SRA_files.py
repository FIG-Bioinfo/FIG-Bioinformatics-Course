import os
import re
import sys

def load_identifiers(identifier_file):
    """Reads identifiers from a one-column file and returns a set of valid identifiers."""
    try:
        with open(identifier_file, 'r') as file:
            identifiers = {line.strip() for line in file if re.match(r'^[A-Za-z]{3}\d+$', line.strip())}
        return identifiers
    except FileNotFoundError:
        print(f"Error: Identifier file '{identifier_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unable to read identifier file '{identifier_file}': {e}", file=sys.stderr)
        sys.exit(1)

def find_unmatched_files(directory, identifiers):
    """Finds files whose prefix up to the first underscore is not in the given identifier set."""
    unmatched_files = []
    pattern = re.compile(r'^([A-Za-z]{3}\d+)_')

    try:
        for filename in os.listdir(directory):
            match = pattern.match(filename)
            if match:
                prefix = match.group(1)
                if prefix not in identifiers:
                    unmatched_files.append(filename)
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied for directory '{directory}'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unable to read directory '{directory}': {e}", file=sys.stderr)
        sys.exit(1)

    return unmatched_files

def main(identifier_file, directory):
    identifiers = load_identifiers(identifier_file)
    unmatched_files = find_unmatched_files(directory, identifiers)

    if unmatched_files:
        print("Files with unmatched prefixes:")
        for file in unmatched_files:
            print(file)
    else:
        print("All files in the directory match a known identifier.", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <identifier_file> <directory>", file=sys.stderr)
        sys.exit(1)

    identifier_file = sys.argv[1]
    directory = sys.argv[2]
    main(identifier_file, directory)
