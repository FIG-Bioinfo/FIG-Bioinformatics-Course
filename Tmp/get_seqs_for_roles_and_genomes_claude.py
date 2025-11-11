#!/usr/bin/env python3
"""
Retrieve DNA or protein sequences for specified roles across specified genomes.
Uses PATRIC/BV-BRC command-line tools to fetch sequences.
"""

import argparse
import subprocess
import sys
import csv
from io import StringIO


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Retrieve sequences for roles across genomes'
    )
    parser.add_argument(
        '-T', '--type',
        required=True,
        choices=['dna', 'protein'],
        help='Sequence type to retrieve'
    )
    parser.add_argument(
        '-G', '--genome-list',
        required=True,
        dest='genome_list',
        help='TSV file containing genome IDs'
    )
    parser.add_argument(
        '-R', '--role-list',
        required=True,
        dest='role_list',
        help='TSV file containing role names'
    )
    return parser.parse_args()


def load_roles(role_file):
    """Load role names from TSV file."""
    roles = []
    try:
        with open(role_file, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            if 'role_name' not in reader.fieldnames:
                print(f"ERROR: 'role_name' column not found in {role_file}", 
                      file=sys.stderr)
                sys.exit(1)
            for row in reader:
                roles.append(row['role_name'])
    except Exception as e:
        print(f"ERROR reading role file {role_file}: {e}", file=sys.stderr)
        sys.exit(1)
    return roles


def count_genomes(genome_file):
    """Count number of genomes in the genome list file."""
    try:
        with open(genome_file, 'r') as f:
            # Skip header, count remaining lines
            return sum(1 for _ in f) - 1
    except Exception as e:
        print(f"ERROR reading genome file {genome_file}: {e}", file=sys.stderr)
        sys.exit(1)


def filter_exact_matches(cmd1_output, role):
    """
    Filter cmd1 output to only include exact matches to role.
    Returns filtered TSV as string.
    """
    lines = cmd1_output.strip().split('\n')
    if not lines:
        return ""
    
    # Parse header to find feature.product column
    header = lines[0]
    header_fields = header.split('\t')
    
    try:
        product_col = header_fields.index('feature.product')
    except ValueError:
        print(f"ERROR: 'feature.product' column not found in output", 
              file=sys.stderr)
        sys.exit(1)
    
    # Filter lines for exact matches
    filtered = [header]
    for line in lines[1:]:
        if not line.strip():
            continue
        fields = line.split('\t')
        if len(fields) > product_col and fields[product_col] == role:
            filtered.append(line)
    
    return '\n'.join(filtered)


def process_role(role, genomes_file, seq_type):
    """
    Process a single role: fetch features and sequences.
    Returns tuple of (sequences_string, sequence_count).
    """
    print(f"Processing role: {role}", file=sys.stderr)
    
    # Command 1: Get genome features
    cmd1 = [
        'p3-get-genome-features',
        '--selective',
        '--input', genomes_file,
        '--col', 'genome_id',
        '--eq', f"product,'{role}'",
        '--attr', 'patric_id,product'
    ]
    
    try:
        result1 = subprocess.run(
            cmd1,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"ERROR in p3-get-genome-features: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR executing p3-get-genome-features: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Print cmd1 stderr to our stderr
    if result1.stderr:
        print(result1.stderr, file=sys.stderr, end='')
    
    # Filter for exact matches
    filtered_output = filter_exact_matches(result1.stdout, role)
    
    if not filtered_output or filtered_output == filtered_output.split('\n')[0]:
        # Only header or empty, no sequences to fetch
        return "", 0
    
    # Command 2: Get feature sequences
    cmd2 = [
        'p3-get-feature-sequence',
        '--col', 'feature.patric_id',
        f'--{seq_type}'
    ]
    
    try:
        result2 = subprocess.run(
            cmd2,
            input=filtered_output,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"ERROR in p3-get-feature-sequence: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR executing p3-get-feature-sequence: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Print cmd2 stderr to our stderr
    if result2.stderr:
        print(result2.stderr, file=sys.stderr, end='')
    
    # Count sequences (FASTA entries start with '>')
    seq_count = result2.stdout.count('\n>')
    if result2.stdout.startswith('>'):
        seq_count += 1
    
    return result2.stdout, seq_count


def main():
    args = parse_arguments()
    
    # Load roles
    roles = load_roles(args.role_list)
    
    # Count genomes
    genome_count = count_genomes(args.genome_list)
    
    # Process each role
    total_sequences = 0
    for role in roles:
        sequences, seq_count = process_role(role, args.genome_list, args.type)
        if sequences:
            print(sequences, end='')
        total_sequences += seq_count
    
    # Report summary
    print(f"\nProcessed {len(roles)} roles", file=sys.stderr)
    print(f"Processed {genome_count} genomes", file=sys.stderr)
    print(f"Retrieved {total_sequences} FASTA sequences", file=sys.stderr)


if __name__ == '__main__':
    main()
