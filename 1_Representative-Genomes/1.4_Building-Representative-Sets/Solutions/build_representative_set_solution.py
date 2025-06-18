########################################################################
# Prompt that generated 'build_representative_set_solution.py',
# after first attaching 'Definitions.html'
"""
I will now give you a description of a command-line interface and
program called `build_representative_set.py` that will compute a
"set of representative sequences" (RepGen set) using the "Stingy Addition" 
algorithm as defined in the uploaded definitions-file.

The script should accept the following mandatory command-line
arguments, in both long-form and the specified short-form:

* Kmer-length  (integer, short argument-name '-K')
* Sim          (similarity threshold, short argument-name '-S')
* input FASTA-file    (filename, short argument-name '-F')
* output RepSeq-file  (filename, short argument-name '-R')
* output Genomes-file (filename, short argument-name '-G')

The measure of similarity to be used is "Number of Kmers in common".

The program should use BioPython to read the FASTA-file.
The first nonwhitespace portion of each FASTA identifier is a "feature-ID",
while the remainder is the "genome-name".
Feature-IDs have the format 'fig|X.Y.peg.Z', where 'X', 'Y', and 'Z' are integers,
and the portions 'fig|' and '.peg.' are literal substrings, not variables.
The subpattern 'X.Y' within the feature-ID is a "genome-ID";
you may extract this subpattern using a regular expression.
Return a dictionary that maps feature-IDs to genome-IDs,
a dictionary that maps genome-IDs to genome-names,
and a list of (feature-ID, sequence) pairs.

The main body of the program should construct a subset of the
input sequence list that satisfies the provided definition
of a "Representative Set" (RepGen set).

When you are done, please write out the representative set
to the RepSeq-file in FASTA format, where the FASTA heading
has the form "genome-ID genome-name".
Please also write a tab-separated file of representative-set 
genome-IDs and genome-names to the genome-names file,
with headings 'genome_id' and 'genome_name'. 
Then exit the program.
"""
########################################################################
# Pseudocode for 'build_representative_set_solution.py'
"""
# Main Execution
START

DEFINE parse_arguments
    PARSE command-line arguments for Kmer-length (-K), similarity threshold (-S), input FASTA file (-F), output RepSeq file (-R), and output Genomes file (-G)
    RETURN parsed arguments

DEFINE parse_genome_data(fasta_file)
    INITIALIZE dictionaries:
        feature_to_genome - map from feature-ID to genome-ID
        genome_to_name - map from genome-ID to genome-name
    INITIALIZE list:
        feature_sequences - list of (feature-ID, sequence) pairs
    SET regex pattern to extract genome-ID from feature-ID
    
    FOR each record in fasta_file
        SET header to record's description
        SET sequence to record's sequence as a string
        SPLIT header into feature_id (first portion) and genome_name (remainder)
        
        IF pattern matches feature_id
            SET genome_id using matched portion
            MAP feature_id to genome_id in feature_to_genome
            MAP genome_id to genome_name in genome_to_name
            ADD (feature_id, sequence) to feature_sequences
            
    RETURN feature_to_genome, genome_to_name, feature_sequences

DEFINE extract_kmers(sequence, k)
    RETURN set of all substrings of length k in sequence

DEFINE compute_repgen_set(feature_sequences, feature_to_genome, kmer_length, sim_threshold)
    INITIALIZE genome_kmers - map from genome-ID to unique set of K-mers
    INITIALIZE repgen_set - set of representative genome-IDs
    
    FOR each (feature_id, sequence) in feature_sequences
        SET genome_id using feature_to_genome[feature_id]
        ADD K-mers from sequence to genome_kmers[genome_id]
        
    FOR each genome_id, kmers in genome_kmers
        SET is_representative to TRUE
        FOR each repgen_id in repgen_set
            SET common_kmers as intersection of genome_kmers[genome_id] and genome_kmers[repgen_id]
            IF size of common_kmers is greater than or equal to sim_threshold
                SET is_representative to FALSE
                BREAK inner loop
        IF is_representative is TRUE
            ADD genome_id to repgen_set
            
    RETURN repgen_set

DEFINE write_output(repgen_set, genome_to_name, feature_sequences, feature_to_genome, repseq_file, genomes_file)
    OPEN repseq_file for writing
        FOR each (feature_id, sequence) in feature_sequences
            SET genome_id using feature_to_genome[feature_id]
            IF genome_id in repgen_set
                SET genome_name from genome_to_name[genome_id]
                WRITE ">genome_id genome_name" and sequence to repseq_file
    
    OPEN genomes_file for writing
        WRITE header "genome_id\tgenome_name"
        FOR each genome_id in repgen_set
            SET genome_name from genome_to_name[genome_id]
            WRITE "genome_id\tgenome_name" to genomes_file

MAIN
    CALL parse_arguments to retrieve arguments
    CALL parse_genome_data(args.fasta_file) to retrieve feature_to_genome, genome_to_name, feature_sequences
    CALL compute_repgen_set(feature_sequences, feature_to_genome, args.kmer_length, args.similarity_threshold) to retrieve repgen_set
    CALL write_output(repgen_set, genome_to_name, feature_sequences, feature_to_genome, args.repseq_file, args.genomes_file)
END
"""

