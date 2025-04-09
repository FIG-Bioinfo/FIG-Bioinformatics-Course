import sys

def interactive_exercise(data_type=None):
    valid_data_types = ["boolean", "integer", "float", "string", "list", "set", "tuple", "dictionary"]
    python_data_types = ["int", "float", "complex", "bool", "str", "list", "tuple", "range", "dict", "set", "frozenset", "bytes", "bytearray", "memoryview"]

    if data_type is None or data_type.lower() == "types":
        print("\nDatatypes described by this program; "
            + "invoke this program with a datatype name\n"
            + "for a description of that datatype, plus examples.")
        for dt in valid_data_types:
            print(f"- {dt.capitalize()}")
        return

    data_type = data_type.lower()

    if data_type not in valid_data_types:
        if data_type in python_data_types:
            print("This datatype is valid, but will not be discussed within this exercise.")
        else:
            print("This datatype is not a valid python datatype")
        return

    def explain_and_example(data_type, description, example):
        print(f"\n{data_type.capitalize()}")
        print(description)
        input("Press Enter to see an example...")
        print(example)

    if data_type == "boolean":
        explain_and_example(
            "Boolean",
            "Booleans represent two values: True or False.\nUseful for conditional checks.",
            """
# Example 1: Checking if a DNA sequence is valid (returns True)
def is_valid_dna(sequence):
    valid_nucleotides = {'A', 'T', 'C', 'G'}
    for nucleotide in sequence:
        if nucleotide not in valid_nucleotides:
            return False
    return True

dna_sequence = "ATCGTTAGC"
is_valid = is_valid_dna(dna_sequence)
print(f"Is the DNA sequence valid? {is_valid}")  # Output: True

# Example 2: Checking if a DNA sequence is valid (returns False)
invalid_dna_sequence = "ATCGTTAGX"
is_valid = is_valid_dna(invalid_dna_sequence)
print(f"Is the DNA sequence valid? {is_valid}")  # Output: False
""")

    elif data_type == "integer":
        explain_and_example(
            "Integer",
            "Integers represent whole numbers.\nUseful for counting or indexing.",
            """
# Example: Counting the number of nucleotides in a DNA sequence
dna_sequence = "ATCGTTAGC"
nucleotide_count = len(dna_sequence)
print(f"The number of nucleotides: {nucleotide_count}")  # Output: 9
""")

    elif data_type == "string":
        explain_and_example(
            "String",
            "Strings represent sequences of characters.\nUseful for storing textual data like DNA sequences.",
            """
# Example: Reverse complement of a DNA sequence
def reverse_complement(sequence):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement[nucleotide] for nucleotide in reversed(sequence))

dna_sequence = "ATCG"
reverse_complement_sequence = reverse_complement(dna_sequence)
print(f"Reverse complement: {reverse_complement_sequence}")  # Output: CGAT
""")

    elif data_type == "list":
        explain_and_example(
            "List",
            "Lists represent ordered collections of items.\n"
            + "Useful for storing sequences of data.\n"
            + "The same data-item can appear in a list more than once.",
            """
# Example: Storing multiple DNA sequences
dna_sequences = ["ATCG", "CGTA", "TTAGC", "CGTA"]
print(dna_sequences)   # Output: ["ATCG", "CGTA", "TTAGC", "CGTA"]

for index, sequence in enumerate(dna_sequences):
    print(f"{index}: {sequence}")
'''
Outputs:
0: ATCG
1: CGTA
2: TTAGC
3: CGTA
'''
""")

    elif data_type == "set":
        explain_and_example(
            "Set",
            "Sets represent unordered collections of unique items.\n"
            + "Useful for ensuring no duplicates.\n"
            + "Unlike lists, no matter how many times you add the same item to a set,\n"
            + "it will only appear in the set once.",
            """
# Example 1: Lists vs. Sets
dna_list = ["ATCG", "CGTA", "TTAGC", "CGTA"]
dna_set  = {"ATCG", "CGTA", "TTAGC", "CGTA"}
print(f"dna_list:\\t{dna_list}\\n"
      + f"dna_set:\\t{dna_set}\\n")
# Output:
dna_list:   ['ATCG', 'CGTA', 'TTAGC', 'CGTA']
dna_set:    {'CGTA', 'TTAGC', 'ATCG'}

# Example 2: Finding unique nucleotides in a DNA sequence
dna_sequence = "ATTATA"
unique_nucleotides = set(dna_sequence)
print(f"Unique nucleotides: {unique_nucleotides}")  # Output: {'A', 'T'}

dna_sequence = "ATCGATTG"
unique_nucleotides = set(dna_sequence)
print(f"Unique nucleotides: {unique_nucleotides}")  # Output: {'A', 'C', 'G', 'T'}
""")

    elif data_type == "tuple":
        explain_and_example(
            "Tuple",
            "Tuples represent ordered collections of items that are immutable.\n"
            + "Useful for fixed collections of data.",
            """
# Example: Storing a DNA sequence and its length
dna_info = ("ATCG", 4)
print(dna_info)    # Output: ('ATCG', 4)
sequence, length = dna_info
print(f"DNA sequence: {sequence}, Length: {length}")  # Output: DNA sequence: ATCG, Length: 4
""")

    elif data_type == "dictionary":
        explain_and_example(
            "Dictionary",
            "Dictionaries represent collections of key-value pairs.\n"
            + "Useful for mapping relationships.",
            """
# Example: Mapping nucleotide counts in a DNA sequence
def count_nucleotides(sequence):
    counts = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
    for nucleotide in sequence:
        counts[nucleotide] += 1
    return counts

dna_sequence = "ATCGATTG"
nucleotide_counts = count_nucleotides(dna_sequence)
print(f"Nucleotide counts: {nucleotide_counts}")  # Output: {'A': 3, 'T': 3, 'C': 1, 'G': 1}
""")

    elif data_type == "float":
        explain_and_example(
            "Float",
            """Floats are numbers with decimals, enabling accurate representation of quantities
that are not whole numbers, such as scientific measurements, percentages, or averages.""",
            """
# Example: Calculating the molecular weight of a DNA sequence
def calculate_molecular_weight(sequence):
    molecular_weights = {'A': 331.2, 'T': 322.2, 'C': 307.2, 'G': 347.2}
    return sum(molecular_weights[nucleotide] for nucleotide in sequence)

dna_sequence = "ATCG"
molecular_weight = calculate_molecular_weight(dna_sequence)
print(f"Molecular weight: {molecular_weight:.2f} g/mol")  # Output: 1307.80 g/mol
""")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        data_type = sys.argv[1]
        interactive_exercise(data_type)
    else:
        interactive_exercise()
