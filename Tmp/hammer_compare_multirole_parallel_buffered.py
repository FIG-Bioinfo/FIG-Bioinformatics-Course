import argparse
import sys
import re
import csv
import multiprocessing
from Bio import SeqIO
from Bio.Seq import reverse_complement
from concurrent.futures import ProcessPoolExecutor

def parse_hammers(hammers_file):
    """Parses the hammers file and returns mappings for analysis."""
    hammer_to_feature = {}
    feature_to_genome = {}
    feature_to_role = {}
    roles = set()
    
    # Open the hammers file with large buffering for efficiency
    with open(hammers_file, 'r', buffering=2**20) as f:
        reader = csv.DictReader(f, delimiter='\t')
        headers = reader.fieldnames
        
        # Ensure required columns exist
        if 'hammer' not in headers or 'fid' not in headers:
            raise ValueError("The hammers file must contain 'hammer' and 'fid' columns.")

        # Read and process each row
        for row in reader:
            hammer = row['hammer']
            feature_id = row['fid']
            role = row.get('role', 'Unknown')

            hammer_to_feature[hammer] = feature_id
            feature_to_role[feature_id] = role
            roles.add(role)

            # Extract genome ID from feature ID using regex
            genome_match = re.match(r'^fig\|(\d+\.\d+)\.peg\.\d+$', feature_id)
            if genome_match:
                genome_id = genome_match.group(1)
                feature_to_genome[feature_id] = genome_id

    # Determine k-mer length from the first hammer entry
    kmer_length = len(next(iter(hammer_to_feature)))
    return kmer_length, roles, hammer_to_feature, feature_to_genome, feature_to_role

def parse_genome_names(genome_names_file):
    """Parses the genome names file and returns a mapping from genome ID to genome name."""
    genome_id_to_name = {}
    
    # Open the genome names file with large buffering
    with open(genome_names_file, 'r', buffering=2**20) as f:
        reader = csv.DictReader(f, delimiter='\t')
        headers = reader.fieldnames

        # Ensure required columns exist
        if 'genome_id' not in headers or 'genome_name' not in headers:
            raise ValueError("The genome-names file must contain 'genome_id' and 'genome_name' columns.")

        # Read and store mappings
        for row in reader:
            genome_id_to_name[row['genome_id']] = row['genome_name']
    
    return genome_id_to_name

def process_sequence_chunk(sequence_chunk, kmer_length, hammer_to_feature, feature_to_genome, feature_to_role):
    """Processes a chunk of DNA sequences to find k-mer matches."""
    genome_counts = {}
    genome_role_counts = {}

    for sequence in sequence_chunk:
        rev_comp_sequence = reverse_complement(sequence)  # Generate reverse complement sequence
        
        for i in range(len(sequence) - kmer_length + 1):
            for kmer in [sequence[i:i + kmer_length], rev_comp_sequence[i:i + kmer_length]]:
                if kmer in hammer_to_feature:
                    feature_id = hammer_to_feature[kmer]
                    genome_id = feature_to_genome[feature_id]
                    role = feature_to_role[feature_id]
                    
                    # Count occurrences of each genome
                    genome_counts[genome_id] = genome_counts.get(genome_id, 0) + 1
                    if genome_id not in genome_role_counts:
                        genome_role_counts[genome_id] = {}
                    genome_role_counts[genome_id][role] = genome_role_counts[genome_id].get(role, 0) + 1
    
    return genome_counts, genome_role_counts

def main():
    """Main function to parse input, process sequences in parallel, and generate output."""
    parser = argparse.ArgumentParser(description="Parallelized hammer analysis. Reads DNA FASTA from STDIN. Writes TSV report to STDOUT.")
    parser.add_argument('-H', '--hammers', required=True, help="Path to the hammers TSV file.")
    parser.add_argument('-G', '--genome-names', required=True, help="Path to the genome names TSV file.")
    parser.add_argument('-F', '--role-fraction', type=float, default=0.8, help="Minimum fraction of roles for genome inclusion (default: 0.8).")
    args = parser.parse_args()

    # Parse input files
    kmer_length, roles, hammer_to_feature, feature_to_genome, feature_to_role = parse_hammers(args.hammers)
    genome_id_to_name = parse_genome_names(args.genome_names)

    # Use buffered reading to speed up large input stream processing
    fasta_sequences = []
    with sys.stdin as fasta_stream:
        fasta_iterator = SeqIO.parse(fasta_stream, 'fasta')
        for record in fasta_iterator:
            fasta_sequences.append(str(record.seq).lower())
    
    num_workers = min(multiprocessing.cpu_count(), 8)  # Use up to 8 CPU cores
    chunk_size = max(len(fasta_sequences) // num_workers, 1)
    sequence_chunks = [fasta_sequences[i:i + chunk_size] for i in range(0, len(fasta_sequences), chunk_size)]

    genome_counts = {}
    genome_role_counts = {}
    
    # Process sequences in parallel using multiple worker processes
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = executor.map(process_sequence_chunk, sequence_chunks, 
                               [kmer_length] * len(sequence_chunks),
                               [hammer_to_feature] * len(sequence_chunks),
                               [feature_to_genome] * len(sequence_chunks),
                               [feature_to_role] * len(sequence_chunks))

    # Aggregate results from all worker processes
    for partial_counts, partial_role_counts in results:
        for genome_id, count in partial_counts.items():
            genome_counts[genome_id] = genome_counts.get(genome_id, 0) + count
        for genome_id, role_dict in partial_role_counts.items():
            if genome_id not in genome_role_counts:
                genome_role_counts[genome_id] = {}
            for role, count in role_dict.items():
                genome_role_counts[genome_id][role] = genome_role_counts[genome_id].get(role, 0) + count
    
    # Filter and sort results
    total_roles = len(roles)
    output = []
    for genome_id, role_counts in genome_role_counts.items():
        num_roles = len(role_counts)
        if num_roles >= total_roles * args.role_fraction:
            genome_name = genome_id_to_name.get(genome_id, 'Unknown sp.')
            score = genome_counts[genome_id]
            output.append((genome_id, genome_name, score, num_roles))

    output.sort(key=lambda x: x[2], reverse=True)
    writer = csv.writer(sys.stdout, delimiter='\t')
    headers = ['genome_id', 'genome_name', 'score', 'num_roles'] if total_roles > 1 else ['genome_id', 'genome_name', 'score']
    writer.writerow(headers)
    for row in output:
        writer.writerow(row)

if __name__ == '__main__':
    main()
