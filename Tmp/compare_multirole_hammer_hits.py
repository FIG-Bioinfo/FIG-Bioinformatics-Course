import sys
import csv

def read_tsv(file_path):
    """
    Reads a TSV (tab-separated values) file and returns the header and data.
    """
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader, None)
        if not header or header[:4] != ["genome_id", "genome_name", "score", "num_roles"]:
            print(f"Error: {file_path} does not have the expected headers.")
            sys.exit(1)
        data = [row for row in reader]
    return header, data

def process_ranked_data(file1, file2):
    """
    Processes and compares ranked genomic data from two TSV files.
    Prints matched and unmatched ranks along with their associated scores and roles.
    """
    header1, data1 = read_tsv(file1)
    header2, data2 = read_tsv(file2)
    
    id_index, name_index, score_index, roles_index = 0, 1, 2, 3
    
    # Print header line
    print("rank1\trank2\tscore1\tscore2\tnum_roles1\tnum_roles2\tgenome_id\tgenome_name")
    
    # Create mappings from ID to rank and attributes
    rank1_map = {row[id_index]: (idx + 1, row[score_index], row[roles_index], row[name_index]) for idx, row in enumerate(data1)}
    rank2_map = {row[id_index]: (idx + 1, row[score_index], row[roles_index], row[name_index]) for idx, row in enumerate(data2)}
    
    processed_ids = set()
    identical_count = 0
    differing_count = 0
    first_differing_rank = None
    missing_in_second = 0
    missing_in_first = 0
    
    # Print ranked matches from file1
    for idx, row in enumerate(data1):
        id_num = row[id_index]
        rank1 = idx + 1
        score1 = row[score_index]
        roles1 = row[roles_index]
        name = row[name_index]
        rank2, score2, roles2, _ = rank2_map.get(id_num, ('-', '-', '-', '-'))
        
        if rank2 == '-':
            missing_in_second += 1
        elif rank1 == rank2:
            identical_count += 1
        else:
            differing_count += 1
            if first_differing_rank is None:
                first_differing_rank = rank1
        
        print(f"{rank1}\t{rank2}\t{score1}\t{score2}\t{roles1}\t{roles2}\t{id_num}\t{name}")
        processed_ids.add(id_num)
    
    print("//")  # Separator for unmatched entries
    
    # Print unmatched entries from file2
    for idx, row in enumerate(data2):
        id_num = row[id_index]
        rank2 = idx + 1
        score2 = row[score_index]
        roles2 = row[roles_index]
        name = row[name_index]
        if id_num not in processed_ids:
            print(f"-\t{rank2}\t-\t{score2}\t-\t{roles2}\t{id_num}\t{name}")
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