########################################################################
# Code for 'build_representative_set_solution.py'
#!/usr/bin/env python

import argparse
import re
from Bio import SeqIO
from collections import defaultdict

# Function to parse the input arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Compute a representative set of sequences (RepGen set) using the Stingy Addition algorithm.")
    parser.add_argument("-K", "--kmer-length", type=int, required=True, help="Length of K-mers to consider.")
    parser.add_argument("-S", "--similarity-threshold", type=int, required=True, help="Similarity threshold (Sim).")
    parser.add_argument("-F", "--fasta-file", type=str, required=True, help="Input FASTA file containing sequences.")
    parser.add_argument("-R", "--repseq-file", type=str, required=True, help="Output file for the representative sequences in FASTA format.")
    parser.add_argument("-G", "--genomes-file", type=str, required=True, help="Output file for genome-IDs and genome-names in tab-separated format.")
    return parser.parse_args()

# Function to parse genome feature IDs and names from FASTA headers
def parse_genome_data(fasta_file):
    feature_to_genome = {}       # Maps feature-ID to genome-ID
    genome_to_name = {}          # Maps genome-ID to genome-name
    feature_sequences = []       # List of (feature-ID, sequence) pairs
    
    pattern = re.compile(r'^fig\|(\d+\.\d+)\.peg\.\d+')
    
    for record in SeqIO.parse(fasta_file, "fasta"):
        header = record.description
        sequence = str(record.seq)
        
        # Split header into feature-ID and genome-name
        feature_id = header.split()[0]
        genome_name = ' '.join(header.split()[1:])
        
        # Extract genome-ID using regex
        match = pattern.match(feature_id)
        if match:
            genome_id = match.group(1)
            feature_to_genome[feature_id] = genome_id
            genome_to_name[genome_id] = genome_name
            feature_sequences.append((feature_id, sequence))
    
    return feature_to_genome, genome_to_name, feature_sequences

# Function to extract K-mers from a sequence
def extract_kmers(sequence, k):
    return {sequence[i:i+k] for i in range(len(sequence) - k + 1)}

# Main function to compute the representative set using Stingy Addition
def compute_repgen_set(feature_sequences, feature_to_genome, kmer_length, sim_threshold):
    genome_kmers = defaultdict(set)   # Maps genome-ID to set of unique K-mers
    repgen_set = set()                # Set of representative genome-IDs

    # Step 1: Compute K-mers for each genome
    for feature_id, sequence in feature_sequences:
        genome_id = feature_to_genome[feature_id]
        genome_kmers[genome_id].update(extract_kmers(sequence, kmer_length))
    
    # Step 2: Construct the RepGen set
    for genome_id, kmers in genome_kmers.items():
        is_representative = True
        for repgen_id in repgen_set:
            # Measure similarity by counting common K-mers
            common_kmers = genome_kmers[genome_id].intersection(genome_kmers[repgen_id])
            if len(common_kmers) >= sim_threshold:
                is_representative = False
                break
        if is_representative:
            repgen_set.add(genome_id)

    return repgen_set

# Function to write output files
def write_output(repgen_set, genome_to_name, feature_sequences, feature_to_genome, repseq_file, genomes_file):
    # Write the representative sequences to the FASTA file
    with open(repseq_file, 'w') as fasta_out:
        for feature_id, sequence in feature_sequences:
            genome_id = feature_to_genome[feature_id]
            if genome_id in repgen_set:
                genome_name = genome_to_name[genome_id]
                fasta_out.write(f">{genome_id} {genome_name}\n{sequence}\n")
    
    # Write the genome-IDs and genome-names to the genomes file
    with open(genomes_file, 'w') as genome_out:
        genome_out.write("genome_id\tgenome_name\n")
        for genome_id in repgen_set:
            genome_name = genome_to_name[genome_id]
            genome_out.write(f"{genome_id}\t{genome_name}\n")

# Main execution
if __name__ == "__main__":
    args = parse_arguments()
    feature_to_genome, genome_to_name, feature_sequences = parse_genome_data(args.fasta_file)
    repgen_set = compute_repgen_set(feature_sequences, feature_to_genome, args.kmer_length, args.similarity_threshold)
    write_output(repgen_set, genome_to_name, feature_sequences, feature_to_genome, args.repseq_file, args.genomes_file)
