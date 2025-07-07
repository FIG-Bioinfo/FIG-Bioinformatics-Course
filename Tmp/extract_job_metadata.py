import os
import sys
import json

# Define the fields to be extracted
FIELDS = [
    "accession", "run_id", "platform_name", "library_strategy",
    "library_layout", "read_length", "total_spots", "size"
]

def extract_metadata(directory):
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Print the header using the FIELDS list
    print("\t".join(FIELDS))

    for filename in os.listdir(directory):
        if filename.startswith("."):
            continue  # Skip dotfiles

        filepath = os.path.join(directory, filename)

        if not os.path.isfile(filepath):
            continue  # Skip non-file entries

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)

                if not isinstance(data, list):
                    print(f"Warning: Skipping file '{filename}' as it does not contain a list.", file=sys.stderr)
                    continue

                for record in data:
                    if isinstance(record, dict):
                        try:
                            # Extract values using the FIELDS list
                            print("\t".join(str(record.get(field, '')) for field in FIELDS))
                        except Exception as e:
                            print(f"Error processing record in file '{filename}': {e}", file=sys.stderr)
                    else:
                        print(f"Warning: Skipping invalid record in file '{filename}'", file=sys.stderr)
        except json.JSONDecodeError:
            print(f"Error: File '{filename}' is not a valid JSON file.", file=sys.stderr)
        except Exception as e:
            print(f"Error reading file '{filename}': {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_job_metadata.py <directory>", file=sys.stderr)
        sys.exit(1)
    extract_metadata(sys.argv[1])
