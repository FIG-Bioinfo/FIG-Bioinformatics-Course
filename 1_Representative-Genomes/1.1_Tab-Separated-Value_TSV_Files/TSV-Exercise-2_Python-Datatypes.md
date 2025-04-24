# Tab-Separated-Value File Exercise 2 - Python Datatypes

Objective: Recognize Python Datatypes

The programs that you will be creating in this course will be written in the `Python` computer-language.
In this exercise, we will explore the different types of data that Python uses within its code. Most of these data types are common to all programming languages.

The program `python_datatypes_interactive_exercise.py` has been created to help you explore these data types while also practicing the use of the command line. Before you begin, ensure that you have a Terminal window open that uses the `bash` profile (macOS and LINUX) or `GitBash` (Windows) profile.
If you are unsure of how to find this setting, please refer to the "Download Instructions" for Git to make it the default setting for VSCode.

## Materials: 
[Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)


```
FIG-Bioinformatics-Course/
├── 1_Representative-Genomes/
│   └── 1.1_Tab-Separated-Value_(TSV)_Files/
│       └── TSV-Exercise-Exercise-2_Python-Datatypes.md  (you are here)
└── Scripts/
    ├── python_datatypes_interactive_exercise.py
    └── dictionary_interactive_exercise.py 
```


## Exercises: 

Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then go to the terminal-window if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.


1. The following is the list of data types that we will be discussing in this lesson. Ask Grimoire to explain each type and its uses to you. Make sure you specify that they are Python Datatypes.

    * Boolean
    * Integer
    * Float
    * String
    * List
    * Set
    * Tuple
    * Dictionary

2. A program called `python_datatypes_interactive_exercise.py`
has been provided in the `Scripts` directory that will return
the above list, and that for each datatype will provide a
short definition for that type of data, followed by a code example
that uses that type of data within a bioinformatics context.
You can run this program at any time during the course
if you need to refresh your memory regarding a particular datatype
and how it is used within the code.
If the example provided within any section of this program is not clear
to you, you can paste that section into Grimoire and ask it to explain
the code to you "line-by-line".
Likewise, if what any line does is not clear to you,
ask Grimoire to explain that line to you "step-by-step".

3. Three of the most basic data-types are `boolean`, `integer`, and `string`.
More complex data-types can be constructed from these basic data-types.
Run the program `python_datatypes_interactive_exercise.py` for each of these three basic datatypes to see examples of the data that they contain:

* `python Scripts/python_datatypes_interactive_exercise.py boolean`

* `python Scripts/python_datatypes_interactive_exercise.py integer`

* `python Scripts/python_datatypes_interactive_exercise.py string`

**NOTE:** The words that follow a program's name are called `arguments`.
The `arguments` of a program are passed to the program to control its behavior or to provide it with necessary information.
If you are unfamiliar with the concept of a "program argument",
please ask Grimoire to explain it to you.

4. Now run the program `python_datatypes_interactive_exercise.py`, with an argument of `list`.

**Hint:** You can access and move back and forward through the previous commands you have entered onto the command line by using the up-arrow and down-arrow keys on your keyboard, and you can edit a previous command before resubmitting it. This trick will save you lots of typing!

Notice that one of the list examples has a duplicated data item,
and that both instances of the data-item are printed out. 
    

5. Next invoke the program with an argument of `set`.
In "Example 1", see if you can spot the difference between a `list` and a `set`. 
Notice that this time, no data is duplicated.
Notice also that the `list` is displayed with square brackets,
while the `set` is displayed with curly brackets.
"Example 2" shows that a list can be converted to a set using the `set()` function.

6. Ask Grimoire to explain to you the difference between a `list`, a `set`, and a `tuple`. The tuple's main feature is that it is immutable. Ask Grimoire to explain to you what "immutable data" is and why it is important to use within programming code.

7. Print the `tuple` example by running the `python_datatypes_interactive_exercise.py` program with the datatype-argument `tuple`.

8. The last datatype is called a `dictionary`. This datatype acts like a traditional dictionary because you can "look up" data by using a "key" that will return an associated "value". For our purposes, the "key" in this sense is a string or an integer that provides a "name" or "identifier" that can be used to refer to its associated data-value. (Python does allow some data-types besides strings and integers to be used as "keys", but the rules governing keys are complicated, and will not be needed for this course.) The value associated with a key can be any python datatype, including sets, lists, or even another dictionary, which allows one to build up an arbitrariy complex data-structure. Ask Grimoire to explain to you what is meant by "key-value" pairs within a python dictionary. 

9. Print the dictionary by calling the `python_datatypes_interactive_exercise.py` program on the datatype `dictionary`. Notice how each "entry" (i.e., key-value pair) is unique.

