import argparse
import sys
import re
import csv
from Bio import SeqIO
from Bio.Seq import reverse_complement

def parse_hammers(hammers_file):
    hammer_to_feature = {}
    feature_to_genome = {}
    feature_to_role = {}
    roles = set()

    with open(hammers_file, 'r') as f:
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

    # Print debugging information to STDERR
    print(f"Kmer length: {kmer_length}", file=sys.stderr)
    print(f"Number of roles found: {len(roles)}", file=sys.stderr)
    print(f"Number of entries in hammer_to_feature: {len(hammer_to_feature)}", file=sys.stderr)
    print(f"Number of entries in feature_to_genome: {len(feature_to_genome)}", file=sys.stderr)
    print(f"Number of entries in feature_to_role: {len(feature_to_role)}", file=sys.stderr)

    return kmer_length, roles, hammer_to_feature, feature_to_genome, feature_to_role

def parse_genome_names(genome_names_file):
    genome_id_to_name = {}
    with open(genome_names_file, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        headers = reader.fieldnames

        if 'genome_id' not in headers or 'genome_name' not in headers:
            raise ValueError("The genome-names file must contain 'genome_id' and 'genome_name' columns.")

        for row in reader:
            genome_id_to_name[row['genome_id']] = row['genome_name']

    # Print debugging information to STDERR
    print(f"Number of entries in genome_id_to_name: {len(genome_id_to_name)}", file=sys.stderr)

    return genome_id_to_name

def main():
    parser = argparse.ArgumentParser(description="program for multirole hammer analysis. Reads DNA FASTA from STDIN. Writes TSV report to STDOUT.")
    parser.add_argument('-H', '--hammers', required=True, help="Path to the hammers TSV file.")
    parser.add_argument('-G', '--genome-names', required=True, help="Path to the genome names TSV file.")
    parser.add_argument('-F', '--role-fraction', type=float, default=0.8, help="Minimum fraction of roles for genome inclusion (default: 0.8).")

    args = parser.parse_args()

    try:
        kmer_length, roles, hammer_to_feature, feature_to_genome, feature_to_role = parse_hammers(args.hammers)
        genome_id_to_name = parse_genome_names(args.genome_names)

        genome_counts = {}
        genome_role_counts = {}

        fasta_record_count = 0
        total_dna_characters = 0
        progress_dots = 0  # Track number of dots in current row

        for record in SeqIO.parse(sys.stdin, 'fasta'):
            sequence = str(record.seq).lower()
            rev_comp_sequence = reverse_complement(sequence)

            fasta_record_count += 1
            total_dna_characters += len(sequence)

            # Print progress indicator after every 1 million sequences
            if fasta_record_count % 1_000_000 == 0:
                print(".", end="", file=sys.stderr, flush=True)
                progress_dots += 1

                # Print a newline after 100 dots
                if progress_dots % 100 == 0:
                    print(file=sys.stderr)
                    progress_dots = 0

            for i in range(len(sequence) - kmer_length + 1):
                kmer = sequence[i:i + kmer_length]
                if kmer in hammer_to_feature:
                    feature_id = hammer_to_feature[kmer]
                    genome_id = feature_to_genome[feature_id]
                    role = feature_to_role[feature_id]

                    genome_counts[genome_id] = genome_counts.get(genome_id, 0) + 1

                    if genome_id not in genome_role_counts:
                        genome_role_counts[genome_id] = {}
                    genome_role_counts[genome_id][role] = genome_role_counts[genome_id].get(role, 0) + 1

                kmer = rev_comp_sequence[i:i + kmer_length]
                if kmer in hammer_to_feature:
                    feature_id = hammer_to_feature[kmer]
                    genome_id = feature_to_genome[feature_id]
                    role = feature_to_role[feature_id]

                    genome_counts[genome_id] = genome_counts.get(genome_id, 0) + 1

                    if genome_id not in genome_role_counts:
                        genome_role_counts[genome_id] = {}
                    genome_role_counts[genome_id][role] = genome_role_counts[genome_id].get(role, 0) + 1

        # Print a newline if progress dots are not at a full row of 100
        if progress_dots % 100 != 0:
            print(file=sys.stderr)

        total_roles = len(roles)
        output = []

        for genome_id, role_counts in genome_role_counts.items():
            num_roles = len(role_counts)
            if num_roles >= total_roles * args.role_fraction:
                genome_name = genome_id_to_name.get(genome_id, 'Unknown sp.')
                if genome_name == 'Unknown sp.':
                    print(f"Warning: genome_id {genome_id} not found in genome-names file.", file=sys.stderr)

                score = genome_counts[genome_id]
                output.append((genome_id, genome_name, score, num_roles))

        output.sort(key=lambda x: x[2], reverse=True)

        writer = csv.writer(sys.stdout, delimiter='\t')
        headers = ['genome_id', 'genome_name', 'score']
        if total_roles > 1:
            headers.append('num_roles')
        writer.writerow(headers)

        for row in output:
            writer.writerow(row)

        # Print FASTA processing stats to STDERR
        print(f"Number of input FASTA records processed: {fasta_record_count}", file=sys.stderr)
        print(f"Total number of DNA characters read from FASTA sequences: {total_dna_characters}", file=sys.stderr)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
