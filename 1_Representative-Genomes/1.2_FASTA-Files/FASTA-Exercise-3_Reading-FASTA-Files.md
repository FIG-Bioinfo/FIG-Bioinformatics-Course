# FASTA Exercise 3 - Reading FASTA files.

Objective: Use Grimoire to write a program that reads and operates on FASTA-formatted sequence-data.

FASTA files are a common format used to store and transmit bioinformatic sequence data. This means that we need to not only understand how these data are represented inside the file, but also have an effective way reading FASTA data and extracting information from it. This exercise creates a rudimentary program that can read a FASTA file, and report a set of summary statistics on the file's contents.

## Materials: 

[Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)

```
FIG-Bioinformatics-Course/
├── 1_Representative-Genomes/
│   └── 1.2_FASTA-Files/
│       ├── FASTA-Exercise-3_Reading-FASTA-Files.md (you are here)
│       └── Solutions/
│           ├── fasta_reader_solution.py
│           ├── rep10.seqs.seed_proteins.solution.tbl
│           └── rep10.seqs.seed_dna.solution.tbl
├── Code/
│   └── fasta_reader.py
└── Data/
    └── Sample1.fasta
```

#### Exercise:

*ALWAYS RESET YOUR PATH* 

Type `source ~/.bashrc` into your command line to reset your path to the Course directory before starting each exercise.

1. Ask Grimoire to explain in pseudocode how to read and parse the sequence of records within a FASTA-format file into a list containing "ID", "Description", and "Sequence" data.

2. Ask Grimoire to convert its pseudocode into python code, and then explain to you how the code works line-by-line if it did not already do so.

3. Ask Grimoire to give pseudocode for and then write a python program that will read a FASTA file from STDIN, treating the first nonwhitespace string in the header as a sequence-ID, and the remainder of the header as a "description" or "comment" field. The program should print a tab-separated sequence-ID and sequence-length for each record to STDOUT with column-headings 'sequence_id' and 'sequence_length'. Finally, the program should print the number of sequences read and the average length of the set of sequences to STDERR, and then exit.

    * WARNING: Grimoire sometimes forgets that the "sequence-ID" stops at the first "whitespace character", and that the rest of the record-header after the sequence-ID is considered a "description" of the sequence, not a part of its ID, so if you see additional text after the sequence-ID in the TSV output-table, you will need to remind Grimoire that it should not include the sequence-description in its TSV output.

4. Copy the pseudocode to the clipboard, and then use VScode to save the pseudocode to the pseudocode section of the program template `Code/fasta_reader.py` 

5. Copy the program itself to the clipboard, and then use VScode to save the program to the code section of the template `Code/fasta_reader.py`.

***Note:*** The program may throw an error when you run it if you have not yet installed the BioPython module. You will know if this is necessary if the `import BioPython` line is in your code.If this happens, run the following pip command to install it:
```
pip install biopython
```


6. Ask Grimoire to explain line-by-line how the program works.

7. Use the VScode terminal-window to run the program `Code/fasta_reader.py` on the file `Data/Sample1.fasta`.
    * Grimoire should have given you an example of how to run the program, but if it didn't, please ask it to show you how. 
    * If you are working within a Windows environment, you should specify that in your questions.

8. Ask Grimoire to tell you about the BioPython module and its uses. 

9. Ask Grimoire to rewrite your program to use the BioPython module. 

* Bonus Exercise 1: In FASTA-Ex-2, you extracted a FASTA-file from a TSV-file, which you saved as `rep10.seed_proteins.faa`. Run `fasta_reader.py` on `rep10.seed_proteins.faa`, and save the TSV-output as follows:
```
python3 Code/fasta_reader.py < Data/rep10.seed_proteins.faa > Data/rep10.seed_proteins.genomes-and-lengths.tab
```

* Bonus Exercise 2: Repeat the procedure from FASTA-Ex-2, but this time extract the field `seed_dna` instead of `seed_protein`:
```
python3 Code/cmd_tsv_select_columns.py genome_id genome_name seed_dna < Data/rep10.seqs.tbl | python3 Code/3col_to_fasta > Data/rep10.seed_dna.fna
```
(Note that this time we have used the file-extension ".fna" instead of ".faa", because we are extracting "nucleic-acid" data instead of "amino-acid" data.)

Now, run `fasta_reader.py` on `rep10.seed_dna.fna`:
```
python3 Code/fasta_reader.py < Data/rep10.seed_dna.fna > Data/rep10.seed_dna.genomes-and-lengths.tab
```
Compare the files `rep10.seed_proteins.genomes-and-lengths.tab` to `rep10.seed_dna.genomes-and-lengths.tab`. You should notice that for each protein-sequence, the corresponding DNA-sequence is 3 times longer; this is because 3 DNA characters translate to a single amino-acid character. We will explore the concept of "sequence translation" further in the next exercise.

# Solution Check instructions:
Use the solution code provided to check your results.