IMPORTANT: Key-value pairs are entered into a `dictionary` by entering the "key" and the "value" separated by a colon. Each "key" can only occur in a dictionary once, but nothing restricts the associated values. For example, in a dictionary listing types of food, the keys "apple" and "pear" can both have the value of "fruit". Example: `{"apple": "fruit", "pear": "fruit", "carrot": "vegetable"}`.
Reentering an old key with a new value will update the key's value.

10. Because "dictionaries" are such an important tool for writing programs, we have included a separate interactive exercise on use of dictionaries. Please launch this exercise as follows:
```
    python3 Scripts/dictionary_interactive_exercise.py
```
The execise will welcome you, provide a brief description of what a "dictionary" is, and then prompt you regarding whether you wish to `add a key-value pair`, `delete a key`, or `quit`. After each operation that you enter, the program will display the new contents of the dictionary. Please experiment by adding an assortment of key-value pairs, deleting keys (and their associated values),
and re-adding old keys with new values, and observe how the contents of the dictionary changes after each operation. Once you think you have a good understanding of how the "add" and "delete" operations alter the contents of the dictionary, you can leave the exercise by typing `q` or `quit`.

We encourage you to open the program `Scripts/dictionary_interactive_exercise.py` and have a look inside. If there is any part of the program that you feel you don't understand, you can paste it into Grimoire and ask Grimoire to explain the code to you "line-by-line". If there are parts that you feel you still don't understand, ask Grimoire to explain those lines "step-by-step".

## Solution Check instructions:
If you are successful, the program should return output that matches the following.

### 3. Booleans, Integers, Floats, and Strings
```
Boolean
Booleans represent two values: True or False.
Useful for conditional checks.
Press Enter to see an example...

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
```

```
Integer
Integers represent whole numbers.
Useful for counting or indexing.
Press Enter to see an example...

# Example: Counting the number of nucleotides in a DNA sequence
dna_sequence = "ATCGTTAGC"
nucleotide_count = len(dna_sequence)
print(f"The number of nucleotides: {nucleotide_count}")  # Output: 9
```

```
Float
Floats are numbers with decimals, enabling accurate representation of quantities
that are not whole numbers, such as scientific measurements, percentages, or averages.
Press Enter to see an example...

# Example: Calculating the molecular weight of a DNA sequence
def calculate_molecular_weight(sequence):
    molecular_weights = {'A': 331.2, 'T': 322.2, 'C': 307.2, 'G': 347.2}
    return sum(molecular_weights[nucleotide] for nucleotide in sequence)

dna_sequence = "ATCG"
molecular_weight = calculate_molecular_weight(dna_sequence)
print(f"Molecular weight: {molecular_weight:.2f} g/mol")  # Output: 1307.80 g/mol
```

```
String
Strings represent sequences of characters.
Useful for storing textual data like DNA sequences.
Press Enter to see an example...

# Example: Reverse complement of a DNA sequence
def reverse_complement(sequence):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement[nucleotide] for nucleotide in reversed(sequence))

dna_sequence = "ATCG"
reverse_complement_sequence = reverse_complement(dna_sequence)
print(f"Reverse complement: {reverse_complement_sequence}")  # Output: CGAT
```

### 4. Lists
```
List
Lists represent ordered collections of items.
Useful for storing sequences of data.
The same data-item can appear in a list more than once.
Press Enter to see an example...

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
```

### 5. Sets
```
Set
Sets represent unordered collections of unique items.
Useful for ensuring no duplicates.
Unlike lists, no matter how many times you add the same item to a set,
it will only appear in the set once.
Press Enter to see an example...

# Example 1: Lists vs. Sets
dna_list = ["ATCG", "CGTA", "TTAGC", "CGTA"]
dna_set  = {"ATCG", "CGTA", "TTAGC", "CGTA"}
print(f"dna_list:\t{dna_list}\n"
      + f"dna_set:\t{dna_set}\n")
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
```

### 7. Tuples
```
Tuple
Tuples represent ordered collections of items that are immutable.
Useful for fixed collections of data.
Press Enter to see an example...

# Example: Storing a DNA sequence and its length
dna_info = ("ATCG", 4)
print(dna_info)    # Output: ('ATCG', 4)
sequence, length = dna_info
print(f"DNA sequence: {sequence}, Length: {length}")  # Output: DNA sequence: ATCG, Length: 4
```

### 8. Dictionaries
```
Dictionary
Dictionaries represent collections of key-value pairs.
Useful for mapping relationships.
Press Enter to see an example...

# Example: Mapping nucleotide counts in a DNA sequence
def count_nucleotides(sequence):
    counts = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
    for nucleotide in sequence:
        counts[nucleotide] += 1
    return counts

dna_sequence = "ATCGATTG"
nucleotide_counts = count_nucleotides(dna_sequence)
print(f"Nucleotide counts: {nucleotide_counts}")  # Output: {'A': 3, 'T': 3, 'C': 1, 'G': 1}
```