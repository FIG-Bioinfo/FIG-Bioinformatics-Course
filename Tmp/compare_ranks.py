import sys
import csv

def read_tsv(file_path):
    """
    Reads a TSV (tab-separated values) file and returns the header and data.
    """
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader, None)
        if not header:
            print(f"Error: {file_path} is empty or missing headers.")
            sys.exit(1)
        data = [row for row in reader]
    return header, data

def validate_headers(header1, header2, file1, file2):
    """
    Validates that the first two columns in both files have matching headers.
    Exits if there is a mismatch.
    """
    if header1[:2] != header2[:2]:
        print(f"Error: Column names in {file1} and {file2} do not match.")
        sys.exit(1)

def process_ranked_data(file1, file2):
    """
    Processes and compares ranked data from two TSV files. Prints matched and unmatched ranks.
    Also prints statistics about the comparison.
    """
    header1, data1 = read_tsv(file1)
    header2, data2 = read_tsv(file2)
    
    validate_headers(header1, header2, file1, file2)
    
    id_index, name_index = 0, 1
    id_name, item_name = header1[id_index], header1[name_index]
    
    # Print header line
    print(f"rank1\trank2\t{id_name}\t{item_name}")
    
    # Create mappings from ID to rank and name
    rank1_map = {row[id_index]: (idx + 1, row[name_index]) for idx, row in enumerate(data1)}
    rank2_map = {row[id_index]: (idx + 1, row[name_index]) for idx, row in enumerate(data2)}
    
    processed_ids = set()
    identical_count = 0
    differing_count = 0
    first_differing_rank = None
    missing_in_second = 0
    missing_in_first = 0
    
    # Print ranked matches from file1
    for idx, row in enumerate(data1):
        id_num = row[id_index]
        name = row[name_index]
        rank1 = idx + 1
        rank2 = rank2_map.get(id_num, ('-', ''))[0]  # Get rank from second file or use "-"
        
        if rank2 == '-':
            missing_in_second += 1
        elif rank1 == rank2:
            identical_count += 1
        else:
            differing_count += 1
            if first_differing_rank is None:
                first_differing_rank = rank1
        
        print(f"{rank1}\t{rank2}\t{id_num}\t{name}")
        processed_ids.add(id_num)
    
    print("//")  # Separator for unmatched entries
    
    # Print unmatched entries from file2
    for idx, row in enumerate(data2):
        id_num = row[id_index]
        name = row[name_index]
        rank2 = idx + 1
        if id_num not in processed_ids:
            print(f"-\t{rank2}\t{id_num}\t{name}")
            missing_in_first += 1
    
    # Print statistics to STDERR
    sys.stderr.write(f"Identical ranks: {identical_count}\n")
    sys.stderr.write(f"Differing ranks: {differing_count}\n")
    sys.stderr.write(f"First differing rank: {first_differing_rank}\n")
    sys.stderr.write(f"Missing in second file: {missing_in_second}\n")
    sys.stderr.write(f"Missing in first file: {missing_in_first}\n")

if __name__ == "__main__":
    """
    Entry point of the script. Ensures correct usage and processes the TSV files.
    """
    if len(sys.argv) != 3:
        print("Usage: python script.py <file1.tsv> <file2.tsv>")
        sys.exit(1)
    
    file1, file2 = sys.argv[1], sys.argv[2]
    process_ranked_data(file1, file2)
