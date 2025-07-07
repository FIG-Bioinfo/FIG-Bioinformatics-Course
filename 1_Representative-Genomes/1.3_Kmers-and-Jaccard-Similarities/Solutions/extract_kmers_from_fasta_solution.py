#!/usr/bin/env python

import argparse
import sys
from Bio import SeqIO

def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract Kmers from a FASTA file.")
    parser.add_argument("-K", "--Kmer", type=int, required=True, help="Length of the Kmer")
    parser.add_argument("-t", "--type", choices=['dna', 'protein'], help="Type of sequence (dna or protein)")
    return parser.parse_args()

def is_valid_dna(kmer):
    valid_dna_chars = set("acgt")
    return all(char in valid_dna_chars for char in kmer)

def is_valid_protein(kmer):
    valid_protein_chars = set("ACDEFGHIKLMNPQRSTVWY")
    return all(char in valid_protein_chars for char in kmer)

def process_sequences(kmer_length, seq_type):
    num_sequences = 0
    num_valid_kmers = 0
    num_invalid_kmers = 0

    for record in SeqIO.parse(sys.stdin, "fasta"):
        num_sequences += 1
        sequence_id = record.id
        sequence = str(record.seq)

        if seq_type == "dna":
            sequence = sequence.lower()
        elif seq_type == "protein":
            sequence = sequence.upper()

        for i in range(len(sequence) - kmer_length + 1):
            kmer = sequence[i:i + kmer_length]

            if seq_type == "dna" and not is_valid_dna(kmer):
                print(f"{kmer}\t{sequence_id}", file=sys.stderr)
                num_invalid_kmers += 1
            elif seq_type == "protein" and not is_valid_protein(kmer):
                print(f"{kmer}\t{sequence_id}", file=sys.stderr)
                num_invalid_kmers += 1
            else:
                print(f"{kmer}\t{sequence_id}")
                num_valid_kmers += 1

    print(f"Sequences read: {num_sequences}", file=sys.stderr)
    print(f"Kmers written to STDOUT: {num_valid_kmers}", file=sys.stderr)
    print(f"Invalid Kmers found: {num_invalid_kmers}", file=sys.stderr)

def main():
    args = parse_arguments()

    if args.Kmer <= 0:
        print("Error: Kmer length must be a positive integer.", file=sys.stderr)
        sys.exit(1)

    process_sequences(args.Kmer, args.type)

if __name__ == "__main__":
    main()
