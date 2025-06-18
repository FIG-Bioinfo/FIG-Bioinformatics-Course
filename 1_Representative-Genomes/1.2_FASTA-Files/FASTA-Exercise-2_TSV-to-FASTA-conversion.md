# FASTA Exercise 2 - TSV to FASTA conversion

Objectives: 
1. Create a program that converts a 3-column tab-separated file into a FASTA-formatted file.

2. Learn how to "pipe" the output of one commmand-line program to the input of another program, thereby chaining these programs together to construct a compound function.

[Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)

```
FIG-Bioinformatics-Course/
├── 1_Representative-Genomes/
│   └── 1.2_FASTA-Files/
│       ├── FASTA-Exercise-2_TSV-to-FASTA-translation.md (you are here)
│       └── Solutions/
│           ├── 3col_to_fasta_solution.py
│           ├── 3col_to_fasta_alternate_solution.py
│           ├── rep10.seqs.seed_proteins.solution.tbl
│           └── rep10.seqs.seed_proteins.alternate_solution.tbl
├── Code/
│   ├── cmd_tsv_select_columns.py
│   └── tsv_headers.py
└── Data/
    └── rep10.seqs.tbl
```

#### Exercise: 

Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then go to the terminal-window if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.

1. In bioinformatics we are often faced with the need to extract data from files and convert these data from the format produced by one program to a different format that is needed by some other program.
In this exercise, you will first create a program that will reformat a 3-column tab-separated file into a FASTA-formatted file. You will then use the program `cmd_tsv_select_columns.py` that you created in `TSV-Ex-3` to extract 3 selected columns from a tab-separated file that contains both genome and sequence-data, and "pipe" them to the program that converts the 3-column data into FASTA format.

If you use your script `Code/tsv_headers.py` on the file `Data/rep10.seqs.tbl`, you should see something like this:
```
% python Code/tsv_headers.py -i Data/rep10.seqs.tbl 
Field names in the TSV file are:
genome_id
genome_name
seed_protein
ssu_rna
seed_dna
```
The above means that `rep10.seqs.tbl` is a 5-column TSV file; the first two columns contain a genome-ID and its human-readable biological name, respectively, while the last three columns contain sequence-data.

2. Ask Grimoire to write a program named `3col_to_fasta.py` that:
    * accepts TSV-data from `STDIN`,
    * skips the header-line,
    * treats the first column as a sequence-ID, the second column as a sequence-description, and the third column as sequence-data,
    * writes the data to `STDOUT` in FASTA format.

Use VScode to save the program to a file named `3col_to_fasta.py` within the `Code/` directory as usual.

3. Use `cmd_tsv_select_columns.py` from TSV-Ex-3 to select the columns 'genome_id', 'genome_name', and 'seed_protein', and "pipe" the output to `3col_to_fasta.py`:
```
python Code/cmd_tsv_select_columns.py genome_id genome_name seed_protein < Data/rep10.seqs.tbl | python Code/3col_to_fasta.py > Data/rep10.seed_proteins.faa
```

* NOTE: The above should all be entered on a single command-line, even though your browser has probably split this command across several lines.

The resulting output should match the corresponding file in the `Solutions/` directory.

* NOTE: If Grimoire did not use `BioPython`, you should instead check the alternate solution file.