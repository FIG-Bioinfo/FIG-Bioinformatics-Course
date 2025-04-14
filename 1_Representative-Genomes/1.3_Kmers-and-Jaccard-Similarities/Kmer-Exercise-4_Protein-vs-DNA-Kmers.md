# Kmer Exercise 4 - Protein vs DNA Kmers

Objectives:
1. Understand how the Jaccard-similarity computed using a DNA-sequence's protein translation correlates with the Jaccard-similarity computed using the DNA itself

2. Get a better feel for the tradeoffs between "sensitivity" and "specificity"



## Materials: 

[Grimoire](https://chat.openai.com/g/g-n7Rs0IK86-grimoire)

```
FIG-Bioinformatics-Course
├── Definitions.html
├── Data/
│   └── rep10.seqs.tbl
└── 1_Representative-Genomes
    └── 1.3_Kmers-and-Jaccard-Similarities
        ├── Kmer-Exercise-4_Protein-vs-DNA-Kmers.md (you are here)
        └── Solutions
            └── (TBD)
```

## Exercises


Launch VScode, and open the course-folder
if VScode has not already done so automatically.
Then got to the terminal-windown if it is open,
else launch a new terminal.
You should see a message indicating that `COURSE_HOME`
has been set to the course-folder, and that the
`cdcourse` command will always bring you back
to the course home.

1. Attach the `Definitions.html` file as in previous exercises, again using the prompt:
    ```
    I am going to give you some definitions in an attached file; you don't need to respond to them, just learn them. I'm then going to ask you some questions.
    ```

2. Ask Grimoire to write a program named `protein_vs_dna_jaccard.py` meeting the following specifications:
    ```
    * Mandatory integer-valued protein Kmer-length argument, short-name `-P`, long-name `--protK`.

    * Mandatory integer-valued DNA Kmer-length argument, short-name `-D`, long-name `--dnaK`.

    * Mandatory TSV-filename argument, short-name `-d`, long-name `--data`.

    * Each line of the TSV-file contains data from a genome. The program should skip the header-line, then read the `genome_id`, `seed_protein`, and `seed_dna` columns.

    * Foreach pair of genomes, calculate the protein jaccard-similarity using the data in column `seed_protein` with protein Kmer-length`protK`, and the DNA jaccard-similarity using the data in column `seed_dna` with DNA Kmer-length `dnaK`; count the number of pairs processed, the number of nonzero protein similarities, and the number of nonzero DNA similarities.

    * Generate a "scatter-plot" of similarity-pairs, with the DNA jaccard-similarity on the X-axis and the protein jaccard-similarity on the Y-axis.

    * Print the number of nonzero protein-similarities and the number of nonzero DNA-similarities to STDERR, then exit.
    ```
***Note:*** The import statements for this program might require you to install the `matplotlib` module. This is a common module for creating graphs and plots in python. It is a very commonly used by statisticians and data scientists to help with visualizing data. Pandas is another common module for data analysis and might also be required. If you get an error saying that the module is not found, run the following commands to install it:
```
pip install matplotlib
pip install pandas
```

3. We suggest that you initially run your program with the following arguments:
    ```
    python3 Code/protein_vs_dna_jaccard.py --protK 8 --dnaK 9 --data Data/rep10.seqs.tbl
    ```

4. Note that the "scatter-plot" of score-pairs indicates that in general a larger protein jaccard-similarity implies a larger DNA jaccard-similarity, albeit the correlation is not "tight", i.e. the pairs do not all fall close to the same straight line. Also, there are many instances where the protein similarity is zero even though the DNA similarity is nonzero, and vice-versa. 

5. Make note of the number of pairs of genomes processed, the number of nonzero protein similarities, and the number of nonzero DNA similarities.
You will see that not every pair of genomes yields a nonzero protein or DNA similarity for a given `--protK` (protein Kmer length) or `--dnaK` (DNA Kmer length), indicating that these sequences are too different ("too far apart") to be recognized using that Kmer length with that type of data.
Please try running the program with different values of `--protK` and `--dnaK`, and observe how these changes impact the number of nonzero protein and DNA similarities that the program returns. 

6. In an earlier exercise, we talked about "sensitivity" (ability to recognize that two sequences are similar) and "specificity" (ability to reject "false positive" similarities), and how there is a tradeoff between these two concepts, i.e. that a larger value of `K` will be more "specific" but less "sensitive". By varying `--protK` and `--dnaK`, you are observing this tradeoff in action.

7. Note that in general, when the number of protein pairs and number of DNA pairs are comparable, `--dnaK` will be larger than `--protK`, i.e., it takes a longer DNA Kmer to achieve the same specificity as a given protein Kmer. Ask Grimoire why this might be.

