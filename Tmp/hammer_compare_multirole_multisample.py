import sys
import argparse
import os
import re
import csv
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from Bio import SeqIO
from Bio.Seq import reverse_complement

def parse_hammers(hammers_file):
    """Parses the hammers file and returns mappings for analysis."""
    hammer_to_feature = {}
    feature_to_genome = {}
    feature_to_role = {}
    roles = set()

    with open(hammers_file, 'r', buffering=2**20) as f:
        reader = csv.DictReader(f, delimiter='\t')
        headers = reader.fieldnames
        
        if 'hammer' not in headers or 'fid' not in headers:
            raise ValueError("The hammers file must contain 'hammer' and 'fid' columns.")

        for row in reader:
            hammer = row['hammer']
            feature_id = row['fid']
            role = row.get('role', 'Unknown')

            hammer_to_feature[hammer] = feature_id
            feature_to_role[feature_id] = role
            roles.add(role)

            genome_match = re.match(r'^fig\|(\d+\.\d+)\.peg\.\d+$', feature_id)
            if genome_match:
                genome_id = genome_match.group(1)
                feature_to_genome[feature_id] = genome_id

    kmer_length = len(next(iter(hammer_to_feature)))
    return kmer_length, roles, hammer_to_feature, feature_to_genome, feature_to_role

def parse_genome_names(genome_names_file):
    """Parses the genome names file and returns a mapping from genome ID to genome name."""
    genome_id_to_name = {}

    with open(genome_names_file, 'r', buffering=2**20) as f:
        reader = csv.DictReader(f, delimiter='\t')
        headers = reader.fieldnames

        if 'genome_id' not in headers or 'genome_name' not in headers:
            raise ValueError("The genome-names file must contain 'genome_id' and 'genome_name' columns.")

        for row in reader:
            genome_id_to_name[row['genome_id']] = row['genome_name']
    
    return genome_id_to_name

def process_sequence_chunk(sequence_chunk, kmer_length, hammer_to_feature, feature_to_genome, feature_to_role):
    """Processes a chunk of DNA sequences to find k-mer matches."""
    genome_counts = {}
    genome_role_counts = {}

    for sequence in sequence_chunk:
        rev_comp_sequence = reverse_complement(sequence)

        for i in range(len(sequence) - kmer_length + 1):
            for kmer in [sequence[i:i + kmer_length], rev_comp_sequence[i:i + kmer_length]]:
                if kmer in hammer_to_feature:
                    feature_id = hammer_to_feature[kmer]
                    genome_id = feature_to_genome.get(feature_id, "unknown")
                    role = feature_to_role.get(feature_id, "unknown")

                    genome_counts[genome_id] = genome_counts.get(genome_id, 0) + 1
                    if genome_id not in genome_role_counts:
                        genome_role_counts[genome_id] = {}
                    genome_role_counts[genome_id][role] = genome_role_counts[genome_id].get(role, 0) + 1
    
    return genome_counts, genome_role_counts

def process_sample(sample_dir, sampleID, kmer_length, hammer_to_feature, feature_to_genome, feature_to_role):
    """Processes all reads for a given sample and aggregates statistics."""
    genome_counts = {}
    genome_role_counts = {}

    fasta_files = [f for f in os.listdir(sample_dir) if re.match(rf"{sampleID}_[12]_.*", f)]
    left_reads = [os.path.join(sample_dir, f) for f in fasta_files if re.match(rf"{sampleID}_1_.*", f)]
    right_reads = [os.path.join(sample_dir, f) for f in fasta_files if re.match(rf"{sampleID}_2_.*", f)]

    all_reads = left_reads + right_reads  # Merge left and right reads
    sequences = []

    for fasta_file in all_reads:
        with open(fasta_file, 'r', buffering=2**24) as f:
            for record in SeqIO.parse(f, 'fasta'):
                sequences.append(str(record.seq).lower())

    num_workers = min(multiprocessing.cpu_count(), 8)
    chunk_size = max(len(sequences) // num_workers, 1)
    sequence_chunks = [sequences[i:i + chunk_size] for i in range(0, len(sequences), chunk_size)]

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = executor.map(process_sequence_chunk, sequence_chunks, 
                               [kmer_length] * len(sequence_chunks),
                               [hammer_to_feature] * len(sequence_chunks),
                               [feature_to_genome] * len(sequence_chunks),
                               [feature_to_role] * len(sequence_chunks))

    for partial_counts, partial_role_counts in results:
        for genome_id, count in partial_counts.items():
            genome_counts[genome_id] = genome_counts.get(genome_id, 0) + count
        for genome_id, role_dict in partial_role_counts.items():
            if genome_id not in genome_role_counts:
                genome_role_counts[genome_id] = {}
            for role, count in role_dict.items():
                genome_role_counts[genome_id][role] = genome_role_counts[genome_id].get(role, 0) + count

    return sampleID, genome_counts, genome_role_counts

def main():
    parser = argparse.ArgumentParser(description="Parallelized hammer analysis for metagenomic samples.")
    parser.add_argument('-H', '--hammers', required=True, help="Path to the hammers TSV file.")
    parser.add_argument('-G', '--genome-names', required=True, help="Path to the genome names TSV file.")
    parser.add_argument('-D', '--directory', required=True, help="Path to the directory containing sample subdirectories.")
    parser.add_argument('-F', '--role-fraction', type=float, default=0.8, help="Minimum fraction of roles for genome inclusion (default: 0.8).")
    args = parser.parse_args()

    kmer_length, roles, hammer_to_feature, feature_to_genome, feature_to_role = parse_hammers(args.hammers)
    genome_id_to_name = parse_genome_names(args.genome_names)

    sample_dirs = [os.path.join(args.directory, d) for d in os.listdir(args.directory) if os.path.isdir(os.path.join(args.directory, d))]
    sampleIDs = [os.path.basename(d) for d in sample_dirs]

    all_results = []
    with ProcessPoolExecutor(max_workers=min(multiprocessing.cpu_count(), 8)) as executor:
        results = executor.map(process_sample, sample_dirs, sampleIDs, 
                               [kmer_length] * len(sampleIDs),
                               [hammer_to_feature] * len(sampleIDs),
                               [feature_to_genome] * len(sampleIDs),
                               [feature_to_role] * len(sampleIDs))

    for sampleID, genome_counts, genome_role_counts in results:
        for genome_id, role_counts in genome_role_counts.items():
            num_roles = len(role_counts)
            if num_roles >= len(roles) * args.role_fraction:
                genome_name = genome_id_to_name.get(genome_id, 'Unknown sp.')
                score = genome_counts[genome_id]
                all_results.append([sampleID, genome_id, genome_name, score, num_roles])

    # **Sorting first by sampleID (ascending), then by score (descending)**
    all_results.sort(key=lambda x: (x[0], -x[3]))

    writer = csv.writer(sys.stdout, delimiter='\t', lineterminator='\n')
    headers = ['sampleID', 'genome_id', 'genome_name', 'score', 'num_roles']
    writer.writerow(headers)
    writer.writerows(all_results)

if __name__ == '__main__':
    main()
