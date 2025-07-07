import sys
import argparse
import os
import re
import csv
import multiprocessing
import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
from Bio import SeqIO
from Bio.Seq import reverse_complement

def parse_hammers(hammers_file):
    """Parses the hammers file and returns mappings for analysis."""
    hammer_to_feature = {}
    feature_to_genome = {}
    feature_to_role = {}
    roles = set()

    with open(hammers_file, 'r', buffering=2**16) as f:  # Reduce buffering to 64KB
        reader = csv.DictReader(f, delimiter='\t')
        
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

    with open(genome_names_file, 'r', buffering=2**16) as f:  # Reduce buffering
        reader = csv.DictReader(f, delimiter='\t')

        for row in reader:
            genome_id_to_name[row['genome_id']] = row['genome_name']
    
    return genome_id_to_name

def process_fasta_file(fasta_file, kmer_length, hammer_to_feature, feature_to_genome, feature_to_role):
    """Processes a FASTA file lazily (streaming) to avoid high memory usage."""
    genome_counts = {}
    genome_role_counts = {}

    with open(fasta_file, 'r', buffering=2**16) as f:  # Reduce buffer size
        for record in SeqIO.parse(f, 'fasta'):
            sequence = str(record.seq).lower()
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
    """Processes all reads for a given sample while keeping memory usage low."""
    genome_counts = {}
    genome_role_counts = {}

    fasta_files = [f for f in os.listdir(sample_dir) if re.match(rf"{sampleID}_[12]_.*", f)]
    left_reads = [os.path.join(sample_dir, f) for f in fasta_files if re.match(rf"{sampleID}_1_.*", f)]
    right_reads = [os.path.join(sample_dir, f) for f in fasta_files if re.match(rf"{sampleID}_2_.*", f)]

    all_reads = left_reads + right_reads

    for fasta_file in all_reads:
        file_counts, file_role_counts = process_fasta_file(fasta_file, kmer_length, hammer_to_feature, feature_to_genome, feature_to_role)

        for genome_id, count in file_counts.items():
            genome_counts[genome_id] = genome_counts.get(genome_id, 0) + count
        for genome_id, role_dict in file_role_counts.items():
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
    with ProcessPoolExecutor(max_workers=min(multiprocessing.cpu_count(), 4)) as executor:  # Reduce parallelism
        with tqdm.tqdm(total=len(sampleIDs), file=sys.stderr, desc="Processing Samples") as pbar:
            futures = {executor.submit(process_sample, sample_dirs[i], sampleIDs[i], kmer_length, 
                                       hammer_to_feature, feature_to_genome, feature_to_role): sampleIDs[i]
                       for i in range(len(sampleIDs))}

            for future in as_completed(futures):
                sampleID, genome_counts, genome_role_counts = future.result()
                for genome_id, role_counts in genome_role_counts.items():
                    num_roles = len(role_counts)
                    if num_roles >= len(roles) * args.role_fraction:
                        genome_name = genome_id_to_name.get(genome_id, 'Unknown sp.')
                        score = genome_counts[genome_id]
                        all_results.append([sampleID, genome_id, genome_name, score, num_roles])
                pbar.update(1)

    all_results.sort(key=lambda x: (x[0], -x[3]))
    writer = csv.writer(sys.stdout, delimiter='\t', lineterminator='\n')
    writer.writerow(['sampleID', 'genome_id', 'genome_name', 'score', 'num_roles'])
    writer.writerows(all_results)

if __name__ == '__main__':
    main()
